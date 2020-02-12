#-*-coding:euc-kr
"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.02.12.
"""
import time
import os
import pyexcel.cookbook as PC
import sys

# 작업 시작 메시지를 출력합니다.
print("Process Start")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 하나로 합칠 파일들이 저장된 폴더 이름을 시스템으로부터 입력받습니다..
directory = sys.argv[1]

# 임시로 생성할 결과물 파일의 이름을 정의합니다.
temp_file_name = "temp.csv"

# 최종 결과물 파일 이름을 정의합니다.
outfile_name = "merged_ID.xlsx"

# 결과물 파일을 생성합니다. 텅 빈 텍스트파일이 생성됩니다.
temp_file = open(temp_file_name, 'w')

# 폴더의 내용물을 열람해 목록을 생성합니다.
input_files = os.listdir(directory)

# 헤더와 관련된 변수를 정의합니다. 헤더는 엑셀의 양식이라 생각하면 됩니다.
headers = []
outfile_has_header = False

# 폴더의 내용물을 하나하나 불러와 합치는 작업을 수행합니다.
# input_files에 저장된 파일 이름을 한 번에 하나씩 불러옵니다.
for filename in input_files:
    # 간혹 텍스트 파일이 아닌 파일이 섞여있을 수 있습니다. 이걸 걸러냅니다.
    if ".txt" not in filename:
        continue

    # 텍스트 파일이 맞다면, 파일을 읽어옵니다.
    file = open(directory + "/" + filename)

    # 파일의 내용물을 저장할 리스트를 정의합니다.
    contents = []

    # 파일의 내용물을 한 줄씩 읽어오면서 작업을 수행합니다.
    for line in file:
        # 엑셀 파일의 양식과 내용물을 분리합니다.
        if ":" in line:
            splits = line.split(":")
            contents.append(splits[-1].strip())

            # 헤더를 정리합니다. 최초 1회만 실행됩니다.
            if len(contents) > len(headers):
                headers.append(splits[0].strip())

    # 헤더를 파일에 입력합니다. 최초 1회만 실행됩니다.
    if not outfile_has_header:
        header = ", ".join(headers)
        temp_file.write(header)
        outfile_has_header = True

    # 결과물 파일에 내용물을 입력합니다.
    new_line = ", ".join(contents)
    temp_file.write("\n" + new_line)

    # 읽어온 파일을 종료합니다.
    file.close()

# 임시 결과물 파일을 종료합니다.
temp_file.close()

# 임시로 저장된 결과물 파일을 엑셀형태로 변환합니다.
PC.merge_all_to_a_book([temp_file_name], outfile_name)

# 임시로 저장된 결과물을 삭제합니다.
os.remove(temp_file_name)

# 작업 종료 메시지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")