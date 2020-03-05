#-*-coding:euc-kr
"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.03.02.
"""

import sys
import os
import time
import thaad


# 작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# id를 입력받습니다.
id = sys.argv[1]

# 패스워드를 입력받습니다.
ps = sys.argv[2]

# 키워드가 기재된 파일을 입력받습니다.
keyword_file_name = sys.argv[3]

# 보호받을 게시물 주소들이 저장된 파일을 입력받습니다.
target_file_name = sys.argv[4]

# 몇 번 반복할 지 입력받습니다. 0을 입력받으면 무한정 반복합니다.
number = int(sys.argv[5])

# 크롤러를 불러옵니다.
BOT = thaad.Thaad(id, ps, keyword_file_name, target_file_name)

# 반복문은 while이 짱입니다.
number -= 1
while number != 0:
    BOT.run_thaad()
    number -= 1
BOT.run_thaad()

# 크롤러를 닫아줍니다.
BOT.kill()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
