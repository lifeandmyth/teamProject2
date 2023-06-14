# datetime(날짜), os 호출

import datetime
import os

# csv 파일로 저장
# 폴더 이름: exc_rate
# 파일 이름: 2023-05-04-시간.csv <= datetime 호출 필요
import csv

# 저장 경로 생성하기
save_dir = "news_h_words/"
os.makedirs(save_dir, exist_ok=True) 


# 각 헤드라인 가져오기
word_list = []

fname = ".csv"
file_path = 'news_t_data/2023-06-13-15.csv'
f = open(file_path, "r", encoding='utf8')
rdr = csv.reader(f)
for line in rdr:
  word_list.append(line[1])
  # print(line[1])

f.close()

from konlpy.tag import Okt

# Okt 객체 선언
okt = Okt()

for w in word_list:
  print(okt.nouns(w))


# 단어로 분해한 제목 리스트를 다시 날짜와 함께 결합해 새 테이블


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