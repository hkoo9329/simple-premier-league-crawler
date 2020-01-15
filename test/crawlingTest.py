from webCrawling import PL_match_crawler
from webCrawling import pl_match
from db import PL_database
import logging
from datetime import datetime
import json
import threading
import platform
class Test:
    def __init__(self):
        self.crawler = PL_match_crawler.PL_match_crawler()
        self.db = PL_database.Database()
        self.log = logging.getLogger("looger")
        self.log.setLevel(logging.INFO)
        stram_hander = logging.StreamHandler()
        self.log.addHandler(stram_hander)


    def 크롤링테스트(self):
        dt = datetime.now()
        self.crawler.PL_match_list(dt.year,range(dt.month,dt.month+1))

    def 쓰레드_타이머_이용_주기적반복_테스트(self):
        print("test")
        threading.Timer(5.0,self.쓰레드_타이머_이용_주기적반복_테스트).start()


if __name__ == '__main__':
    test = Test()
    test.크롤링테스트()
    test.쓰레드_타이머_이용_주기적반복_테스트()

