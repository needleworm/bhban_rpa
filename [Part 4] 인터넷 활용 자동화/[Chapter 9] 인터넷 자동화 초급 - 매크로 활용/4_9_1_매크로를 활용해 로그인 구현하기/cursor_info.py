"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 파이썬으로 6개월치 업무를 하루만에 끝내기
Last Modification : 2020.03.02.
"""

import pywinmacro as pw

position = pw.get_mouse_position()
print("Your Mouse Position is " + str(position))
print("color in hex is " + str(pw.get_color(position)))
