from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import win32api, win32con, win32gui
import os


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
        self.options.add_argument("window-size=848x1500")
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

    # 마스킹을  
    def save_screenshot_withhout_masking(self, querry, out_dir, key1, key2):
        url = make_url(querry)
        self.driver.get(url)
        if not self.unlock_masking(key1, key2):
            return False
        redbox_based_awake()
        self.driver.save_screenshot(out_dir + "/"+querry + ".png")
        return True

    def unlock_masking(self, key1, key2):
        button_location = (650, 170)
        time.sleep(3)
        key1_location = (185, 235)
        key2_location = (185, 263)
        popup_ok_location = (210, 310)

        click(button_location)
        redbox_based_sleep()
        click(key1_location)
        type_in(key1)
        click(key2_location)
        type_in(key2)
        time.sleep(0.1)
        click(popup_ok_location)
        if kill_error_page():
            return False
        return True


def click(location):
    x, y = location
    win32api.SetCursorPos(location)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def type_in(string):
    command = 'echo ' + string.strip() + '| clip'
    os.system(command)
    win32api.keybd_event(0x11, 0, 0x00, 0)
    win32api.keybd_event(0x56, 0, 0x00, 0)
    win32api.keybd_event(0x11, 0, 0x02, 0)
    win32api.keybd_event(0x56, 0, 0x02, 0)


def get_color(location):
    x, y = location
    return hex(win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), x, y))


def redbox_based_sleep():
    redbox_location = (385, 123)
    while get_color(redbox_location) != "0x392ddd":
        time.sleep(0.01)


def redbox_based_awake():
    redbox_location = (385, 123)
    while get_color(redbox_location) == "0x392ddd":
        time.sleep(0.1)


def kill_error_page():
    error_button = (390, 170)
    quit_button = (400, 10)
    time.sleep(1)
    if get_color(error_button) != "0xffffff":
        click(quit_button)
        return True
    return False
