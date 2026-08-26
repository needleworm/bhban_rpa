"""
Author : Byunghyun Ban
Book : 6개월 치 업무를 하루 만에 끝내는 업무 자동화
"""
import time

try:
    import pyperclip
    import pyautogui
except ModuleNotFoundError:
    import pip

    pip.main(['install', 'pyautogui'])
    pip.main(['install', 'pillow'])
    pip.main(['install', 'pyperclip'])
    pip.main(['install', 'opencv-python'])
    try:
        import pyperclip
        import pyautogui
    except ModuleNotFoundError:
        time.sleep(2)
        import pyperclip
        import pyautogui

# 라이브러리에서 사용할 키맵을 미리 세팅합니다.
KEYMAP = {
    # 제어 키
    "esc": "esc", "window": "win",
    "command": "command", "option": "option",
    "control": "ctrl", "alt": "alt", "kor_eng": "hanguel",
    "print_screen": "prtsc", "scroll_lock": "scrolllock",
    "pause_break": "pause", "vol_up": "volumeup",
    "vol_down": "volumedown", "vol_mute": "volumemute",
    "hanja": "hanja",

    # 기능 키
    "f1": "f1", "f2": "f2", "f3": "f3", "f4": "f4",
    "f5": "f5", "f6": "f6", "f7": "f7", "f8": "f8",
    "f9": "f9", "f10": "f10", "f11": "f11", "f12": "f12",

    # 화살표 키
    "left_arrow": "left", "right_arrow": "right",
    "up_arrow": "up", "down_arrow": "down",

    # 탐색 키
    "insert": "insert", "home": "home", "page_up": "pageup",
    "delete": "delete", "end": "end", "page_down": "pgdn",

    # 입력 키 (편집)
    "backspace": "backspace", "enter": "enter", "shift": "shift",
    "tab": "tab", "caps_lock": "capslock", "spacebar": "space",

    # 입력 키 (숫자)
    "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
    "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",

    # 입력 키 (알파벳)
    "a": "a", "b": "b", "c": "c", "d": "d", "e": "e",
    "f": "f", "g": "g", "h": "h", "i": "i", "j": "j",
    "k": "k", "l": "l", "m": "m", "n": "n", "o": "o",
    "p": "p", "q": "q", "r": "r", "s": "s", "t": "t",
    "u": "u", "v": "v", "w": "w", "x": "x", "y": "y", "z": "z",

    # 입력 키 (특수문자)
    ";": ";", "=": "=", ",": ",", "-": "-", ".": ".",
    "/": "/", "`": "`", "[": "[", "\\": "\\", "]": "]",
    "'": "'",

    # 넘패드
    "num_lock": "numlock", "numpad_/": "", "numpad_*": "multiply",
    "numpad_-": "-", "numpad_+": "+", "numpad_.": ".",
    "numpad_7": "num7", "numpad_8": "num8", "numpad_9": "num9",
    "numpad_4": "num4", "numpad_5": "num5", "numpad_6": "num6",
    "numpad_1": "num1", "numpad_2": "num2", "numpad_3": "num3",
    "numpad_0": "num0",
}

# 대문자 특수문자를 위한 딕셔너리입니다.
UPPER_SPECIAL = {
    "!": 1, "@": 2, "#": 3, "$": 4, "%": 5, "^": 6,
    "&": 7, "*": 8, "(": 9, ")": 0, "_": "-", "~": '`', "|": '\\',
    "{": "[", "}": "]", ":": ";", '"': "'", "?": "/", "<": ",", ">": "."
}


# 마우스를 특정위치로 이동시키는 함수
def move_mouse(location):
    # location 을 입력받아 이 위치로 마우스를 이동시킵니다.
    pyautogui.moveTo(location)


# 마우스의 현재 좌표를 구하는 함수
def get_mouse_position():
    # 마우스 커서의 현재 위치를 출력합니다.
    # 매크로를 제작하는 과정에서, 콘솔에서 불러와서 쓰면 유용합니다.
    return tuple(pyautogui.position())


# 지정된 위치로 마우스 커서를 이동하고 왼쪽 버튼을 클릭하는 함수
def click(location):
    # 마우스를 클릭합니다..
    pyautogui.click(location)


# 지정된 위치로 마우스 커서를 이동하고 오른쪽 버튼을 클릭하는 함수
def right_click(location):
    pyautogui.click(location, button='right')


# 더블클릭
def double_click(location):
    pyautogui.click(location, button='left', clicks=2, interval=0.25)


# 키를 한 번 눌렀다가 떼는 함수입니다.
def key_press_once(key):
    key_on(key)
    key_off(key)


# 글자 입력 (클립보드에 복사 후 붙여넣기)
# 한글일 경우에만 사용하세요. 한글은 형태소 분해가 곤란하여 그렇습니다.
def type_in(string):
    # 클립보드에 스트링을 집어넣습니다.
    pyperclip.copy(string)
    # Ctrl v로 붙여넣기 합니다.
    ctrl_v()


# 영어, 숫자, 특수문자로 된 스트링을 바로 입력하는 함수입니다.
def typing(string):
    pyautogui.write(string)


# 키를 계속 누르고 있도록 하는 함수입니다.
def key_on(key):
    # 전역변수 KEYMAP에 접근할 것임을 선언합니다.
    global KEYMAP
    # 입력받은 값을 소문자로 변환합니다.
    key = str(key)
    if key.isupper:
        key = key.lower()
    try:
        # 키맵에서 키 코드를 뽑아옵니다.
        key_code = KEYMAP[key.lower()]
        pyautogui.keyDown(key_code)
    except KeyError:
        # 키맵에 세팅되지 않은 키를 요청했습니다. 에러메시지를 출력합니다.
        print(key + " is not an available key input.")
        # 프로그램을 종료합니다.
        exit(1)


# 눌렀던 키를 떼게 하는 함수입니다.
def key_off(key):
    # 전역변수 KEYMAP에 접근할 것임을 선언합니다.
    global KEYMAP
    # 입력받은 값을 소문자로 변환합니다.
    key = str(key)
    if key.isupper:
        key = key.lower()
    try:
        # 키맵에서 키 코드를 뽑아옵니다.
        key_code = KEYMAP[key.lower()]
        pyautogui.keyUp(key_code)
    except KeyError:
        # 키맵에 세팅되지 않은 키를 요청했습니다. 에러메시지를 출력합니다.
        print(key + " is not an available key input.")
        # 프로그램을 종료합니다.
        exit(1)


# 마우스를 현재 자리에서 왼쪽 버튼을 클릭하는 함수
def l_click():
    pyautogui.click()


# 마우스를 현재 자리에서 오른쪽 버튼을 클릭하는 함수
def r_click():
    pyautogui.click(button='right')


# 마우스 스크롤을 올리는 함수
def mouse_upscroll(number=1000):
    x, y = get_mouse_position()
    # 몇 칸이나 올릴지 number에 입력받습니다.
    pyautogui.scroll(number, x=x, y=y)


# 마우스 스크롤을 내리는 함수
def mouse_downscroll(number=1000):
    x, y = get_mouse_position()
    # 몇 칸이나 올릴지 number에 입력받습니다.
    pyautogui.scroll(-1 * number, x=x, y=y)


# 드래그드롭 함수
def drag_drop(frm, to):
    # 좌표값을 입력받습니다.
    x, y = to
    # 클릭 시작지점으로 커서를 옮깁니다.
    move_mouse(frm)
    # 드래그를 수행합니다
    pyautogui.dragTo(x, y, 0.5, button='left')


# 특정 좌표의 색상을 16진수로 읽어 오는 함수입니다.
def get_color(location):
    # 좌표를 구합니다.
    x, y = location
    # RGB 픽셀값을 구합니다.
    try:
        pixel = pyautogui.pixel(x, y)
    except OSError:
        print("OS Error 발생. 다시 시도합니다.")
        return get_color(location)
    return '0x%02x%02x%02x' % pixel


# Ctrl C (복사)
def ctrl_c():
    # Ctrl을 누릅니다.
    key_on("control")
    # c도 누릅니다.
    key_on("c")
    # 두 키를 모두 뗍니다.
    key_off("control")
    key_off("c")


# Ctrl V (붙여넣기)
def ctrl_v():
    # Ctrl을 누릅니다.
    key_on("control")
    # v도 누릅니다.
    key_on("v")
    # 두 키를 모두 뗍니다.
    key_off("control")
    key_off("v")


# Ctrl A (모두 선택)
def ctrl_a():
    # Ctrl을 누릅니다.
    key_on("control")
    # a도 누릅니다.
    key_on("a")
    # 두 키를 모두 뗍니다.
    key_off("control")
    key_off("a")


# Ctrl F (찾기)
def ctrl_f():
    # Ctrl을 누릅니다.
    key_on("control")
    # a도 누릅니다.
    key_on("f")
    # 두 키를 모두 뗍니다.
    key_off("control")
    key_off("f")


# Alt F4 (종료)
def alt_f4():
    # Alt를 누릅니다.
    key_on("alt")
    # F4도 누릅니다.
    key_on("f4")
    # 두 키를 모두 뗍니다.
    key_off("alt")
    key_off("f4")


# Alt Tab (화면 전환)
def alt_tab():
    # Alt를 누릅니다.
    key_on("alt")
    # F4도 누릅니다.
    key_on("tab")
    # 두 키를 모두 뗍니다.
    key_off("alt")
    key_off("tab")


# 이미지를 입력받아 화면에서 위치를 탐색합니다.
# 화면에서 이미지가 발견되지 않을 경우 False를 리턴합니다.
def find_on_screen(filename, confidence=0.7):
    a = pyautogui.locateCenterOnScreen(filename, confidence=confidence)
    if not a:
        return False
    else:
        return a[0], a[1]
