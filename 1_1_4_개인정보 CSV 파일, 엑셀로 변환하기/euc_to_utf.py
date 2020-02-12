"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.02.12.
"""
import sys

# 파일 이름을 입력받습니다.
filename = sys.argv[1]

# euc-kr로 인코딩된 파일을 실행합니다.
in_file = open(filename, encoding="euc-kr")

# utf-8로 저장할 파일을 실행합니다.
out_file = open("utf8_" + filename, 'w', encoding="utf8")

content = in_file.read()

out_file.write(content)

in_file.close()
out_file.close()

