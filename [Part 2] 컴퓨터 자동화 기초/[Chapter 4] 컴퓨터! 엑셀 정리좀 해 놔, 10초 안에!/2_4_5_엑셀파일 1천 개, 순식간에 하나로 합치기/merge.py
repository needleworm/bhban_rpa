#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 파이썬으로 6개월치 업무를 하루만에 끝내기
Last Modification : 2020.02.12.
"""
import time
import os
import pyexcel as px
import sys

# 작업 시작 메시지를 출력합니다.
print("Process Start")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 하나로 합칠 파일들이 저장된 폴더 이름을 시스템으로부터 입력받습니다.
directory = sys.argv[1]

# 결과물 파일의 이름을 정의합니다.
outfile_name = "merged_ID.xlsx"

# 폴더의 내용물을 열람해 목록을 생성합니다.
input_files = os.listdir(directory)

# 엑셀파일에 들어갈 내용물을 기록할 리스트를 만듭니다.
CONTENTS = []

# 폴더의 내용물을 하나하나 불러와 합치는 작업을 수행합니다.
# input_files에 저장된 파일 이름을 한 번에 하나씩 불러옵니다.
for filename in input_files:
    # 간혹 xlsx 파일이 아닌 파일이 섞여있을 수 있습니다. 이걸 걸러냅니다.
    if ".xlsx" not in filename:
        continue

    # 엑셀 파일이 맞다면, 파일을 리스트 형태로 읽어옵니다.
    data_array = px.get_array(file_name=directory + "/" + filename)

    # 헤더를 분리합니다.
    header = data_array[0]
    data_array = data_array[1:]

    # 헤더를 입력합니다. 최초 1회만 실행됩니다.
    if len(CONTENTS) == 0:
        CONTENTS.append(header)

    # 결과물에 내용물을 입력합니다.
    CONTENTS += data_array

# 완성된 엑셀파일을 저장합니다.
px.save_as(array=CONTENTS, dest_file_name=outfile_name)

# 작업 종료 메시지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
