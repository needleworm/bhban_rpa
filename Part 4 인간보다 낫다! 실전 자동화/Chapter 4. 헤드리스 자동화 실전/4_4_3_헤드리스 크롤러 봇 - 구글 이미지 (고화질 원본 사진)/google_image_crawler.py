#-*-coding:euc-kr
"""
Author : Byunghyun Ban
GitHub : https://github.com/needleworm
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.03.02.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class ImgCrawler:
    def __init__(self, out_dir):
        # 쿼리 베이스를 제작합니다.
        self.querry ="https://www.google.co.in/search?tbm=isch&q="
        # 셀레늄 웹드라이버에 입력할 옵션을 지정합니다.
        self.options = Options()
        # 옵션에 헤드리스를 명시합니다. 이러면 헤드리스로 작업이 수행됩니다.
        self.options.add_argument("headless")
        # 헤드리스 브라우저의 창 크기를 지정해 줍니다.
        self.options.add_argument("--window-size=848,1500")
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

    # 이미지 검색 화면에서 첫 번째 이미지를 클릭해 미리보기 창을 띄우는 함수입니다.
    def select_picture(self):
        # 구글 검색의 이미지들은 <img> 태그로 감싸져 있습니다. 이 중 맨 위의 태그를 골라버립시다.
        picture_element = self.driver.find_element_by_tag_name("img")
        # 클릭합니다. 확대 이미지 창이 뜰겁니다.
        picture_element.click()
        # 5초 기다립니다.
        time.sleep(5)

    # 이미지 검색창의 확대샷이 열린 상태에서 이미지를 저장하고, 다음 사진으로 넘어가는 함수입니다.
    def crawl_one_image(self):
        # 확대된 이미지에서 이미지 요소를 뽑아옵니다.
        # 이 요소의 xpath는 '//*[@id="Sva75c"]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/a/img' 입니다.
        img_xpath = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/a/img'
        # 이미지 요소를 가져옵니다.
        image_element = self.driver.find_element_by_xpath(img_xpath)
        # 이미지에서 원본 출처 링크를 뽑아냅니다.
        image_url = image_element.get_attribute("src")
        # 이미지만 새 창에 따로 불러와서 작업합시다.
        # 드라이버 새 탭을 엽니다.
        self.driver.execute_script("window.open('');")
        # 새 탭은 driver.window_handles 안에 리스트로 저장됩니다.
        # 나중에 추가된 탭일수록 리스트의 뒤에 추가됩니다.
        # 리스트의 맨 뒤의 탭을 가져옵니다.
        new_tab = self.driver.window_handles[-1]
        # 새 탭으로 이동합니다.
        self.driver.switch_to.window(new_tab)
        # 이미지 링크로 이동합니다.
        self.driver.get(image_url)
        # 로딩 되기까지 좀 기다립니다.
        time.sleep(5)
        # 큰 이미지가 창에 떠 있습니다. 이 창에서 이미지 태그만 긁어옵시다.
        image = self.driver.find_element_by_tag_name("img")
        # 이미지를 저장합니다.
        image.screenshot(self.out_dir + "/" + str(time.time()) + ".png")
        # 볼 일이 끝났으니 이 탭은 닫아줍니다.
        self.driver.close()
        # 원래 탭으로 돌아옵니다.
        self.driver.switch_to.window(self.driver.window_handles[0])

    # 다음 이미지로 넘어가는 함수입니다.
    def next_image(self):
        # 다음 이미지로 넘어가기 위해 다음 버튼을 찾습니다.
        # 이 버튼의 xpath는 '//*[@id="Sva75c"]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[1]/a[2]/div' 입니다.
        button_xpath = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[1]/a[2]/div'
        # 버튼 요소를 가져옵시다.
        next_button = self.driver.find_element_by_xpath(button_xpath)
        # 버튼을 눌러 다음 이미지로 넘어갑니다.
        next_button.click()
        # 로딩을 위해 잠시 기다립니다.
        time.sleep(2)

    # 코드 간소화를 위해 자기가 알아서 구글 검색하고, 이미지 크롤링하는 함수를 만듭니다.
    def crawl_images(self, keyword, num=100):
        # 이미지 검색을 수행합니다.
        self.search_image(keyword)
        # 첫 번째 이미지를 눌러 확대창을 켭니다.
        self.select_picture()
        # num 번 만큼 반복하며 이미지를 저장합니다.
        for i in range(num):
            # 이미지를 저장하고
            self.crawl_one_image()
            # 다음 이미지로 넘어갑니다.
            self.next_image()
