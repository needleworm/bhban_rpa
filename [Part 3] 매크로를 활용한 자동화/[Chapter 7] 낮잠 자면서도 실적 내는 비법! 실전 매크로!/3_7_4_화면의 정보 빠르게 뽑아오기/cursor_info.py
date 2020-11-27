"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 파이썬으로 6개월치 업무를 하루만에 끝내기
Last Modification : 2020.03.02.
"""

import pywinmacro as pw

# 마우스 좌표 주적
position = pw.get_mouse_position()

#마우스 좌표 출력
print("Your Mouse Position is " + str(position))

# 마우스 좌표의 색상을 추출해서 출력
print("color in hex is " + str(pw.get_color(position)))
