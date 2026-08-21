import pyautogui
import time

# ===================== SETTINGS =====================
SCROLL_DELAY = 0.03     # Delay between scroll steps
SCROLL_STEPS = 8        # Default number of scroll actions


# ===================== BASIC SCROLL =====================
def scroll_up(steps=SCROLL_STEPS):
    """Scroll up smoothly"""
    for _ in range(steps):
        pyautogui.scroll(120)
        time.sleep(SCROLL_DELAY)


def scroll_down(steps=SCROLL_STEPS):
    """Scroll down smoothly"""
    for _ in range(steps):
        pyautogui.scroll(-120)
        time.sleep(SCROLL_DELAY)


# ===================== FAST SCROLL =====================
def fast_scroll_up():
    """Fast jump up"""
    pyautogui.keyDown("ctrl")
    pyautogui.scroll(1000)
    pyautogui.keyUp("ctrl")


def fast_scroll_down():
    """Fast jump down"""
    pyautogui.keyDown("ctrl")
    pyautogui.scroll(-1000)
    pyautogui.keyUp("ctrl")


# ===================== PAGE NAVIGATION =====================
def scroll_to_top():
    """Go to top of page"""
    pyautogui.hotkey("home")


def scroll_to_bottom():
    """Go to bottom of page"""
    pyautogui.hotkey("end")


# ===================== SAFETY TEST =====================
if __name__ == "__main__":
    print("Testing scroll module in 3 seconds...")
    time.sleep(3)
    scroll_down()
    scroll_up()
    scroll_to_bottom()
    scroll_to_top()
