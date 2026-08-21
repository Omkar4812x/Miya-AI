
# 🧞 JARVIS AI Assistant (V1.0)

A futuristic, Iron Man-inspired AI assistant featuring a holographic HUD, voice interaction, and specific personality traits matching J.A.R.V.I.S.

![Jarvis HUD Preview](assets/jarvis.png)

## 💻 System Requirements
- **OS**: Windows 10/11 (Recommended)
- **Python**: 3.10 or newer (Tested on 3.11)
- **RAM**: 8GB+ (for local AI model)
- **Microphone**: Required for voice commands
- **Speaker**: Required for voice response

---

## 🚀 Installation Guide (New PC)

Follow these steps exactly to set up Jarvis on a new machine.

### 1. Install Python
Download and install Python from [python.org](https://www.python.org/downloads/).
*   **IMPORTANT**: Check the box **"Add Python to PATH"** during installation.

### 2. Install Ollama (The Brain)
Jarvis uses a local AI model so he works offline and is completely private.
1.  Download **Ollama** from [ollama.com](https://ollama.com/).
2.  Install it.
3.  Open a terminal (Command Prompt or PowerShell) and run:
    ```powershell
    ollama pull phi3:mini
    ```
    *(Wait for this to finish downloading 2-3GB)*.

### 3. Setup the Project
1.  Copy the `Jarvis_AI` folder to your new PC.
2.  Open the folder in VS Code or Terminal.
3.  Create a virtual environment (Optional but Recommended):
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```

### 4. Install Dependencies
Run the following command to install all necessary libraries:
```powershell
pip install -r requirements.txt
```

---

## ⚠️ Common Errors & Fixes

### ❌ Error: "Could not install PyAudio"
This is the most common error on Windows.
*   **Solution 1**: Try installing it directly:
    ```powershell
    pip install pipwin
    pipwin install pyaudio
    ```
*   **Solution 2**: if that fails, you need to verify your "C++ Build Tools". Install Visual Studio Build Tools if missing.

### ❌ Error: "Ollama connection failed"
*   **Reason**: The Ollama background service isn't running.
*   **Fix**: Open the **Ollama** app from your Start Menu before running Jarvis.

### ❌ Error: "QtWebEngineWidgets not found"
*   **Fix**: Reinstall the PyQt web component:
    ```powershell
    pip install PyQtWebEngine
    ```

### ❌ UI shows "NO CAPITAL" or Missing Image
*   **Fix**: Place a cool PNG image of Jarvis or an Iron Man HUD into the `assets` folder and name it `jarvis.png`.

---

## 🎮 How to Run
Once everything is installed:
1.  Make sure your microphone is connected.
2.  Run the main script:
    ```powershell
    python main.py
    ```
3.  **Controls**:
    *   **ESC**: Close the application.
    *   **Click & Drag**: Move the window (if not in fullscreen).
    *   **Speaking**: Just talk! He listens automatically after he finishes speaking.

---

## 📂 Project Structure
*   `main.py`: The entry point.
*   `ui/`: Contains the HTML/CSS/JS for the futuristic interface.
*   `core/`: Contains the Brain (AI), Voice (TTS/STT), and Logic.
*   `assets/`: Images and sound files.
*   `config.py`: Change settings like Voice, AI Name, or Volume here.
