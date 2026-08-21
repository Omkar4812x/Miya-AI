# MIT License
# Copyright (c) 2024 Geremy

import os
import time
import socket
import threading
import datetime
import subprocess
import webbrowser

import requests
import pyautogui
import pywhatkit
import pygame
import gtts
import speech_recognition as sr
import ollama

from browser import *
from scrole import *

# ===================== INIT =====================
pygame.init()

AUDIO_DIR = os.path.join(os.getcwd(), "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

audio_counter = 1

DEFAULT_SYSTEM_PROMPT = (
    "You are MIA, a friendly desktop AI assistant created by Geremy. "
    "Always answer in clear, simple English. "
    "Keep responses short (2–4 sentences max). "
    "Do NOT over-explain unless the user asks. "
    "Never end responses with unfinished words."
)

# ===================== AI (OLLAMA) =====================
def create_completion_ollama(prompt):
    try:
        stream = ollama.chat(
            model="phi3:mini",
            messages=[
                {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )

        response_text = ""
        for chunk in stream:
            response_text += chunk["message"]["content"]
            print(chunk["message"]["content"], end="", flush=True)

        print()
        return response_text

    except Exception as e:
        print("Ollama error:", e)
        return "Sorry, I had a problem generating a response."

# ===================== SPEECH =====================
def speak(text):
    global audio_counter, IS_SPEAKING
    IS_SPEAKING = True

    try:
        filename = os.path.join(AUDIO_DIR, f"audio_{audio_counter}.mp3")
        audio_counter += 1

        tts = gtts.gTTS(text=text, lang="en")
        tts.save(filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)

        pygame.mixer.music.unload()
        time.sleep(0.2)
        os.remove(filename)

    finally:
        IS_SPEAKING = False



def listen():
    global IS_SPEAKING

    if IS_SPEAKING:
        return ""

    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.8)
            audio = r.listen(source)

        text = r.recognize_google(audio, language="en-US")
        print("You said:", text)
        return text.lower()

    except Exception:
        return ""



# ===================== TOOLS =====================
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unable to get IP address"

def take_screenshot():
    img = pyautogui.screenshot()
    path = os.path.join(os.getcwd(), "screenshot.png")
    img.save(path)
    speak("Screenshot saved.")

def lock_screen():
    os.system("rundll32.exe user32.dll,LockWorkStation")
    speak("Screen locked.")

def play_song(song):
    speak(f"Playing {song}")
    pywhatkit.playonyt(song)

# ===================== MAIN ASSISTANT =====================
def start_assistant():
    speak("Mia is online. How can I help you?")

    while True:
        command = listen()
        if not command:
            continue

        if "shutdown" in command or "exit" in command:
            speak("Goodbye.")
            break

        elif "time" in command:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {now}")

        elif "play" in command:
            play_song(command.replace("play", "").strip())

        elif "open" in command:
            app = command.replace("open", "").strip()
            os.system(f"start {app}")
            speak(f"Opening {app}")

        elif "ip address" in command:
            speak(f"Your IP address is {get_ip()}")

        elif "screenshot" in command:
            take_screenshot()

        elif "lock screen" in command:
            lock_screen()

        elif "new tab" in command:
            pyautogui.hotkey("ctrl", "t")

        elif "close tab" in command:
            pyautogui.hotkey("ctrl", "w")

        elif "scroll up" in command:
            scroll_up()

        elif "scroll down" in command:
            scroll_down()

        elif "top" in command:
            scroll_to_top()

        elif "bottom" in command:
            scroll_to_bottom()

        else:
            print("Thinking...")
            reply = create_completion_ollama(command)
            speak(reply)

# ===================== RUN =====================
if __name__ == "__main__":
    assistant_thread = threading.Thread(target=start_assistant)
    assistant_thread.start()
