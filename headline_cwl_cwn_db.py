# requests, BS, datetime(날짜), os 호출
import requests as req
from bs4 import BeautifulSoup as BS
# selenium 관련 라이브러리
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


import datetime
import time
import os

# cwn.co.kr의 링큰
url = "https://www.cwn.kr/news/articleList.html?sc_section_code=S1N15&view_type=sm"


# Selenium webdriver -> 해당 사이트의 '더보기' 버튼을 n회 누르기
options = webdriver.ChromeOptions()
# 브라우저 크기 설정 (가로 * 세로)
options.add_argument("window-size=1000,1000")
# 샌드박스 사용 안하겠다. 탭별로 분리하겠다.
options.add_argument("no-sandbox")

# 현재 파일 실행될 때 인터넷을 통해서 크롬드라이버 설치 실행
# 브라우저의 버전은 자동으로 업데이트가 되기 때문에
# 자동으로 브라우저 버전에 맞게 셋팅해줌
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)
# 창 켜질때까지 대기
# driver.implicitly_wait(10)

wait = WebDriverWait(driver, 8)
def find(wait, css_selector):
  # wait는 WebDriverWait를 담은 변수, css_selector는 CSS_SELECTOR로 찾을 태그/아이디/클래스명/...
  return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

html = ''
page = 1
while page <= 20:
  try:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    search = find(wait, "a.list-btn-more")
    search.click()
    time.sleep(1.5)
    page += 1
  except:
    break



# url로 request 요청 -> http응답결과 옴
# res = req.get(url)
# 핵심! 더보기를 n회 한 뒤 바뀐 '새로운' 페이지 링크를 식별자에 담는다


html = driver.page_source
# print(html)
soup = BS(html, "html.parser")
# print(soup)
ulbody = soup.select(".type2 > li")
# 전역 변수 (global variable) exc_list 선언:
# 전체 레코드를 저장하는 리스트

news_t_list = []
for li in ulbody:
    # 통화명, 매매기준율 추출하기(텍스트만, 양옆 여백 제거(strip))
    news_date = li.select_one(".byline > em").get_text(strip=True)
    # print(news_date)
    # 매매기준율 = trading standard rate
    # news_title = li.select_one("h4.titles > a")
    news_title = li.select_one("h4.titles > a").get_text(strip=True)
    # news_title = li.select_one("div.view-cont > h4.titles > a").get_text(strip=True)
    print(news_title)
    # 숫자 네번째 자리수에 붙는 , 제거하기(replace)
    # news_title = news_title.replace(",",'')
    # news_title = news_title.replace('""','')
    # news_title = news_title.replace("''",'')

    # 현찰 - 사실 때
    # cash_buy = tr.select_one("td:nth-child(2) + td").get_text(strip=True)
    news_text_sm = li.select_one(".lead.line-6x2 > a").get_text(strip=True)
    news_text_sm = news_text_sm.replace(",",'')
    news_text_sm = news_text_sm.replace('""','')
    # 해당 게시물 링크의 페이지로 들어가 크롤링
    attr = li.select_one("h4.titles > a ")
    # soup에 넣기 위해 완성된 링크 주소 만들기
    url_in = "https://www.cwn.kr" + attr['href']
    # print(url_in)

    # 게시물 링크의 soup
    res_in = req.get(url_in)
    soup_in = BS(res_in.text, "html.parser")
    section_b = soup_in.select(".article-view-content")
    
    news_tags_f_l = []
    for s in section_b:

      # news_title = s.select_one(".heading").get_text(strip=True)
      news_writer = s.select_one(".writer .name").get_text()
      # print(news_writer)

      news_tags_l = s.select(".tag")
      news_tags_f_l = []
      # print(news_tags)
      for tag in news_tags_l:
        news_tag = tag.get_text(strip=True)
        # print(news_tag)
        news_tags_f_l.append(news_tag)
      # news_writer = s.select_one(".information > li > .icon-user-o")
      # print(news_writer)

    #2차원 리스트 만들기: exc_list에 row리스트(=레코드) 한 줄씩 입력(for문)

    # news_tags_f_l를 하나의 str 요소로 만들기 위해 문자열화
    tags_string = ','.join(news_tags_f_l)
    # print(tags_string)

    # 모든 crawling한 내용물을 news_t_list에 입력
    news_t_list.append([news_date, news_title, news_text_sm, url_in, news_writer, tags_string])


# print(news_t_list)

# 크롤링 다했으면 창 닫기
driver.close()

# csv 파일로 저장
# 폴더 이름: exc_rate
# 파일 이름: 2023-05-04-시간.csv <= datetime 호출 필요
import csv

# 저장 경로 생성하기
save_dir = "news_t_data/"
os.makedirs(save_dir, exist_ok=True) 

# 저장할 파일 이름 구하기
now_t = datetime.datetime.today()

# 날짜 시간값을 원하는 포맷으로 변경
now_t = now_t.strftime("%Y-%m-%d-%H")

fname = now_t + ".csv"
file_path = save_dir + fname
with open(file_path, "w", newline="", encoding="utf-8") as f:

  csv_writer = csv.writer(f)
  head = [
    'news_date',
    'news_title',
    'news_text_sm',
    'url_in',
    'news_writer',
    'tags_string'

  ]
  csv_writer.writerow(head)

  ## 바디 붙이기
  for row in news_t_list:
    # data는 1차원 리스트여야 함.
    csv_writer.writerow(row)    

#==============================
# mySQL db에 업로드하기

# import pymysql
# from mydb_local_env import *
# conn = pymysql.connect(host=host, port=port, user=user, password=password, charset=charset)

# with conn:
#   cur = conn.cursor()
#   # DB 만들기
#   sql_db_drop = """
#     DROP DATABASE IF EXISTS cwn_cwl_db;
#   """
#   sql_db = """
#     CREATE DATABASE cwn_cwl_db DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
#   """
#   cur.execute(sql_db_drop)
#   cur.execute(sql_db)
#   conn.commit()
#   # 해당 연결의 현존하는 db 목록 뽑기
#   cur.execute("SHOW DATABASES")
#   # for data in cur:
#   #   print(data)

# db = "cwn_cwl_db"
# conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
# # 커서 만들기
# cur = conn.cursor()

# # table 만들기
# # news_t_list.append([news_date, news_title, news_text_sm, url_in, news_writer, tags_string])
# sql_cwn_data_t ="""
# CREATE TABLE IF NOT EXISTS cwn_cwl_data(
# idx INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
# news_date VARCHAR(20) NOT NULL, 
# news_title VARCHAR(80) NOT NULL, 
# news_text_sm MEDIUMTEXT NOT NULL, 
# url_in VARCHAR(100) NOT NULL,
# news_writer CHAR(10) NOT NULL,
# tags_string VARCHAR(150) 
# )
# """
# cur.execute(sql_cwn_data_t)

# # 2차원 리스트로 변환
# total_news_list = []
# for a in news_t_list:
#     # a.append(now_t)
#     total_news_list.append(a)
# # print(total_news_list) 

# cur.executemany("INSERT INTO cwn_cwl_data(news_date, news_title, news_text_sm, url_in, news_writer, tags_string) VALUES (%s,%s,%s,%s,%s,%s)", total_news_list)

# # db 적용, 트랜젝션 종료
# conn.commit()

# # 조회, 터미널 출력
# sql_query = "SELECT * FROM cwn_cwl_data"
# cur.execute(sql_query)
# # print("뉴스날짜\t\t뉴스제목\t링크주소\t태그목록")
# for row in cur.fetchall():
#   # 메모리공간 16자리 왼쪽 정렬, 공간 10자리 우정렬 소수점2자리까지, 16자리 우정렬 소수점2자리, 19자리 우정렬
#   # 한글 영문이 차지하는 메모리공간이 달라서 여백이 균일하게 나오지 않음 -> 별개 처리 필요
#   print("{} {} {} {}".format(row[1], row[2], row[4], row[5]))
# conn.close()