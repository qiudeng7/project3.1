import os

from abc import abstractmethod, ABC

from DrissionPage import ChromiumPage, ChromiumOptions, WebPage
from DrissionPage._units.listener import Listener
from time import sleep, perf_counter
import json
from logger import logger
from time import sleep

"""
对Drissionpage库进行简单的封装和调整
包括设置浏览器启动参数，设置cookie，自定义监听器
"""


class BasePageCrawler(ChromiumPage, ABC):
    def __init__(self):
        super().__init__(
            ChromiumOptions()
            .set_argument(arg="--no-first-run")
            .set_argument(arg="--disable-infobars")
            .set_argument(arg="--disable-popup-blocking")
            .set_argument(arg="--no-sandbox")
            .set_argument(arg="--disable-dev-shm-usage")
            .auto_port()  # auto_port内也有set_paths，容易覆盖自己写的set_paths.
            .set_paths(browser_path="/usr/bin/google-chrome")
        )

        # 设置cookie
        logger.info("setting cookie")
        with open("cookie/cookie.json", encoding="utf-8") as f:
            cookie_dict = json.load(f)
        self.get("https://www.douyin.com", timeout=0.5)
        self.set.cookies(cookie_dict)
        
        self.startCrawlingOnData()

    @property
    def listen(self):
        if self._listener is None:
            self._listener = MyListener(self)
        return self._listener

    def startCrawlingOnData(self):
        """
        启动爬虫，等有URL之后开始爬取。
        """
        while True:
            url = self.get_input_url()
            if url is None:
                sleep(5)
                logger.info("waiting for url")
                continue
            else:
                self.crawl_page(url)

    @abstractmethod
    def crawl_page(self, url):
        pass

    @abstractmethod
    def get_input_url(self) -> str: 
        pass


class MyListener(Listener):
    timeout = 20 if os.getenv("mode") == "homepage" else None

    # 修改原版的steps,添加自定义中断条件
    def steps(self, timeout=timeout, whether_stop: callable =None):

        end = perf_counter() + timeout if timeout else None
        while True:

            if whether_stop and whether_stop():
                return

            if (timeout and perf_counter() > end) or self._driver._stopped.is_set():
                return
            # if self._caught.qsize() >= gap:
            if self._caught.qsize() >= 1:
                # yield self._caught.get_nowait() if gap == 1 else [self._caught.get_nowait() for _ in range(gap)]
                yield self._caught.get_nowait()
                if timeout:
                    end = perf_counter() + timeout
            sleep(0.03)
