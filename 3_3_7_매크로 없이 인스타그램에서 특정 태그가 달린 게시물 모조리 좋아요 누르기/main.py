#-*-coding:euc-kr
"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.03.02.
"""

import sys
import time
import insta_bot_like as ib


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

# 반복 회수를 입력받습니다.
NUMBER = int(sys.argv[4].strip())

# 크롤러를 불러옵니다.
BOT = ib.LikeBot()

# 인스타그램 로그인을 합니다.
BOT.login(id, ps)

# 작업을 수행합니다.
BOT.insta_jungdok(id, ps, tag, NUMBER)

# 크롤러를 닫아줍니다.
BOT.kill()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
