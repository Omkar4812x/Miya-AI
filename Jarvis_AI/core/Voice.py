
import asyncio
import edge_tts
import pygame
import os
import sys

# Add parent dir to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

# Global flag to stop speaking
STOP_SPEAKING = False

def stop_speaking():
    """Stop current speech playback."""
    global STOP_SPEAKING
    STOP_SPEAKING = True
    try:
        pygame.mixer.music.stop()
    except:
        pass

async def text_to_speech(text):
    """Convert text to speech using edge-tts and play it."""
    global STOP_SPEAKING
    STOP_SPEAKING = False
    
    # Update UI to speaking state
    if config.SPEAKING_CALLBACK:
        config.SPEAKING_CALLBACK(True)
        
    output_file = os.path.join(config.AUDIO_DIR, "response.mp3")
    
    try:
        communicate = edge_tts.Communicate(text, config.VOICE_NAME, rate=config.SPEECH_RATE, volume=config.SPEECH_VOLUME)
        await communicate.save(output_file)
        
        # Play audio
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        
        # Check for interruption during playback
        while pygame.mixer.music.get_busy():
            if STOP_SPEAKING:
                pygame.mixer.music.stop()
                break
            pygame.time.Clock().tick(10)
            
        pygame.mixer.quit()
        
        # Clean up
        if os.path.exists(output_file):
            os.remove(output_file)
            
    except Exception as e:
        print(f"TTS Error: {e}")
    finally:
        # Update UI to idle state
        if config.SPEAKING_CALLBACK:
            config.SPEAKING_CALLBACK(False)

def speak(text):
    """Synchronous wrapper for text_to_speech."""
    if not text: return
    asyncio.run(text_to_speech(text))

import speech_recognition as sr

def listen():
    """Listen to microphone input and return text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        if config.STATUS_CALLBACK:
            config.STATUS_CALLBACK("Listening...")
            
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing...")
            if config.STATUS_CALLBACK:
                config.STATUS_CALLBACK("Processing...")
                
            text = r.recognize_google(audio)
            print(f"You: {text}")
            if config.STATUS_CALLBACK:
                config.STATUS_CALLBACK(f"You: {text}")
            return text
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
