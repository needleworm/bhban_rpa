#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 6개월 치 업무를 하루 만에 끝내는 업무 자동화
Last Modification : 2020.03.02.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pywinmacro as pw
import time


class CaptureBot:
    def __init__(self):
        # 쿼리 베이스를 제작합니다.
        self.querry ="https://www.instagram.com/explore/tags/"
        # 셀레늄 웹드라이버에 입력할 옵션을 지정합니다.
        self.options = Options()
        # 옵션에 해상도를 입력합니다.
        self.options.add_argument("--window-size=1024,768")
        # 크롬 웹드라이버를 불러옵니다.
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)

    # 크롤러를 종료하는 메서드입니다.
    # 굳이 한줄짜리 코드를 함수로 만든 데에는 여러 이유가 있습니다만,
    # 쉽게 설명하자면 클래스 외부에서 클래스 내부 자료에 너무 깊게 관여하는 상황을 원하지 않기 때문입니다.
    def kill(self):
        self.driver.quit()

    # 페이지를 새로고침합니다.
    def refresh(self):
        pw.key_press_once("f5")

    # 스크린샷을 저장하는 함수입니다.
    def save_screenshot(self, filename):
        self.driver.save_screenshot(filename)

    # 인스타그램 로그인 함수입니다.
    def login(self, id, ps):
        # 로그인 페이지로 이동합니다.
        self.driver.get("https://www.instagram.com/accounts/login")
        # 로딩이 오래 걸릴 수 있으니 잠시 대기합니다.
        time.sleep(5)
        # 탭 키를 한 번 누르면 아이디 입력창으로 이동합니다.
        pw.key_press_once("tab")
        # 아이디를 입력합니다.
        pw.typing(id)
        # 탭 키를 한 번 눌러 비밀번호 입력창으로 이동합니다.
        pw.key_press_once("tab")
        # 비밀번호도 입력합니다.
        pw.typing(ps)
        # 엔터키를 눌러 로그인을 시도합니다.
        pw.key_press_once("enter")
        # 로딩이 완료되기까지 충분히 기다려줍니다.
        time.sleep(10)

    # 인스타그램에서 태그를 검색하는 함수입니다.
    def search_tag(self, tag):
        self.driver.get(self.querry + tag)
        # 로딩이 오래 걸릴 수 있으니 잠시 대기합니다.
        time.sleep(5)

    # 태그 검색 화면에서 임의의 사진을 하나 선택하는 함수입니다.
    def select_picture(self):
        # 탭 키를 여러번 눌러 사진으로 이동하는 전략을 사용합니다.
        # 검색 결과에 예시로 나오는 '관련 해시태그' 개수가 매번 다르므로
        # 첫 번째 사진을 고르려면 매번 다른 회수의 탭을 눌러야 합니다.
        # 차라리 첫 몇개는 버리고 충분히 넉넉하게 탭을 누릅시다.
        for i in range(20):
            pw.key_press_once("tab")
        pw.key_press_once("enter")
        # 잠시 기다립니다.
        time.sleep(5)

    # 검색결과들을 돌아다니며 모조리 캡처합니다.
    # num에는 몇 개의 게시물을 캡처할 지 입력합니다.
    # -1을 입력하면 사용자가 직접 종료하기 전까지 무한정 계속합니다.
    def capture_pictures(self, directory, num):
        # 반복 회수를 결정하기 위한 변수입니다.
        count = num
        # count 가 0이 될때까지 반복합니다.
        while count != 0:
            # 카운트를 한 개씩 깎아내립니다.
            # num이 -1인 경우 계속 0보다 작아지기만 하고 0이 되지는 않으므로 영원히 실행됩니다.
            count -= 1
            # 스크린샷을 땁니다.
            self.save_screenshot(directory + "/" + str(time.time()) + ".png")
            # 다음 게시물로 넘어갑니다. 오른쪽 화살표버튼만 누르면 됩니다.
            pw.key_press_once("right_arrow")
            # 로딩을 위해 5초가량 기다립니다.
            time.sleep(5)

    # 코드 간소화를 위해 자기가 알아서 인스타 로그인하고, 검색하고, 캡처도 다 하는 메서드를 만듭시다.
    def insta_jungdok(self, tag, directory, num=100):
        # 태그도 검색하고
        self.search_tag(tag)
        # 사진 한 장을 선택한 다음
        self.select_picture()
        # 좋아요를 누르면서 사진을 샥 샥 넘깁니다.
        self.capture_pictures(directory, num)
