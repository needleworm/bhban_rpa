#-*-coding:euc-kr
"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.02.12.
"""
import time
import random
import os


# 작업 시작 메시지를 출력합니다.
print("Process Start.")

# 시작 시점의 시간을 기록합니다.
start_time = time.time()

# 생성할 개인정보 파일 개수를 정의합니다.
NUM_SAMPLES = 1000


# 이메일 생성에 사용할 샘플 글자들을 정의합니다.
alphabet_samples = "abcdefghizklmnopqrstuvwxyz1234567890"


# 무작위로 생성된 영어 글자를 생성하는 함수입니다.
def random_string(length):
    result = ""
    for i in range(length):
        result += random.choice(alphabet_samples)
    return result


# 이름 생성에 사용할 샘플 글자들을 정의합니다.
first_name_samples = "김이박최정강조윤장임"
middle_name_samples = "민서예지도하주윤채현지"
last_name_samples = "준윤우원호후서연아은진"


# 무작위로 사람 이름을 생성하는 함수입니다.
def random_name():
    result = ""
    result += random.choice(first_name_samples)
    result += random.choice(middle_name_samples)
    result += random.choice(last_name_samples)
    return result


# 결과물을 저장할 폴더를 생성합니다.
os.mkdir("personal_info")

# 헤더를 정의합니다.
header = ", ".join(["name", "age", "e-mail", "division", "telephone", "sex"]) + "\n"

# 개인정보 파일을 자동으로 생성하는 부분입니다.
# NUM_SAMPLES 회수만큼 반복합니다.
# 이를테면, NUM_SAMPLES가 100이면 무작위 개인정보 생성을 100회 반복합니다.
for i in range(NUM_SAMPLES):
    # 무작위로 사람 이름을 생성합니다.
    name = random_name()

    # 결과물 파일의 이름을 정의합니다.
    filename = "personal_info/" + str(i) + "_" + name + ".csv"
    # 결과물 파일을 생성합니다. 텅 빈 파일이 생성됩니다.
    outfile = open(filename, 'w')

    # 결과물 파일에 헤더를 기재합니다.
    outfile.write(header)

    # 결과물 파일에 이름을 기재합니다.
    outfile.write(name + ", ")

    # 결과물 파일에 무작위로 생성된 나이를 기재합니다.
    outfile.write(str(time.time())[-2:] + ", ")

    # 결과물 파일에 무작위로 생성된 이메일을 기재합니다.
    outfile.write(random_string(8) + "@bhban.com, ")

    # 결과물 파일에 무작위로 생성된 부서명을 기재합니다.
    outfile.write(random_string(3) + ", ")

    # 결과물 파일에 무작위로 생성된 핸드폰 번호를 기재합니다.
    outfile.write("010-" + str(time.time())[-4:] + "-" + str(time.time())[-6:-2] + ', ')

    # 결과물 파일에 무작위로 선정된 성별을 기재합니다.
    outfile.write(random.choice(["male", "female"]) )

    # 결과물 파일 수정을 마무리합니다.
    outfile.close()


# 작업 종료 메세지를 출력합니다.
print("Process Done.")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
