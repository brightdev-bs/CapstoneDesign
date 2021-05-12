import requests as req

files = {'face': open("testImage.png", 'rb')}
pageUrl = "www.test.com"
precision = "87%"
doneDetection = ""

try:
    result = req.post('http://localhost:8080/api/detection/result', files=files, data={'url': pageUrl, 'precision':precision})

    # detection이 끝났을 때.
    result = req.post('http://localhost:8080/api/detection/result', files=files, data={'url': doneDetection, 'precision':doneDetection})

    # result = req.post('http://ec2-13-209-242-131.ap-northeast-2.compute.amazonaws.com:8080/api/detectuin/result',
    #                   data={"fileName": fileName, "url": pageUrl})
    print(result)
except Exception as E:
    print("Encode 전송 에러")
    print(E)
    pass

print("이미지 전송 완료.")
