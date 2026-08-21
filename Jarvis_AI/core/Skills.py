
import os
import subprocess
import webbrowser
import sys
import psutil

def open_app(app_name):
    """Open common applications or URLs."""
    app_name = app_name.lower().strip()
    
    # Common App Mapping
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "spotify": "spotify",
        "cmd": "cmd.exe",
        "settings": "start ms-settings:",
        "explorer": "explorer.exe",
        "task manager": "taskmgr.exe"
    }

    if app_name in apps:
        target = apps[app_name]
        try:
            if target.startswith("http"):
                webbrowser.open(target)
                return f"Opening {app_name}, Sir."
            elif target.startswith("start "):
                os.system(target)
                return f"Opening Settings, Sir."
            else:
                # Try to launch directly or via 'start'
                try:
                    subprocess.Popen(target)
                except FileNotFoundError:
                    os.system(f"start {app_name}")
                return f"Launching {app_name} now."
        except Exception as e:
            return f"I attempted to open {app_name}, but encountered an error: {e}"
    
    # Generic open attempt
    try:
        os.system(f"start {app_name}")
        return f"Attempting to open {app_name}, Sir."
    except:
        return f"I could not find {app_name} in my protocols."

def system_control(command):
    """Handle system operations."""
    command = command.lower()
    
    if "shutdown" in command:
        os.system("shutdown /s /t 5")
        return "Initiating system shutdown sequence in 5 seconds, Sir."
    
    elif "restart" in command:
        os.system("shutdown /r /t 5")
        return "Rebooting system in 5 seconds, Sir."
        
    elif "volume up" in command:
        # Requires pycaw or specialized lib, simple placeholder
        return "Volume controls are not fully integrated yet, Sir."
    
    elif "battery" in command or "power" in command:
        battery = psutil.sensors_battery()
        if battery:
            return f"Power levels are at {battery.percent} percent, Sir."
        return "We are running on AC power, Sir."
        
    return None
import requests
import pywhatkit
import time

def get_weather(city=""):
    """Get weather from wttr.in (Free, no key)."""
    if not city: return "Which city, Sir?"
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        res = requests.get(url)
        return f"Current weather in {city}: {res.text.strip()}"
    except Exception as e:
        return "I am unable to connect to the weather satellite, Sir."

def send_whatsapp(contact_name, message):
    """Send WhatsApp message using Web Automation."""
    # NOTE: In a real app, you'd need a contact book mapping.
    # For now, we will ask for the number if not known, or assume user provides number.
    # Or simpler: Just open the chat for them to type?
    # User asked: "send msg to galaxy on whatsapp hii"
    
    # Simple mapping for demo
    contacts = {
        "galaxy": "+919876543210", # PLEASE UPDATE THIS
        "mom": "+910000000000"
    }
    
    number = contacts.get(contact_name.lower())
    if not number:
        return f"I do not have a number for {contact_name} in my database, Sir."
        
    try:
        # This will open web.whatsapp.com and type the message
        pywhatkit.sendwhatmsg_instantly(number, message, wait_time=15, tab_close=True)
        return f"Message sent to {contact_name}: '{message}'"
    except Exception as e:
        return f"Failed to send message: {e}"

def play_video(topic):
    """Play a video on YouTube."""
    try:
        pywhatkit.playonyt(topic)
        return f"Playing {topic} on YouTube, Sir."
    except Exception as e:
        return f"I could not play the video. Error: {e}"

def get_news(count=5):
    """Get top news headlines using free GNews API."""
    try:
        # Using Google News RSS feed (no API key needed)
        url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
        import xml.etree.ElementTree as ET
        
        response = requests.get(url)
        root = ET.fromstring(response.content)
        
        news_items = []
        items = root.findall('.//item')[:count]
        
        for i, item in enumerate(items, 1):
            title = item.find('title').text
            news_items.append(f"{i}. {title}")
        
        if news_items:
            return "Here are today's top headlines, Sir:\n" + "\n".join(news_items)
        return "I could not fetch the news at this moment, Sir."
        
    except Exception as e:
        return f"Failed to retrieve news: {e}"

