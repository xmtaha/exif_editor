import os
import json
import time
import re
from datetime import datetime
from PIL import Image
import piexif

SUPPORTED_PHOTOS = [".jpg", ".jpeg", ".png", ".heic", ".webp"]
SUPPORTED_VIDEOS = [".mp4", ".mov"]

def get_timestamp_from_json(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return int(data["photoTakenTime"]["timestamp"])
    except:
        return None

def get_timestamp_from_filename(filename):
    try:
        match1 = re.search(r"(\d{4})\.(\d{2})\.(\d{2}) (\d{2})\.(\d{2})\.(\d{2})", filename)
        if match1:
            dt = datetime.strptime(match1.group(0), "%Y.%m.%d %H.%M.%S")
            return int(dt.timestamp())

        match2 = re.search(r"(\d{8})[_-](\d{6})", filename)
        if match2:
            dt_str = match2.group(1) + match2.group(2)
            dt = datetime.strptime(dt_str, "%Y%m%d%H%M%S")
            return int(dt.timestamp())

        match3 = re.search(r"(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})", filename)
        if match3:
            dt_str = f"{match3.group(1)}-{match3.group(2)}-{match3.group(3)} {match3.group(4)}:{match3.group(5)}:{match3.group(6)}"
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            return int(dt.timestamp())

        match4 = re.search(r"(VID|IMG)[-_](\d{8})[-_]", filename)
        if match4:
            dt = datetime.strptime(match4.group(2), "%Y%m%d")
            return int(dt.timestamp())

        match5 = re.search(r"-?(\d{8})(?:-\d+)?", filename)
        if match5:
            dt = datetime.strptime(match5.group(1), "%Y%m%d")
            return int(dt.timestamp())

    except:
        return None
    return None


def update_exif_date(image_path, timestamp):
    try:
        formatted_time = datetime.utcfromtimestamp(timestamp).strftime("%Y:%m:%d %H:%M:%S")
        exif_dict = piexif.load(image_path)
        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = formatted_time
        exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = formatted_time
        exif_dict["0th"][piexif.ImageIFD.DateTime] = formatted_time
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_path)
        print(f"[EXIF] {image_path} updated to {formatted_time}")
    except:
        print(f"[ERROR] Failed to write EXIF to {image_path}")

def update_file_system_date(file_path, timestamp):
    try:
        os.utime(file_path, (timestamp, timestamp))
        print(f"[FSYS] {file_path} file system timestamp updated.")
    except:
        print(f"[ERROR] Failed to update file system timestamp for {file_path}")

def process_file(file_path):
    base, ext = os.path.splitext(file_path)
    ext = ext.lower()
    json_path = file_path + ".supplemental-meta.json"
    timestamp = None
    if os.path.exists(json_path):
        timestamp = get_timestamp_from_json(json_path)
    if not timestamp:
        timestamp = get_timestamp_from_filename(os.path.basename(file_path))
    if not timestamp:
        print(f"[SKIP] No timestamp found for {file_path}")
        return
    if ext in [".jpg", ".jpeg"]:
        update_exif_date(file_path, timestamp)
        update_file_system_date(file_path, timestamp)
    elif ext in SUPPORTED_PHOTOS + SUPPORTED_VIDEOS:
        update_file_system_date(file_path, timestamp)

def scan_and_process(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in SUPPORTED_PHOTOS + SUPPORTED_VIDEOS):
                full_path = os.path.join(root, file)
                process_file(full_path)

if __name__ == "__main__":
    folder = input("Enter the path to your media folder: ").strip()
    if os.path.exists(folder):
        scan_and_process(folder)
    else:
        print("Invalid folder path.")
