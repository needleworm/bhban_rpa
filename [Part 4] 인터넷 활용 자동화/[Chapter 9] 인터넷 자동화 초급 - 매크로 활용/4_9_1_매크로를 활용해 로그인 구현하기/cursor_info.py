"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 6개월 치 업무를 하루 만에 끝내는 업무 자동화
Last Modification : 2020.03.02.
"""

import pywinmacro as pw

position = pw.get_mouse_position()
print("Your Mouse Position is " + str(position))
print("color in hex is " + str(pw.get_color(position)))
