from BasePageCrawler import BasePageCrawler

class UserPageCrawler(BasePageCrawler):

    def crawl_page(self,url):
        listen_target = 'comment/list'
        self.listen.start(listen_target)

    def get_input_url(self) -> str:
        return super().get_input_url()