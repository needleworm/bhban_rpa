#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.02.15.
"""
import time
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import sys

# 작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 사원 증명사진이 저장된 폴더를 시스템으로부터 입력받습니다.
member_photo = sys.argv[1]

# 개인정보가 저장된 CSV파일을 불러옵니다.
personal_IDs = sys.argv[2]

# 명함에 삽입할 로고 파일을 입력받습니다.
logo_filename = sys.argv[3]

# 명함에 삽입할 템플릿 정보를 입력받습니다.
template_filename = sys.argv[4]

try:
    template = Image.open(template_filename)
except:
    template = Image.new("RGBA", (800, 1268), 'white')

Xdim, Ydim = template.size

# 사원증에 삽입할 회사 정보를 기재합니다.
url = "http://sangsang.farm"

# 결과물을 저장할 폴더를 생성합니다.
out_dir ="idcards"
if out_dir not in os.listdir():
    os.mkdir(out_dir)

# 로고 파일을 불러옵니다.
logo = Image.open(logo_filename)
logo_x, logo_y = logo.size

# 증명사진 목록을 불러옵니다.
photos = os.listdir(member_photo)
PHOTOS = []
for el in photos:
    if el.strip().split(".")[-1] not in "PNG png JPG jpg BMP bmp JPEG jpeg":
        continue
    PHOTOS.append(el)

# 지금까지 제작한 명함 개수를 저장하는 카운터를 만듭니다.
COUNT = 0

# 로고 크기를 삽입하기 좋게 편집합니다. 사원증은 가로가 짧으니 가로 길이를 기준으로 작업합니다.
# 로고의 너비를 사원증 너비의 20%로 조절합니다.
new_logo_x = int(Xdim * 0.2)
# 로고의 y축 길이는 비례식으로 계산합니다.
# new_logo_y : logo_y = new_logo_x : logo_x
# 간단합니다. 초등학교때 다들 배웠습니다.
new_logo_y = int(logo_y * (new_logo_x / logo_x))

# 사원증에 삽입하기 좋게 로고 크기를 수정합니다.
resized_logo = logo.resize((new_logo_x, new_logo_y))

# 수정 전 로고를 닫아줍니다.
logo.close()

# 인적사항을 불러옵니다.
IDs = open(personal_IDs)

# 헤더를 뽑아냅니다.
header = IDs.readline()

# 빈 사원증 좌하단에 로고를 삽입하겠습니다.
# 대충 여백을 10%정도 주면 적당하겠죠? 이건 여러분의 취향에 달려 있습니다.
template.paste(resized_logo, (int(Xdim * 0.1), int(Ydim * 0.95 - new_logo_y)))

# 로고를 닫아줍니다.
resized_logo.close()

# 사원증에 삽입할 폰트들을 결정합니다.
# 폰트 이름을 변경하시면 바뀝니다. 기본은 굴림입니다. 컴퓨터를 막 굴리기 때문입니다.
# 이름은 큰 글자로 삽입합시다.
nameFont = ImageFont.truetype("font/gulim.ttc", 70)
# URL과 주소는 구석에 작게 삽입할겁니다.
smallFont = ImageFont.truetype("font/gulim.ttc", 40)
# 나머지 정보들은 적당한 크기로 작성합니다.
infoFont = ImageFont.truetype("font/gulim.ttc", 50)

# 사원증 우측 최상단에 URL을 삽입합니다.
# 좌우 여백은 맨 우측 5%를 띄울겁니다.
x_offset = int(Xdim * 0.95 - smallFont.getsize(url)[0])
# 상단 여백은 2%정도면 충분할 것 같습니다.
y_offset = int(Ydim * 0.02)
# 사원증에 홈페이지 주소를 삽입합니다.
ImageDraw.Draw(template).text(xy=(x_offset, y_offset), text=url, font=smallFont, fill="black")

# 인적사항을 한줄씩 읽어오면서, 한 번에 사원증을 한 장씩 만들겁니다.
for line in IDs:
    # CSV니까 컴마 단위로 쪼갤 수 있습니다. 쪼갭시다.
    splt = line.strip().split(", ")

    # 사원증에 들어갈 정보들만 추출합니다.
    name = splt[0]
    division = splt[3]

    # 사원증 템플릿을 복제합니다.
    idcard = template.copy()

    # 삽입할 사진을 불러옵시다.
    photo_for_id = Image.open(member_photo + "/" + PHOTOS[COUNT])

    # 사진의 너비를 사원증 너비의 50% 크기로 조정합니다.
    photo_for_id = photo_for_id.resize((int(Xdim/2), int(Xdim/2 * (4/3))))

    # 사진을 사원증 정 중앙에 삽입합시다.
    idcard.paste(photo_for_id, (int(Xdim/4), int(Ydim/2 - Xdim/2*(4/3)/2)))

    # 이름을 삽입할겁니다.
    # 이름 사이사이 공백을 삽입해서 더 잘 보이게 합니다.
    temp_name = ""
    for el in name:
        temp_name += el + " "
    name = temp_name[:-1]

    # 이름은 좌우 가운데정렬할겁니다.
    x_offset = int(Xdim * 0.5 - nameFont.getsize(name)[0]/2)
    # 상하 여백은 20%쯤 줍시다.
    y_offset = int(Ydim * 0.8 - nameFont.getsize(name)[1])
    # 명함에 이름을 삽입합니다.
    ImageDraw.Draw(idcard).text(xy=(x_offset, y_offset), text=name, font=nameFont, fill="black")

    # 이름 밑에 부서명을 삽입할겁니다.
    # 부서도 가운데정렬입니다.
    x_offset = int(Xdim * 0.5 - infoFont.getsize(division)[0]/2)
    # 상하 여백은 15%쯤 줍시다.
    y_offset = int(Ydim * 0.85 - infoFont.getsize(division)[1])
    # 명함에 이름을 삽입합니다.
    ImageDraw.Draw(idcard).text(xy=(x_offset, y_offset), text=division, font=infoFont, fill="black")

    # 완성된 사원증을 저장합니다.
    idcard.save(out_dir + "/" + PHOTOS[COUNT])

    # 저장도 했으니 명함을 닫아줍니다.
    idcard.close()

    COUNT += 1
    idcard.close()

# 템플릿도 닫아줍니다.
template.close()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
