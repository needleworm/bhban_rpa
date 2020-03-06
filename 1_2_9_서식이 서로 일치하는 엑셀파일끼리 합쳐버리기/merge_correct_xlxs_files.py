#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.02.13.
"""
import time
import os
import pyexcel as px
import sys

# 작업 시작 메시지를 출력합니다.
print("Process Start")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 서식을 분석해 합칠 파일들이 저장된 폴더 이름을 시스템으로부터 입력받습니다.
directory = sys.argv[1]

# 결과물을 저장할 폴더를 생성합니다.
out_dir ="merged_" + directory
if out_dir not in os.listdir():
    os.mkdir(out_dir)


# 폴더의 내용물을 열람해 목록을 생성합니다.
input_files = os.listdir(directory)

# 헤더들을 저장할 리스트를 만듭니다.
HEADERS = []

# 엑셀 내용들을 저장할 리스트를 만듭니다.
CONTENTS = []

# input_files에 저장된 파일 이름을 한 번에 하나씩 불러옵니다.
for filename in input_files:
    # 간혹 xlsx 파일이 아닌 파일이 섞여있을 수 있습니다. 이걸 걸러냅니다.
    if ".xlsx" not in filename:
        continue

    # 엑셀 파일이 맞다면, 파일을 리스트 형태로 읽어옵니다.
    file = px.get_array(file_name=directory + "/" + filename)

    # 엑셀 파일의 첫 번째 열, 그러니까 헤더만 불러옵니다.
    header = file[0]
    content = file[1:]

    # 불러온 파일의 헤더가 이미 읽어왔던 파일과 일치하는지 분석합니다.
    # 아래 코드는 새로운 헤더가 발견될 때에만 작동합니다.
    if header not in HEADERS:
        # 처음 발견된 헤더라면 기록해 둡니다.
        HEADERS.append(header)
        # 출력할 파일 템플릿 리스트를 제작하여 저장해 둡니다.
        CONTENTS.append([header])

    # 저장할 파일 리스트를 불러옵니다.
    index = HEADERS.index(header)

    # 리스트에 데이터 값을 입력합니다.
    CONTENTS[index] += content

# 합쳐진 데이터들을 각각 엑셀 파일로 저장합니다.
for i in range(len(CONTENTS)):
    px.save_as(array=CONTENTS[i], dest_file_name=out_dir + "/" + str(i) + "_merged_File.xlsx")

# 작업 종료 메시지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")