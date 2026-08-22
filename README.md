# YouTube Video Downloader 🎥

A desktop application built with **Python**, **PyQt5**, and **yt-dlp** that allows you to download videos directly from YouTube with full video/audio quality. Features a modern dark UI, custom save folder selection, dynamic progress bar tracking, and execution threading.

---

## ✨ Features

- **High-Quality Downloads:** Downloads optimal video and audio streams using `yt-dlp` and automatically merges them into `.mp4` format using `ffmpeg`.
- **Dark Theme Interface:** Modern, accessible user interface loaded dynamically via Qt Designer (`interface.ui`).
- **Progress Tracking:** Real-time progress bar displaying download percentage.
- **Multi-Threaded Architecture:** Powered by `QThread` to keep the user interface responsive during network downloads.
- **Cancel Download:** Stop active downloads cleanly at any time.
- **Custom Destination:** Easily select target directories via a native folder picker.

---

## 📋 Prerequisites

Before running the application, make sure you have:
1. **Python 3.8+** installed on your system.
2. **FFmpeg binaries** (`ffmpeg.exe` and `ffprobe.exe`) placed directly in the project root folder.

---

## 🚀 How to Run

### Step 1: Download/Clone the Repository
Download the project as a `.zip` from GitHub and extract it, or clone it using Git:
```bash
git clone [https://github.com/oueslatimohamedali2007-sys/YOUR_REPOSITORY_NAME.git](https://github.com/oueslatimohamedali2007-sys/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME
