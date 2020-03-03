"""
Author : Byunghyun Ban
Book : 일반인을 위한 업무 자동화
Last Modification : 2020.02.18.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import win32api, win32con, win32gui
import pyperclip

# querry를 다듬어 URL로 만들어주는 함수입니다.
# 반드시 필요한 것은 아니지만,
# 코드를 좀 더 간결하고 가독성 좋게 만들기 위해 함수를 사용합니다.
def make_url(querry):
    readurl = 'http://service.epost.go.kr/trace.RetrieveRegiPrclDeliv.postal?sid1='
    return readurl + querry


# 클래스를 선언합니다. 필자는 사실 객체지향을 선호합니다.
# 객체지향이 무슨 뜻인지는 따로 공부해 보시기 바랍니다.
class PostCrawler:
    def __init__(self):
        # 셀레늄 웹드라이버에 입력할 옵션을 지정합니다.
        self.options = Options()
        # 옵션에 해상도를 입력합니다. 해상도는 848x1500이며, 모니터를 90도 회전시켜 사용하면 적절합니다.
        self.options.add_argument("--window-size=848,1500")
        # 옵션을 입력해서 크롬 웹드라이버를 불러옵니다.
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)

    # 크롤러를 종료하는 함수입니다.
    # 굳이 한줄짜리 코드를 함수로 만든 데에는 여러 이유가 있습니다만,
    # 쉽게 설명하자면 클래스 외부에서 클래스 내부 자료에 너무 깊게 관여하는 상황을 원하지 않기 때문입니다.
    def kill(self):
        self.driver.quit()

    # 쿼리를 입력하면 등기발송내역 스크린샷을 찍는 함수입니다.
    def save_screenshot(self, querry, out_dir):
        # querry를 입력받아 URL로 만들어 줍니다.
        url = make_url(querry)
        # rul을 주소창에 입력하고, 이동하는 기능이라고 생각하시면 됩니다.
        self.driver.get(url)
        # 스크린샷을 찍어서 저장합니다.
        self.driver.save_screenshot(out_dir + "/"+querry + ".png")

    # 마스킹을 해제하면서 스크린샷을 찍는 함수입니다.
    # 쿼리, 스크린샷을 저장할 폴더, 그리고 두 개의 키를 입력받습니다.
    # 키는 각각 발신인과 수신인의 이름 두 번째 글자입니다.
    def save_screenshot_withhout_masking(self, querry, out_dir, key1, key2):
        # querry를 입력받아 URL로 만들어 줍니다.
        url = make_url(querry)
        # rul을 주소창에 입력하고, 이동하는 기능이라고 생각하시면 됩니다.
        self.driver.get(url)
        # 로딩이 느릴 수 있으므로 5초정도 기다립니다.
        time.sleep(5)
        # 마스킹 해제를 시도합니다.
        # 일단 코딩을 할 때에는 unlock_masking() 함수가 존재한다고 가정하고 코딩합니다.
        # 이 함수는 마스킹을 해제해 주면서, 성공하면 True를, 실패하면 False를 리턴해 주면 좋을 것 같네요.
        # 아래 if문의 조건은 not이 붙어있으므로 마스킹 해제에 실패할 경우 True가 됩니다.
        if not self.unlock_masking(key1, key2):
            # 마스킹해제에 실패할 경우, False를 리턴하고 종료합니다.
            return False
        # 마스킹 해제에 성공한 경우 마스킹이 해제된 페이지가 로딩될때까지 기다립니다.
        # 로딩이 완료되어 팝업창의 빨간 색상이 사라질때까지 기다려주는 redbox_based_awake()함수가 있다고 가정하고 코드를 짭니다.
        redbox_based_awake()
        # 페이지 로딩이 완료되었다면 스크린샷을 저장합니다.
        self.driver.save_screenshot(out_dir + "/"+querry + ".png")
        # 스크린샷 저장에 성공하였으므로 True를 리턴합니다.
        return True

    # save_screenshot_withhout_masking() 함수에서 사용한 함수입니다.
    # 마스킹을 해제해 주는 기능을 수행해야 합니다.
    # 성공하면 True를, 실패하면 False를 리턴합니다.
    def unlock_masking(self, key1, key2):
        # 마스킹 해제조회 버튼의 좌표를 입력합니다.
        unmaking_button_location = (650, 170)
        # 마스킹 해제를 위한 정보를 입력해야합니다. 키1과 키2의 좌표를 입력합니다.
        key1_location = (185, 235)
        key2_location = (185, 263)
        # 팝업창의 확인 버튼 좌표를 입력합니다.
        popup_ok_location = (210, 310)

        # 마스킹 해제 버튼을 클릭합니다.
        # 좌표를 입력하면 클릭해 주는 click() 함수가 있다고 가정하고 코드를 짭니다.
        click(unmaking_button_location)
        # 로딩이 끝나기를 기다립니다.
        redbox_based_sleep()
        # 키1을 입력하기 위해 클릭합니다.
        click(key1_location)
        # 키1의 내용물을 입력합니다.
        # 글자를 입력하면 화면에 타이핑해주는 type_in() 함수가 있다고 가정하고 코드를 짭니다.
        type_in(key1.strip())
        # 같은 방법으로 키2를 입력합니다.
        click(key2_location)
        type_in(key2.strip())
        # 로딩이 되기까지 잠시만 대기합니다. 오래된 컴퓨터에서는 여기서 대기가 필요하더군요.
        time.sleep(0.1)
        # 팝업창의 확인버튼을 클릭합니다.
        click(popup_ok_location)
        # 로딩이 오래 걸릴 수 있으니 1초를 기다립니다.
        time.sleep(1)
        # 마스킹 해제가 잘 됐는지 검증할 필요가 있습니다.
        # 마스킹 해제에 문제가 발생해 에러페이지가 발생했다면
        # True를 리턴하고, 문제가 없었다면 False를 리턴하는 kill_error_page() 함수가 있다고 가정하고 코딩합니다.
        if kill_error_page():
            # 에러가 발생하면 False를 리턴합니다.
            return False
        # 에러 없이 무사히 마스킹이 해제되었다면 True를 리턴합니다.
        return True


# 좌표를 입력하면 클릭을 해 주는 함수입니다.
def click(location):
    # x좌표와 y좌표를 입력받습니다.
    x, y = location
    # win32api를 활용합니다. 윈도우와 파이썬이 소통하기 위한 모듈이라 생각하변 됩니다.
    # 파이썬을 사용해 윈도우를 제어할 수 있습니다.
    # SetCursorPos() 함수는 좌표를 입력받아 마우스의 위치를 그 좌표로 입력합니다.
    win32api.SetCursorPos(location)
    # mouse_event()함수는 마우스를 조작합니다.
    # 마우스 왼쪽 버튼을 누르고
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    # 마우스 왼쪽 버튼을 뗍니다.
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


# 스트링을 입력받아 시스템에 입력하는 함수입니다.
# 윈도우 시스템에서 한글을 직접 타이핑하는일은 매우 고되고 귀찮은 일이니 우회합시다.
# 입력하고 싶은 스트링을 클립보드에 집어넣고
# Ctrl + V 를 입력해 붙여넣기 하겠습니다.
def type_in(string):
    # pyperclip 모듈의 copy() 명령어를 사용하면 클립보드에 스트링을 입력할 수 있습니다.
    pyperclip.copy(string)
    # Ctrl 키와 V 키를 누릅니다.
    win32api.keybd_event(0x11, 0, 0x00, 0)
    win32api.keybd_event(0x56, 0, 0x00, 0)
    # Ctrl 키와 V 키를 뗍니다.
    win32api.keybd_event(0x11, 0, 0x02, 0)
    win32api.keybd_event(0x56, 0, 0x02, 0)


# 로딩이 완료될때까지 기다리는 함수입니다.
# 팝업창이 뜨면서 화면에 빨간 박스가 표기될때까지 기다립니다.
def redbox_based_sleep():
    # 빨간색 박스의 좌표를 입력합니다.
    redbox_location = (385, 123)
    # 특정 좌표의 색상을 입력받는 get_color() 함수가 있다고 가정하고 코딩합니다.
    # 해당 지점의 색상이 "0x392ddd"인지 비교합니다. 이 색은 우체국 화면에서 사용하는 붉은색입니다.
    while get_color(redbox_location) != "0x392ddd":
        # 아직 색상이 변하지 않았다면 0.1초를 더 대기합니다.
        # 변했다면 대기를 종료합니다.
        time.sleep(0.1)


# 로딩이 완료될때까지 기다리는 함수입니다.
# 팝업창이 사라지며 빨간색 박스가 화면에서 사라지는 순간을 포착합니다.
def redbox_based_awake():
    # 빨간색 박스의 좌표를 입력합니다.
    redbox_location = (385, 123)
    # 특정 좌표의 색상을 입력받는 get_color() 함수가 있다고 가정하고 코딩합니다.
    # 해당 지점의 색상이 "0x392ddd"인지 비교합니다. 이 색은 우체국 화면에서 사용하는 붉은색입니다.
    while get_color(redbox_location) == "0x392ddd":
        # 아직 색상이 변하지 않았다면 0.1초를 더 대기합니다.
        # 변했다면 대기를 종료합니다.
        time.sleep(0.1)


# 특정 좌표의 색상을 16진수로 출력합니다.
def get_color(location):
    # x, y좌표를 저장합니다.
    x, y = location
    # win32gui에 내장된 GetPixel 모듈을 사용합니다.
    return hex(win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), x, y))


# 에러가 발생하면 그 페이지를 종료하는 함수입니다.
def kill_error_page():
    # 에러 버튼의 좌표를 입력합니다.
    error_button = (390, 170)
    # 종료 버튼의 좌표를 입력합니다.
    quit_button = (400, 10)
    # 에러유무를 판단합니다.
    # 버튼의 색상이 "0xffffff"이면 에러가 발생하지 않은 것입니다.
    # 에러가 발생하면 아래 if문이 실행됩니다.
    if get_color(error_button) != "0xffffff":
        # 에러가 발생했으므로 종료버튼을 클릭합니다.
        click(quit_button)
        # 에러가 발생했다는 의미로 true를 리턴합니다.
        return True
    # 에러가 발생하지 않았다는 의미로 false를 리턴합니다.
    return False
