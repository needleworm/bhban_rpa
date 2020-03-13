#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.02.13.
"""
import time
import os
from PIL import Image
import sys

# 작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 사진이 저장된 폴더명을 입력받습니다.
directory = sys.argv[1]

# 사진에 삽입할 로고 파일을 입력받습니다.
logo_filename = sys.argv[2]

# 결과물을 저장할 폴더를 생성합니다.
out_dir ="images_with_logo"
if out_dir not in os.listdir():
    os.mkdir(out_dir)


# 폴더의 내용물을 열람해 목록을 생성합니다.
input_files = os.listdir(directory)

# 로고 파일을 불러옵니다.
logo = Image.open(logo_filename)
logo_x, logo_y = logo.size

# input_files에 저장된 파일 이름을 한 번에 하나씩 불러옵니다.
for filename in input_files:
    # 간혹 이미지 파일이 아닌 파일이 섞여있을 수 있습니다. 이걸 걸러냅니다.
    exp = filename.strip().split('.')[-1]
    if exp not in "JPG jpg JPEG jpeg PNG png BMP bmp":
        continue

    # 이미지를 불러옵니다.
    image = Image.open(directory + "/" + filename)

    # 이미지의 크기를 알아냅니다.
    Xdim, Ydim = image.size

    # 로고파일을 이미지에 맞게 적당히 확대/축소합니다.
    # 이미지와 로고의 가로/세로 비율이 다르기 때문에 비례식을 사용해야 합니다.
    # 초등학교 교과과정입니다. 따라서 어려워 보인다면 착각입니다. 아무튼 쉬운겁니다.

    # 이 경우 로고의 X축 길이가 이미지에 비해서 좀 깁니다.
    if logo_x / Xdim > logo_y / Ydim:
        # 로고의 x축 길이를 이미지의 x축 길이의 1/5로 조절합니다.
        new_logo_x = int(Xdim/5)
        # 로고의 y축 길이는 비례식으로 계산합니다.
        # new_logo_y : logo_y = new_logo_x : logo_x
        # 간단합니다. 초등학교때 다들 배웠습니다.
        new_logo_y = int(logo_y * (new_logo_x / logo_x))
    # 로고의 y축 길이가 이미지에 비해 긴 경우 반대로 합니다.
    else:
        new_logo_y = int(Ydim / 5)
        new_logo_x = int(logo_x * (new_logo_y / logo_y))

    # 이미지 크기에 맞게 축소/확대된 로고입니다.
    resized_logo = logo.resize((new_logo_x, new_logo_y))

    # 입력받은 사진에 로고를 삽입합니다. 적당한 위치에 말이죠.
    # 대충 여백을 2%정도 주면 적당하겠죠? 이건 여러분의 취향에 달려 있습니다.
    image.paste(resized_logo, (int(Xdim/50), int(Ydim/50)))

    # 변경된 이미지를 저장합니다.
    image.save(out_dir + "/" + filename)

    # 이미지를 닫아 줍니다.
    image.close()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
