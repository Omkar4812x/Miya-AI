
import sys
import os
import json
import ollama

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class ConversationManager:
    def __init__(self, memory_file=config.MEMORY_FILE):
        self.memory_file = memory_file
        self.history = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.history, f, indent=4)

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
        # Keep history manageable (last 20 messages)
        if len(self.history) > 20:
            self.history = self.history[-20:]
        self.save_memory()

    def get_context(self):
        return self.history

conversation_manager = ConversationManager()

import google.generativeai as genai
from openai import OpenAI

# Configure OpenRouter (OpenAI-compatible)
openrouter_client = None
if config.USE_OPENROUTER and config.OPENROUTER_API_KEY:
    openrouter_client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=config.OPENROUTER_API_KEY,
    )

# Configure Gemini if key is present
gemini_chat = None
if config.USE_GEMINI and config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=config.SYSTEM_PROMPT)
    gemini_chat = model.start_chat(history=[])


# Import Skills
from core import Skills

def correct_speech(raw_input):
    """Use AI to correct misheard speech before processing."""
    if not raw_input: return raw_input
    
    # Quick correction prompt - lightweight
    correction_prompt = f"""The user said: "{raw_input}"
This may have been misheard by speech recognition. 
Correct any obvious mistakes and return ONLY the corrected text.
If it seems correct, return the original.
Examples:
- "open new tab" -> "open new tab" (correct)
- "play song believer" -> "play song believer" (correct)
- "top five length" -> "top five news" (corrected)
- "what's the whether" -> "what's the weather" (corrected)

Return ONLY the corrected text, nothing else:"""

    try:
        # Use Ollama for quick correction
        response = ollama.chat(
            model="phi3:mini",
            messages=[{"role": "user", "content": correction_prompt}],
        )
        corrected = response['message']['content'].strip().strip('"').strip("'")
        
        if corrected and len(corrected) < 200:  # Sanity check
            if corrected.lower() != raw_input.lower():
                print(f"DEBUG: Corrected '{raw_input}' -> '{corrected}'")
            return corrected
    except:
        pass
    
    return raw_input

def think(user_input):
    """Process user input with OpenRouter, Gemini, or Ollama."""
    if not user_input: return None
    
    # STEP 0: Correct misheard speech
    user_input = correct_speech(user_input)
    
    # 1. CHECK FOR DIRECT COMMANDS (The "Real Jarvis" part)
    ui_lower = user_input.lower()
    
    if "open" in ui_lower:
        # Extract app name "open notepad" -> "notepad"
        app = ui_lower.replace("open", "").strip()
        # Clean up "and play a song" triggers if accidental
        if "and" in app: app = app.split("and")[0].strip()
        
        if app:
            response = Skills.open_app(app)
            if config.STATUS_CALLBACK: config.STATUS_CALLBACK(f"Action: {response}")
            return response
            
    if "play" in ui_lower:
        # "play a song", "play iron man trailer"
        topic = ui_lower.replace("play", "").strip()
        response = Skills.play_video(topic)
        if config.STATUS_CALLBACK: config.STATUS_CALLBACK(f"Media: {response}")
        return response
            
    if "shutdown" in ui_lower or "restart" in ui_lower or "battery" in ui_lower:
        response = Skills.system_control(ui_lower)
        if response:
            if config.STATUS_CALLBACK: config.STATUS_CALLBACK(f"System: {response}")
            return response
            
    if "weather" in ui_lower:
        # Extract city "weather in mumbai"
        city = ui_lower.split("in")[-1].strip() if "in" in ui_lower else ""
        response = Skills.get_weather(city)
        return response
        
    if "whatsapp" in ui_lower or "send msg" in ui_lower:
        # Heuristic parsing: "send msg to [Name] [Message]"
        try:
            parts = ui_lower.split("to")[-1].strip().split(" ")
            name = parts[0]
            msg = " ".join(parts[1:])
            
            response = Skills.send_whatsapp(name, msg)
            if config.STATUS_CALLBACK: config.STATUS_CALLBACK(f"WhatsApp: {response}")
            return response
        except:
            return "I didn't catch the name and message properly, Sir."
    
    # News detection with common misheard variations
    news_triggers = ["news", "headlines", "headline", "new", "views", "noose", "moves"]
    if any(trigger in ui_lower for trigger in news_triggers) and ("top" in ui_lower or "today" in ui_lower or "give" in ui_lower or "show" in ui_lower or "what" in ui_lower):
        print(f"DEBUG: News command detected!")
        # Extract count if specified "top 5 news"
        count = 5  # Default
        import re
        numbers = re.findall(r'\d+', ui_lower)
        if numbers:
            count = min(int(numbers[0]), 10)  # Max 10
        response = Skills.get_news(count)
        if config.STATUS_CALLBACK: config.STATUS_CALLBACK(f"News: Fetched {count} headlines")
        return response
    
    # 2. IF NOT A COMMAND, ASK THE AI MODAL (Conversation)
    
    # Update UI to Thinking
    if config.STATUS_CALLBACK:
        config.STATUS_CALLBACK("Thinking...")

    try:
        # 1. OpenRouter (Top Priority if Enabled)
        if config.USE_OPENROUTER and openrouter_client:
            print(f"DEBUG: Asking OpenRouter ({config.OPENROUTER_MODEL})...")
            completion = openrouter_client.chat.completions.create(
                model=config.OPENROUTER_MODEL,
                messages=[
                    {"role": "system", "content": config.SYSTEM_PROMPT},
                    {"role": "user", "content": user_input},
                ],
            )
            response_text = completion.choices[0].message.content
            return response_text

        # 2. Google Gemini
        elif config.USE_GEMINI and gemini_chat:
            print(f"DEBUG: Asking Gemini... Input: {user_input}")
            response = gemini_chat.send_message(user_input)
            print(f"DEBUG: Gemini Response: {response.text}")
            return response.text
            
        # 3. Local Ollama (Fallback)
        else:
            print(f"DEBUG: Asking Local Ollama ({config.MODEL_NAME})... Input: {user_input}")
            # Add user message to history
            conversation_manager.add_message("user", user_input)
            messages = [{"role": "system", "content": config.SYSTEM_PROMPT}] + conversation_manager.get_context()
            response = ollama.chat(model=config.MODEL_NAME, messages=messages)
            content = response['message']['content']
            print(f"DEBUG: Ollama Response: {content}")
            conversation_manager.add_message("assistant", content)
            return content

    except Exception as e:
        print(f"ERROR in AI.think: {e}")
        return f"I encountered an error processing that request, Sir: {str(e)}"
