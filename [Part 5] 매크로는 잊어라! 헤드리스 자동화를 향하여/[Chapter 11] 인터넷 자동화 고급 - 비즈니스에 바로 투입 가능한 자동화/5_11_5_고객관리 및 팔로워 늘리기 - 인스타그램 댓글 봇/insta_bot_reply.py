#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 6개월 치 업무를 하루 만에 끝내는 업무 자동화
Last Modification : 2020.03.02.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import random


class ReplyBot:
    def __init__(self, replyfile):
        # 쿼리 베이스를 제작합니다.
        self.querry ="https://www.instagram.com/explore/tags/"
        # 셀레늄 웹드라이버에 입력할 옵션을 지정합니다.
        self.options = Options()
        # 옵션에 헤드리스를 명시합니다. 주석을 해제하면 헤드리스로 작업이 수행됩니다.
        # self.options.add_argument("headless")
        # 옵션에 해상도를 입력합니다.
        self.options.add_argument("--window-size=1024,768")
        # 크롬 웹드라이버를 불러옵니다.
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)
        # 댓글 내용이 적힌 파일을 불러옵니다. 인코딩이 utf8이 아니면 바꿔주세요.
        self.replyfile = open(replyfile, encoding="utf8")
        # 댓글 내용 리스트를 만듭니다.
        self.replylist = self.replyfile.read().split("\n")

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
        # 로딩을 위해 5초 정도 기다려 줍니다.
        time.sleep(5)
        # ID, PS 입력 요소는 <input> 태그입니다. 요소를 찾아줍시다.
        input_field = self.driver.find_elements_by_tag_name("input")
        # 첫 번째 요소가 아이디입니다. 아이디를 입력합니다.
        input_field[0].send_keys(id)
        # 비밀번호 입력 요소는 두 번째입니다. 비밀번호를 입력합니다.
        input_field[1].send_keys(ps)
        # 엔터키를 쳐서 로그인을 마무리합니다.
        input_field[1].send_keys(Keys.RETURN)
        # 10초 정도 기다려 줍니다.
        time.sleep(5)

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

    # 검색결과들을 돌아다니며 모조리 좋아요를 누르고 댓글도 답니다.
    # num에는 몇 개의 게시물을 좋아요 할지 입력합니다.
    # -1을 입력하면 사용자가 직접 종료하기 전까지 무한정 계속합니다.
    def press_like_and_reply(self, num):
        # 반복 회수를 결정하기 위한 변수입니다.
        count = num
        # count 가 1개씩 깎이면서, 0이 될때까지 반복합니다.
        # num이 -1인 경우 계속 0보다 작아지기만 하고 0이 되지는 않으므로 영원히 실행됩니다.
        while count != 0:
            # 좋아요 버튼의 태그를 직접 찾기는 힘듭니다. 좋아요 버튼은 <svg> 태그로 만들어져 있는데
            # 이 화면에 <svg> 태그를 갖고 있는 버튼이 한 두 개가 아닙니다.
            # 그러므로 일단 <svg> 태그를 가진 요소를 몽땅 갖고옵니다.
            svg = self.driver.find_elements_by_tag_name("svg")
            # <svg> 태그는 내부에 aria-label 이라는 이름의 어트리뷰트를 갖고 있습니다.
            # 이 어트리뷰트가 '좋아요' 인 svg요소만 찾아내 클릭합시다.
            # for 문으로 일단 svg 태그들을 모조리 불러옵니다.
            for el in svg:
                # 태그 내부의 aria-label 어트리뷰트가 좋아요 인 경우만 잡아냅니다.
                # 이미 좋아요가 눌려져 있는 경우 어트리뷰트 값이 "좋아요 취소" 로 변경됩니다.
                # 따라서 이 방법은 이미 좋아요를 눌러 둔 게시물은 건너뛸 수 있다는 장점도 가집니다.
                # 이미 좋아요를 누른 게시물은 건너뜁니다.
                if el.get_attribute("aria-label") == "좋아요 취소":
                    break
                # 좋아요 버튼을 찾습니다.
                if el.get_attribute("aria-label") == "좋아요":
                    # 좋아요 버튼을 클릭합니다.
                    el.click()
                    # 적당히 오래 기다려 줍니다.
                    time.sleep(5)
                    # 댓글 파일 중 랜덤으로 하나를 뽑아서 댓글을 달아줍시다.
                    # 에러가 나면 두 번 더 시도합니다.
                    # 어지간해선 3번이면 됩니다.
                    # 이렇게 try except문을 겹쳐 쓰는건 원래는 절대 하지 말아야 할 코딩 방법입니다.
                    try:
                        self.send_reply(random.choice(self.replylist))
                    except:
                        time.sleep(5)
                        try:
                            self.send_reply(random.choice(self.replylist))
                        except:
                            time.sleep(5)
                            self.send_reply(random.choice(self.replylist))
                    # 카운트를 한 개씩 깎아내립니다.
                    count -= 1
                    break
            # 다음 게시물로 넘어갑시다. 다음 버튼에는 link text가 "다음"으로 기재되어 있습니다. 요소를 찾습니다.
            next_button = self.driver.find_element_by_link_text("다음")
            # 클릭합니다.
            next_button.click()
            # 댓글은 좀 긴 텀을 두고 달아야 합니다. 안 그러면 인스타 운영진들이 댓글 개제 중단 재제를 줍니다.
            time.sleep(30)

    # 댓글을 남기는 함수입니다.
    def send_reply(self, text):
        # 댓글 입력창은 <textarea> 라는 태그로 되어 있습니다.
        textarea = self.driver.find_element_by_tag_name("textarea")
        textarea.send_keys(text + Keys.RETURN)

    # 코드 간소화를 위해 자기가 알아서 인스타 로그인하고, 검색하고, 댓글도 다 다는
    def insta_jungdok(self, tag, num=100):
        # 태그도 검색하고
        self.search_tag(tag)
        # 사진 한 장을 선택한 다음
        self.select_picture()
        # 좋아요를 누르고, 댓글을 달면서 사진을 한 장씩 넘겨줍니다.
        self.press_like_and_reply(num)
