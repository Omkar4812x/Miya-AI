# =========================================================
# MIA – Voice Assistant (FINAL STABLE VERSION)
# Author: Geremy
# License: MIT
# =========================================================

import os
import time
import datetime
import socket
import threading

import pygame
import gtts
import speech_recognition as sr
import ollama

# =========================================================
# INIT
# =========================================================

pygame.init()
pygame.mixer.init()

AUDIO_DIR = os.path.join(os.getcwd(), "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

audio_counter = 1
IS_SPEAKING = False

MODEL_NAME = "phi3:mini"

SYSTEM_PROMPT = (
    "You are MIA, a friendly desktop AI assistant created by Geremy. "
    "Always respond in simple, clear English. "
    "Keep answers short (2–4 sentences max). "
    "Do not over-explain unless asked."
)

# =========================================================
# AI
# =========================================================

def think(prompt: str) -> str:
    try:
        stream = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )

        response = ""
        for chunk in stream:
            response += chunk["message"]["content"]

        return clean_response(response)

    except Exception as e:
        print("Ollama error:", e)
        return "Sorry, something went wrong."

def clean_response(text: str) -> str:
    text = text.strip()
    for bad in (" and", " or", " but", " so"):
        if text.lower().endswith(bad):
            text = text[: -len(bad)]
    return text

# =========================================================
# SPEECH OUTPUT (TTS)
# =========================================================

def speak(text: str):
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

    except Exception as e:
        print("TTS error:", e)

    finally:
        IS_SPEAKING = False

# =========================================================
# LISTEN (VOICE → TEXT, SAFE)
# =========================================================

def listen() -> str:
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

    except Exception as e:
        print("Voice unavailable, switching to text:", e)
        return input("Type command: ").strip().lower()

# =========================================================
# UTILITIES
# =========================================================

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unable to get IP address"

# =========================================================
# MAIN LOOP
# =========================================================

def start_assistant():
    speak("MIA is online. How can I help you?")

    while True:
        command = listen()

        if not command:
            continue

        # EXIT
        if command in ("exit", "shutdown", "quit", "stop"):
            speak("Goodbye.")
            break

        # BASIC COMMANDS
        elif "time" in command:
            speak(datetime.datetime.now().strftime("The time is %H:%M"))

        elif "ip" in command:
            speak(f"Your IP address is {get_ip()}")

        elif "thank" in command:
            speak("You're welcome.")

        # AI RESPONSE
        else:
            print("Thinking...")
            response = think(command)
            speak(response)

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    start_assistant()
