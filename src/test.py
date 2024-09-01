from DrissionPage import WebPage
# from PageCrawler.PageCrawler import PageCrawler 
import time

# page = WebPage()
# page.listen.start('comment/list')
# page.get('https://www.douyin.com/video/7388879961026759974')

# for packet in page.listen.steps():
#     print(packet.url)
#     print(packet.response.body)


# crawler = PageCrawler()
# crawler.get("https://www.douyin.com/video/7388879961026759974")
# cookie = crawler.cookies(True,False,True)
# print(cookie)

# import database
# database.get().execute("select * from boss")

# while True:
#     time.sleep(20)


# from logger import logger
# logger.info("test %s",'123')


from dotenv import load_dotenv
import os
load_dotenv()
print(os.getenv('cookie'))