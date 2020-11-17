#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 일반인을 위한 업무 자동화
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

# 최종 결과물 파일 이름을 정의합니다.
outfile_name = "merged_ID.xlsx"

# 폴더의 내용물을 열람해 목록을 생성합니다.
input_files = os.listdir(directory)

# 데이터가 저장될 리스트를 만듭니다.
CONTENTS = []

# 헤더를 저장할 리스트를 만듭니다.
HEADERS = []

# 헤더 입력을 위한 불리언 변수를 만듭니다.
contents_has_header = False

# 폴더의 내용물을 하나하나 불러와 합치는 작업을 수행합니다.
# input_files에 저장된 파일 이름을 한 번에 하나씩 불러옵니다.
for filename in input_files:
    # 간혹 텍스트 파일이 아닌 파일이 섞여있을 수 있습니다. 이걸 걸러냅니다.
    if ".txt" not in filename:
        continue

    # 텍스트 파일이 맞다면, 파일을 읽어옵니다.
    file = open(directory + "/" + filename)

    # 내용을 저장할 리스트를 만듭니다.
    contents = []

    # 파일의 내용물을 한 줄씩 읽어오면서 작업을 수행합니다.
    for line in file:
        # 양식이 잘못된 라인을 버립니다.
        if " : " not in line:
            continue

        # 텍스트파일의 헤더와 내용물을 분리합니다.
        header, content = line.strip().split(" : ")

        # 아직 헤더가 입력되지 않았다면 헤더를 만듭니다.
        # 이 코드는 처음 한 개의 파일에서만 실행됩니다.
        if not contents_has_header:
            HEADERS.append(header)

        # 읽어온 데이터를 정리합니다.
        contents.append(content)

    # 아직 헤더가 입력되지 않았다면 헤더를 입력합니다.
    # 이 코드는 한 번만 실행됩니다.
    if not contents_has_header:
        CONTENTS.append(HEADERS)
        contents_has_header = True

    # CONTENTS 에 헤더와 내용물을 입력합니다.
    CONTENTS.append(contents)

    # 읽어온 파일을 종료합니다.
    file.close()

# CONTENTS에 저장된 자료를 엑셀파일로 출력합니다.
px.save_as(array=CONTENTS, dest_file_name=outfile_name)

# 작업 종료 메시지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")