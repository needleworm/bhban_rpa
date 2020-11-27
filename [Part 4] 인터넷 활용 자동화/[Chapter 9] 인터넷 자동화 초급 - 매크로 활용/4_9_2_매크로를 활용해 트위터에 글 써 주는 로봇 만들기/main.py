#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 파이썬으로 6개월치 업무를 하루만에 끝내기
Last Modification : 2020.03.02.
"""

import sys
import time
import twitter_bot_tweet as tb


# 작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 아이디를 입력받습니다.
id = sys.argv[1]

# 패스워드를 입력받습니다.
ps = sys.argv[2]

# 트윗할 내용들이 적힌 파일을 입력받습니다.
filename = sys.argv[3]

# 크롤러를 불러옵니다.
BOT = tb.TwitterBot(filename)

# 로그인을 시도합니다.
BOT.login(id, ps)

# 로그인에 성공했으니 스크린샷이나 한 번 찍어줍시다.
BOT.save_screenshot(str(time.time) + ".png")

# 트위터에 모든 멘션을 올립니다.
BOT.tweet_all()

# 결과 화면을 잠시 감상하기 위해 10초동안 방치합니다.
time.sleep(10)

# 크롤러를 닫아줍니다.
BOT.kill()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
