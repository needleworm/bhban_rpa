#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 6개월 치 업무를 하루 만에 끝내는 업무 자동화
Last Modification : 2020.02.17.
"""
import time
import os
import sys
import datetime

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

# 수여대상자가 기재된 CSV파일을 불러옵니다.
personal_IDs = sys.argv[1]

# 배경 템플릿 정보를 입력받습니다.
template_filename = sys.argv[2]

# 템플릿을 열어줍니다.
template = Image.open(template_filename)
Xdim, Ydim = template.size


# 결과물을 저장할 폴더를 생성합니다.
out_dir ="suryojungs"
if out_dir not in os.listdir():
    os.mkdir(out_dir)

# 인적사항을 불러옵니다.
IDs = open(personal_IDs)

# 헤더를 뽑아냅니다.
header = IDs.readline()

# 수료증(상장)에 삽입할 폰트들을 결정합니다.
# 폰트 이름을 변경하시면 바뀝니다. 기본은 굴림입니다. 컴퓨터를 막 굴리기 때문입니다.
# 이름은 큰 글자로 삽입합시다.
nameFont = ImageFont.truetype("font/gulim.ttc", 30)
# 수여날짜는 조금 더 작은 폰트로 기재합시다.
dateFont = ImageFont.truetype("font/gulim.ttc", 25)
# 수여번호는 더 더 작은 폰트로 기재합시다.
smallFont = ImageFont.truetype("font/gulim.ttc", 18)

# 배경에 입력할 수여날자를 계산합니다.
date = str(datetime.datetime.today().date())
date = date.split("-")
DATE = date[0] + "년 " + date[1] + "월 " + date[2] + "일"

# 수여날짜를 배경에 입력합니다.
# 좌우 여백은 가운데정렬입니다.
x_offset = int(Xdim / 2 - dateFont.getsize(DATE)[0]/2)
# 상하 여백은 대충 30% 가량 잡아봅니다.
y_offset = int(Ydim * .7)
# 배경에 수여날짜를 기재합니다.
ImageDraw.Draw(template).text(xy=(x_offset, y_offset), text=DATE, font=dateFont, fill="black")

# 지금까지 제작한 증서 개수를 저장하는 카운터를 만듭니다.
# 수료증서 시작번호를 적어주시면 됩니다. 예를들어 연번이 50번부터 시작하면 COUNT=50입니다.
COUNT = 0

# 인적사항을 한줄씩 읽어오면서, 한 번에 수료증(상장)을 한 장씩 만들겁니다.
for line in IDs:
    # CSV니까 컴마 단위로 쪼갤 수 있습니다. 쪼갭시다.
    splt = line.strip().split(", ")

    # 이름과 소속만 추출합니다.
    name = splt[0]
    division = splt[3]

    # 수료증(상장) 템플릿을 복제합니다.
    suryojung = template.copy()

    # 이름을 삽입할겁니다.
    # 이름 사이사이 공백을 삽입해서 더 잘 보이게 합니다.
    temp_name = ""
    for el in name:
        temp_name += el + " "
    # 이름을 수료증(상장)에 기재하기 좋게 양식으로 다듬어줍니다.
    name = "성      명 : " + temp_name[:-1]

    # 부서명을 삽입할겁니다.
    # 부서명 사이사이 공백을 삽입해서 더 잘 보이게 합니다.
    temp_division = ""
    for el in division:
        temp_division += el + " "
    # 부서명을 수료증(상장)에 기재하기 좋게 양식으로 다듬어줍니다.
    division = "소속부서 : " + temp_division

    # 이름과 대충 좌측으로부터 15% 떨어진 곳에 기재합시다.
    x_offset = int(Xdim * 0.15)
    # 이름은 대충 상단으로부터 35% 위치에 기재합시다.
    y_offset = int(Ydim * 0.35)
    # 수료증(상장)에 이름을 삽입합니다.
    ImageDraw.Draw(suryojung).text(xy=(x_offset, y_offset), text=name, font=nameFont, fill="black")

    # 부서명은 이름보다 좀 더 아래에 삽입해야겠죠.
    y_offset += nameFont.getsize(name)[1]*1.5
    # 수료증(상장)에 부서명을 삽입합니다.
    ImageDraw.Draw(suryojung).text(xy=(x_offset, y_offset), text=division, font=nameFont, fill="black")

    # 수여번호도 입력해야겠죠?
    suyeo = "수여번호 : %d-%06d" % (int(DATE[:4]),  COUNT)
    # 수여번호는 상 12%지점쯤에 입력합시다.
    y_offset = int(Ydim * 0.12)
    # 수료증(상장)에 수여번호를 삽입합니다.
    ImageDraw.Draw(suryojung).text(xy=(x_offset, y_offset), text=suyeo, font=smallFont, fill="black")

    # 완성된 증서를 저장합니다.
    suryojung.save(out_dir + "/" + str(COUNT) + ".png")

    # 저장도 했으니 이미지를 닫아줍니다.
    suryojung.close()

    COUNT += 1

# 템플릿도 닫아줍니다.
template.close()

# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
