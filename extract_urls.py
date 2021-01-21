#!/usr/bin/python3

import requests
import logging
import pandas as pd
import os
from pprint import pprint

logger = logging.getLogger(__name__)

API_URL = 'https://apidata.mos.ru/v1/datasets/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
SAVE_PATH = './out'


def get_datasets_list():
    """
    Getting list of all datasets from data.mos.ru in JSON format
    :return:
    """
    params = {'api_key': api_key, '$inlinecount': 'allpages', 'foreign': 'false'}
    response = requests.get(API_URL, params=params, headers=HEADERS)
    if response.status_code == requests.codes.ok:
        logger.info(f"Quantity of datasets {len(response.json()['Items'])}")
        return response.json()['Items']
    else:
        return None


def get_dataset(dataset):
    dataset_id = dataset['Id']
    caption = dataset['Caption']
    url_id = dataset['SefUrl']
    isarchive = dataset['IsArchive']
    logger.info(f"Trying extract from {caption=}, {url_id=}")
    if not isarchive:
        params = {'api_key': api_key}
        response = requests.get(API_URL+str(dataset_id), params=params, headers=HEADERS)
        if response.status_code == requests.codes.ok:
            sites_columns = find_web_site_column(response)
            if len(sites_columns) == 1:
                logger.debug(f"{sites_columns=}")
                urls = get_urls(dataset_id, sites_columns)
                sites_info = {
                    'dataset_id': dataset_id,
                    'caption': caption,
                    'url_id': url_id,
                    'url_list': urls
                }
                logger.info(f"Extracted {len(urls)} urls.")
                return sites_info
            else:
                logger.info("Sites column not found")
                return None
        else:
            logger.warning(f"{response.status_code=}")
            return None
    else:
        logger.info(f"Dataset is archived")

def find_web_site_column(response):
    """
    Return list of columns with sites urls
    :param response:
    :return: List of columns names
    """
    return [column['Name'] for column in response.json()['Columns'] if column['Caption'] == 'Сайт']


def extract_column_to_list(response, column_name):
    return [row['Cells'][column_name] for row in response.json()]


def get_urls(dataset_id, columns):
    headers = {'Content-Type': 'application/json'}
    raw_data = str(columns).replace('\'', '\"')
    response = requests.post(url=API_URL + str(dataset_id) + '/rows' +
                             f'?api_key={api_key}', headers=headers, data=raw_data)
    if response.status_code == requests.codes.ok:
        sites_list = extract_column_to_list(response, 'WebSite')
        return sites_list
    else:
        logger.error(f"{dataset_id=}, {response.status_code=}")
        return None


def main():
    sites_list = []
    datasets_list = get_datasets_list()
    for i, dataset in enumerate(datasets_list):
        logger.info(f'Extracting {i}/{len(datasets_list)}')
        try:
            sites_list.append(get_dataset(dataset))
        except Exception as ex:
            logger.error(f"{ex}")
    sites_list = [dataset for dataset in sites_list if isinstance(dataset, dict)]
    df = pd.DataFrame(sites_list)
    df = df.explode('url_list', ignore_index=True)
    df.to_csv('./out/sites_list.csv', index=False, header=True)


if __name__ == '__main__':
    with open('apikey.txt', "r") as f:
        api_key = f.read()
    logging.basicConfig(level=logging.INFO)
    main()
