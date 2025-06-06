# Google Photos EXIF Editor GUI

## Overview
This project is a cross-platform Python application for batch editing and fixing EXIF metadata and filesystem timestamps of photos and videos exported from Google Photos. It provides a modern, user-friendly graphical interface built with PyQt5 and features a Nordic-inspired dark theme. The tool is especially useful for restoring correct photo/video dates after exporting from Google Photos, which often loses or misplaces original metadata.

## Features
- **Folder Selection**: Easily select a folder to process all supported media files within it (including subfolders).
- **Supported Formats**: Works with JPEG, PNG, HEIC, WEBP, MP4, and MOV files.
- **EXIF & Filesystem Date Fix**: For JPEGs, both EXIF metadata and filesystem timestamps are updated. For other supported formats, only the filesystem timestamp is updated.
- **Google Photos JSON Support**: If a `.supplemental-meta.json` file is present (as exported by Google Takeout), the tool extracts the original timestamp from it.
- **Filename Parsing**: If no JSON is found, the tool attempts to extract the date from the filename using several common Google Photos and camera naming patterns.
- **Progress Bar**: Visual progress bar and counters show how many files have been processed and how many remain.
- **Log Window**: Real-time log output with color-coded messages for success, errors, and warnings.
- **Threaded Processing**: File processing runs in a background thread, keeping the UI responsive.
- **Start/Stop Controls**: You can start or stop the batch process at any time.
- **Modern Nordic Theme**: The GUI uses a stylish, dark Nordic color palette for comfortable use.

## Project Structure
```
google-photos-exif-editor/
├── README.md
├── requirements.txt
├── delete_json_files.py
└── src/
    ├── main.py                # Application entry point
    ├── assets/
    │   └── logo.svg           # App logo (Nordic style)
    ├── core/
    │   ├── __init__.py
    │   └── exif_processor.py  # All EXIF and timestamp logic
    └── gui/
        ├── __init__.py
        ├── app.py             # Main GUI window and logic
        └── nordic_theme.py    # Nordic theme stylesheet for PyQt5
```

## How It Works
- The user selects a folder containing exported Google Photos files.
- The app scans for supported media files (recursively).
- For each file:
  - If a `.supplemental-meta.json` exists, the original timestamp is extracted from it.
  - If not, the filename is parsed for a date using several regex patterns.
  - For JPEGs, the EXIF `DateTimeOriginal`, `DateTimeDigitized`, and `DateTime` fields are updated, and the filesystem timestamp is set.
  - For other supported formats, only the filesystem timestamp is set.
- The progress bar and log window update in real time.
- At the end, a summary of successes and failures is shown.

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/xmtaha/google-photos-exif-editor
   cd google-photos-exif-editor
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   - Required: `PyQt5`, `piexif`, `Pillow`

## Usage
Run the application with:
```sh
python src/main.py
```
- Click "Browse..." to select your Google Photos export folder.
- Click "Start Processing" to begin fixing dates.
- Watch the progress and logs. You can stop at any time.

## Example Use Case
If you exported your photos from Google Photos using Google Takeout, and the files have lost their original dates, this tool will:
- Restore the correct date/time to the EXIF metadata (for JPEGs)
- Set the correct filesystem modification date for all supported files
- Use the `.json` metadata or, if missing, the filename

## Limitations
- Only the listed file types are supported.
- For non-JPEG images and videos, only the filesystem timestamp is updated (not EXIF).
- The tool does not upload or sync photos; it only fixes local files.

## License
MIT License

## Author
Developed by xmtaha 

## Support
https://coff.ee/xmtaha