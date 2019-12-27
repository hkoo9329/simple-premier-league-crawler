from selenium import webdriver
from bs4 import BeautifulSoup
import os.path
import logging
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import getpass


def writehrefLink(LinkList):
    for x in LinkList:
        href_file.write(x+"\n")



#username = input("Input ID : ")# User ID
#password = getpass.getpass("Input PWD : ")# User PWD
hashTag = input("Input HashTag # : ")# Search #
url = "https://www.instagram.com/explore/tags/"+hashTag
if os.path.exists('D:/'+hashTag+'HrefData.txt'):
    href_file = open('D:/' + hashTag + 'HrefData.txt', 'a', encoding='utf8')
else:
    href_file = open('D:/'+hashTag+'HrefData.txt','wt',encoding='utf8')

if os.path.exists('D:/'+hashTag+'tagData.txt'):
    tag_file = open('D:/' + hashTag + 'tagData.txt', 'a', encoding='utf8')
else:
    tag_file = open('D:/'+hashTag+'tagData.txt','wt',encoding='utf8')

driver = webdriver.Chrome("D:/chromedriver.exe")# Chromedriver PATH
driver.set_window_size(1920,1080)
driver.get(url)

log = logging.getLogger('logData')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


pageDown = 1000
aTagList = []
hrefList = []
while href_file.readable():
    line = href_file.readline()
    if not line:
        break;
    else:
        hrefList+=line


# 링크를 가지고 있는 a 태그 객체를 가지고 온다. 정확한 태그를 가져오기 위해 Selector를 이용했다.
# 위에 가져오는 select는 인기 게시물이고, 아래 select는 일반 게시물 두 게시물의 select의 경로가 다름으로
# 어쩔 수 없이 이와 같은 방법을 취하였다.
# 설정한 pageDown만큼 실행하여 태크들을 가져온다.
while pageDown:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    aTagList += soup.select(
        '#react-root > section > main > article > div.EZdmt > div > div > div > div > a'
    )
    aTagList += soup.select(
        '#react-root > section > main > article > div > div > div > div > a'
    )
    elem = driver.find_element_by_tag_name("body")
    elem.send_keys(Keys.PAGE_DOWN)
    sleep(1.5)
    log.info(pageDown)
    pageDown -= 1
# 가져온 a태그 객체에서 href 정보를 가져온다.
# 배열에 해당 href 정보를 입력하고 중복되는 href는 제거한다.
# 그리고 얻은 href의 정보를 텍스트 파일로 저장한다.
for x in aTagList:
    hrefList+=x.get_attribute_list('href')
hrefList = list(set(hrefList))
writehrefLink(hrefList)
print(len(hrefList))
href_file.close()


'''
hrefDriver =webdriver.Chrome("D:/chromedriver.exe")
for href in hrefList:
    url = "https://www.instagram.com/"+href
    hrefDriver.get(url)
    soup = BeautifulSoup(hrefDriver.page_source, "html.parser")
    tag_list=soup.find_all('a')
    searchText = "#"
    for tag in tag_list:
        if searchText in tag.text:
            tag_file.write(tag.text)
    tag_file.write("\n")
    sleep(0.8)

tag_file.close()
'''