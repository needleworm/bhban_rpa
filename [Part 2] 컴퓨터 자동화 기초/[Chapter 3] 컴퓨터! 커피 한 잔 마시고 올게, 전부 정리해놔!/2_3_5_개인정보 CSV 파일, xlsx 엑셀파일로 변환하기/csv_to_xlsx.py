#-*-coding:utf-8
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 6개월 치 업무를 하루 만에 끝내는 업무 자동화
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
# 엑셀로 변환하고자 하는 CSV 파일의 이름을 입력합니다.
input_file = sys.argv[1]
# 합쳐진 결과물 파일을 어떤 이름으로 저장할지 입력받습니다.
result_file = sys.argv[2]

# 엑셀 파일 하나로 합쳐주는 함수입니다.
# 라이브러리가 기본적으로 제공해 주는 함수입니다.
pc.merge_all_to_a_book([input_file], result_file)

# 작업 종료 메시지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")