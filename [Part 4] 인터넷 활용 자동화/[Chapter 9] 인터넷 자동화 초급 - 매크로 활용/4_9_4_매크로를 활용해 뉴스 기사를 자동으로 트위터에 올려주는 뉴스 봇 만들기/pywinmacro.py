#-*-coding:euc-kr
"""
Author : Byunghyun Ban
Book : 6개월 치 업무를 하루 만에 끝내는 업무 자동화
"""

import win32api
import win32con
import win32gui
import pyperclip

# 라이브러리에서 사용할 키맵을 미리 세팅합니다.
KEYMAP = {
    # 제어 키
    "esc": 0x1B,  "window": 0x5B,
    "control": 0x11,    "alt": 0x12,  "kor_eng": 0x15,
    "print_screen": 0x2C,    "scroll_lock": 0x91,   "pause_break": 0x13,

    # 기능 키
    "f1": 0x70,    "f2": 0x71,    "f3": 0x72,    "f4": 0x73,
    "f5": 0x74,    "f6": 0x75,    "f7": 0x76,    "f8": 0x77,
    "f9": 0x78,    "f10": 0x79,    "f11": 0x7A,    "f12": 0x7B,

    # 화살표 키
    "left_arrow": 0x25,    "right_arrow": 0x27,
    "up_arrow": 0x26,    "down_arrow": 0x28,

    # 탐색 키
    "insert": 0x2D,    "home": 0x24,    "page_up": 0x21,
    "delete": 0x2E,    "end": 0x23,     "page_down": 0x22,

    # 입력 키 (편집)
    "backspace": 0x08,  "enter": 0x0D,  "shift": 0x10,
    "tab": 0x09,    "caps_lock": 0x14,  "spacebar": 0x20,

    # 입력 키 (숫자)
    "0": 0x30,    "1": 0x31,    "2": 0x32,    "3": 0x33,    "4": 0x34,
    "5": 0x35,    "6": 0x36,    "7": 0x37,    "8": 0x38,    "9": 0x39,

    # 입력 키 (알파벳)
    "a": 0x41,    "b": 0x42,    "c": 0x43,    "d": 0x44,    "e": 0x45,
    "f": 0x46,    "g": 0x47,    "h": 0x48,    "i": 0x49,    "j": 0x4A,
    "k": 0x4B,    "l": 0x4C,    "m": 0x4D,    "n": 0x4E,    "o": 0x4F,
    "p": 0x50,    "q": 0x51,    "r": 0x52,    "s": 0x53,    "t": 0x54,
    "u": 0x55,    "v": 0x56,    "w": 0x57,    "x": 0x58,    "y": 0x59,  "z": 0x5A,

    # 입력 키 (특수문자)
    ";": 0xBA,    "=": 0xBB,    ",": 0xBC,    "-": 0xBD,    ".": 0xBE,
    "/": 0xBF,    "`": 0xC0,    "[": 0xDB,    "\\": 0xDC,    "]": 0xDD,
    "'": 0xDE,

    # 넘패드
    "num_lock": 0x90, "numpad_/": 0x6F, "numpad_*": 0x6A,
    "numpad_-": 0x6D, "numpad_+": 0x6B, "numpad_.": 0x6E,
    "numpad_7": 0x67, "numpad_8": 0x68, "numpad_9": 0x69,
    "numpad_4": 0x64, "numpad_5": 0x65, "numpad_6": 0x66,
    "numpad_1": 0x61, "numpad_2": 0x62, "numpad_3": 0x63,
    "numpad_0": 0x60,
}


# 대문자 특수문자를 위한 딕셔너리입니다.
UPPER_SPECIAL = {
    "!": 1,    "@": 2,    "#": 3,    "$": 4,    "%": 5,    "^": 6,
    "&": 7,    "*": 8,    "(": 9,    ")": 0,    "_": "-",   "~": '`',    "|": '\\',
    "{": "[",   "}": "]",    ":": ";",    '"': "'", "?": "/", "<": ",", ">": "."
}


# 마우스를 특정위치로 이동시키는 함수
def move_mouse(location):
    # location 을 입력받아 이 위치로 마우스를 이동시킵니다.
    win32api.SetCursorPos(location)


# 마우스의 현재 좌표를 구하는 함수
def get_mouse_position():
    # 마우스 커서의 현재 위치를 출력합니다.
    # 매크로를 제작하는 과정에서, 콘솔에서 불러와서 쓰면 유용합니다.
    return win32gui.GetCursorPos()


# 지정된 위치로 마우스 커서를 이동하고 왼쪽 버튼을 클릭하는 함수
def click(location):
    # 마우스를 이동시킵니다.
    move_mouse(location)
    # 왼쪽 버튼을 클릭합니다.
    l_click()


# 지정된 위치로 마우스 커서를 이동하고 오른쪽 버튼을 클릭하는 함수
def right_click(location):
    # 마우스를 이동시킵니다.
    move_mouse(location)
    # 왼쪽 버튼을 클릭합니다.
    r_click()


# 더블클릭
def double_click(location):
    # 마우스를 이동시킵니다.
    move_mouse(location)
    # 왼쪽 버튼을 클릭하는 함수를 두 번 호출합니다.
    l_click()
    l_click()


# 키를 한 번 눌렀다가 떼는 함수입니다.
def key_press_once(key):
    # 키를 누릅니다.
    key_on(key)
    # 키를 뗍니다.
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
    for el in string:
        if el.isupper():
            key_on("shift")
            key_press_once(el.lower())
            key_off("shift")
        elif el in UPPER_SPECIAL:
            key_on("shift")
            key_press_once(UPPER_SPECIAL[el])
            key_off("shift")
        else:
            key_press_once(el)


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
        win32api.keybd_event(key_code, 0, 0x00, 0)
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
        win32api.keybd_event(key_code, 0, 0x02, 0)
    except KeyError:
        # 키맵에 세팅되지 않은 키를 요청했습니다. 에러메시지를 출력합니다.
        print(key + " is not an available key input.")
        # 프로그램을 종료합니다.
        exit(1)


# 마우스를 현재 자리에서 왼쪽 버튼을 클릭하는 함수
def l_click():
    # 마우스 왼쪽 버튼을 누릅니다.
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # 마우스 왼쪽 버튼을 뗍니다.
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# 마우스를 현재 자리에서 오른쪽 버튼을 클릭하는 함수
def r_click():
    # 마우스 오른쪽 버튼을 누릅니다.
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    # 마우스 오른쪽 버튼을 뗍니다.
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


# 마우스 스크롤을 올리는 함수
def mouse_upscroll(number=1000):
    x, y = get_mouse_position()
    # 몇 칸이나 올릴지 number에 입력받습니다.
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, number, 0)

# 마우스 스크롤을 내리는 함수
def mouse_downscroll(number=1000):
    x, y = get_mouse_position()
    # 몇 칸이나 내릴지 number에 입력받습니다. 기본은 한 칸 내립니다.
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, -1*number, 0)


# 드래그드롭 함수
def drag_drop(frm, to):
    # 좌표값을 입력받습니다.
    x1, y1 = frm
    x2, y2 = to
    # 클릭 시작지점으로 커서를 옮깁니다.
    move_mouse(frm)
    # 왼쪽 버튼을 클릭합니다.
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # 클릭을 유지한 채로 마우스 위치를 이동시킵니다.
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x2-x1, y2-y1, 0, 0)
    # 마우스 버튼을 뗍니다.
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# 특정 좌표의 색상을 16진수로 읽어 오는 함수입니다.
def get_color(location):
    # 좌표를 구합니다.
    x, y = location
    # win32gui모듈로 색상값을 따 오고, 16진수로 변환하여 리턴합니다.
    return hex(win32gui.GetPixel(win32gui.GetDC(win32gui.GetActiveWindow()), x, y))


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

