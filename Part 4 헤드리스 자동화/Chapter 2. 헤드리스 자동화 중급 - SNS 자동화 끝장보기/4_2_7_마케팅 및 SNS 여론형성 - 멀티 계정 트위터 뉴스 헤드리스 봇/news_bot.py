"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.03.02.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time


class NewsBot:
    def __init__(self, endswith):
        # 셀레늄 웹드라이버에 입력할 옵션을 지정합니다.
        self.options = Options()
        # 옵션에 헤드리스를 명시합니다. 이러면 헤드리스로 작업이 수행됩니다.
        self.options.add_argument("headless")
        # 옵션에 해상도를 입력합니다.
        self.options.add_argument("--window-size=1024,768")
        # 옵션을 입력해서 크롬 웹드라이버를 불러옵니다.
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)
        # 트윗할 메시지들을 저장할 공간을 만듭니다.
        self.contents = []
        # 쿼리를 만듭니다.
        self.query = "https://www.google.com/search?tbm=nws&q="
        # 글 말미에 붙일 문구를 입력합니다.
        self.endswith = endswith

    # 크롤러를 종료하는 메서드입니다.
    # 굳이 한줄짜리 코드를 함수로 만든 데에는 여러 이유가 있습니다만,
    # 쉽게 설명하자면 클래스 외부에서 클래스 내부 자료에 너무 깊게 관여하는 상황을 원하지 않기 때문입니다.
    def kill(self):
        self.driver.quit()

    # 크롤러를 껐다가 다시 켜는 메서드입니다.
    def driver_refresh(self):
        # 드라이버를 종료합니다.
        self.kill()
        # 드라이버를 다시 켭니다.
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)
        # 트윗할 메시지들을 저장할 공간을 초기화합니다.
        self.contents = []

    # 로그인을 수행하는 메서드입니다.
    def login(self, id, ps):
        # 트위터 로그인창으로 들어갑니다.
        self.driver.get("https://twitter.com/login")
        # 로딩이 오래 걸릴 수 있으니 잠시 대기합니다.
        time.sleep(3)
        # 아이디를 입력하기 위해 아이디 입력창 요소를 찾아옵니다.
        # 트위터의 경우 아이디 입력창은 session[username_or_email] 이라는 이름을 갖고 있습니다.
        id_input = self.driver.find_element_by_name("session[username_or_email]")
        # id를 입력합니다.
        id_input.send_keys(id)

        # 비밀번호를 입력합니다.
        # 트위터의 경우 비밀번호 입력창은 session[password] 라는 이름을 갖고 있습니다.
        ps_input = self.driver.find_element_by_name("session[password]")
        ps_input.send_keys(ps)
        ps_input.send_keys(Keys.RETURN)
        time.sleep(3)

    # 구글에서 뉴스를 긁어와 트윗하기 좋게 다듬는 함수입니다.
    def prepare_contents(self, keyword):
        self.contents = []
        # 검색을 수행합니다.
        self.driver.get(self.query + keyword)
        # 뉴스 기사와 관련된 엘레먼트를 한번에 다 따겠습니다.
        # 구글 뉴스 검색 결과는 'g' 라는 이름의 클래스로 제공됩니다.
        news_elements = self.driver.find_elements_by_class_name("g")
        # 모든 엘레멘트로부터 정보를 추출하겠습니다.
        for el in news_elements:
            # 기사 제목을 추출합니다. <h3> 태그로 작성되었습니다.
            headline = el.find_element_by_tag_name("h3").text
            # 기사 하이퍼링크 태그를 추출합니다.
            hyperlink = el.find_element_by_tag_name("a")
            # 기사 하이퍼링크 태그에서 기사 주소를 추출합니다.
            news_url = hyperlink.get_attribute("href")
            # 신문사 정보를 추출합니다. "dhIWpd"라는 클래스 이름으로 저장되어 있습니다.
            reference = el.find_element_by_class_name("dhIWPd").text
            # 뉴스 앞 부분을 추출해 냅니다. "st"라는 클래스로 기록되어 있습니다.
            head = el.find_element_by_class_name("st").text
            # 트윗에 올릴 기사 요약을 만듭니다.
            news_summary = "\n".join((headline, reference, head, self.endswith, news_url))
            self.contents.append(news_summary)

    # 메시지를 입력받아 트윗하는 매서드입니다.
    def tweet(self, string):
        # 트윗 멘션을 쉽게 입력할 수 있게 전용 페이지로 이동합니다.
        self.driver.get("https://twitter.com/intent/tweet")
        time.sleep(5)
        # 메시지 입력창 요소를 찾습니다. xpath를 복사합니다.
        board = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div')
        # 메시지 입력창에 메시지를 보냅니다.
        board.send_keys(string)
        # Ctrl + Enter를 눌러 메시지를 게시합니다.
        board.send_keys(Keys.CONTROL + Keys.RETURN)

    # self.contents에 저장된 모든 메시지를 하나씩 트윗하는 매서드입니다.
    def tweet_all(self, interval):
        # for문을 사용해 모든 메시지를 하나씩 접근합니다.
        for el in self.contents:
            # 메시지를 하나씩 트윗합니다.
            self.tweet(el)
            # 로딩에 좀 걸릴 수 있으므로 기다려줍니다.
            time.sleep(interval)

    # 키워드를 입력받아 뉴스를 검색하고, 트위터에도 업로드하는 봇을 만듭니다.
    def news_go_go(self, keyword, interval=10):
        # 뉴스 기사를 긁어옵니다.
        self.prepare_contents(keyword)
        # 긁어온 모든 자료를 올립니다.
        self.tweet_all(interval)

    def save_screenshot(self):
        self.driver.save_screenshot("test.png")
