from selenium import webdriver
from bs4 import BeautifulSoup
from db import PL_database
from webCrawling.pl_match import match
import re
import time
import datetime
import os.path
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests


class PL_match_crawler:
    before_match_sql = """insert into pl_match_db (match_day, left_team, right_team)
                                values (%s,%s,%s)"""
    after_match_sql = """insert into pl_match_db (match_day, left_team, right_team, score)
                                values (%s,%s,%s,%s)"""
    driver = None
    db = None
    season = [[2019,range(8,13)],[2020,range(1,6)]]

    def __init__(self):
        self.db = PL_database.Database()
        self.before_match_list = []
        self.after_match_list = []
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        self.driver = webdriver.Chrome("D:/chromedriver.exe", options=options)

        ## 인스턴스 생성 시 테이블이 비어있다면 전체 리그 일정 생성
        row = self.db.executeOne("select exists (select 1 from pl_match_db)")
        if row['exists (select 1 from pl_match_db)'] == 0:
            self.createMatchListAll()


    def PL_match_update(self):
        row = self.db.executeAll("select * from pl_match_db where score is null")
        day = str(row[0]['match_day'])
        date = re.findall(r"[\w']+", day)
        year = date[0]
        month = date[1]
        self.PL_match_list(year, range(int(month),int(month)+1))
        for match in self.after_match_list:
            print(match.getDatetime()+"   "+match.getLeftTeam() + " : " + match.getRightTeam()+"\n ================================")
            for db_match in row:
                print(str(db_match['match_day'])+"   "+db_match['left_team'] + " : " + db_match['right_team'])
                if match.compareToEqual(str(db_match['match_day']),str(db_match['left_team'])):

                    self.db.execute("update pl_match_db set score ='"+match.score
                                    +"' where id ="+str(db_match['id']))
                    self.db.commit()
                    break




    def PL_match_list(self, year, month):
        for i in month:
            url = "https://sports.news.naver.com/wfootball/schedule/index.nhn?year=" + str(year) + "&month=" + str(
                i) + "&category=premier"
            self.driver.get(url)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            check = True
            size = 1
            while check:
                day_list = soup.select(
                    '#_monthlyScheduleList > tr:nth-child(' + str(size) + ') > th > div > em'
                )
                timeList = soup.select(
                    '#_monthlyScheduleList > tr:nth-child(' + str(size) + ') > td.time_place > div > span.time'
                )
                left_team = soup.select(
                    '#_monthlyScheduleList > tr:nth-child(' + str(size) + ') > td > div > span.team_left > span.name'
                )
                left_team_score = soup.select(
                    '#_monthlyScheduleList > tr:nth-child(' + str(size) + ') > td > div > span.team_left > span.score'
                )
                right_team_score = soup.select(
                    '#_monthlyScheduleList > tr:nth-child(' + str(size) + ') > td > div > span.team_right > span.score'
                )
                right_team = soup.select(
                    '#_monthlyScheduleList > tr:nth-child(' + str(size) + ') > td > div > span.team_right > span.name'
                )
                # # 날짜가 없는 child도 있기 때문에 day로 미리 저장해둠
                if day_list and timeList:
                    day = day_list[0].get_text()
                    dt = datetime.datetime.strptime(str(year)+"-"+day.replace(".","-")+" "+timeList[0].get_text(),
                                                    "%Y-%m-%d %H:%M")
                # # 아직 결과가 나오지 않은 경기
                if timeList and not left_team_score:
                    match_info = match(str(dt), left_team[0].get_text(), right_team[0].get_text(),None)
                    self.before_match_list.append(match_info)
                    # self.db.execute(self.before_match_sql,(dt,left_team[0].get_text(),right_team[0].get_text()))
                    # self.db.commit()
                # # 이미 끝난 경기
                if timeList and left_team_score and right_team_score:
                    score = left_team_score[0].get_text() + ":" + right_team_score[0].get_text()
                    match_info = match(str(dt), left_team[0].get_text(), right_team[0].get_text(), score)
                    self.after_match_list.append(match_info)
                    # self.db.execute(self.after_match_sql,(dt,left_team[0].get_text(),right_team[0].get_text(),score))
                    # self.db.commit()
                if not day_list and not timeList:
                    break
                # 다음 child 탐색을 위해 size +1 씩 증가시키며 탐색
                size += 1

    def driverExit(self):
        self.driver.quit()

    def createMatchListAll(self):
        self.PL_match_list(self.season[0][0],self.season[0][1])
        self.PL_match_list(self.season[1][0],self.season[1][1])
        for after_match in self.after_match_list:
            datetime = after_match.getDatetime()
            leftTeam = after_match.getLeftTeam()
            rightTeam = after_match.getRightTeam()
            score = after_match.getScore()
            self.db.execute(self.after_match_sql, (datetime, leftTeam, rightTeam, score))
            self.db.commit()
        for before_match in self.before_match_list:
            datetime = before_match.getDatetime()
            leftTeam = before_match.getLeftTeam()
            rightTeam = before_match.getRightTeam()
            self.db.execute(self.before_match_sql, (datetime, leftTeam, rightTeam))
            self.db.commit()


if __name__=="__main__":
    crawler=PL_match_crawler()
    crawler.PL_match_update()