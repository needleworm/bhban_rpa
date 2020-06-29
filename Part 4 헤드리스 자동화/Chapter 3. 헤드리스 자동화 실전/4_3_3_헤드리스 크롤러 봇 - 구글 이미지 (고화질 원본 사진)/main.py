#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.03.02.
"""

import sys
import os
import time
import google_image_crawler as ic


# 작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 수집된 사진을 저장할 디렉터리를 입력받습니다.
out_dir = sys.argv[1]

# 검색할 키워드를 입력받습니다.
keyword = sys.argv[2]

# 수집할 이미지 개수를 입력받습니다.
number = int(sys.argv[3])

# 결과물을 저장할 폴더를 생성합니다.
if out_dir not in os.listdir():
    os.mkdir(out_dir)

# 크롤러를 불러옵니다.
BOT = ic.ImgCrawler(out_dir)

# 크롤러에게 이미지 크롤링을 시킵니다.
BOT.crawl_images(keyword, number)

# 크롤러를 닫아줍니다.
BOT.kill()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
