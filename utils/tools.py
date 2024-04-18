import json
import re
from typing import Optional

CACHE_FILE = '../cache.json'


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


def get_link_from_text(text: str) -> Optional[str]:
    pattern = r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+
    |(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"""
    urls = re.findall(pattern, text)
    return urls[0][0].split("，")[0] if urls else None
