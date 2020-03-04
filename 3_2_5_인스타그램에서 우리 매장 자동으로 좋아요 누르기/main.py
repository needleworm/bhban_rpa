#-*-coding:euc-kr
"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.03.02.
"""

import sys
import time
import insta_jungdok as ij


# 작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 아이디를 입력받습니다.
id = sys.argv[1]

# 패스워드를 입력받습니다.
ps = sys.argv[2]

# 검색할 태그를 입력받습니다.
tag = sys.argv[3]

# 좋아요 버튼 파일이름을 입력받습니다.
like_button = sys.argv[4]

# 빨간색 좋아요 버튼 파일이름을 입력받습니다.
red_like_button = sys.argv[5]

# 반복 회수를 입력받습니다.
NUMBER = int(sys.argv[6].strip())

# 크롤러를 불러옵니다.
BOT = ij.LikeBot(like_button, red_like_button)

# 작업을 수행합니다.
BOT.insta_jungdok(id, ps, tag, NUMBER)

# 크롤러를 닫아줍니다.
BOT.kill()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
