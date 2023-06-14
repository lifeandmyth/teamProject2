# 필요한 라이브러리 호출
# 필요한 데이터 url 지정하기

# soup.select("요소")로 원하는 데이터 추출 진행
# 출력할 곳 정하기(터미널, 파일, db)

import requests as req
from bs4 import BeautifulSoup as BS
import datetime
import os

# 네이버 뉴스의 head line을 추출하기
url = "https://news.naver.com/"

# url로 request 요청 -> http응답결과 옴
res = req.get(url)

# 응답결과의 text를 soup객체로 만들기 : html 요소 지정 용이함
soup = BS(res.text, "html.parser")
# print(soup)

# 추출할 데이터(크롤링할 데이터)의 요소 찾기(html tag, css selector)
# 뉴스 헤드라인들을 가져오기
# hls = soup.select("div.cjs_t")

# 리스트로 저장하기
hls = soup.select("div.cjs_t")
# print(hls)


# print(hls_content)

# naver_news/ 가 있는 체크, 없으면 만들기
# 뉴스 목록 파일에 저장, 파일명 : 년-월-일-시.csv

# 저장할 파일 이름 구하기
now_t = datetime.datetime.today()

# 날짜 시간값을 원하는 포맷으로 변경
now_t = now_t.strftime("%Y-%m-%d-%H")
# 저장 file 이름 문자열로 정의
fname = now_t + ".csv"

# naver_news/ 디렉토리가 있는지 체크, 없으면 생성
save_dir = "naver_news/"
if not os.path.exists(save_dir):
  os.makedirs(save_dir, exist_ok=True) 

# 파일명 'naver_news/(날짜)'
# hls_content 리스트를 한 줄 한 줄 나눠 fname 파일에 입력

# hls_content = []
# for 문으로 저장한 리스트를 한줄한줄 출력하기
# for headline in hls:
#   # print(headline.text)

#   # print(headline.get_text(strip=True))
#   # get_text의 경우, headline.get_text(strip=True)처럼
#   # 양쪽 여백을 자를 수 있음
#   # print(headline.get_text())
#   hls_content.append(headline.get_text(strip=True))

# file_path : naver_news/2023-05-03-15.csv
file_path = save_dir + fname
with open(file_path, "w", encoding="utf-8") as f:
  
  # 헤드라인 태그 편집을 파일 생성과 같이 처리:
  # 방법1
  i = 1
  for hl in hls:
    hl = hl.get_text(strip=True)
    # f.write(str(i) + "_" + now_t + "," + hl + "\n")
    f.write(f"{str(i)}_{now_t} , {hl}\n")
    i = i + 1

  # 방법2 enumerate(list) : index와 요소값을 리턴함
  # for idx, hl in enumerate(hls_content):
  #   f.write(f"{str(idx+1)}_{now_t} , {hl}\n")