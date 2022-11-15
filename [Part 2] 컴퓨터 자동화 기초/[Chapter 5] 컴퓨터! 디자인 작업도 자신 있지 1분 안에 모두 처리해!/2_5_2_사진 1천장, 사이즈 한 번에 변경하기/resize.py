#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 6개월 치 업무를 하루 만에 끝내는 업무 자동화
Last Modification : 2020.02.13.
"""
import time
import os
import sys

try:
    from PIL import Image
except ModuleNotFoundError:
    import pip
    pip.main(['install', 'pillow'])
    try:
        from PIL import Image
    except ModuleNotFoundError:
        time.sleep(2)
        from PIL import Image

# 작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 사진이 저장된 폴더명을 입력받습니다.
directory = sys.argv[1]

# 몇 퍼센트 비율로 사이즈를 변경할 것인지 입력받습니다.
percent = float(sys.argv[2])/100

# 결과물을 저장할 폴더를 생성합니다.
out_dir ="resized_image"
if out_dir not in os.listdir():
    os.mkdir(out_dir)


# 폴더의 내용물을 열람해 목록을 생성합니다.
input_files = os.listdir(directory)

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

    # 여기에 배율을 곱해 새로운 이미지의 사이즈를 계산합니다.
    Xdim *= percent
    Ydim *= percent

    # 이미지 사이즈를 변경합니다.
    image = image.resize((int(Xdim), int(Ydim)))

    # 변경된 이미지를 저장합니다.
    image.save(out_dir + "/" + filename)

    # 이미지를 닫아줍니다.
    image.close()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
