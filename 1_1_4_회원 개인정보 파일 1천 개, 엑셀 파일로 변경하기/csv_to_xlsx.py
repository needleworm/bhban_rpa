from pyexcel.cookbook import merge_all_to_a_book
import sys


# 터미널에서 인자를 입력받기 위한 코드입니다.
input_file = sys.argv[1]
result_file = sys.argv[2]

merge_all_to_a_book([input_file], result_file)