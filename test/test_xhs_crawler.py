from unittest import TestCase
from telegram import InputMediaPhoto, InputMediaVideo

from crawler.xhs import XHSCrawler


class TestXHSCrawler(TestCase):
    def setUp(self):
        self.xhs_crawler = XHSCrawler()

    def test_one_image(self):
        medias = self.xhs_crawler.get_medias("http://xhslink.com/UrxUPG")
        self.assertEqual(1, len(medias))

    def test_many_images(self):
        medias = self.xhs_crawler.get_medias("http://xhslink.com/C9zSQG")
        self.assertLess(1, len(medias))
        for media in medias:
            self.assertIsInstance(media, InputMediaPhoto)

    def test_video(self):
        medias = self.xhs_crawler.get_medias("http://xhslink.com/SATSQG")
        self.assertEqual(1, len(medias))
        self.assertIsInstance(medias[0], InputMediaVideo)