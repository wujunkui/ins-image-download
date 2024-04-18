import re
import requests

from lxml import etree
from telegram import InputMediaVideo, InputMediaPhoto


class XHSCrawler:
    @staticmethod
    def get_html(url: str) -> str:
        headers = {
            "authority": "www.xiaohongshu.com",
            "cache-control": "max-age=0",
            "sec-ch-ua": '"Chromium";v="21", " Not;A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "accept-language": "zh-CN,zh;q=0.9",
        }
        response = requests.get(url, headers=headers, verify=False)
        return response.text

    @staticmethod
    def get_video_url(html: str) -> str | None:
        # 小红书的视频分享链接只有一个视频
        root = etree.HTML(html)
        video_lst = root.xpath('//head/meta[@name="og:video"]/@content')
        return video_lst[0] if video_lst else None

    @staticmethod
    def get_image_urls(html: str) -> list[str]:
        root = etree.HTML(html)
        image_lst = root.xpath('//head/meta[@name="og:image"]/@content')
        return image_lst

    def get_medias(self, url) -> list[InputMediaVideo | InputMediaPhoto]:
        # 先获取视频，获取到就只有视频
        html = self.get_html(url)
        video = self.get_video_url(html)
        if video:
            return [InputMediaVideo(video)]
        images = self.get_image_urls(html)
        return [InputMediaPhoto(image) for image in images]
