#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 6개월 치 업무를 하루 만에 끝내는 업무 자동화
Last Modification : 2020.02.12.
"""
import time
import os
import sys
try:
    import pyexcel as px
except ModuleNotFoundError:
    import pip
    pip.main(['install', 'pyexcel'])
    pip.main(['install', 'pyexcel-xlsx'])
    try:
        import pyexcel as px
    except ModuleNotFoundError:
        time.sleep(2)
        import pyexcel as px

# 작업 시작 메시지를 출력합니다.
print("Process Start")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 파일들이 저장된 폴더 이름을 시스템으로부터 입력받습니다.
directory = sys.argv[1]

# 분석 결과 보고서 이름을 시스템으로부터 입력받습니다.
report_filename = sys.argv[2]

# 폴더의 내용물을 열람해 목록을 생성합니다.
input_files = os.listdir(directory)

# 헤더들을 저장할 딕셔너리를 만듭니다.
HEADERS = {}

# input_files에 저장된 파일 이름을 한 번에 하나씩 불러옵니다.
# 양식이 몇 종류인지 분석합니다.
for filename in input_files:
    # 간혹 xlsx 파일이 아닌 파일이 섞여있을 수 있습니다. 이걸 걸러냅니다.
    if ".xlsx" not in filename:
        continue

    # 엑셀 파일이 맞다면, 파일을 리스트 형태로 읽어옵니다.
    file = px.get_array(file_name=directory + "/" + filename)

    # 엑셀 파일의 첫 번째 열, 그러니까 헤더만 불러와 스트링으로 변환합니다.
    header = str(file[0])

    # 딕셔너리에 헤더가 삽입되어 있는지 확인합니다.
    if header in HEADERS:
        # 이미 삽입되어 있다면 값을 1개 증가시킵니다.
        HEADERS[header] += 1
    else:
        HEADERS[header] = 1

# 결과물 레포트를 작성하기 위한 스트링을 생성합니다.
REPORT = ""

# 레포트에 내용물을 자동으로 작성합니다.
for key in HEADERS:
    REPORT += "Header : " + key + "\n"
    REPORT += "Count : " + str(HEADERS[key]) + "\n\n"

# 레포트를 화면에 출력합니다.
print(REPORT)

# 레포트 파일에 레포트를 저장합니다.
report_file = open(report_filename, 'w')
report_file.write(REPORT)
report_file.close()

# 작업 종료 메시지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
