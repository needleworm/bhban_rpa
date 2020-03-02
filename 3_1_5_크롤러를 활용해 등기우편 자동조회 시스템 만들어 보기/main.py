#-*-coding:euc-kr
"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.02.18.
"""
import post_crawler as pc
import os
import time
import sys

#작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 등기번호가 기재된 CSV파일을 불러옵니다.
post_codes = sys.argv[1]

# 결과물이 저장될 폴더명을 입력받습니다.
out_dir = sys.argv[2]

# 결과물을 저장할 폴더를 제작해 줍니다.
if out_dir not in os.listdir():
    os.mkdir(out_dir)

# CSV 파일을 읽어옵니다.
csv = open(post_codes)

# 지금까지 작업한 등기번호 개수를 세기 위한 카운터를 제작합니다.
count = 1

# 크롤러를 불러옵니다.
crawler = pc.PostCrawler()

# 작업이 끝 난 쿼리를 걸러내기 위한 부분입니다.
# 작업이 끝 난 등기번호를 저장할 리스트를 제작합니다.
done_list = []
# 출력 폴더 안의 결과물을 읽어옵니다.
temp = os.listdir(out_dir)

# 출력 폴더 안의 결과물들을 하나하나 불러오면서
# png파일일 경우 리스트에 이름을 등재합니다.
for el in temp:
    if ".png" in el:
        done_list.append(el)

# CSV 파일을 한줄씩 읽으며 작업을 수행합니다.
for line in csv:
    # CSV 파일이니까 컴마로 쪼갤 수 있습니다. 쪼개줍시다.
    # 만약 등기번호만 적혀 있다면 등기번호만 들어있는 리스트가 반환되고
    # 등기번호와 이름이 입력된 양식이라면 등기번호만 뽑혀나옵니다.
    querry = line.split(",")[0].strip()

    # 만약 쿼리에 '-' 가 입력되어 있다면 다듬어서 없애줍시다.
    if "-" in querry:
        # 하이픈을 기준으로 쪼개줍니다.
        splt = querry.split("-")
        querry = "".join(splt)

    # 쿼리가 13글자 순수한 숫자인지 검토합니다. 아니라면 다음 쿼리로 넘겨버립니다.
    if len(querry) != 13 or not querry.isdigit():
        continue

    # 이미 스크린샷을 캡처한 쿼리인 경우 작업을 중단하고 다음 쿼리로 넘겨버립니다.
    if querry + ".png" in done_list:
        continue

    # 스크린샷을 가볍게 찍어 줍시다.
    crawler.save_screenshot(querry, out_dir)

    # 카운터를 1 증가시킵니다.
    count += 1

# 크롤러를 닫아줍니다.
crawler.kill()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
