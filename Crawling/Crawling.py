import requests as rq
from bs4 import BeautifulSoup as bs
from selenium import webdriver

#크롤링 연습

#---------url에서 요청 받아오기.--------------
url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%ED%81%AC%EB%A1%A4%EB%A7%81&oquery=test&tqi=hbtHPdp0J14ssOZUNACssssstId-189547"
res = rq.get(url)

#--------모든 헤더 내용 가져오기 (딕셔너리)----
for h in res.headers:
    res.headers[h]

#-------------------html 불러오기 content가 incoding이 깨지지 않아 유리---------.
res.text
# html = """<p>test<p>"""
html = res.content
#-----------파싱(html, 파서)----------
soup =bs(html, 'lxml')
# print(soup.prettify())
tag_title = soup.title
print(tag_title) #type : class bs4.element.Tag
print(tag_title.attrs)

print(tag_title.text)  #해당 태그의 자식까지 모두 출력
print(tag_title.string) #정확히 해당 태그만 출력
print(tag_title.name)

#-------------img tag의 src 속성 가져오기-----------.
tag_img = soup.img
#key가 존재하지 않을경우 error발생 get을 이용하면 방지가능.
# print(tag_img['src'])
print(tag_img.get('src'))

html = """<html> <head><title>test site</title></head> <body><p>test1</p>
<p><span>test2</span><span>test3</span></p><p>test4</p></body></html>"""
soup = bs(html,'lxml')

#-------태그의 자식들을 리스트로 가져오기.--------
tag_p_childrens = soup.p.contents
print(tag_p_childrens)

#child는 iterator 객체로 반환.
tag_p_childrens2 = soup.p.children
for child in tag_p_childrens2:
    print(child)

#--------바로 윗 부모 태그 가져오기----------
tag_span_parent = soup.span.parent
print(tag_span_parent)

# ----------모든 조상 태그 가져오기.--------
tag_title_parent = soup.title.parents
for parent in tag_title_parent:
    print(parent)

# ----------형제 태그 가져오기-------
span1 = soup.span.next_sibling
span2 = span1.previous_sibling

span3 = soup.span.next_siblings
span4 = span1.previous_siblings

#---------다음, 이전 요소 접근하기. --------
#형제 태그와는 달리 요소이기 때문에 태그,태그안에 있는 자식, 문자를 모두 포함함.
tag_p =soup.p
tag_p_nexts = tag_p.next_elements

#--------------type 검사 ------------
from bs4 import NavigableString, Tag
for element in tag_p_nexts:
    isString = type(element) == NavigableString
    isTag = type(element) ==Tag


html = """<html> <head><title>test site</title></head> <body><p>test1</p>
<p>test2</p><p id는 ='f' class= "t">test3</p><a>aaa</a><b>bbb</b></body></html>"""
soup = bs(html, 'lxml')
#------------- find_all()--------
print("============find_all=========")
soup.find_all() #모든 태그 가져오기.
print(soup.find_all('p'))
print("id =f : ",soup.find_all(id='f'))
print("id absence :",soup.body.find_all(id=False))
print("id presence :", soup.find_all('p',id=True)) # p태그중 id가 있는
print("class presence :", soup.find_all('p',class_=True)) # p태그중 class가 있는
print("class presence :", soup.find_all('p', 't')) # p태그중 t class가 있는 class_생갹 가능.
print("text = test1", soup.find_all('p',text='test1'))
#href, src,등도 가능.

#찾는 태그의 양 제한
soup.find_all('p', limit=1)

#여러 태그 가져오기
print(soup.find_all(['a','b']))

#-----------웹 드라이버 --------------
# driver = webdriver.Chrome('./chromedriver')


