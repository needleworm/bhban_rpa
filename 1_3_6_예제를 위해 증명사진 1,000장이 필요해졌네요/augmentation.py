#-*-coding:euc-kr
"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.02.15.
"""
import time
import os
from PIL import Image
import sys

# 작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 부풀릴 이미지 이름을 입력받습니다.
image_filename = sys.argv[1]

# 결과물을 저장할 폴더를 생성합니다.
out_dir ="augmentation"
if out_dir not in os.listdir():
    os.mkdir(out_dir)

# 샘플 이미지 파일을 불러옵니다.
image = Image.open(image_filename)
Xdim, Ydim = image.size

# 저장된 파일 개수를 저장해 둘 카운터를 생성합니다.
COUNT = 1

# 일단 원본을 저장합니다. 2의 0승
temp_new_file_name = "%05d.png" %COUNT
COUNT += 1
image.save(out_dir + "/" + temp_new_file_name)
image.close()

# 출력 파일명을 저장할 리스트를 만듭니다.
FILELIST = [temp_new_file_name]

# 폴더 내의 이미지를 모두 읽어와 좌우대칭을 저장합니다. 2의 1승
for i in range(len(FILELIST)):
    image = Image.open(out_dir + "/" + FILELIST[i])
    new_temp_name = "%05d.png" %COUNT
    COUNT += 1
    image = image.transpose(Image.FLIP_LEFT_RIGHT)
    image.save(out_dir + "/" + new_temp_name)
    image.close()
    FILELIST.append(new_temp_name)

# 폴더 내의 이미지를 모두 읽어와 상하대칭을 저장합니다. 2의 2승
for i in range(len(FILELIST)):
    image = Image.open(out_dir + "/" + FILELIST[i])
    new_temp_name = "%05d.png" % COUNT
    COUNT += 1
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save(out_dir + "/" + new_temp_name)
    image.close()
    FILELIST.append(new_temp_name)

# 폴더 내의 이미지를 모두 읽어와 흑백버전을 저장합니다. 2의 3승
for i in range(len(FILELIST)):
    image = Image.open(out_dir + "/" + FILELIST[i])
    new_temp_name = "%05d.png" % COUNT
    COUNT += 1
    image = image.convert('1')
    image.save(out_dir + "/" + new_temp_name)
    image.close()
    FILELIST.append(new_temp_name)

# 폴더 내의 이미지를 모두 읽어와 1도씩 회전합니다. 2의 3승 * 180
for el in FILELIST:
    for i in range(180):
        # 깔끔하게 1,000장만 만듭시다.
        if COUNT > 1000:
            break
        image = Image.open(out_dir + "/" + el)
        image = image.rotate(i+1)
        image = image.resize((Xdim, Ydim))
        new_temp_name = "%05d.png" % COUNT
        COUNT += 1
        image.save(out_dir + "/" + new_temp_name)
        image.close()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
