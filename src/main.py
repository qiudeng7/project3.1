import sys
import argparse
from PageCrawler import userPageCrawler
import database
from PageCrawler import videoPageCrawler
from PageCrawler.BasePageCrawler import BasePageCrawler


def main():

    parser = argparse.ArgumentParser(description='douyin crawler program.')
    parser.add_argument(
        '--page_type', type=str, help='douyin page type, select ( video | user )',
                        choices=["video","user"],default="video")
    
    database.get().setup_table_schema()
    
    page_type = parser.parse_args().page_type
    pageCrawlers:dict[BasePageCrawler] = {
        'video':videoPageCrawler,
        'user':userPageCrawler
    }
    
    crawler: BasePageCrawler = pageCrawlers[page_type]
    
    crawler()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()