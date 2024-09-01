from BasePageCrawler import BasePageCrawler
from threading import Thread
from time import sleep
from logger import logger
import database


class VideoPageCrawler(BasePageCrawler):

    def crawl_page(self, url):
        """
        爬取视频页面中的评论，并将评论数据插入到数据库中。
        """
        
        self.listen.start("comment/list")
        self.stop_sign = False
        
        on_stop = lambda: self.stop_sign = True
        self.start_operate_page(url,on_stop)
        
        for package in self.listen.steps(whether_stop=self.get_stop_sign):
            logger.info("resolving video data")
            query = convert_video_comment_data_into_sql(package)
            database.get().execute(query)

    def get_stop_sign(self):
        """
        返回页面操作结束的信号，用于中断监听。
        停止表示该页面所有评论都爬取完毕。
        """
        return self.stop_sign

    def start_operate_page(self, url,on_stop):
        """
        启动一个视频页面操作线程
        
        参数：
            url：要打开的视频页面的 URL。
            on_stop：一个可选的回调函数，将在操作完成时调用。
        返回值：
            无
        """
        Thread(target=self.operate_page, args=[url, on_stop]).start()

    def get_input_url(self) -> str:
        """
        获取输入的URL

        获取全局唯一的database对象，然后检查指定表中的待处理视频数量。如果没有视频，
        方法将等待5秒并输出一条日志消息，然后重复检查。如果有视频，方法将获取一
        个视频ID，从表中删除该ID对应的记录，并返回一个包含该ID的URL。

        返回：
            将要爬取的URL
        """
        
        db = database.get()
        while True:
            count = db.execute("select count(*) from project3.video_todo;")[0]['count(*)']
            if count == 0:
                logger.info("no video to crawl")
                sleep(5)
            elif count > 0:
                break
            elif count <0:
                logger.error("send 'select count(*) from project3.video_todo;' got error value: %s ",count)
                sleep(5)
        
        video_id = db.execute("SELECT video_id FROM project3.video_todo LIMIT 1;")[0]["video_id"]
        db.execute("DELETE FROM project3.video_todo WHERE video_id = %s", video_id)
        return f"https://www.douyin.com/video/{video_id}"

    def operate_page(self, url, on_stop: callable = None):
        """
        打开一个视频页面，然后打开所有的子评论。
        它接受一个 URL 和一个可选的回调函数作为参数。
        如果提供了回调函数，它将在操作完成后被调用。
        
        参数：
            url: 要打开的视频页面的 URL。
            on_stop: 一个可选的回调函数，将在操作完成时调用。

        返回值：
            这个函数没有返回值。
        """
        logger.info("opening video page")
        self.open_video_page(url)
        count = 0
        while True:
            logger.info("opening more comments, count: %s", count)
            if not self.open_next_comment():
                break
        on_stop()

    def open_next_comment(self) -> bool:
        target_comment = self.ele('xpath://div[contains(@data-e2e,"comment-list")]/div')
        if not target_comment:
            return False
        self.open_all_sub_comment(target_comment)
        self.remove_ele(target_comment)
        return True

    def open_all_sub_comment(self, target_comment):
        """
        打开目标评论下的所有子评论
        参数：
            target_comment：要展开子评论的目标评论
        返回值：无
        """
        while True:
            sub_comment = target_comment.ele("@data-e2e=comment-item")
            if sub_comment:
                self.remove_ele(sub_comment)
                continue

            button = target_comment.ele("tag:button@text():展开")
            if button:
                button.click()
                continue
            break

    def open_video_page(self, url):
        """
        打开页面并进行预处理，比如删除视频DOM防止占用流量和内存
        """
        self.get(url)
        self.remove_ele(self.ele(".video-detail-container"))


def convert_video_comment_data_into_sql(package):
    """
    将视频评论数据转换为 SQL 语句
    参数：
        package：包含视频评论数据的包
    返回值：
        一条 SQL 插入语句，用于将视频评论数据插入到数据库中
    """
    raw_comments = package.response.body.get('comments')
    total_comments: list[dict] = []
    for raw_comment in raw_comments:
        single_comment = {
            "comment_id": raw_comment.get("cid"),
            "reply_id": raw_comment.get("reply_id"),
            "user_nickname": raw_comment.get("user").get("nickname"),
            "content": raw_comment.get("text", "评论内容为纯图片"),
            "like_count": raw_comment.get("digg_count"),
            "create_time": raw_comment.get("create_time"),
            "sec_uid": raw_comment.get("user").get("sec_uid"),
            "video_id": raw_comment.get("aweme_id"),
        }
        total_comments.append(single_comment)
    
    query_prefix = """
    insert into project3.comment_all 
    (comment_id, reply_id, user_nickname, content, like_count,create_time,sec_uid,video_id)
    values
    """
    values = [ f""" (
        "${c['comment_id']}",
        "${c['reply_id']}",
        "${c['user_nickname']}",
        "${c['content']}",
        ${c['like_count']},
        "${c['create_time']}",
        "${c['sec_uid']}",
        "${c['video_id']}" )
        """ for c in total_comments ]
    query = query_prefix + ",".join(values) + ";"
    return query