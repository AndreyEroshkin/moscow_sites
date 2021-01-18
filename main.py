#!/usr/bin/python3

#a quick and dirty script to scrape/harvest resource-level metadata records from data.gov.sg
#the original purpose of this work is to support the ongoing international city open data index project led by SASS

import requests
# import datetime
# import time
# from bs4 import BeautifulSoup
# import scraperwiki

API_URL = 'https://apidata.mos.ru/v1/datasets'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
SAVE_PATH = './data'


with open('apikey.txt', "r") as f:
    api_key = f.read()

def get_datasets_list():
    """

    :return:
    """
    params = {'api_key': api_key, '$inlinecount':'allpages', 'foreign': 'true'}
    response = requests.get(API_URL, params=params, headers=HEADERS)
    print(f'{response=}')
    return response.json()['Items']



print(get_datasets_list())