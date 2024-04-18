from utils import tools


class TestLinkGetter:
    def test_get_link(self):
        testcase_map = {
            "40 汤姆特发布了一篇小红书笔记，快来看吧！ 😆 RwGWvkRcw3CYLr1 😆 http://xhslink.com/4CdeRG，复制本条信息，打开【小红书】App查看精彩内容！": "http://xhslink.com/4CdeRG",
            "https://www.instagram.com/p/C5lcU6CS4dg/?igsh=bGx6bW8yaWI4YWZ6": "https://www.instagram.com/p/C5lcU6CS4dg/?igsh=bGx6bW8yaWI4YWZ6",
            "no link text hahaha": None
        }
        for text, expected in testcase_map.items():
            link = tools.get_link_from_text(text)
            assert link == expected

