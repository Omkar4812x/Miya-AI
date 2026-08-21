import pyautogui
import time

# ===================== SETTINGS =====================
ACTION_DELAY = 0.1   # Small delay between actions for stability


# ===================== TAB MANAGEMENT =====================
def open_new_tab():
    pyautogui.hotkey("ctrl", "t")
    time.sleep(ACTION_DELAY)


def close_tab():
    pyautogui.hotkey("ctrl", "w")
    time.sleep(ACTION_DELAY)


def switch_to_next_tab():
    pyautogui.hotkey("ctrl", "tab")
    time.sleep(ACTION_DELAY)


def switch_to_previous_tab():
    pyautogui.hotkey("ctrl", "shift", "tab")
    time.sleep(ACTION_DELAY)


# ===================== PAGE CONTROL =====================
def refresh_page():
    pyautogui.hotkey("ctrl", "r")
    time.sleep(ACTION_DELAY)


def go_back():
    pyautogui.hotkey("alt", "left")
    time.sleep(ACTION_DELAY)


def go_forward():
    pyautogui.hotkey("alt", "right")
    time.sleep(ACTION_DELAY)


def open_history():
    pyautogui.hotkey("ctrl", "h")
    time.sleep(ACTION_DELAY)


# ===================== ZOOM =====================
def zoom_in():
    pyautogui.hotkey("ctrl", "+")
    time.sleep(ACTION_DELAY)


def zoom_out():
    pyautogui.hotkey("ctrl", "-")
    time.sleep(ACTION_DELAY)


def reset_zoom():
    pyautogui.hotkey("ctrl", "0")
    time.sleep(ACTION_DELAY)


# ===================== WINDOW / TOOLS =====================
def open_dev_tools():
    pyautogui.hotkey("ctrl", "shift", "i")
    time.sleep(ACTION_DELAY)


def toggle_full_screen():
    pyautogui.press("f11")
    time.sleep(ACTION_DELAY)


def open_private_window():
    pyautogui.hotkey("ctrl", "shift", "n")
    time.sleep(ACTION_DELAY)


def open_start_menu():
    pyautogui.press("win")
    time.sleep(ACTION_DELAY)


# ===================== SAFETY TEST =====================
if __name__ == "__main__":
    print("Browser control test starts in 3 seconds...")
    time.sleep(3)
    open_new_tab()
    open_history()
    close_tab()
