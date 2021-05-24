
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
from PIL import Image
import imagehash

from argparser import args

'''
class saveFileErrorHandling(Exception):
  def __str__(self, string:str, savePath:str):
        os.remove(savePath)
        return string
'''


'''
      DTO lists
      savePath : 경로
      saveUrl : 다운받은 URL
'''
class lists:
    
    def __init__(self, savePath:str, saveUrl:str):
        self.savePath = savePath
        self.saveUrl = saveUrl
        
    def getLists(self):
        return self.savePath, self.saveUrl

    def parseName(self):
        return self.savePath.split("/")[-1]

    #need to be str
    def getHash(self):
        img = Image.open(self.savePath)
        hash = (imagehash.average_hash(img))
        return hash

        
'''
    크롤링 class의 기본 base class

'''
class utillClass(threading.Thread):
  
  def __init__(self, loop_time = 1.0/60):
    super(utillClass, self).__init__()
    self.timeout = loop_time
    self.user_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    
    os.makedirs(args.saveDir, exist_ok = True)
    os.makedirs(args.garbageDir, exist_ok = True)
    os.makedirs(args.saveVideoDir, exist_ok = True)
    os.makedirs(args.DBfileDir, exist_ok = True)
    
    
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
  

#크롤링 이미지에서 얼굴이 있는 이미지만 추출하는 함수
  def get_faceKeyFrame(self, saveInformation:lists):
    
      succ_lists = []
    
      print("이미지 수집 완료. 이미지 분류를 시작합니다.")
      
      for i_lists in saveInformation:

        base_image_path = i_lists.savePath

        print(base_image_path)
        
        try:
          temp_face_location = face_recognition.load_image_file(base_image_path)
        except Exception as E:
            print(E, end=" ")
            self.saveFileErrorHandling("get_faceKeyFrame exception handling - 알수없는 형식", i_lists)
            continue
        
        w, h, color = temp_face_location.shape

        #너무 작은 이미지 제거
        if(w<= 112 or h<=112):
          self.saveFileErrorHandling(" delete. - size too small", i_lists)
          continue

        #너무 큰 사진(카드 뉴스 등) 제거 
        #if(w>=4900 or h>=4900):
        # self.saveFileErrorHandling(" delete. - size too big", i_lists)
        # continue

        temp_encoding = face_recognition.face_encodings(temp_face_location)
        countofpics = 0


        if len(temp_encoding) == 0:
          self.saveFileErrorHandling(" delete. - no face", i_lists)
        else:
            for (top, right, bottom, left) in face_recognition.face_locations(temp_face_location):
                
                face_img = temp_face_location[top:bottom, left:right]
                
                #opencv는 gif 취급안해서 삭제
                #svimg = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
                
                pil_img = Image.fromarray(face_img)

                head, ext = i_lists.savePath.split(".")[1:]
                head = "./"+head + "_changed_" + str(countofpics)+ "." + ext
                
                pil_img.save(head)

                #cv2.imwrite(head, svimg)
                countofpics +=1
                succ_lists.append(lists(head, i_lists.saveUrl))

            #self.sender(i_lists.saveUrl)
            os.remove(i_lists.savePath)
      
      return succ_lists
      

#분류완료후 DB에 전송
#이미지의 Hash 정보를 이용하여 유일한 이미지만 저장소에 저장되게 관리한다.
#이미지나 url의 값은 DB에서 중복되도 된다.
#보낸 시간대를 primary key로 사용한다

#connection: keep-alive 
  def sender(self, base_image_paths:lists):
    
   
    if len(base_image_paths) != 0:
      print("이미지 분류 완료. 이미지 등록을 시작합니다.")
      time.sleep(2)
      
      now = datetime.datetime.now()
      count =0

      for base_image_path in base_image_paths:
        # files = {'face': open(base_image_path, 'rb')}
        #fileName = base_image_path.split("/")[-1]
        
        count+=1

        #file_ext = ("."+base_image_path.savePath.split('.')[-1]).strip()
        #print(file_ext)

        #file_id = str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "_" + str(now.hour) + "_" + str(now.minute) + "_" + str(now.second) +"_"+str(count) + file_ext

        file_hash = str(base_image_path.getHash())

        file_url = base_image_path.saveUrl
        
        try:

          #print(file_id)
          print(file_url)
          print(file_hash)

          #result = req.post('http://ec2-13-209-242-131.ap-northeast-2.compute.amazonaws.com:8080/api/saveface', json ={"url": file_url, "hash": file_hash})
          #print(result)

        except Exception as E:
          print("Encode 전송 에러")
          print(E)
          self.saveFileErrorHandling("Encode 전송 에러", base_image_path)
          pass
        shutil.move(base_image_path.savePath, args.DBfileDir+file_hash+".jpg")
      print("이미지 전송 완료.")
      
    else:
      print("Get Face Dection PASS")
      pass

  #dummy function
  def moveAndDelete(self, toPath:str, fromPath:str, currentTimeDir:str="", folderName:str='frames_', ext:str='jpg'):
    count=0
    print(fromPath+ currentTimeDir+"*."+ext)    
    for i in glob.glob(fromPath+ currentTimeDir+"/*."+ext):
      print("move " + i)
      newName = toPath+currentTimeDir +"_"+str(count)+"."+ext
      print(newName)
      shutil.move(i, newName)
      count+=1
  
    os.rmdir(fromPath+ currentTimeDir+"/")


