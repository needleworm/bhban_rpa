#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.03.02.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pywinmacro as pw
import time
import pyperclip


class NewsBot:
    def __init__(self):
        # 쿼리 베이스를 제작합니다.
        self.querry ="https://www.google.com/search?tbm=nws&q="
        # 셀레늄 웹드라이버에 입력할 옵션을 지정합니다.
        self.options = Options()
        # 옵션에 해상도를 입력합니다.
        self.options.add_argument("--window-size=1024,768")
        # 크롬 웹드라이버를 불러옵니다.
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)
        # 정리된 뉴스를 저장할 변수를 만듭니다.
        self.news_list = []
        self.news_text = ""
        # 일단 트위터 로그인화면으로 갑니다.

    # 크롤러를 종료하는 메서드입니다.
    # 굳이 한줄짜리 코드를 함수로 만든 데에는 여러 이유가 있습니다만,
    # 쉽게 설명하자면 클래스 외부에서 클래스 내부 자료에 너무 깊게 관여하는 상황을 원하지 않기 때문입니다.
    def kill(self):
        self.driver.quit()

    # 검색을 실시합니다.
    def search(self, keyword):
        self.driver.get(self.querry + keyword)
        # 로딩이 오래 걸릴 수 있으니 잠시 대기합니다.
        time.sleep(3)

    # 페이지를 새로고침합니다.
    def refresh(self):
        pw.key_press_once("f5")

    # 페이지의 모든 내용을 선택하고 클립보드에 복사합니다.
    def copy_all(self):
        pw.ctrl_a()
        # 한 번 눌러서는 안 될 때도 있습니다. 한국인의 근성을 보여줍시다.
        time.sleep(1)
        pw.ctrl_c()
        time.sleep(1)
        pw.ctrl_c()
        time.sleep(1)
        pw.ctrl_c()

    # 페이지의 모든 내용을 선택해 뉴스 기사만 뽑아내는 함수입니다.
    def scrap_news(self):
        # 일단 페이지의 모든 내용물을 복사합니다.
        self.copy_all()
        # 뉴스 리스트를 초기화합니다.
        self.news_list = []
        # 텍스트를 클립보드에서 추출해 스트링으로 따 옵니다.
        self.news_text = pyperclip.paste()
        # 한 줄씩 쪼개줍니다.
        splt = self.news_text.split("\n")

        # 구글 뉴스는 이미지 정보, 헤드라인, 게시 시간, 본문 요약 순으로 정보가 제공됩니다.
        # 내용물을 한 줄씩 읽으면서 정보를 취합해 봅시다.

        # 글자들을 한 줄씩 불러옵니다.
        for i, line in enumerate(splt):
            # 라인을 죽 넘기다가 읽으며 '스토리 이미지'라는 글자가 없는 줄은 넘깁니다.
            if "스토리 이미지" not in line:
                continue
            # '스토리 이미지' 라는 단어가 발견되면 그 다음에 오는 3줄을 뭉쳐 하나의 스트링으로 만듭니다.
            new_news = "\n".join(splt[i+1:i+4])
            # 만들어진 뉴스를 news_list에 삽입합니다.
            self.news_list.append(new_news)

    # 뉴스 기사를 구글에서 검색한 뒤, 리스트로 다듬는 함수입니다.
    def news_crawler(self, keyword):
        self.search(keyword)
        self.scrap_news()

    # 스크린샷을 저장하는 함수입니다.
    def save_screenshot(self, filename):
        self.driver.save_screenshot(filename)

    # 트위터 페이지에 접속하는 메서드입니다.
    def go_to_twitter(self):
        # 트위터 홈페이지로 이동합니다.
        self.driver.get("http://twitter.com/")
        # 로딩이 오래 걸릴 수 있으니 잠시 대기합니다.
        time.sleep(2)

    # 트위터 홈으로 이동하는 메서드입니다.
    def twitter_home(self):
        self.driver.get("https://twitter.com/home")
        # 로딩이 오래 걸릴 수 있으니 잠시 대기합니다.
        time.sleep(2)

    # 로그인을 수행하는 메서드입니다.
    def login(self, id, ps):
        self.go_to_twitter()
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

    # 트위터에 글을 올리는 함수입니다.
    def tweet(self, text, interval):
        # 글을 쉽게 작성하기 위해 작성 전용 페이지로 이동합니다.
        self.driver.get("https://twitter.com/intent/tweet")
        time.sleep(2)
        # 커서가 기본적으로 입력창에 가 있습니다. 트윗 내용을 입력합니다.
        pw.type_in(text)
        time.sleep(1)
        # 컨트롤 키와 엔터키를 누르면 트윗이 입력됩니다.
        pw.key_on("control")
        pw.key_on("enter")
        pw.key_off("control")
        pw.key_off("enter")

        # 로딩 될때까지 몇 초 기다립니다.
        time.sleep(interval)

    # 스크랩한 모든 뉴스를 트위터에 올리는 함수입니다.
    # 15초 간격으로 뉴스를 올립니다. 시간 간격을 바꾸고 싶으면 함수를 호출할 때 시간을 초단위로 입력합니다.
    # 해시태그를 입력할 경우 함께 삽입합니다.
    def tweet_all(self, hashtags="", interval=15):
        for el in self.news_list:
            self.tweet(el.strip() + " " + hashtags, interval)

    # 구글에서 뉴스를 검색하고,
    # 트위터에 자동으로 로그인 한 뒤,
    # 긁어온 모든 뉴스를 업로드까지 하는 함수입니다.
    # 15초 간격으로 뉴스를 올립니다. 시간 간격을 바꾸고 싶으면 함수를 호출할 때 시간을 초단위로 입력합니다.
    # 해시태그를 입력할 경우 함께 삽입합니다.
    def tweet_all_news(self, keyword, hashtags="", interval=15):
        self.news_crawler(keyword)
        self.twitter_home()
        self.tweet_all(hashtags, interval)
        time.sleep(interval)
