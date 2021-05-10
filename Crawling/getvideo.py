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
import shutil

import utills

from argparser import args 

'''
    youtube에서 video 받아오는 class 
'''
class _Video(utills.utillClass):

  def __init__(self, loop_time = 1.0/60):
    print("Start")
    self.timeout = loop_time
    self.BASE_SEARCH_URL = "https://www.youtube.com/results?search_query="
    self.keyword='강남스타일' #<--------------원하는 키워드입력! 위의 url은 변경하지 말것

    super(_Video, self).__init__()


  # get uri lists
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
  
  #video youtube에서 받아와서 ffmpeg로 변환 
  def get_Video(self, url:str, current_time:str):
    yt=pytube.YouTube(url)
    
    #가장 화질 괜찮은것 받아옴
    videos=yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    
    #print("*******************************len"+str(len(videos)))

    down_dir=args.saveVideoDir
    os.makedirs(args.saveDir, exist_ok = True)
    os.makedirs(args.garbageDir, exist_ok = True)
    os.makedirs(args.saveVideoDir, exist_ok = True)
    
    videos.download(down_dir)
    newFileName = current_time+videos.default_filename
    oriFileName = videos.default_filename

    subprocess.call(['ffmpeg','-i',os.path.join(down_dir,oriFileName),os.path.join(down_dir,newFileName)])

    print("========================")
    print(oriFileName+" 저장 완료")
    print("========================")
    video_path=args.saveVideoDir+newFileName

    #os.remove(args.saveVideoDir+oriFileName)

    return oriFileName, utills.lists(video_path, url)

 #frame 추출
  def get_Frame(self, video_list:utills.lists, current_time_dir:str):
    vf.extract_keyframes(video_list.savePath, method='iframes', output_dir_keyframes=current_time_dir)

    lists = []
    
    count = 0 

    for i in glob.glob(args.saveVideoDir + current_time_dir+"/*.jpg"):
      newname = args.saveVideoDir + current_time_dir + "/" + current_time_dir + "_" + str(count) + ".jpg" 
      os.rename(i, newname)
      count+=1 
      lists.append(utills.lists(newname, video_list.saveUrl))
    
    return lists

    
  def run(self):
    print("SEARCH_KEYWORD: "+ self.keyword )
    url_list=self.get_UrlList()
    count=1

    print(url_list)
    
    pics_lists = []

    oriName_lists = []


    for url in url_list:
       
       print("++++++++++++ {} 번째 동영상 저장 시작++++++++++++".format(count))
       count+=1
       now = datetime.datetime.now()
       current_time = str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "_" + str(now.hour) + "_" + str(now.minute) + "_" + str(now.second)
       current_time_dir = 'frames_' + current_time
       
       ori_name, video_list=self.get_Video(url, current_time)
       oriName_lists.append(ori_name)
       
       time.sleep(1)
       saveInformation = self.get_Frame(video_list, current_time_dir)
       pics_lists.extend(self.get_faceKeyFrame(saveInformation))

       try:
           print("1")
       
       #음성파일 Exception로 제거
       except Exception as E:
           print(E)
           self.saveFileErrorHandling("remove only record file", video_list)
           continue
         
       #self.moveAndDelete(args.saveDir, args.saveVideoDir, current_time_dir, "frames_")
       
       shutil.move(video_list.savePath, args.saveVideoDir+current_time_dir+"/"+ori_name)
       time.sleep(3)
       if(count>=5):
           break
    #trim videos
    for i in oriName_lists:
        print("trimming" + i)
        os.remove(args.saveVideoDir+i)
        


    print("키워드 "+self.keyword+"에 대한 동영상 저장 완료")
  
if __name__ == '__main__':
  _Video().run()
