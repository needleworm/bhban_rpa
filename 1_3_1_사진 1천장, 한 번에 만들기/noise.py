#-*-coding:euc-kr
"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.02.13.
"""
import time
import os
import numpy as np
from PIL import Image


# 작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 생성할 이미지 파일 개수를 정의합니다.
NUM_SAMPLES = 1000

# 결과물을 저장할 폴더를 생성합니다.
os.mkdir("random_image")


# NUM_SAMPLES 회수만큼 반복하며 그림을 생성합니다.
# 이를테면, NUM_SAMPLES가 100이면 랜덤 이미지 100개를 생성합니다.
for i in range(NUM_SAMPLES):
    # 저장할 파일 이름을 정합니다. 현재 시각을 그대로 가져오죠.
    name = str(time.time())[-7:] + ".png"

    # 랜덤 이미지를 생성하기 위해 사이즈를 정의합니다. 사이즈마저도 랜덤입니다.
    Xdim, Ydim = np.random.randint(100, 400, size=2)

    # 랜덤 이미지를 생성합니다.
    image = np.random.randint(256, size=(Xdim, Ydim, 3)).astype('uint8')

    # 결과물을 PIL Image 형태로 만듭니다.
    result = Image.fromarray(image)

    # 결과물 파일을 저장합니다.
    result.save("random_image/"+name)

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
