# requests, BS, datetime(날짜), os 호출
import requests as req
from bs4 import BeautifulSoup as BS
import datetime
import os

# 네이버 증권의 환전고시 환율표를 추출하기
url = "https://www.cwn.kr/news/articleList.html?sc_section_code=S1N15&view_type=sm"

# url로 request 요청 -> http응답결과 옴
res = req.get(url)

soup = BS(res.text, "html.parser")

ulbody = soup.select(".type2 > li")
# 전역 변수 (global variable) exc_list 선언:
# 전체 레코드를 저장하는 리스트
news_t_list = []
for li in ulbody:
    # 통화명, 매매기준율 추출하기(텍스트만, 양옆 여백 제거(strip))
    news_date = li.select_one(".byline > em").get_text(strip=True)
    # 매매기준율 = trading standard rate
    news_title = li.select_one(".view-cont > .titles > a ").get_text(strip=True)
    # 숫자 네번째 자리수에 붙는 , 제거하기(replace)
    news_title = news_title.replace(",",'')
    news_title = news_title.replace('""','')
    news_title = news_title.replace("''",'')

    # 현찰 - 사실 때
    # cash_buy = tr.select_one("td:nth-child(2) + td").get_text(strip=True)
    news_text_sm = li.select_one(".view-cont > p > a").get_text(strip=True)
    news_text_sm = news_text_sm.replace(",",'')
    news_text_sm = news_text_sm.replace('""','')
    # 해당 게시물 링크의 페이지로 들어가 크롤링
    attr = li.select_one(".view-cont > .titles > a ")
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

    # print(f"{exc_name}, {ts_rate}")
    #2차원 리스트 만들기: exc_list에 row리스트(=레코드) 한 줄씩 입력(for문)

    # news_tags_f_l를 하나의 str 요소로 만들기 위해 문자열화
    tags_string = ','.join(news_tags_f_l)
    # print(tags_string)
    news_t_list.append([news_date, news_title, news_text_sm, url_in, news_writer, news_tags_f_l])

# print(news_t_list)

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
  
  ## 바디 붙이기
  for row in news_t_list:
    # data는 1차원 리스트여야 함.
    csv_writer.writerow(row)    

#==============================
# mySQL db에 업로드하기

# import pymysql
# from mydb_local_env import *
# conn = pymysql.connect(host=host, port=port, user=user, password=password, charset=charset)