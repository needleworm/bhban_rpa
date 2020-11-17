#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.03.02.
"""

import sys
import time
import twitter_bot_news as tb


# 작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 계정 정보가 입력된 파일 이름을 입력받습니다.
id_filename = sys.argv[1]

# 뉴스 검색을 할 키워드를 입력받는다.
keyword = sys.argv[2]

# 트윗 말미에 입력할 문구를 작성합니다.
# 너무 길면 트윗이 입력이 안 됩니다. 짧게 입력합시다.
endswith = "#뉴스 #수집 #봇"

# 크롤러를 불러옵니다.
BOT = tb.TwitterBot(endswith)

# id가 기록된 파일을 열어 옵니다.
IDS = open(id_filename)

# 파일을 한 줄씩 읽으며 작업을 수행합니다.
for line in IDS:
    # 읽어온 파일을 한 줄씩 읽어와, 컴마를 기준으로 쪼개줍니다.
    splt = line.split(",")
    # 컴마를 기준으로 쪼갠 결과물이 2조각이 아니면 다음 줄로 넘어갑니다.
    if len(splt) != 2:
        continue
    # 컴마를 기준으로 쪼갠 결과물 중 첫 번째 값을 아이디, 두 번째 값을 비밀번호로 지정합니다.
    id = splt[0].strip()
    ps = splt[1].strip()
    # 로그인을 시도합니다.
    BOT.login(id, ps)
    # 작업을 수행합니다.
    BOT.news_go_go(keyword)
    # 브라우저를 껐다가 켭니다.
    # 사실 이렇게 코드를 짜면 불필요한 리로드가 발생합니다.
    # 작업이 끝나면 창을 바로 닫으면 되는데, 이렇게 코딩하면 마지막 순서가 끝난 뒤 굳이 창을 한 번 껐다가 켠 다음 다시 끕니다.
    # 그런데 똘똘하게 코딩하는 것도 좋지만, 빨리 만드는게 더 중요하잖아요.
    # 그러니 그냥 내버려 둡시다.
    # 효율적인 코드가 좋긴 하지만, 업무를 자동화 하는 데 있어서 효율이란 '제작 과정의 효율' 입니다.
    # 단기간에 자동화 코드를 만들 수 있다면, 작동 방식이 조금 어설퍼도 효율적인 것입니다.
    # 잘 짠 코드보다 좀 느리면 어때요. 퇴근할때 돌려 두고 집에 가면 되지.
    BOT.reload_browser()
    # 10초정도 대기합니다.
    time.sleep(10)

# 크롤러를 닫아줍니다.
BOT.kill()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
