#-*-coding:utf-8
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.02.12.
"""

import pyexcel.cookbook as pc
import sys
import time


# 작업 시작 메시지를 출력합니다.
print("Process Start")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()


# 터미널에서 인자를 입력받기 위한 코드입니다.
input_file = sys.argv[1]
result_file = sys.argv[2]

pc.merge_all_to_a_book([input_file], result_file)

# 작업 종료 메시지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")