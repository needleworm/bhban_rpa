#-*-coding:euc-kr
"""
Author : Byunghyun Ban
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

# 서식 예시로 사용할 파일 이름을 시스템으로부터 입력받습니다.
template = sys.argv[1]

# 파일들이 저장된 폴더 이름을 시스템으로부터 입력받습니다.
directory = sys.argv[2]

# 폴더의 내용물을 열람해 목록을 생성합니다.
input_files = os.listdir(directory)

# 템플릿 파일을 읽어와 헤더를 분리합니다.
HEADER = px.get_array(file_name=template)[0]

# 데이터를 저장할 리스트를 만듭니다. 헤더도 넣어줍니다.
CONTENTS = [HEADER]

# input_files에 저장된 파일 이름을 한 번에 하나씩 불러옵니다.
for filename in input_files:
    # 간혹 xlsx 파일이 아닌 파일이 섞여있을 수 있습니다. 이걸 걸러냅니다.
    if ".xlsx" not in filename:
        continue

    # 엑셀 파일이 맞다면, 파일을 리스트 형태로 읽어옵니다.
    file = px.get_array(file_name=directory + "/" + filename)

    # 엑셀 파일의 첫 번째 열, 그러니까 헤더만 불러옵니다.
    header = file[0]

    # 불러온 파일의 헤더가 템플릿과 일치하는지 분석합니다.
    if HEADER != header:
        # 일치하지 않는다면 건너뛰어버립시다
        continue

    # CONTENTS 리스트에 엑셀 파일의 내용물을 입력합니다.
    CONTENTS += file[1:]

# 합쳐진 엑셀 파일을 저장합니다.
px.save_as(array=CONTENTS, dest_file_name="merged_FILE.xlsx")

# 총 몇개의 파일이 합쳐졌는지를 출력합니다.
print("Total " + str(len(CONTENTS) - 1) + " files were merged.")

# 작업 종료 메시지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
