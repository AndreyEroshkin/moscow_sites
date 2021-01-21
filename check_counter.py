import requests
import logging
import pandas as pd
import os
from pprint import pprint

logger = logging.getLogger(__name__)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
SAVE_PATH = './out/sites_list.csv'
COUNTER_STR = 'https://stats.mos.ru/counter.js'

def check_counter(url, counter_str):
    try:
        response = requests.get(prepeare_url(url), headers=HEADERS, timeout=10)
    except Exception as ex:
        logger.error(f"{ex}")
        return 'сайт недоступен'
    if response.status_code == requests.codes.ok:
        html = response.text
        if counter_str in html:
            logger.debug(f'{url=} counter found.')
            return 'есть'
        else:
            logger.debug(f'{url=} counter not found.')
            return 'нет'
    else:
        return f'сайт недоступен код {response.status_code}'


def prepeare_url(url):
    if url.startswith('http'):
        return url
    else:
        return 'http://' + url


def main():
    df = pd.read_csv(SAVE_PATH)
    status = []
    for i, url in enumerate(df['url_list']):
        logger.info(f'Row {i}/{len(df)}')
        status.append(check_counter(url, COUNTER_STR))
    df['status'] = status
    df.to_csv('./out/sites_list_checked.csv', index=False, header=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
