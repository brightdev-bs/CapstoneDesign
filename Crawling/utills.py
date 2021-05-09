
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
import shutil

from argparser import args

'''
class saveFileErrorHandling(Exception):
  def __str__(self, string:str, savePath:str):
        os.remove(savePath)
        return string
'''
class lists:
    
    def __init__(self, savePath:str, saveUrl:str):
        self.savePath = savePath
        self.saveUrl = saveUrl

    def getLists(self):
        return self.savePath, self.saveUrl

class utillClass(threading.Thread):
  
  def __init__(self, loop_time = 1.0/60):
    self.timeout = loop_time
    self.user_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    super(utillClass, self).__init__()
    
  def saveFileErrorHandling(self, string:str, i_lists:lists):
    print(string+ " - "+i_lists.saveUrl)
    print("PATH= "+i_lists.savePath)

    #mvdir = args.garbageDir
    #shutil.move(i_lists.savePath, mvdir+foldername+filename)
    #디버깅용, 삭제하지않고 일단 사진 폴더 이동
    os.remove(i_lists.savePath)

    F = open("./imgs/LogOfSaveFile.txt","a")
    print(string+"-"+i_lists.saveUrl+"\n", file=F)
    F.close()
    
  def get_faceKeyFrame(self, saveInformation:lists):
    
      base_image_paths = []
    
      for i in saveInformation:
          path = i
          base_image_paths.append(path)
          
      print("이미지 수집 완료. 이미지 분류를 시작합니다.")
      time.sleep(2)
      for i_lists in base_image_paths:

        base_image_path = i_lists.savePath
        print(base_image_path)
        
        try:
          temp_face_location = face_recognition.load_image_file(base_image_path)
        except Exception as E:
            print(E, end=" ")
            self.saveFileErrorHandling("get_faceKeyFrame exception handling - 알수없는 형식", i_lists)
            continue
        
        w, h, color = temp_face_location.shape

        if(w<= 112 or h<=112):
          self.saveFileErrorHandling(" delete. - size too small", i_lists)
          continue

        if(w>=6000 or h>=6000):
          self.saveFileErrorHandling(" delete. - size too big", i_lists)
          continue

        temp_encoding = face_recognition.face_encodings(temp_face_location)

        if len(temp_encoding) == 0:
          self.saveFileErrorHandling(" delete. - no face", i_lists)

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


  
  def moveAndDelete(self, toPath:str, fromPath:str, currentTimeDir:str, folderName='frames_', ext='jpg'):
    count=0
    print(fromPath+ currentTimeDir+"*."+ext)    
    for i in glob.glob(fromPath+ currentTimeDir+"/*."+ext):
      print("move " + i)
      newName = toPath+currentTimeDir +"_"+str(count)+"."+ext
      print(newName)
      shutil.move(i, newName)
      count+=1
  
    os.rmdir(fromPath+ currentTimeDir+"/")


