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


# 각종 사이트들의 로그인 주소를 미리 저장해 둔 딕셔너리입니다.
LOGIN_URLS = {
    "twitter": "https://twitter.com/login",
    "daum": "https://logins.daum.net/accounts/signinform.do"
}


class LoginBot:
    def __init__(self, site):
        # 셀레늄 웹드라이버에 입력할 옵션을 지정합니다.
        self.options = Options()
        # 옵션에 해상도를 입력합니다.
        self.options.add_argument("--window-size=1600,900")
        # 옵션을 입력해서 크롬 웹드라이버를 불러옵니다.
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)
        # 로그인하려는 사이트로 이동해 로그인창을 켭니다.
        try:
            self.driver.get(LOGIN_URLS[site.lower()])
            # 로딩이 오래 걸릴 수 있으니 잠시 대기합니다.
            time.sleep(5)
        except KeyError:
            # 미리 세팅되지 않은 주소입니다. 주소창에 바로 입력을 시도합니다.
            self.driver.get(site)
            # 로딩이 오래 걸릴 수 있으니 잠시 대기합니다.
            time.sleep(5)

    # 크롤러를 종료하는 메서드입니다.
    # 굳이 한줄짜리 코드를 함수로 만든 데에는 여러 이유가 있습니다만,
    # 쉽게 설명하자면 클래스 외부에서 클래스 내부 자료에 너무 깊게 관여하는 상황을 원하지 않기 때문입니다.
    def kill(self):
        self.driver.quit()

    # 로그인을 수행하는 메서드입니다.
    def login(self, id, ps):
        # 아이디를 입력합니다.
        pw.typing(id)
        # tab 키를 눌러줍시다. 대부분의 사이트에서 암호창으로 이동합니다.
        pw.key_press_once("tab")
        # 비밀번호를 마저 입력합니다.
        pw.typing(ps)
        # 엔터키를 눌러줍니다. 대부분의 사이트에서 로그인이 실행됩니다.
        pw.key_press_once("enter")
        # 로딩이 오래 걸릴 수 있으니 잠시 대기합니다.
        time.sleep(5)

    def save_screenshot(self):
        self.driver.save_screenshot("test.png")