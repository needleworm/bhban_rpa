#-*-coding:euc-kr
"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.03.02.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time


class CaptureBot:
    def __init__(self):
        # 쿼리 베이스를 제작합니다.
        self.querry ="https://www.instagram.com/explore/tags/"
        # 셀레늄 웹드라이버에 입력할 옵션을 지정합니다.
        self.options = Options()
        # 옵션에 해상도를 입력합니다.
        #self.options.add_argument("--window-size=1024,768")
        # 크롬 웹드라이버를 불러옵니다.
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)

    # 크롤러를 종료하는 메서드입니다.
    # 굳이 한줄짜리 코드를 함수로 만든 데에는 여러 이유가 있습니다만,
    # 쉽게 설명하자면 클래스 외부에서 클래스 내부 자료에 너무 깊게 관여하는 상황을 원하지 않기 때문입니다.
    def kill(self):
        self.driver.quit()

    # 스크린샷을 저장하는 함수입니다.
    def save_screenshot(self, filename):
        self.driver.save_screenshot(filename)

    # 인스타그램 로그인 함수입니다.
    def login(self, id, ps):
        # 로그인 페이지로 이동합니다.
        self.driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        # ID, PS 입력 요소는 <input> 태그입니다. 요소를 찾아줍시다.
        input_field = self.driver.find_elements_by_tag_name("input")
        # 첫 번째 요소가 아이디입니다. 아이디를 입력합니다.
        input_field[0].send_keys(id)
        # 비밀번호 입력 요소는 두 번째입니다. 비밀번호를 입력합니다.
        input_field[1].send_keys(ps)
        # 엔터키를 쳐서 로그인을 마무리합니다.
        input_field[1].send_keys(Keys.RETURN)

    # 인스타그램에서 태그를 검색하는 함수입니다.
    def search_tag(self, tag):
        self.driver.get(self.querry + tag)
        # 로딩이 오래 걸릴 수 있으니 잠시 대기합니다.
        time.sleep(5)

    # 태그 검색 화면에서 최근에 게시된 첫 번째 사진을 골라 클릭합니다.
    def select_picture(self):
        # 최근 사진의 xpath는 아래와 같습니다.
        recent_picture_xpath = '//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]'
        # 최근 사진의 요소를 가져옵니다.
        recent_picture = self.driver.find_element_by_xpath(recent_picture_xpath)
        # 최근 사진을 클릭합니다.
        recent_picture.click()

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
            # 화면을 통째로 캡처하는건 의미가 없으니 사진과 게시물 부분만 캡쳐합시다.
            # 이 영역의 xpath는 '/html/body/div[4]/div[2]/div/article' 입니다.
            article_xpath = '/html/body/div[4]/div[2]/div/article'
            # 요소를 찾아 줍니다.
            article_element = self.driver.find_element_by_xpath(article_xpath)
            # 요소별로 스크린샷을 찍을 수 있습니다. 찍어 줍시다.
            article_element.screenshot(directory + "/" + str(time.time()) + ".png")
            # 잠시 기다려 줍시다.
            time.sleep(2)
            # 다음 게시물로 넘어갑시다. 다음 버튼에는 link text가 "다음"으로 기재되어 있습니다. 요소를 찾습니다.
            next_button = self.driver.find_element_by_link_text("다음")
            # 클릭합니다.
            next_button.click()
            # 로딩을 위해 5초정도 기다려 줍니다.
            time.sleep(5)

    # 코드 간소화를 위해 자기가 알아서 인스타 로그인하고, 검색하고, 캡처도 다 하는 메서드를 만듭시다.
    def insta_jungdok(self, tag, directory, num=100):
        # 태그도 검색하고
        self.search_tag(tag)
        # 사진 한 장을 선택한 다음
        self.select_picture()
        # 캡처를 따면서 사진을 한 장씩 넘겨줍니다.
        self.capture_pictures(directory, num)
