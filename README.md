# Dali video YouTube Downloader 🎥

A desktop application built with **Python**, **PyQt5**, and **yt-dlp** that allows you to download videos from YouTube with high-quality video and audio. The application features a modern dark-themed interface, custom download folder selection, real-time progress tracking, download cancellation, and background threading to keep the UI responsive.

---

## ✨ Features

* **🎞️ High-Quality Downloads** — Uses `yt-dlp` to download the best available video and audio streams and automatically merges them into an `.mp4` file using FFmpeg.
* **🌙 Dark Theme Interface** — Modern and accessible UI designed with Qt Designer and loaded from `interface.ui`.
* **📊 Real-Time Progress Tracking** — Displays download progress with a dynamic progress bar.
* **🧵 Multi-Threaded Downloads** — Uses `QThread` to perform downloads in the background without freezing the interface.
* **⏹️ Cancel Downloads** — Allows active downloads to be stopped cleanly.
* **📁 Custom Destination Folder** — Choose where downloaded videos should be saved using a native folder picker.

---

## 📋 Prerequisites

Before running the application, make sure you have the following installed:

1. **Python 3.8 or newer**
2. **FFmpeg** — Both `ffmpeg.exe` and `ffprobe.exe` must be available in the project root directory.

### Required Python Packages

The application uses:

* `PyQt5`
* `yt-dlp`

---

## 🚀 Installation & Usage

### 1. Clone the Repository

Clone the repository using Git:

```bash
git clone https://github.com/oueslatimohamedali2007-sys/Dali-video-YouTube-Downloader.git
cd Dali-video-YouTube-Downloader
```

Alternatively, download the repository as a `.zip` file from GitHub and extract it.

### 2. Install Dependencies

Open a terminal, PowerShell, or Command Prompt inside the project directory and run:

```bash
pip install PyQt5 yt-dlp
```

### 3. Add FFmpeg

Make sure the FFmpeg executables are located directly in the project root:

```text
ffmpeg.exe
ffprobe.exe
```

These files are required to merge the separate video and audio streams downloaded by `yt-dlp`.

### 4. Verify the Project Structure

Your project directory should look similar to this:

```text
Dali-video-YouTube-Downloader/
│
├── main.py          # Main Python application
├── interface.ui     # Qt Designer interface
├── ffmpeg.exe       # FFmpeg executable
├── ffprobe.exe      # FFprobe executable
└── README.md        # Project documentation
```

### 5. Run the Application

Start the application with:

```bash
python main.py
```

---

## 📖 How to Use

1. Launch the application with `python main.py`.
2. Copy the URL of a YouTube video.
3. Paste the URL into the application's URL field.
4. Click **Browse** and select the destination folder.
5. Click **Download** to start the download.
6. Monitor the real-time progress bar.
7. Once the download is complete, the video will be available in the selected folder.

---

## 🛠️ Troubleshooting

### `yt-dlp` Error or Signature Extraction Failure

YouTube frequently changes its systems, so an outdated version of `yt-dlp` may stop working.

Update `yt-dlp` with:

```bash
pip install --upgrade yt-dlp
```

### Video Has No Sound or Audio/Video Are Not Merged

Make sure both FFmpeg executables are present in the project root:

```text
ffmpeg.exe
ffprobe.exe
```

They should be located alongside `main.py`.

### `interface.ui` Not Found

Make sure `interface.ui` exists in the project directory and that you are running the application from the correct directory:

```bash
python main.py
```

If the application expects the UI file relative to the script, keep `interface.ui` in the same directory as `main.py`.

### Python Package Errors

If you encounter a missing-module error, reinstall the required dependencies:

```bash
pip install --upgrade PyQt5 yt-dlp
```

---

## ⚖️ Legal & Responsible Use

This application is intended for downloading content that you have permission to download or that is otherwise legally available for downloading.

Users are responsible for complying with YouTube's Terms of Service, copyright laws, and any other applicable regulations. The project does not encourage unauthorized downloading or redistribution of copyrighted content.

---

## 📄 License

This project is open-source and released under the **MIT License**.
