#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.03.02.
"""

import sys
import time
import insta_bot_reply as ib


# 작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 계정 정보가 입력된 파일 이름을 입력받습니다.
id_filename = sys.argv[1]

# 검색할 태그가 기록된 파일을 입력받습니다.
tag_filename = sys.argv[2]

# 크롤러를 불러옵니다.
BOT = ib.LikeBot()

# id 파일을 불러옵니다.
id_file = open(id_filename)
# 리스트로 만들어 줍니다.
IDs = []
for line in id_file:
    splt = line.split(",")
    if len(splt) != 2:
        continue
    IDs.append((splt[0].strip(), splt[1].strip()))

# 태그 파일도 불러옵니다.
tag_file = open(tag_filename)

# 리스트로 만들어 줍니다.
Tags = tag_file.read().split("\n")

# 무한반복 할 때에는 while True가 최고입니다.
while True:
    # 계정을 하나씩 불러옵니다.
    for account in IDs:
        # 계정이 바뀌었으니 드라이버를 껐다가 켜 줍니다.
        BOT.driver_refresh()
        # 로그인을 합시다.
        BOT.login(account)
        # 태그를 하나씩 불러옵니다.
        for tag in Tags:
            # 불러온 태그를 대상으로 탐색하며 좋아요를 누릅니다. 게시물은 한 번에 100개씩만 좋아요 누르고 댓글 답니다.
            BOT.insta_jungdok(tag, num=100)
        # 계정이 바뀔 때마다 1분씩 기다려 줍니다.
        # 동일한 멘션을 너무 자주 입력하면 밴을 당하기 때문입니다.
        time.sleep(60)

# 크롤러를 닫아줍니다.
BOT.kill()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
