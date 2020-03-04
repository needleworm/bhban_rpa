#-*-coding:euc-kr
"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.03.02.
"""

import sys
import time
import news_bot as nb


# 작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 아이디를 입력받습니다.
id = sys.argv[1]

# 비밀번호를 입력받습니다.
ps = sys.argv[2]

# 스크랩할 뉴스 키워드를 입력받습니다.
keyword = sys.argv[3]

# 트윗 말미에 입력할 문구를 작성합니다.
# 너무 길면 트윗이 입력이 안 됩니다. 짧게 입력합시다.
endswith = "#뉴스 #수집 #봇"

# 크롤러를 불러옵니다.
BOT = nb.NewsBot(endswith)

# 트위터 로그인을 시도합니다.
BOT.login(id, ps)

# 작업을 수행합니다.
BOT.news_go_go(keyword)

# 크롤러를 닫아줍니다.
BOT.kill()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
