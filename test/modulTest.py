from webCrawling import PL_match_crawler
from webCrawling import pl_match
from db import PL_database
import logging

class Test:
    def __init__(self):
        self.crawler = PL_match_crawler.PL_match_crawler()
        self.db = PL_database.Database()
        self.log = logging.getLogger("looger")
        self.log.setLevel(logging.INFO)
        stram_hander = logging.StreamHandler()
        self.log.addHandler(stram_hander)

    def 크롤링테스트(self,year,month):
        self.crawler.PL_match_list(year,month)

if __name__ == '__main__':
    test = Test()

    test.크롤링테스트(2020,range(1,2))
    # json=test.db.executeAll("select * from pl_match_db")
    # match_list = list()
    # for i in range(1,len(json)):
    #     datetime=json[i]['match_day']
    #     leftTeam = json[i]['left_team']
    #     rightTeam = json[i]['right_team']
    #     score = json[i]['score']
    #     match_list.append(pl_match.match(datetime,leftTeam,rightTeam,score))
    #
    # for i in match_list:
    #     print(str(i.getDatetime())+" "+str(i.getLeftTeam())+i.getRightTeam())

