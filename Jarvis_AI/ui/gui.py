
import sys
import os
import psutil
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject, pyqtSlot, QUrl, QTimer, Qt

# Import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class CallHandler(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot()
    def shutdown(self):
        print("Shutdown requested from UI")
        QApplication.quit()

class JarvisUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS SYSTEM")
        self.showFullScreen()
        
        self.browser = QWebEngineView()
        self.browser.page().setBackgroundColor(Qt.transparent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        
        self.setCentralWidget(self.browser)
        
        self.channel = QWebChannel()
        self.handler = CallHandler(self)
        self.channel.registerObject('py_handler', self.handler)
        self.browser.page().setWebChannel(self.channel)
        
        self.browser.loadFinished.connect(self.on_load_finished)
        
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html"))
        self.browser.load(QUrl.fromLocalFile(html_path))
        
        self.page_ready = False

    def on_load_finished(self, ok):
        if ok:
            print("UI Loaded Successfully")
            self.page_ready = True
            # Init Image
            self.inject_image()
            # Start stats timer
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_cpu)
            self.timer.start(1000)

    def inject_image(self):
        # Allow user to provide 'jarvis.png' or use existing 'miya.png' or fallback
        paths = [
            os.path.join(config.ASSETS_DIR, "jarvis.png"),
            os.path.join(config.ASSETS_DIR, "miya.png"), 
            r"d:\TryToCreateJarvis\Miya ai\M.I.A-main\Mia\Img\1.png"
        ]
        final_path = ""
        for p in paths:
            if os.path.exists(p):
                # Convert to file URL for browser
                final_path = QUrl.fromLocalFile(p).toString()
                break
        
        if final_path:
            # Use single quotes for JS strings
            self.browser.page().runJavaScript(f"setImage('{final_path}');")

    def update_cpu(self):
        if not self.page_ready: return
        val = psutil.cpu_percent()
        self.browser.page().runJavaScript(f"setCpu({val});")

    def set_status(self, text):
        if not self.page_ready: return
        
        status = "Active"
        if "Listening" in text: status = "Listening"
        elif "Thinking" in text: status = "Thinking"
        elif "Processing" in text: status = "Thinking"
        
        safe_text = str(text).replace("'", "\\'").replace("\n", " ")
        self.browser.page().runJavaScript(f"updateStatus('{status}', '{safe_text}');")

    def set_speaking(self, is_speaking):
        if not self.page_ready: return
        status = "Speaking" if is_speaking else "Active"
        self.browser.page().runJavaScript(f"updateStatus('{status}', '');")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = JarvisUI()
    win.show()
    sys.exit(app.exec_())
