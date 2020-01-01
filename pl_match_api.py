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
    row = db.executeOne("select exists (select 1 from pl_match_db)")
    if row['exists (select 1 from pl_match_db)'] == 0:
        crawler = PL_match_crawler.PL_match_crawler()
        crawler.PL_match_list(2019,range(8,13))
        crawler.PL_match_list(2020,range(1,6))
        db.close()
    # app.run('0.0.0.0', port=8080)
    # app.run()