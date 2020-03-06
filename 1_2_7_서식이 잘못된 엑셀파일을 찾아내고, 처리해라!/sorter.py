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

# 서식 예시로 사용할 파일 이름을 시스템으로부터 입력받습니다.
template = sys.argv[1]

# 파일들이 저장된 폴더 이름을 시스템으로부터 입력받습니다.
directory = sys.argv[2]

# 작동 모드를 시스템으로부터 입력받습니다.
MODE = sys.argv[3]

# 폴더의 내용물을 열람해 목록을 생성합니다.
input_files = os.listdir(directory)

# 템플릿 파일을 읽어와 헤더를 분리합니다.
HEADER = px.get_array(file_name=template)[0]

# 삭제 모드인 경우 총 몇개의 파일이 삭제되었는지 세기 위해 카운터를 만듭니다.
if MODE in "DELETEdelete":
    count = 0
# 보고 모드일 경우 보고서 작성을 위한 파일을 생성합니다.
elif MODE in "REPORTreport":
    REPORT = open("report.txt", 'w')
# 분류 모드일 경우 분류된 파일을 저장하기 위한 폴더를 생성합니다.
elif MODE in "SEPARATEseparate":
    os.mkdir("wrong_files")
    # 파일 이동을 수행하기 위한 라이브러리도 불러옵니다.
    import shutil

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
    if HEADER == header:
        # 일치한다면 살려둡시다.
        continue

    # 일치하지 않는다면 이 아래 부분의 코드가 작동됩니다.
    if MODE in "DELETEdelete":
        # 삭제 모드인 경우 삭제합니다.
        os.remove(directory + "/" + filename)
        count += 1
    elif MODE in "REPORTreport":
        # 보고 모드인 경우 보고서에 파일 이름을 기재합니다.
        REPORT.write(filename + "\n")
    elif MODE in "SEPARATEseparate":
        # 분류 모드일 경우 별도의 폴더로 파일을 이동시킵니다.
        shutil.move(directory + "/" + filename, "wrong_files/" + filename)

# 삭제 모드인 경우 총 몇개의 파일이 삭제되었는지 출력합니다.
if MODE in "DELETEdelete":
    print("Total " + str(count) + " files were removed.")

# 보고 모드인 경우 보고서를 종료합니다.
if MODE in "REPORTreport":
    REPORT.close()

# 작업 종료 메시지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
