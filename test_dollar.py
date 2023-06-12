# 데이터 수집을 위해 필요한 라이브러리 호출
# pip install beautifulsoup4
# pip install requests
import requests as req
from bs4 import BeautifulSoup as BS
import datetime
import os
# HTML 가져오기
url = "https://finance.naver.com/marketindex/"
res_html = req.get(url)

# 해당 url의 text만 가져와서 html.parser로 파싱한 BS 객체
soup = BS(res_html.text, "html.parser")
# urllib : 파이썬 내장 lib
# import urllib.request

# HTML 분석하기
# 원하는 데이터 추출하기 -- (※1)
# 이것만 정답이 아니다. 다른 태그를 지정해서 갖고 오는 것도 가능.
# 바로 밑이면 >, 아니면 그냥 띄워놓기
# soup.select() : 지정한 요소를 찾아서 모두 list로 리턴함
# soup.select_one() : 지정한 요소 첫번째 것만 리턴함
# price = soup.select("div.market1 div.head_info > span.value")
# print(price[0].text)

# 가장 먼저 뽑아오는 하나만 갖고 오기
# 문법의 확장선상으로 미리 .text를 붙여 처리도 가능

price = soup.select_one("div.market1 div.head_info > span.value").text
print(price)
print("usd/krw", price)

# price값을 DB에 입력할 때는 숫자(int)값으로 넣어야 하고, 콤마(,)도 제거해야 한다.
# 콤마 제거 : , 를 '없음'으로
price = price.replace(',','')
print(type(price))
# 저장할 파일 이름 구하기
now_t = datetime.datetime.today()

# 날짜 시간값을 원하는 포맷으로 변경
now_t = now_t.strftime("%Y-%m-%d-%H")
# 저장 file 이름 문자열로 정의
fname = now_t + ".csv"
# 파일로 저장하기
# with open(fname, "w", encoding="utf-8") as f:
#     f.write(now_t + "," + price)

# 문제1 : dollar_data/ 폴더가 없다면 폴더를 만들고
# 그 폴더에 파일을 저장해라

save_dir = "dollar_data/"
if not os.path.exists(save_dir):
  os.makedirs(save_dir, exist_ok=True) 

fname = save_dir + fname
with open(fname, "w", encoding="utf-8") as f:
  f.write(now_t + "," + price)



