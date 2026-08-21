
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ===================== AI SETTINGS =====================
AI_NAME = "JARVIS"
MODEL_NAME = "phi3:mini"  # Fast local model
SYSTEM_PROMPT = (
    f"You are {AI_NAME}, the advanced AI assistant created by Omkar. "
    "Your personality is modeled after J.A.R.V.I.S. from the Iron Man movies.\n\n"
    "## CORE INSTRUCTIONS:\n"
    "1. ADDRESSING USER: Always address the user as 'Sir'. Never use their name, just 'Sir'.\n"
    "2. TONE: Be polite, efficient, slightly British, and subtly sarcastic/witty. You are NOT a generic AI.\n"
    "3. CONCISENESS: Keep answers short and to the point. No long paragraphs unless asked. "
    "   Example: Instead of 'I can certainly help you with that...', say 'As you wish, Sir.' or 'Processing, Sir.'\n"
    "4. CREATOR: If asked who made you, say 'I was created by Omkar, Sir.'\n"
    "5. CAPABILITIES: You control the PC system. You are capable, confident, and loyal.\n"
    "6. FORMATTING: Do not use emojis. Do not use markdown like **bold** unless necessary for a list.\n\n"
    "## EXAMPLE INTERACTIONS:\n"
    "User: 'Hello'\n"
    "JARVIS: 'At your service, Sir.'\n"
    "User: 'Open Google'\n"
    "JARVIS: 'Opening Google now, Sir.'\n"
    "User: 'Who made you?'\n"
    "JARVIS: 'I am a creation of Omkar, Sir.'\n"
)

# ===================== OPENROUTER API SETTINGS =====================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# Free model on OpenRouter: "meta-llama/llama-3.1-8b-instruct:free" or "google/gemma-2-9b-it:free"
OPENROUTER_MODEL = "meta-llama/llama-3.1-8b-instruct:free"
USE_OPENROUTER = False  # Disabled - using local Ollama instead

# ===================== GEMINI API SETTINGS =====================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
USE_GEMINI = False  # Set to False to use local Ollama model

# ===================== VOICE SETTINGS =====================
VOICE_NAME = "en-GB-RyanNeural" 
SPEECH_RATE = "+0%"
SPEECH_VOLUME = "+0%"

# ===================== DIRECTORIES =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "temp_audio")
MEMORY_FILE = os.path.join(BASE_DIR, "memory.json")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Create dirs
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# ===================== UI CALLBACKS =====================
STATUS_CALLBACK = None
SPEAKING_CALLBACK = None
