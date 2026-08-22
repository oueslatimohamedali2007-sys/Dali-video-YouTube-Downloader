import os
import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
import yt_dlp

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class DownloadThread(QThread):
    progress = pyqtSignal(int)
    status_info = pyqtSignal(str)
    success = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, url, save_path, quality_option):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.quality_option = quality_option
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
                
                eta = d.get('eta', None)
                speed = d.get('speed', None)
                
                eta_str = f"{eta}s" if eta is not None else "Calculating..."
                if speed:
                    speed_mb = speed / (1024 * 1024)
                    speed_str = f"{speed_mb:.2f} MB/s"
                else:
                    speed_str = "0 MB/s"

                self.status_info.emit(f"Speed: {speed_str} | Time left: {eta_str}")

        output_template = os.path.join(self.save_path, '%(title)s.%(ext)s')

        if self.quality_option == "Best Quality":
            format_spec = 'bestvideo+bestaudio/best'
        elif self.quality_option == "1080p":
            format_spec = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
        elif self.quality_option == "720p":
            format_spec = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
        elif self.quality_option == "480p":
            format_spec = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
        elif self.quality_option == "Audio Only (MP3)":
            format_spec = 'bestaudio/best'
        else:
            format_spec = 'bestvideo+bestaudio/best'

        ydl_opts = {
            'format': format_spec,
            'merge_output_format': 'mp4',
            'outtmpl': output_template,
            'force_ipv4': True,
            'socket_timeout': 30,
            'progress_hooks': [hook],
            'ffmpeg_location': resource_path('.'),
        }

        if self.quality_option == "Audio Only (MP3)":
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

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
    quality = w.qualityCombo.currentText() if hasattr(w, 'qualityCombo') else "Best Quality"

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
    
    w.thread = DownloadThread(url, save_path, quality)
    w.thread.progress.connect(update_progress)
    w.thread.status_info.connect(update_status_label)
    w.thread.success.connect(download_finished)
    w.thread.error.connect(download_error)
    w.thread.start()

def stop_download():
    if hasattr(w, 'thread'):
        w.thread.stop()
        w.b2.setEnabled(False)

def update_progress(percent):
    w.progressBar.setValue(percent)

def update_status_label(text):
    if hasattr(w, 'statusLabel'):
        w.statusLabel.setText(text)

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
    if hasattr(w, 'statusLabel'):
        w.statusLabel.setText("")
    w.b1.setEnabled(True)
    w.b2.setEnabled(False)
    w.b3.setEnabled(True)

app = QApplication([])

ui_path = resource_path("interface.ui")
with open(ui_path, "r", encoding="utf-8") as ui_file:
    w = loadUi(ui_file)

w.setWindowTitle("Dali Video YouTube Downloader ")
if os.path.exists(resource_path("logo.png")):
    w.setWindowIcon(QIcon(resource_path("logo.png")))

w.progressBar.setValue(0)
w.b2.setEnabled(False)

if hasattr(w, 'qualityCombo'):
    w.qualityCombo.addItems(["Best Quality", "1080p", "720p", "480p", "Audio Only (MP3)"])

w.b3.clicked.connect(browse_folder)
w.b1.clicked.connect(start_download)
w.b2.clicked.connect(stop_download)

w.show()
app.exec_()
