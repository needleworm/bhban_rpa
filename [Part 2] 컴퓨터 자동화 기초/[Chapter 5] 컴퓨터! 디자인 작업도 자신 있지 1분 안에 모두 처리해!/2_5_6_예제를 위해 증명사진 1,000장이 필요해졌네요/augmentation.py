#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 파이썬으로 6개월치 업무를 하루만에 끝내기
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
# 저장할 파일의 이름을 입력합니다.
temp_new_file_name = "%05d.png" %COUNT
# 카운트를 1 증가시킵니다.
COUNT += 1
# 원본 이미지를 저장합니다.
image.save(out_dir + "/" + temp_new_file_name)
image.close()

# 출력 파일명을 저장할 리스트를 만듭니다.
FILELIST = [temp_new_file_name]

# 폴더 내의 이미지를 모두 읽어와 좌우대칭을 저장합니다. 2의 1승
for i in range(len(FILELIST)):
    # 파일을 불러옵니다.
    image = Image.open(out_dir + "/" + FILELIST[i])
    # 변환된 파일을 저장하기 위해 새로운 이름을 지정합니다.
    new_temp_name = "%05d.png" %COUNT
    # 사진이 한 장 만들어질때마다 count를 1씩 증가시킵니다.
    COUNT += 1
    # 이미지를 좌우 반전합니다.
    image = image.transpose(Image.FLIP_LEFT_RIGHT)
    # 좌우 반전된 이미지를 저장합니다.
    image.save(out_dir + "/" + new_temp_name)
    image.close()
    # 출력 파일명을 리스트에 저장합니다.
    FILELIST.append(new_temp_name)

# 리스트 안의 이미지를 모두 읽어와 상하대칭을 저장합니다. 2의 2승
for i in range(len(FILELIST)):
    # 파일을 불러옵니다.
    image = Image.open(out_dir + "/" + FILELIST[i])
    # 변환된 파일을 저장하기 위해 새로운 이름을 지정합니다.
    new_temp_name = "%05d.png" % COUNT
    # 사진이 한 장 만들어질때마다 count를 1씩 증가시킵니다.
    COUNT += 1
    # 이미지를 상하 반전합니다.
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    # 상하 반전된 이미지를 저장합니다.
    image.save(out_dir + "/" + new_temp_name)
    image.close()
    # 출력 파일명을 리스트에 저장합니다.
    FILELIST.append(new_temp_name)

# 리스트 안의 이미지를 모두 읽어와 흑백버전을 저장합니다. 2의 3승
for i in range(len(FILELIST)):
    # 파일을 불러옵니다.
    image = Image.open(out_dir + "/" + FILELIST[i])
    # 변환된 파일을 저장하기 위해 새로운 이름을 지정합니다.
    new_temp_name = "%05d.png" % COUNT
    # 사진이 한 장 만들어질때마다 count를 1씩 증가시킵니다.
    COUNT += 1
    # 이미지를 흑백으로 만듭니다.
    image = image.convert('1')
    # 흑백으로 변환된 이미지를 저장합니다.
    image.save(out_dir + "/" + new_temp_name)
    image.close()
    # 출력 파일명을 리스트에 저장합니다.
    FILELIST.append(new_temp_name)

# 리스트 안의 이미지를 모두 읽어와 1도씩 회전합니다. 2의 3승 * 180
for el in FILELIST:
    for i in range(180):
        # 깔끔하게 1,000장만 만듭시다.
        # 결과물이 1000개를 넘어서면 코드를 종료합니다.
        if COUNT > 1000:
            break
        # 파일을 불러옵니다.
        image = Image.open(out_dir + "/" + el)
        # 변환된 파일을 저장하기 위해 새로운 이름을 지정합니다.
        new_temp_name = "%05d.png" % COUNT
        # 사진이 한 장 만들어질때마다 count를 1씩 증가시킵니다.
        COUNT += 1
        # 사진을 회전시킵니다.
        image = image.rotate(i+1)
        # 간혹 이미지 크기가 변경된다는 이야기가 있어 resize()를 실행합니다.
        image = image.resize((Xdim, Ydim))
        # 회전 된 이미지를 저장합니다.
        image.save(out_dir + "/" + new_temp_name)
        image.close()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
