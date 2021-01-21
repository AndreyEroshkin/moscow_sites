import pandas as pd
import json


SAVE_PATH = './out/sites_list.csv'


def str_to_list(s:str):
    if isinstance(s, str):
        if s.startswith('['):
            s = s.replace('\'', '\"')
            d = json.loads(s)
            return [el['WebSite'] for el in d]
    return s

df = pd.read_csv(SAVE_PATH)

df['url_list'] = df.url_list.apply(str_to_list)
df = df.explode('url_list', ignore_index=True)
df.drop_duplicates(inplace=True)
df = df[df.url_list.notnull()]
df.to_csv('./out/sites_list.csv', index=False, header=True)
