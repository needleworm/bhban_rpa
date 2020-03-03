#-*-coding:euc-kr
"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.03.02.
"""

import sys
import time
import twitter_automention as ta


# 작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 아이디를 입력받습니다.
idfile = sys.argv[1]

# 트윗할 내용들이 적힌 파일을 입력받습니다.
filename = sys.argv[2]

# 트윗 입력 x좌표를 입력받습니다.
mention_x = int(sys.argv[4].strip())

# 트윗 입력 y좌표를 입력받습니다.
mention_y = int(sys.argv[5].strip())

# 아이디와 비밀번호를 세트로 저장해 둘 리스트를 만듭니다.
IDs = []

# 아이디가 기재된 파일을 불러옵니다.
idfile = open(filename)

# 이걸 한 줄씩 읽어옵니다.
for line in idfile:
    # 각 줄을 컴마로 쪼개 줍니다.
    splt = line.split(",")
    # 내용물이 두개가 아닌 라인은 모두 날려줍니다.
    if len(splt) != 2:
        continue
    # IDs에 아이디와 비밀번호를 저장합니다.
    IDs.append((splt[0].strip(), splt[1].strip()))

# 크롤러를 불러옵니다.
BOT = ta.TwitterBot(filename, (mention_x, mention_y))

# IDs에 저장된 계정을 하나씩 불러옵니다.
for ids in IDs:
    # 로그인을 시도합니다.
    BOT.login(ids)
    # 로그인에 성공했으니 스크린샷이나 한 번 찍어줍시다.
    BOT.save_screenshot(str(time.time) + ".png")
    # 트위터에 모든 멘션을 올립니다.
    BOT.tweet_all()
    # 크롤러를 닫아줍니다.
    BOT.kill()
    # 크롤러를 다시 켜서 트위터로 접속합니다.
    BOT.go_to_twitter()

# 결과 화면을 잠시 감상하기 위해 10초동안 방치합니다.
time.sleep(10)

# 크롤러를 닫아줍니다.
BOT.kill()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
