from selenium import webdriver
from bs4 import BeautifulSoup
from db import PL_database
import os.path
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests


class PL_match_crawler:
    driver = None
    db = None

    def __init__(self):
        self.db = PL_database.Database()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        self.driver = webdriver.Chrome("D:/chromedriver.exe", options=options)

    def PL_match_list(self,year, month):
        before_match_sql = """insert into pl_match_db (match_day, left_team, right_team)
                            values (%s,%s,%s)"""
        after_match_sql = """insert into pl_match_db (match_day, left_team, right_team, score)
                            values (%s,%s,%s,%s)"""
        for i in month:
            url_2019 = "https://sports.news.naver.com/wfootball/schedule/index.nhn?year=" + str(year) + "&month=" + str(
                i) + "&category=premier"
            self.driver.get(url_2019)
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
                # 날짜가 없는 child도 있기 때문에 day로 미리 저장해둠
                if day_list and timeList:
                    day = day_list[0].get_text()
                    datetime = str(year) + "-" + day.replace(".", "-") + " " + timeList[0].get_text()
                # 아직 결과가 나오지 않은 경기
                if timeList and not left_team_score:
                    self.db.execute(before_match_sql,(datetime,left_team[0].get_text(),right_team[0].get_text()))
                    self.db.commit()
                # 이미 끝난 경기
                if timeList and left_team_score and right_team_score:
                    score = left_team_score[0].get_text() + ":" + right_team_score[0].get_text()
                    self.db.execute(after_match_sql,(datetime,left_team[0].get_text(),right_team[0].get_text(),score))
                    self.db.commit()
                if not day_list and not timeList:
                    break
                # 다음 child 탐색을 위해 size +1 씩 증가시키며 탐색
                size += 1

    def driverExit(self):
        self.driver.quit()


