import requests as rq
from bs4 import BeautifulSoup as bs
from selenium import webdriver

url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%ED%81%AC%EB%A1%A4%EB%A7%81&oquery=test&tqi=hbtHPdp0J14ssOZUNACssssstId-189547"
res = rq.get(url)

#모든 헤더 내용 가져오기 (딕셔너리)
for h in res.headers:
    res.headers[h]

#html 불러오기 content가 incoding이 깨지지 않아 유리.
res.text
html = res.content

#파싱(html, 파서)
soup =bs(html, 'lxml')

#웹 브라우저
driver = webdriver.Chrome('./chromedriver')


