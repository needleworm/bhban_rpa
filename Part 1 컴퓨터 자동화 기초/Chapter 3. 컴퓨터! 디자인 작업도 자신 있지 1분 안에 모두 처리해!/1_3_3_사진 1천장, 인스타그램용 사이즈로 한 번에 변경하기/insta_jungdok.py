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

# 사진의 배경 색깔을 입력받습니다.
background_color = sys.argv[2]

# 결과물을 저장할 폴더를 생성합니다.
out_dir ="squared_images"
if out_dir not in os.listdir():
    os.mkdir(out_dir)

# 폴더의 내용물을 열람해 목록을 생성합니다.
input_files = os.listdir(directory)

# input_files에 저장된 파일 이름을 한 번에 하나씩 불러옵니다.
for filename in input_files:
    # 간혹 이미지 파일이 아닌 파일이 섞여있을 수 있습니다. 이걸 걸러냅니다.
    name, exp = filename.strip().split('.')
    if exp not in "JPG jpg JPEG jpeg PNG png BMP bmp":
        continue

    # 이미지를 불러옵니다.
    image = Image.open(directory + "/" + filename)

    # 이미지의 크기를 알아냅니다.
    Xdim, Ydim = image.size

    # 정사각형으로 만들어 주기 위한 연산이 필요합니다.
    # X축과 Y축 중 어느 길이가 더 긴지 알아냅니다.
    if Xdim > Ydim:
        # X축 길이가 더 길 경우의 계산입니다.
        new_size = Xdim
        x_offset = 0
        y_offset = int((Xdim - Ydim) / 2)
    else:
        # Y축 길이가 더 길 경우의 계산입니다.
        new_size = Ydim
        x_offset = int((Ydim - Xdim) / 2)
        y_offset = 0

    # 새로운 이미지를 생성합니다. 텅 빈 정사각형이고 색깔은 background_color 입니다.
    new_image = Image.new("RGBA", (new_size, new_size), background_color)

    # 텅 빈 배경에 원본 이미지를 덮어씌웁니다. 적당한 위치에 말이죠.
    new_image.paste(image, (x_offset, y_offset))

    # 변경된 이미지를 저장합니다.
    new_image.save(out_dir + "/" + name + ".png")

    # 이미지들을 닫아줍니다.
    image.close()
    new_image.close()


# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
