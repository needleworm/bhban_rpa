#-*-coding:euc-kr
"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.02.13.
"""
import time
import os
import pyexcel as px
import sys
import random

# 작업 시작 메시지를 출력합니다.
print("Process Start")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 서식을 망가뜨릴 파일들이 저장된 폴더 이름을 시스템으로부터 입력받습니다.
directory = sys.argv[1]

# 몇 퍼센트의 데이터를 망가뜨릴 것인지 시스템으로부터 입력받습니다.
percent = float(sys.argv[2])/100

# 폴더의 내용물을 열람해 목록을 생성합니다.
input_files = os.listdir(directory)

# 원래 있던 자료 대신 집어넣을 약오르는 단어들을 모아줍니다.
TERROR = ["고양이", "야옹", "야옹이", "미야옹", "팀장님사랑해요"]

# input_files에 저장된 파일 이름을 한 번에 하나씩 불러옵니다.
for filename in input_files:
    # 간혹 xlsx 파일이 아닌 파일이 섞여있을 수 있습니다. 이걸 걸러냅니다.
    if ".xlsx" not in filename:
        continue

    # 엑셀 파일이 맞다면, 파일을 리스트 형태로 읽어옵니다.
    data = px.get_array(file_name=directory + "/" + filename)

    # 원본 파일을 삭제합니다.
    os.remove(directory + "/" + filename)

    # 2중 for문으로 데이터에 접근합니다.
    for i in range(len(data)):
        for j in range(len(data[i])):
            # 파괴 확률을 적용합니다.
            if random.random() < percent:
                # 확률상 당첨이 되었다면 데이터를 파괴합니다.
                data[i][j] = random.choice(TERROR)

    # 수정이 완료된 파일로 바꿔치기합니다.
    px.save_as(array=data, dest_file_name=directory + "/" + filename)

# 작업 종료 메시지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
