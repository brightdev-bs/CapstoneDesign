# _*_ coding:utf-8 _*_

import utills
import requests as req
from urllib import request
from bs4 import BeautifulSoup as bs
from utills import utillClass


from utills import lists
from argparser import args

import time
import datetime
import os
import face_recognition
import glob
import threading
import sys


#import videokf as vf

#DCinside 크롤링하는 class
class _DCImage(utills.utillClass):
  def __init__(self, loop_time = 1.0/60):
    super(_DCImage, self).__init__()
    print("DCinside Crawler Init")
  
    self.BASE_PARSER_URL = "https://gall.dcinside.com/m"
    self.DC = "https://gall.dcinside.com/"
    
#카테고리 긁어오는 함수
  def get_Categories(self):
    res = req.get(self.BASE_PARSER_URL,headers = {'User-Agent' : self.user_Agent})
    soup = bs(res.content, 'lxml')
    #갤러리 카테고리 get
    categories = soup.select('#categ_listwrap > div:nth-child(1) > div > div ul li a')
  
    category_url = {}
    
    for category in categories:
        
      #print(category.text)
      
      #도배 게시
      if(category.text =="이승윤 유튜브" or category.text =="이승윤(가수)"):
          print("pass"+category.text)
          continue
        
      category_url[category.text] =category.get('href')
    
    #print(category_url)    
    return category_url

#게시판 페이지 하나 긁어오는 함수
  def set_Category(self, page, keyUrl):
    url = keyUrl
    myurl , myid = url.split('?id=')

    res = req.get(myurl , params={'id': myid, 'page': page}, headers = {'User-Agent' : self.user_Agent})    
    soup = bs(res.content, 'lxml')

    return soup
  
#image가 있는 게시판만 순회
  def get_UrlList(self, soup):
    posts = soup.find('tbody').find_all('tr')     
    
    url_list = []
    
    #post중 image아이콘이 있는 post만 탐색.
    for post in posts:
        image_flag = post.find('em', class_='icon_img icon_pic')
        if image_flag is None:
            continue
        title_tag = post.find('a', href=True)
        url_list.append(self.DC+title_tag['href'])
    return url_list

#이미지 다운로드
  def get_Image(self, view):
    now = datetime.datetime.now()
    count = 0

   
    image_response =  req.get(view, headers={'User-Agent' : self.user_Agent})
    
    print(image_response.url)
    
    soup = bs(image_response.content, 'lxml')
    #image_tag = soup.find('div', class_='writing_view_box').find_all('div')
        
    image_downloader = soup.find('div', class_='appending_file_box').find('ul').find_all('li')
    
    images =[]
    
    for li in image_downloader:
        
        time.sleep(1)
        
        img_tag = li.find('a', href=True)
        img_url = img_tag['href']
        
        print("url : "+img_url)
        
        file_ext = img_url.split('.')[-1]

        current_time = str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "__" + str(now.hour) + "_" + str(now.minute) + "_" + str(now.second)


        savedir = args.saveDir
        garbagedir = args.garbageDir
        
        savename = savedir+current_time + str(count)+"."+file_ext
        count+=1
        
        opener = request.build_opener()
        opener.addheaders = [('User-agent', self.user_Agent), ('Referer', image_response.url)]
        
        request.install_opener(opener)
        request.urlretrieve(img_url, savename)
        images.append(lists(savename, image_response.url))
    
    return images

  def run(self):
    print("국내 커뮤니티 사이트 URL : "+self.BASE_PARSER_URL)
    print("DC Crawler run")

    category_list = self.get_Categories()
    
    
    
    for key_name in category_list.keys():  
        url_list = []
        
        #1~25 page
        for page in range(1,25):
            count = 0
            print("*"+str(page)+"*")
            try:
                #time.sleep(2)
                category_page = self.set_Category(page, category_list.get(key_name))
                url_list += self.get_UrlList(category_page)
                
            except Exception as E:
                print(E)
                continue
            
        pics_lists = []
        
        for url in url_list:
          # vf.extract_keyframes(url, method='iframes', output_dir_keyframes='./img')
          
            view = url
              
            try:
                time.sleep(2) 
                saveInformation = self.get_Image(view)
                pics_lists.extend(self.get_faceKeyFrame(saveInformation))

            except AttributeError as E:
              #get_image에서 soup가 null(cotent가 null)일때 일어나는 Exception
                print(E)
                continue
              
              #request 관련 error (게시판이 삭제될경우 많이 일어남)
            except Exception as E:
                print(E)
                print("EXCEPTION")
                  
                time.sleep(10)
                continue
       
            count += 1
            #이미지 20개 단위로 전송
            if(len(pics_lists)>=20):
                self.sender(pics_lists)
                pics_lists.clear()
                
        #connection: keep-alive 

        self.sender(pics_lists)
        print(key_name + " 카테고리의 모든 수집을 완료했습니다. 다음 카테고리로 넘어갑니다.")
        pics_lists.clear()
        url_list.clear()

if __name__ == '__main__':
    _DCImage().run()
