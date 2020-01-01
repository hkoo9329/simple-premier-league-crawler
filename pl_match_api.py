from flask import Flask, request, jsonify
from db import PL_database
from webCrawling import PL_match_crawler
from selenium import webdriver
from bs4 import BeautifulSoup


app = Flask(__name__)
@app.route("/match", methods=['GET','POST'])
def match():
    row = db.executeAll("show tables")
    return jsonify(row)


if __name__ =='__main__':
    db = PL_database.Database()
    # crawler = PL_match_crawler.PL_match_crawler()
    # crawler.PL_match_list(2020,range(1,2))
    # crawler.driverExit()
    db.execute("insert into pl_matchs (match_day, match_time, left_team, right_team) "+
                                    "values ('2019-01-01','19:00','teser1','tester2')")
    db.commit()
    # app.run('0.0.0.0', port=8080)
    # app.run()