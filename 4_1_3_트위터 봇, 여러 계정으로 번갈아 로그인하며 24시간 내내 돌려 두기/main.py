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

# 계정 정보가 입력된 파일 이름을 입력받습니다.
id_filename = sys.argv[1]

# 기사 검색을 할 키워드가 기록된 파일을 입력받습니다.
keyword_filename = sys.argv[3]

# 트윗 말미에 입력할 문구를 작성합니다.
# 너무 길면 트윗이 입력이 안 됩니다. 짧게 입력합시다.
endswith = "#뉴스 #수집 #봇"

# 크롤러를 불러옵니다.
BOT = nb.NewsBot(endswith)

# id 파일을 불러옵니다.
id_file = open(id_filename)
# 리스트로 만들어 줍니다.
IDs = []
for line in id_file:
    splt = line.split(",")
    if len(splt) != 2:
        continue
    IDs.append((splt[0].strip(), splt[1].strip()))

# 키워드 파일도 불러옵니다.
keyword_file = open(keyword_filename)
# 리스트로 만들어 줍니다.
Keywords = keyword_file.read().split("\n")

# 무한반복 할 때에는 while True가 최고입니다.
while True:
    # 계정을 하나씩 불러옵니다.
    for account in IDs:
        # 계정이 바뀌었으니 드라이버를 껐다가 켜 줍니다.
        BOT.driver_refresh()
        # 키워드를 하나씩 불러옵니다.
        for keyword in Keywords:
            # 불러온 키워드를 대상으로 검색과 포스팅을 수행합니다.
            BOT.news_go_go(keyword)
        # 계정이 바뀔 때마다 1분씩 기다려 줍니다.
        # 동일한 멘션을 너무 자주 입력하면 트위터로부터 밴을 당하기 때문입니다.
        # 단, 키워드를 충분히 넉넉하게 입력했다면 동일 키워드로 다시 뉴스기사를 검색하는 확률이 줄어드므로
        # 키워드가 충분히 다양하다면 대기 시간을 줄여도 됩니다.
        time.sleep(60)

# 크롤러를 닫아줍니다.
BOT.kill()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
