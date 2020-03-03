#-*-coding:euc-kr
"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.03.02.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pywinmacro as pw
import time


class TwitterBot:
    def __init__(self, contents, mention_location, encoding="utf-8"):
        # 멘션 좌표를 튜플로 저장합니다.
        self.mention_location = mention_location
        # 셀레늄 웹드라이버에 입력할 옵션을 지정합니다.
        self.options = Options()
        # 옵션에 해상도를 입력합니다.
        self.options.add_argument("window-size=1024x768")
        # 트위터 홈페이지로 이동합니다.
        self.go_to_twitter()

        # 컨텐츠 파일을 읽어옵니다. 인코딩이 utf-8이 아닌 파일을 읽으면 에러가 날겁니다.
        # 이때는 인코딩을 명시해 주시면 됩니다. 기본값은 utf8입니다.
        self.contents_file = open(contents, encoding=encoding)
        # 읽어온 파일을 쪼개 리스트로 만듭니다.
        self.contents = self.contents_file.read().split("\n")

    # 크롤러를 종료하는 메서드입니다.
    # 굳이 한줄짜리 코드를 함수로 만든 데에는 여러 이유가 있습니다만,
    # 쉽게 설명하자면 클래스 외부에서 클래스 내부 자료에 너무 깊게 관여하는 상황을 원하지 않기 때문입니다.
    def kill(self):
        self.driver.quit()

    # 트위터 페이지에 접속하는 메서드입니다.
    def go_to_twitter(self):
        # 크롬 웹드라이버를 불러옵니다.
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)
        # 트위터 홈페이지로 이동합니다.
        self.driver.get("https://twitter.com/")
        # 로딩이 오래 걸릴 수 있으니 잠시 대기합니다.
        time.sleep(5)


    # 로그인을 수행하는 메서드입니다.
    def login(self, id, ps):
        # 아이디를 입력합니다.
        pw.typinrg(id)
        # tab 키를 눌러줍시다. 대부분의 사이트에서 암호창으로 이동합니다.
        pw.key_press_once("tab")
        # 비밀번호를 마저 입력합니다.
        pw.typinrg(ps)
        # 1초 쉬어줍니다.
        time.sleep(1)
        # 엔터키를 눌러줍니다. 대부분의 사이트에서 로그인이 실행됩니다.
        pw.key_press_once("enter")
        # 로딩이 오래 걸릴 수 있으니 잠시 대기합니다.
        time.sleep(5)

    # 스크린샷을 저장하는 함수입니다.
    def save_screenshot(self, filename):
        self.driver.save_screenshot(filename)

    # 트위터에 글을 올리는 함수입니다.
    def tweet(self, mention):
        #멘션창을 몇 번 클릭해 줍니다. 한번만 해서는 안 될 때가 있습니다.
        pw.click(self.mention_location)
        pw.click(self.mention_location)
        pw.type_in(mention)
        # 1초 쉬어줍니다.
        time.sleep(1)
        # 탭 키를 여섯 번 누릅니다.
        for i in range(6):
            pw.key_press_once("tab")
        # 1초 쉬어줍니다.
        time.sleep(1)
        #엔터키를 칩니다.
        pw.key_press_once("enter")

    # 읽어온 모든 멘션들을 업로드하는 함수입니다.
    # 3초 간격으로 멘션을 올립니다. 시간 간격을 바꾸고 싶으면 함수를 호출할 때 시간을 초단위로 입력합니다.
    def tweet_all(self, interval=15):
        for el in self.contents:
            time.sleep(interval)
            self.tweet(el.strip())
