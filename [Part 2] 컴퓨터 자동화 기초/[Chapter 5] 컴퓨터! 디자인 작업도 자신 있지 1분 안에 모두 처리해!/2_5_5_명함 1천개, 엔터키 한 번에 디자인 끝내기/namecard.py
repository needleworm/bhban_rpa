#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 6개월 치 업무를 하루 만에 끝내는 업무 자동화
Last Modification : 2020.02.14.
"""
import time
import os
import sys

try:
    from PIL import Image
    from PIL import ImageFont
    from PIL import ImageDraw
except ModuleNotFoundError:
    import pip
    pip.main(['install', 'pillow'])
    try:
        from PIL import Image
        from PIL import ImageFont
        from PIL import ImageDraw
    except ModuleNotFoundError:
        time.sleep(2)
        from PIL import Image
        from PIL import ImageFont
        from PIL import ImageDraw

# 작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 개인정보가 저장된 CSV파일을 불러옵니다.
personal_IDs= sys.argv[1]

# 명함에 삽입할 로고 파일을 입력받습니다.
logo_filename = sys.argv[2]

# 명함에 삽입할 회사 정보를 기재합니다.
location = "경기도 파주시 문발동 광인사길 143"
url = "https://bit.ly/2FqKtba"

# 결과물을 저장할 폴더를 생성합니다.
out_dir ="namecards"
if out_dir not in os.listdir():
    os.mkdir(out_dir)

# 로고 파일을 불러옵니다.
logo = Image.open(logo_filename)
logo_x, logo_y = logo.size

# 명함의 해상도를 지정합니다. 구글링 해 보니 1039*697 사이즈가 좋대요.
Xdim = 1039
Ydim = 697

# 로고 크기를 명함에 삽입하기 좋게 편집합니다. 명함은 세로가 짧으니 세로 길이를 기준으로 작업합니다.
# 로고의 높이를 명함 높이의 40%로 조절합니다.
new_logo_y = int(Ydim * 0.4)
# 로고의 x축 길이는 비례식으로 계산합니다.
# new_logo_y : logo_y = new_logo_x : logo_x
# 간단합니다. 초등학교때 다들 배웠습니다.
new_logo_x = int(logo_x * (new_logo_y / logo_y))

# 명함에 삽입하기 좋게 로고 크기를 수정합니다.
resized_logo = logo.resize((new_logo_x, new_logo_y))

# 수정 전 로고를 닫아줍니다.
logo.close()

# 인적사항을 불러옵니다.
IDs = open(personal_IDs)

# 헤더를 뽑아냅니다.
header = IDs.readline()

# 명함을 저장할 새로운 이미지를 제작해 줍니다.
# 참고로 배경색은 일단 흰색으로 지정합시다.
# 명함을 천 장 씩이나 찍어야 될 회사면 임원진 취향이 보수적일 가능성이 높으며
# 흰 색이 아닌 다른 명함을 원한다 하더라도 흰색이 아닌 다른 색 종이에 인쇄하면 됩니다.
image = Image.new("RGBA", (Xdim, Ydim), "white")

# 빈 명함 좌상단에 로고를 삽입하겠습니다.
# 대충 여백을 10%정도 주면 적당하겠죠? 이건 여러분의 취향에 달려 있습니다.
image.paste(resized_logo, (int(Xdim * 0.1), int(Ydim * 0.1)))

# 로고를 닫아줍니다.
resized_logo.close()

# 명함에 삽입할 폰트들을 결정합니다.
# 폰트 이름을 변경하시면 바뀝니다. 기본은 굴림입니다. 컴퓨터를 막 굴리기 때문입니다.
# 이름은 큰 글자로 삽입합시다.
nameFont = ImageFont.truetype("font/gulim.ttc", 70)
# URL과 주소는 구석에 작게 삽입할겁니다.
smallFont = ImageFont.truetype("font/gulim.ttc", 40)
# 나머지 정보들은 적당한 크기로 작성합니다.
infoFont = ImageFont.truetype("font/gulim.ttc", 50)


# 명함 우측 최상단에 URL을 삽입합니다.
# 좌우 여백은 맨 우측 5%를 띄울겁니다.
left, top, right, bottom = smallFont.getbbox(url)
text_width = right - left
text_height = bottom - top

x_offset = int(Xdim * 0.95 - text_width[0])
# 상단 여백은 5%정도면 충분할 것 같습니다.
y_offset = int(Ydim * 0.05)
# 명함에 홈페이지 주소를 삽입합니다.
ImageDraw.Draw(image).text(xy=(x_offset, y_offset), text=url, font=smallFont, fill="black")

# 명함 하단에 사무실 주소를 입력합니다.
left, top, right, bottom = smallFont.getbbox(location)
text_width = right - left
text_height = bottom - top

# 좌우 여백은 우측 5%를 띄울겁니다.
x_offset = int(Xdim * 0.95 - text_width)
# 하단 여백도 마찬가지로 5%정도면 예쁠 것 같군요.
y_offset = int(Ydim * 0.95 - text_height)
# 명함에 사무실 주소를 삽입합니다.
ImageDraw.Draw(image).text(xy=(x_offset, y_offset), text=location, font=smallFont, fill="black")

# 인적사항을 한줄씩 읽어오면서, 한 번에 명함을 한 장씩 만들겁니다.
for line in IDs:
    # CSV니까 컴마 단위로 쪼갤 수 있습니다. 쪼갭시다.
    splt = line.strip().split(", ")

    # 명함에 들어갈 정보들만 추출합니다.
    name = splt[0]
    e_mail = splt[2]
    division = splt[3]
    telephone = splt[4]

    # 명함 템플릿을 복제합니다.
    namecard = image.copy()

    # 이름을 삽입할겁니다.
    # 이름 사이사이 공백을 삽입해서 더 잘 보이게 합니다.
    temp_name = ""
    for el in name:
        temp_name += el + " "
    name = temp_name[:-1]

    left, top, right, bottom = nameFont.getbbox(name)
    text_width = right - left
    text_height = bottom - top

    # 이름은 우측 여백을 10% 줍시다.
    x_offset = int(Xdim * 0.9 - text_width)
    # 상하 여백은 60%쯤 줍시다.
    y_offset = int(Ydim * 0.4 - text_height)
    # 명함에 이름을 삽입합니다.
    ImageDraw.Draw(namecard).text(xy=(x_offset, y_offset), text=name, font=nameFont, fill="black")

    # 이름 밑에 부서명을 삽입할겁니다.
    left, top, right, bottom = infoFont.getbbox(division)
    text_width = right - left
    text_height = bottom - top
    # 부서도 우측 여백을 10% 줍시다.
    x_offset = int(Xdim * 0.9 - text_width)
    # 상하 여백은 50%쯤 줍시다.
    y_offset = int(Ydim * 0.5 - text_height)
    # 명함에 이름을 삽입합니다.
    ImageDraw.Draw(namecard).text(xy=(x_offset, y_offset), text=division, font=infoFont, fill="black")

    # 그 밑에 전화번호를 삽입할겁니다.
    left, top, right, bottom = infoFont.getbbox(telephone)
    text_width = right - left
    text_height = bottom - top
    # 우측 여백을 10% 줍시다.
    x_offset = int(Xdim * 0.9 - text_width)
    # 상하 여백은 35%쯤 줍시다.
    y_offset = int(Ydim * 0.65 - text_height)
    # 명함에 이름을 삽입합니다.
    ImageDraw.Draw(namecard).text(xy=(x_offset, y_offset), text=telephone, font=infoFont, fill="black")

    # 그 밑에 이메일을 삽입할겁니다.
    left, top, right, bottom = infoFont.getbbox(e_mail)
    text_width = right - left
    text_height = bottom - top
    # 우측 여백을 10% 줍시다.
    x_offset = int(Xdim * 0.9 - text_width)
    # 상하 여백은 25%쯤 줍시다.
    y_offset = int(Ydim * 0.75 - text_height)
    # 명함에 이름을 삽입합니다.
    ImageDraw.Draw(namecard).text(xy=(x_offset, y_offset), text=e_mail, font=infoFont, fill="black")

    # 완성된 명함을 저장합니다.
    namecard.save(out_dir + "/" + division + "_" + name + "_" + telephone + ".png")

    # 저장도 했으니 명함을 닫아줍니다.
    namecard.close()

# 템플릿도 닫아줍니다.
image.close()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
