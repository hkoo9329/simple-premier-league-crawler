from flask import Flask, request, jsonify
from selenium import webdriver
from bs4 import BeautifulSoup


app = Flask(__name__)

@app.route("/match", methods=['GET','POST'])
def match():
    content = request.json
    result = {'result' : True}
    return jsonify(result)


if __name__ =='__main__':
    app.run('0.0.0.0', port=8080)