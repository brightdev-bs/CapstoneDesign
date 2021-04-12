import requests as req
from bs4 import BeautifulSoup as bs
import time
import datetime
import os
import face_recognition
import glob
import threading


class _Ilbe(threading.Thread):
    def __init__(self, loop_time=1.0 / 60):
        print("Ilbe Crawler Init")
        self.timeout = loop_time
        self.BASE_PARSER_URL = "https://www.dcinside.com/"

        self.DC = "https://gall.dcinside.com/list.php?id="

        self.myHeader = [
            {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}, ]

        super(_Ilbe, self).__init__()

    def get_Categories(self):
        res = req.get(self.BASE_PARSER_URL)
        soup = bs(res.content, 'lxml')

        # print(soup)

        categories = soup.select('.all_list dl a')

        # print(categories)
        category_url = {}

        for category in categories:
            category_url[category.text] = category.get('href')

        # print("****"+str(category_url))
        print(category_url)

        return category_url

    def set_Category(self, keyUrl):
        url = keyUrl

        if url.find("https://gall.dcinside.com/list.php?id=") != -1:
            newurl = "https://gall.dcinside.com/list.php?id="
        elif url.find("https://gall.dcinside.com/board/lists/?id=") != -1:
            newurl = "https://gall.dcinside.com/board/lists/?id"
        else:
            return 0, 0

        print(url)

        myid = url.split('?id=')[1]

        # print(myid)

        res = req.get(newurl, params={'id': myid, 'page': 0}, headers=self.myHeader[0])

        # print(res)

        soup = bs(res.content, 'html.parser')

        art_list = soup.find('tbody').find_all('tr')

        # print(art_list)

        list_size = url.split('&listSize=')[1].split('&listStyle')[0]

        post_count = soup.select('div.board-list script')[1].string.split('.html("')[1].split('");')[0].replace(',', '')
        page = int(int(post_count) // int(list_size))
        rest = int(post_count) % int(list_size)

        if rest != 0:
            page = page + 1

        return page, list_size

    def get_UrlList(self, url):
        res = req.get(url)
        soup = bs(res.content, 'lxml')
        posts = soup.select('li span.title a.subject')

        url_list = []

        for post in posts:
            url_list.append(post.get('href'))

        return url_list

    def get_Image(self, view):
        now = datetime.datetime.now()

        res = req.get(view)
        soup = bs(res.content, 'lxml')
        images = soup.select('img.-up-content.-lazy-image')

        if len(images) != 0:
            for i in range(len(images)):
                image_data = images[i].get('data')

                if '.jpg' in image_data or '.jpeg' in image_data:
                    image_format = 'jpg'

                    image_url = req.get(image_data)
                    time.sleep(2)
                    current_time = str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "__" + str(
                        now.hour) + "_" + str(now.minute) + "_" + str(now.second)
                    if os.path.isdir('Ilbe') == False:
                        os.mkdir('Ilbe')
                    file = open('Ilbe/ilbe_' + str(i) + "_" + current_time + '.' + image_format, 'wb')
                    file.write(image_url.content)
                    file.close()
        else:
            print("Get Image PASS")
            pass

    def get_faceKeyFrame(self):
        base_image_paths = glob.glob('./Ilbe/*.jpg')
        print("이미지 수집 완료. 이미지 분류를 시작합니다.")
        time.sleep(2)
        for base_image_path in base_image_paths:
            temp_face_location = face_recognition.load_image_file(base_image_path)
            temp_encoding = face_recognition.face_encodings(temp_face_location)

            if len(temp_encoding) == 0:
                print(base_image_path + "를 삭제합니다.")
                os.remove(base_image_path)

    def get_faceDetection(self, pageUrl):
        base_image_paths = glob.glob('./Ilbe/*.jpg')
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
        print("국내 커뮤니티 사이트 URL : https://www.ilbe.com")
        print("Ilbe Crawler run")

        category_list = self.get_Categories()
        count = 0
        for key_name in category_list.keys():
            print(key_name)
            continue
            category_page, category_list_size = self.set_Category(category_list.get(key_name))

            for page in range(1, category_page + 1):
                get_url = self.BASE_PARSER_URL + category_list.get(key_name) + "?page=" + str(
                    page) + "&listSize=" + str(category_list_size) + "&listStyle=list"

                url_list = self.get_UrlList(get_url)

                for url in url_list:
                    view = self.BASE_PARSER_URL + url

                    print("이미지 수집 시작. Ilbe 폴더에 저장됩니다.")
                    print("카테고리 이름 : " + key_name)
                    print("카테고리 URL  : " + get_url)
                    print("게시글 URL    : " + view)
                    print("페이지        : " + str(page) + "/" + str(category_page))
                    print("리스트 사이즈 : " + str(category_list_size))
                    time.sleep(2)

                    self.get_Image(view)
                    self.get_faceKeyFrame()
                    self.get_faceDetection(view)
                    count += 1

                print(key_name + " 카테고리의 " + str(page) + "페이지 수집을 완료했습니다. " + str(page + 1) + "페이지 수집을 시작합니다.")
            print(key_name + " 카테고리의 모든 수집을 완료했습니다. 다음 카테고리로 넘어갑니다.")


_Ilbe().run()