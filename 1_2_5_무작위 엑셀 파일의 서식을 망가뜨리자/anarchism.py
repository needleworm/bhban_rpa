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
import random

# 작업 시작 메시지를 출력합니다.
print("Process Start")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 서식을 망가뜨릴 파일들이 저장된 폴더 이름을 시스템으로부터 입력받습니다.
directory = sys.argv[1]

# 몇 퍼센트나 되는 파일의 서식을 망가뜨릴지 비율을 시스템으로부터 입력받습니다.
percent = float(sys.argv[2]) / 100

# 폴더의 내용물을 열람해 목록을 생성합니다.
input_files = os.listdir(directory)

# 서식을 망가뜨릴 총 파일 개수를 계산합니다.
DESTROY_COUNT = int(len(input_files) * percent)

# 파일 순서를 섞어버립니다.
random.shuffle(input_files)

# 파괴 대상이 된 불쌍한 파일 목록을 만듭니다.
destroy_them = input_files[:DESTROY_COUNT]

# 총 3가지 재앙을 준비했습니다. 재앙을 일으키기 위한 카운트를 정합니다.
# 카운트다운을 하다가 shift_1, shift_2가 되면 재앙의 종류가 바뀝니다.
shift_1 = DESTROY_COUNT/3*2
shift_2 = DESTROY_COUNT/3

# 서식을 파괴할 파일들을 하나씩 읽어와 작업을 수행합니다.
# destroy_them에 저장된 파일 이름을 한 번에 하나씩 불러옵니다.
for filename in destroy_them:
    # 간혹 xlsx 파일이 아닌 파일이 섞여있을 수 있습니다. 이걸 걸러냅니다.
    if ".xlsx" not in filename:
        continue

    # 엑셀 파일이 맞다면, 파일을 읽어옵니다.
    file = px.get_sheet(file_name=directory + "/" + filename)

    # 원래 있던 파일은 지워버립시다. 파일의 명복을 빕니다.
    os.remove(directory + "/" + filename)

    # 엑셀 파일을 리스트로 변환합니다.
    data_array = file.array

    # column 서식을 망가뜨리는게 가장 쉽습니다. column이 몇개인지 알아냅시다.
    num_columns = len(data_array[0])
    # 무작위 열을 하나 망가뜨리기 위해 랜덤 숫자를 생성합니다.
    victim = random.randint(0, num_columns - 1)

    # 첫 번째 재앙입니다.
    if DESTROY_COUNT > shift_1:
        # 무작위 열을 하나 지워버립니다.
        file.delete_columns([victim])

    # 두 번째 재앙입니다.
    elif DESTROY_COUNT > shift_2:
        # 바꿔치기할 열을 만듭니다. 내용물을 모두 '고양이'로 채워버립니다. 야옹.
        CAT = ["고양이" for i in range(file.number_of_rows())]

        # 원래 엑셀 파일의 내용물과 고양이를 바꿔치기합니다. 야옹.
        file.column[victim] = CAT

    # 세 번째 재앙입니다.
    else:
        # 선택된 열을 복제해 붙여넣어 버립니다.
        file.column += file.column[victim].copy()

    # 서식이 망가진 불쌍한 엑셀파일을 저장합니다.
    px.save_as(array=data_array, dest_file_name=directory + "/" + filename)

    # 카운트다운을 한 개씩 합니다.
    DESTROY_COUNT -= 1

# 작업 종료 메시지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")