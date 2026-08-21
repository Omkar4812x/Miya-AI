
import sys
import os
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

# Import modular components
import config
from ui.gui import JarvisUI
from core import AI, Voice

class JarvisBackend(QThread):
    status_signal = pyqtSignal(str)
    speaking_signal = pyqtSignal(bool)

    def run(self):
        # Initial greeting
        text = f"{config.AI_NAME} is online."
        self.status_signal.emit(text)
        Voice.speak(text)
        
        while True:
            user_input = Voice.listen()
            if user_input:
                # Stop any ongoing speech immediately
                Voice.stop_speaking()
                
                if "exit" in user_input.lower() or "shutdown" in user_input.lower():
                    Voice.speak("Shutting down system.")
                    QApplication.instance().quit()
                    break
                
                response = AI.think(user_input)
                if response:
                    Voice.speak(response)
            
            time.sleep(0.5)

def main():
    # Setup callbacks
    # Backend instance will be created after UI is ready to connect signals?
    # No, we need a global way or pass update functions.
    # Config hack is simplest for now.
    
    app = QApplication(sys.argv)
    window = JarvisUI()
    
    # Create Backend
    backend = JarvisBackend()
    
    # Connect signals
    backend.status_signal.connect(window.set_status)
    backend.speaking_signal.connect(window.set_speaking)
    
    # Also set config callbacks for non-signal updates (hacky but works for modular files)
    # BUT, QThread cannot directly update UI. Signals are needed.
    # So we must wrap the callbacks to emit signals.
    
    def status_wrapper(text):
        backend.status_signal.emit(str(text))
        
    def speaking_wrapper(is_speaking):
        backend.speaking_signal.emit(is_speaking)
        
    config.STATUS_CALLBACK = status_wrapper
    config.SPEAKING_CALLBACK = speaking_wrapper
    
    window.show()
    backend.start()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
