# -*-coding:euc-kr
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


class Thaad:
    def __init__(self, id, ps, keyword_file_name, target_file_name):
        # 셀레늄 드라이버에 들어갈 옵션을 지정합니다.
        self.options = Options()
        # 옵션에 헤드리스를 명시합니다. 이러면 헤드리스로 작업이 수행됩니다.
        self.options.add_argument("headless")
        # 필요한 경우 브라우저 창 크기를 지정해 줍니다.
        self.options.add_argument("--window-size=848,1500")
        # 옵션을 반영해 크롬드라이버를 열어 줍니다.
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)
        # 로그인을 수행합니다.
        self.brunch_login(id, ps)
        # 지금까지 삭제한 악플 개수를 기록하기 위한 변수를 만듭니다.
        self.count = 0
        # 로그파일을 제작합니다. 이 클래스를 선언하는 순간의 시간으로 파일명이 정해집니다.
        self.log_output = str(time.time()) + ".txt"
        # 삭제 대상 키워드를 저장할 공간을 만듭니다.
        self.kill_keywords = []
        # 삭제 대상 키워드 파일을 읽어옵니다.
        self.read_kill_keyword(keyword_file_name)
        # 보호 대상 게시물 주소를 저장할 공간을 만듭니다.
        self.target_urls = []
        # 보호 대상 게시물 주소 파일을 읽어옵니다.
        self.read_target_urls(target_file_name)
        print("file read done.")

    def brunch_login(self, id, ps):
        # 로그인을 위한 준비를 합니다. 카카오브런치의 경우 로그인 주소가 굉장히 깁니다.
        # 다른 사이트를 활용하실 경우 앞선 로그인 예제들을 참고하여 로그인 주소를 변경하여 주세요.
        brunch_login_url = "https://accounts.kakao.com/login?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fclient_id%3De0201caea90cafbb237e250f63a519b5%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fbrunch.co.kr%252Fcallback%252Fauth%252Fkakao%26scope%3D%26state%3DaHR0cHM6Ly9icnVuY2guY28ua3IvL3NpZ25pbi9maW5pc2g_c2lnbmluPXRydWUmdXJsPSUyRg%26grant_type%3Dauthorization_code"
        # 로그인 주소로 이동합니다.
        self.driver.get(brunch_login_url)
        # 브런치의 경우 아이디 입력 요소의 이름이 'email'입니다. 이 요소를 찾아내 바로 id를 입력합시다.
        self.driver.find_element_by_name("email").send_keys(id)
        # 브런치의 경우 비밀번호 입력 요소의 이름이 'password'입니다. 이 요소를 찾아내 바로 ps를 입력합시다.
        # 추가로 엔터키도 쳐서 로그인을 수행합니다.
        self.driver.find_element_by_name("password").send_keys(ps + Keys.RETURN)
        # 10초정도 기다립니다.
        time.sleep(10)
        print("login success")

    # 삭제 대상 키워드 파일을 불러오는 함수입니다.
    def read_kill_keyword(self, filename):
        # 파일을 읽어옵니다.
        file = open(filename)
        # 파일을 한 줄씩 읽어옵니다.
        for line in file:
            # 각 라인을 self.kill_keywords에 입력합니다.
            self.kill_keywords.append(line.strip())
        # 파일을 닫아줍니다.
        file.close()

    def read_target_urls(self, filename):
        # 파일을 읽어옵니다.
        file = open(filename)
        # 파일을 한 줄씩 읽어옵니다.
        for line in file:
            # 각 라인을 self.target_urls에 입력합니다.
            # 뒤에 있는 "#comments"에 주목하세요. 브런치의 경우 게시물 주소 뒤에 #comments를 입력하면
            # 댓글 창으로 바로 접속할 수 있습니다. 구현 난이도가 확 내려갑니다.
            # 현실에서 업무자동화를 만드려면 최대한 생각을 많이 하고, 정보를 많이 확보해야 합니다.
            # 코딩보다 설계에 시간을 더 많이 투자하세요.
            self.target_urls.append(line.strip() + "#comments")
        # 파일을 닫아줍니다.
        file.close()

    # 크롤러를 종료하는 메서드입니다.
    # 굳이 한줄짜리 코드를 함수로 만든 데에는 여러 이유가 있습니다만,
    # 쉽게 설명하자면 클래스 외부에서 클래스 내부 자료에 너무 깊게 관여하는 상황을 원하지 않기 때문입니다.
    def kill(self):
        self.driver.quit()

    # 스크린샷을 저장하는 함수입니다.
    def save_screenshot(self, filename):
        self.driver.save_screenshot(filename)

    # 사드를 가동하는 함수입니다.
    def run_thaad(self):
        # 로그 파일을 생성합니다. 여기에 악플을 삭제할 때마다 로그를 기록합니다.
        log = open(self.log_output, 'w')
        # 보호 대상 url들을 하나씩 불러옵니다.
        for target_url in self.target_urls:
            # 게시물로 이동합니다.
            self.driver.get(target_url)
            # 로딩을 위해 3초 정도 기다립니다.
            time.sleep(3)
            # 브런치의 경우 한 번만에 댓글이 로드되지 않습니다.
            # 한번 더 페이지 이동을 요청합니다. 이러면 댓글창이 뜹니다.
            self.driver.get(target_url)
            # 댓글은 cont_info 라는 이름의 클래스로 표기됩니다. 이걸 모두 불러옵시다.
            replies = self.driver.find_elements_by_class_name("cont_info")
            # 만약 댓글을 하나도 불러오지 못 하는 경우가 발생할 수 있겠죠.
            if len(replies) == 0:
                # 이 경우 다음 게시물로 넘어가버립니다.
                continue

            # 이제 댓글 내용을 분석해서 금지 키워드가 입력되어 있나 확인합니다.
            # 댓글 요소를 하나씩 불러옵니다.
            for i, elm in enumerate(replies):
                # 코드를 짧게 만들기 위해 변수를 만듭니다.
                # 댓글을 검사하고, 금지 키워드가 댓글에 입력되어 있다면 True로 바뀝니다.
                target_detected = False
                # 금지 키워드를 하나씩 불러옵니다.
                for keyword in self.kill_keywords:
                    # 키워드가 댓글 안에 있는지 검사합니다.
                    if keyword in elm.text:
                        # 댓글에서 키워드가 발견된다면 target_detected를 True로 바꾸고 루프를 종료합니다.
                        target_detected = True
                        break
                # 댓글에서 키워드가 발견된 경우 아래 코드가 실행됩니다.
                if target_detected:
                    # 발견한 악플 개수를 1개 추가합니다.
                    self.count += 1
                    # 현재 시각과 댓글의 내용을 정리합니다.
                    line = time.ctime() + "\n" + elm.text
                    # 그걸 화면에 출력합니다.
                    print(line)
                    # 브런치의 경우 댓글이 화면에 표시가 안 되는 경우가 있습니다. 요소는 검색 되면서 말이죠.
                    # 댓글을 클릭해야지 삭제버튼이 활성화되므로 일단 클릭에 성공해야 합니다.
                    # 댓글이 클릭 가능한 상태가 될때까지 스크롤을 살살 내려줍니다.
                    for i in range(30):
                        try:
                            # 댓글 클릭을 시도합니다.
                            elm.click()
                        # 클릭에 실패한 경우
                        except:
                            # 아래 방향 화살표 키보드를 살살 눌러봅니다.
                            for j in range(i):
                                self.driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_DOWN)
                            continue
                        # 클릭에 성공했다면 삭제 버튼이 활성화됩니다.
                        del_button = elm.find_elements_by_tag_name("button")[-1]
                        # 삭제 버튼이 발견되었는지 검사합니다.
                        # 발견되지 않았다면 일단 다음 댓글로 넘어갑니다.
                        if "삭제" in del_button.text:
                            # 삭제버튼을 클릭합니다.
                            del_button.click()
                            # 삭제버튼을 클릭하면 경고창이 팝업으로 뜹니다. 확인 버튼을 눌러줍시다.
                            # 셀레늄이 이렇게 똑똑합니다.
                            self.driver.switch_to.alert.accept()
                            # 삭제에 성공했으므로 로그를 파일에 기록합니다.
                            log.write(line)
                            # 삭제 성공 여부를 화면에 출력합니다.
                            print("Deleted Success")
                            # 일단 댓글 하나를 삭제했으므로 이런저런 태그들이 흐트러집니다.
                            # 다시 보호 대상 게시물의 댓글창으로 이동해 작업을 반복합니다.
                            self.driver.get(elm)
                            break
        # 작업이 끝났으니 로그 파일을 저장합니다.
        log.close()
