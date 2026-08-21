import subprocess
import time
import os

# ===================== GENERIC APP LAUNCHER =====================
def open_app(path, wait=2):
    """
    Safely open any application by path
    """
    try:
        subprocess.Popen(path, shell=True)
        time.sleep(wait)
        return True
    except Exception as e:
        print(f"Failed to open app: {e}")
        return False


# ===================== SPECIFIC APPS =====================
def open_steam():
    paths = [
        r"C:\Program Files (x86)\Steam\steam.exe",
        r"C:\Program Files\Steam\steam.exe"
    ]

    for path in paths:
        if os.path.exists(path):
            open_app(path)
            return

    print("Steam not found")


def open_calculator():
    open_app("calc")


def open_notepad():
    open_app("notepad")


def open_cmd():
    open_app("cmd")


def open_chrome():
    open_app("chrome")


def open_edge():
    open_app("msedge")


# ===================== SAFETY TEST =====================
if __name__ == "__main__":
    print("Testing app launcher in 3 seconds...")
    time.sleep(3)
    open_calculator()
