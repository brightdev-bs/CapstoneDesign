# _*_ coding:utf-8 _*_

import requests as req
from urllib import request
from bs4 import BeautifulSoup as bs
import time
import datetime
import os
import face_recognition
import glob
import threading
import sys
#import videokf as vf


class lists:
    
    def __init__(self, savePath:str, saveUrl:str):
        self.savePath = savePath
        self.saveUrl = saveUrl
        
    def getLists(self):
        return self.savePath, self.saveUrl
    
class _DCImage(threading.Thread):
  def __init__(self, loop_time = 1.0/60):
    print("Ilbe Crawler Init")
    self.timeout = loop_time
    self.BASE_PARSER_URL = "https://gall.dcinside.com/m"
    self.DC = "https://gall.dcinside.com/"
    self.user_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"

    super(_DCImage, self).__init__()
    

  def get_Categories(self):
    res = req.get(self.BASE_PARSER_URL,headers = {'User-Agent' : self.user_Agent})
    soup = bs(res.content, 'lxml')
    #갤러리 카테고리 get
    categories = soup.select('#categ_listwrap > div:nth-child(1) > div > div ul li a')
  
    category_url = {}
    for category in categories:
      category_url[category.text] =category.get('href')
    
    return category_url


  def set_Category(self, keyUrl):
    url = keyUrl
    myurl , myid = url.split('?id=')

    res = req.get(myurl , params={'id': myid, 'page': 1}, headers = {'User-Agent' : self.user_Agent})    
    soup = bs(res.content, 'lxml')

    return soup
  

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
        img_tag = li.find('a', href=True)
        img_url = img_tag['href']
        
        print("url : "+img_url)
        
        file_ext = img_url.split('.')[-1]

        current_time = str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "__" + str(now.hour) + "_" + str(now.minute) + "_" + str(now.second)
        savedir ="./imgs/"
        savename = savedir+current_time + str(count)+"."+file_ext
        count+=1
        os.makedirs(savedir, exist_ok = True)

        opener = request.build_opener()
        opener.addheaders = [('User-agent', self.user_Agent), ('Referer', image_response.url)]
        
        request.install_opener(opener)
        request.urlretrieve(img_url, savename)
        images.append(lists(savename, img_url))
    
    return images
    
    
  def get_faceKeyFrame(self, saveInformation):
    
    base_image_paths = []
    
    for i in saveInformation:
        path = i.savePath
        base_image_paths.append(path)
    
    print(base_image_paths)
    print("이미지 수집 완료. 이미지 분류를 시작합니다.")
    time.sleep(2)
    for base_image_path in base_image_paths:
      temp_face_location = face_recognition.load_image_file(base_image_path)
      temp_encoding = face_recognition.face_encodings(temp_face_location)

      if len(temp_encoding) == 0:
        print(base_image_path + "를 삭제합니다.")
        os.remove(base_image_path)


  def get_faceDetection(self, pageUrl):
    base_image_paths = glob.glob('./imgs/*.jpg')
    if len(base_image_paths) != 0:
      print("이미지 분류 완료. 이미지 등록을 시작합니다.")
      time.sleep(2)
      for base_image_path in base_image_paths:
        files = {'face': open(base_image_path, 'rb')}
        
        try:
          result = req.post('http://api.kuuwang.com/face/encode', files=files, data={'url': pageUrl}).text
          print(result)
        except Exception as E:
          print("Encode 전송 에러")
          print(E)
          pass

      print("이미지 등록 완료.")
    else:
      print("Get Face Dection PASS")
      pass


  def run(self):
    print("국내 커뮤니티 사이트 URL : "+self.BASE_PARSER_URL)
    print("DC Crawler run")


    category_list = self.get_Categories()
    count = 0
    for key_name in category_list.keys():      
      category_page = self.set_Category(category_list.get(key_name))
      url_list = self.get_UrlList(category_page)
        
      for url in url_list:
          # vf.extract_keyframes(url, method='iframes', output_dir_keyframes='./img')
          view = url
          time.sleep(2)
          saveInformation = self.get_Image(view)
          self.get_faceKeyFrame(saveInformation)
          # self.get_faceDetection(view)
          count += 1

      print(key_name + " 카테고리의 모든 수집을 완료했습니다. 다음 카테고리로 넘어갑니다.")

_DCImage().run()