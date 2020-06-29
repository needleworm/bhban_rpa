#-*-coding:euc-kr
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


class ImgCrawler:
    def __init__(self, out_dir):
        # 쿼리 베이스를 제작합니다.
        self.querry ="https://www.google.co.in/search?tbm=isch&q="
        # 셀레늄 웹드라이버에 입력할 옵션을 지정합니다.
        self.options = Options()
        # 옵션에 헤드리스를 명시합니다. 이러면 헤드리스로 작업이 수행됩니다.
        self.options.add_argument("headless")
        # 옵션에 해상도를 입력합니다.
        self.options.add_argument("--window-size=1024,768")
        # 크롬 웹드라이버를 불러옵니다.
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)
        # 결과물을 저장할 디렉터리를 기록합니다.
        self.out_dir = out_dir

    # 크롤러를 종료하는 메서드입니다.
    # 굳이 한줄짜리 코드를 함수로 만든 데에는 여러 이유가 있습니다만,
    # 쉽게 설명하자면 클래스 외부에서 클래스 내부 자료에 너무 깊게 관여하는 상황을 원하지 않기 때문입니다.
    def kill(self):
        self.driver.quit()

    # 스크린샷을 저장하는 함수입니다.
    def save_screenshot(self, filename):
        self.driver.save_screenshot(filename)

    # 키워드를 구글 이미지에서 검색하는 함수입니다.
    def search_image(self, keyword):
        self.driver.get(self.querry + keyword)
        # 로딩이 오래 걸릴 수 있으니 잠시 대기합니다.
        time.sleep(5)

    # 이미지 검색 화면을 스크롤 다운하는 함수입니다.
    def scroll_down(self):
        # 사이트의 뼈대인 <body> 태그를 찾습니다.
        body = self.driver.find_element_by_tag_name("body")
        # 대충 많이 스크롤질 합시다.
        for i in range(50):
            body.send_keys(Keys.END)
            time.sleep(0.5)
        # 다시 맨 위로 올라갑시다. 기분 좋으라고 넣는겁니다. 없어도 됩니다.
        body.send_keys(Keys.HOME)

    # 이미지 검색 결과창의 모든 이미지를 긁어오는 함수입니다.
    def crawl_pictures(self, num):
        # 구글 검색은 초기에 이미지 검색 결과를 일부만 표기합니다.
        # 스크롤을 맨 아래까지 내려서 사진을 추가로 로드합니다.
        # 저자의 컴퓨터 기준으로 총 400개의 사진이 표기됩니다.
        self.scroll_down()
        # <img> 태그를 갖고있는 모든 요소를 불러옵시다.
        img_elements = self.driver.find_elements_by_tag_name("img")
        # for 문을 이용해 위 요소들을 하나하나 다운받습니다.
        for i, el in enumerate(img_elements):
            # 초기 세팅한 개수만큼 사진을 다운받았다면 루프를 끝내 줍니다.
            if i == num:
                break
            # 화면이 신나게 번쩍이면서 다운로드됩니다.
            el.screenshot(self.out_dir + "/" + str(i) + ".png")
            time.sleep(0.1)
        # 요청받은 개수보다 사진을 더 적게 다운받았다면
        if i < num:
            # 키워드를 바꿔서 다시 검색해 달라는 메시지를 출력합니다.
            print("Not enough search result. Please change the keyword and try again.")

    # 코드 간소화를 위해 자기가 알아서 구글 검색하고, 이미지 크롤링하는 함수를 만듭니다.
    def crawl_images(self, keyword, num):
        # 이미지 검색을 수행합니다.
        self.search_image(keyword)
        # 작업을 수행합니다.
        self.crawl_pictures(num)
