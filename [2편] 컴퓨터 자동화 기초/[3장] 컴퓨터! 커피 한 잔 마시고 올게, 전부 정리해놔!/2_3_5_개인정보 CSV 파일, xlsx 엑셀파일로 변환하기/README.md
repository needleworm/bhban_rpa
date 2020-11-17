# 개인정보 CSV 파일, 엑셀로 변환하기

###아래 명령어를 실행하여 파이엑셀 라이브러리를 설치합니다.

> pip install pyexcel pyexcel-xlsx

### 아래 명령어를 실행하시면 예제가 실행됩니다.

> python  csv_to_xlsx.py  <INPUT\>   <OUTPUT\>

<INPUT\>에는 CSV로 변환할 파일 이름을, <OUTPUT\>에는 결과물 파일 이름을 적어주세요.


###책의 예제는 아래와 같습니다.

>python csv_to_xlsx.py merged_ID.csv merged_ID.xlsx 



###인코딩 관련 에러가 출력될 수 있습니다. 이 경우 'euc_to_utf.py'를 이용해 인코딩을 변경해 주세요. 사용방법은 아래와 같습니다.

>python euc_to_utf.py <INPUT\>   <OUTPUT\>

<INPUT\>에는 euc-kr로 인코딩된 파일 이름을, <OUTPUT\>에는 결과물 파일 이름을 적어주세요.
