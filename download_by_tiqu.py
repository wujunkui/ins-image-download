import time
import json

import requests

from loguru import logger
from telegram import InputMediaPhoto, InputMediaVideo

from get_sign import generate_signature

CACHE_FILE = './cache.json'


class APIError(Exception):
    pass


def persist_to_file_sync(original_func):
    try:
        cache = json.load(open(CACHE_FILE, 'r'))
    except (IOError, ValueError):
        cache = {}

    def decorator(_, param):
        if param not in cache:
            cache[param] = original_func(_, param)
            json.dump(cache, open(CACHE_FILE, 'w'))
        return cache[param]

    return decorator


class TiQuRequest:
    def __init__(self):
        self.url_head = "https://wapi.tiqu.cc/api/all/"
        self.secret_token = "bfa95f704ce74c5cba31820ea1c0da05"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Referer": "https://wapi.tiqu.cc/",
            "Origin": "https://wapi.tiqu.cc",
        }

    def get_param(self, instagram_url: str) -> dict:
        t = int(time.time())
        data = {'url': instagram_url, 't': t}
        sign = generate_signature(data, self.secret_token)
        data['sign'] = sign
        return data

    @persist_to_file_sync
    def request(self, instagram_url: str) -> dict:
        param = self.get_param(instagram_url)
        res = requests.get(self.url_head, params=param, headers=self.headers, verify=False)
        logger.debug(res.text)
        return res.json()

    def get_url(self, instagram_url: str) -> list[str]:
        data_dict = self.request(instagram_url)
        if data_dict['err'] != 0:
            raise APIError
        images = data_dict['images']
        url_lst = [row['url'] for row in images]
        return url_lst

    def get_medias(self, instagram_url: str) -> list | None:
        media_lst = []
        data_dict = self.request(instagram_url)
        if data_dict['err'] != 0:
            raise APIError
        if data_dict['type'] == 1:
            for row in data_dict['images']:
                media_lst.append(InputMediaPhoto(row['url']))
        elif data_dict['type'] == 2:
            for row in data_dict['videos']:
                media_lst.append(InputMediaVideo(row['url']))
        return media_lst


if __name__ == '__main__':
    Tiqu = TiQuRequest()
    print(Tiqu.request("https://www.instagram.com/reel/C5vHrCJSWXg/?igsh=MW1lMGoyYnk0dnpvNg=="))
