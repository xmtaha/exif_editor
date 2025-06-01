# Media Timestamp Sync

A Python script that automatically restores correct **EXIF timestamps** and **file system creation dates** for your photos and videos based on:

- Google Takeout `.supplemental-meta.json` files (if available)
- Filename-based date parsing (e.g. `2021.01.24 10.18.30.jpg`, `VID_20250523_154344.mp4`, `Screenshot_2025-04-05-22-39-47-013.jpg`)

## ✅ Supported Formats

- Photos: `.jpg`, `.jpeg`, `.png`, `.heic`
- Videos: `.mp4`, `.mov`

## 🔍 How It Works

1. If a `.json` file (Google Takeout metadata) exists → timestamp is read from it.
2. If not, the script attempts to extract the date from the filename.
3. If successful:
   - For JPEGs: EXIF fields (`DateTimeOriginal`, etc.) are updated.
   - For all: File system creation/modification time is updated.

## 🛠️ Installation

```bash
pip install pillow piexif

