import re

from fastapi import FastAPI, HTTPException
from loguru import logger

from crawler.instagram_tiqu import InstagramCrawler
from crawler.xhs import XHSCrawler
from utils import tools

app = FastAPI()


@app.get("/api/media_link")
async def media_link(link_text: str):
    text = link_text.strip()
    link = tools.get_link_from_text(text)
    if not link:
        raise HTTPException(status_code=400)
    if re.search(r"xhslink.com", link):
        crawler = XHSCrawler()
    else:
        crawler = InstagramCrawler()

    # 2. get the url
