import os
import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
import yt_dlp

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    success = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.is_cancelled = False

    def stop(self):
        self.is_cancelled = True

    def run(self):
        def hook(d):
            if self.is_cancelled:
                raise Exception("Download cancelled")
            
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total > 0:
                    percent = int((downloaded / total) * 100)
                    self.progress.emit(percent)

        output_template = os.path.join(self.save_path, '%(title)s.%(ext)s')

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': output_template,
            'force_ipv4': True,        # Forces IPv4 to bypass WinError 10051
            'socket_timeout': 30,      # Prevents premature timeout disconnects
            'progress_hooks': [hook],  # Connects yt-dlp progress into our PyQt thread
            
            # Points to ffmpeg location dynamically whether running as script or .exe
            'ffmpeg_location': resource_path('.'),
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            
            if not self.is_cancelled:
                self.success.emit()
                
        except Exception as e:
            self.error.emit(str(e))


def browse_folder():
    folder_path = QFileDialog.getExistingDirectory(w, "Select Save Folder")
    if folder_path:
        w.l2.setText(folder_path)

def start_download():
    url = w.l1.text().strip()
    save_path = w.l2.text().strip()
    
    if url == "":
        QMessageBox.critical(w, "Error", "You should paste the link")
        return
        
    if save_path == "":
        QMessageBox.critical(w, "Error", "Please choose a save location first")
        return
        
    w.progressBar.setValue(0)
    w.b1.setEnabled(False)
    w.b2.setEnabled(True)
    w.b3.setEnabled(False)
    
    w.thread = DownloadThread(url, save_path)
    w.thread.progress.connect(update_progress)
    w.thread.success.connect(download_finished)
    w.thread.error.connect(download_error)
    w.thread.start()

def stop_download():
    if hasattr(w, 'thread'):
        w.thread.stop()
        w.b2.setEnabled(False)

def update_progress(percent):
    w.progressBar.setValue(percent)

def download_finished():
    QMessageBox.information(w, "Success", "Video downloaded successfully!")
    reset_ui()

def download_error(error_msg):
    if "cancelled" in error_msg.lower():
        QMessageBox.warning(w, "Cancelled", "Download was stopped by user.")
    else:
        QMessageBox.critical(w, "Error", f"An error occurred:\n{error_msg}")
    reset_ui()

def reset_ui():
    w.progressBar.setValue(0)
    w.b1.setEnabled(True)
    w.b2.setEnabled(False)
    w.b3.setEnabled(True)

app = QApplication([])

# Dark mode styling injection for native QMessageBox dialogs
app.setStyleSheet("""
    QMessageBox {
        background-color: #1a1a1a;
    }
    QMessageBox QLabel {
        color: #ffffff;
        font-size: 11pt;
    }
    QMessageBox QPushButton {
        background-color: #444444;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 6px 16px;
        font-size: 10pt;
        font-weight: bold;
        min-width: 70px;
    }
    QMessageBox QPushButton:hover {
        background-color: #ff0000;
    }
""")

# Load UI using resource_path to support compiled .exe environments
ui_path = resource_path("interface.ui")
with open(ui_path, "r", encoding="utf-8") as ui_file:
    w = loadUi(ui_file)

w.progressBar.setValue(0)
w.b2.setEnabled(False)

w.b3.clicked.connect(browse_folder)
w.b1.clicked.connect(start_download)
w.b2.clicked.connect(stop_download)

w.show()
app.exec_()