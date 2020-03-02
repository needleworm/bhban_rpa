"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.03.02.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pywinmacro as pw


# 각종 사이트들의 로그인 주소를 미리 저장해 둔 딕셔너리입니다.
LOGIN_URLS = {
    "naver": "https://nid.naver.com/nidlogin.login?",
    "google": "https://accounts.google.com/signin",
    "daum": "https://logins.daum.net/accounts/signinform.do",
    "twitter": "https://twitter.com/",
    "instagram": "https://www.instagram.com/accounts/login",
    "facebook": "https://facebook.com",
    "coupang": "https://login.coupang.com/login/login.pang"
}

class LoginBot:
    def __init__(self, site):
        # 셀레늄 웹드라이버에 입력할 옵션을 지정합니다.
        self.options = Options()
        # 옵션에 해상도를 입력합니다.
        self.options.add_argument("window-size=1024x768")
        # 옵션을 입력해서 크롬 웹드라이버를 불러옵니다.
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)
        # 로그인하려는 사이트로 이동해 로그인창을 켭니다.
        try:
            self.driver.get(LOGIN_URLS[site.lower()])
        except KeyError:
            print(site + " is not listed on the LOGIN_URLS dictionary.")
            exit(1)

    # 크롤러를 종료하는 메서드입니다.
    # 굳이 한줄짜리 코드를 함수로 만든 데에는 여러 이유가 있습니다만,
    # 쉽게 설명하자면 클래스 외부에서 클래스 내부 자료에 너무 깊게 관여하는 상황을 원하지 않기 때문입니다.
    def kill(self):
        self.driver.quit()

    # 로그인을 수행하는 메서드입니다.
    def login(self, id, ps, x, y):
        # 로그인창을 클릭합니다.
        pw.click((x, y))
        # 아이디를 입력합니다.
        pw.typinrg(id)

        # tab 키를 눌러줍시다. 대부분의 사이트에서 암호창으로 이동합니다.
        pw.key_press_once("tab")

        # 비밀번호를 마저 입력합니다.
        pw.typinrg(ps)

        # 엔터키를 눌러줍니다. 대부분의 사이트에서 로그인이 실행됩니다.
        pw.key_press_once("enter")
