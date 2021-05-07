import pytube
import shutil
import os
import subprocess
import time
import datetime
import threading
import requests
import lxml
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
import videokf as vf
import face_recognition
import glob

class _Video(threading.Thread):
  def __init__(self, loop_time = 1.0/60):
    print("Start")
    self.timeout = loop_time
    self.BASE_SEARCH_URL = "https://www.youtube.com/results?search_query="
    self.keyword='강남스타일' #<--------------원하는 키워드입력! 위의 url은 변경하지 말것

    super(_Video, self).__init__()
    
  def get_Video(self,url):
    yt=pytube.YouTube(url)
    videos=yt.streams.all()
    
    for i in range(len(videos)):  #비디오 길이
      print(i,',',videos[i])

    cNum=14 #화질 0~21

    down_dir="./videos/"
    os.makedirs(down_dir, exist_ok = True)
    videos[cNum].download(down_dir)
    now = datetime.datetime.now()
    current_time = str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "__" + str(now.hour) + "_" + str(now.minute) + "_" + str(now.second)
    newFileName = current_time + ".mp4"
    oriFileName = videos[cNum].default_filename

    subprocess.call(['ffmpeg','-i',os.path.join(down_dir,oriFileName),os.path.join(down_dir,newFileName)])
    print("========================")
    print(oriFileName+" 저장 완료")
    print("========================")
    video_path="./videos/"+newFileName

    return video_path

  def get_UrlList(self):
    url = self.BASE_SEARCH_URL+self.keyword

    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get(url)
    soup = bs(driver.page_source, 'html.parser')
    driver.close()

    video_url = soup.select('a#video-title')

    url_list = []

    for i in video_url:
        url_list.append('{}{}'.format('https://www.youtube.com',i.get('href')))

    return url_list

  def get_faceKeyFrame(self, paths):
    for base_image_path in paths:
      temp_face_location = face_recognition.load_image_file(base_image_path)
      temp_encoding = face_recognition.face_encodings(temp_face_location)
      if len(temp_encoding) == 0:
        print(base_image_path + "를 삭제하였습니다.")
        os.remove(base_image_path)

  def get_Frame(self,video_path):
    vf.extract_keyframes(video_path, method='iframes', output_dir_keyframes='frames')
    time.sleep(3)
    now = datetime.datetime.now()
    current_time = str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "__" + str(now.hour) + "_" + str(now.minute) + "_" + str(now.second)
    current_time_dir = 'frames_' + current_time

    os.rename("./videos/frames", current_time_dir)
    print("폴더명 변경")

    base_image_paths = glob.glob('./'+current_time_dir+'/*.jpg')
    self.get_faceKeyFrame(base_image_paths)

  def run(self):
    print("SEARCH_KEYWORD: "+ self.keyword )
    url_list=self.get_UrlList()
    count=1

    # for url in url_list:
    #   print("++++++++++++ {} 번째 동영상 저장 시작++++++++++++".format(count))
    #   count+=1
    #   video_path=self.get_Video(url)
    #   self.get_Frame(video_path)
    #   time.sleep(3)

    print("++++++++++++ {} 번째 동영상 저장 시작++++++++++++".format(count))
    video_path=self.get_Video(url_list[0])
    self.get_Frame(video_path)
    
    print("키워드 "+self.keyword+"에 대한 동영상 저장 완료")
  
_Video().run()