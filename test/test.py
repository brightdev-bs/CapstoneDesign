import requests as req
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--sessionId', type=str)
args = parser.parse_args()

files = {'face': open("testImage.png", 'rb')}
hash = "ffe7e4fcdc824020"
precision = "87%"
header = {'cookie': 'JSESSIONID='+args.sessionId}

try:
    result = req.post('http://localhost:8080/api/detection/result', files=files, data={'hash': hash, 'precision':precision}, headers =header)
    files = {'face': open("testImage.png", 'rb')}
    result = req.post('http://localhost:8080/api/detection/result', files=files, data={'hash': hash, 'precision':precision}, headers =header)
    files = {'face': open("testImage.png", 'rb')}
    result = req.post('http://localhost:8080/api/detection/result', files=files, data={'hash': hash, 'precision':precision}, headers =header)

    print(result)
except Exception as E:
    print("Encode 전송 에러")
    print(E)
    pass

print("이미지 전송 완료.")
