import os
import json
import time
import re
from datetime import datetime
from PIL import Image
import piexif

DESTEKLENEN_FOTOLAR = [".jpg", ".jpeg", ".png", ".heic"]
DESTEKLENEN_VIDEOLAR = [".mp4", ".mov"]

def jsondan_zaman_al(json_yolu):
    try:
        with open(json_yolu, "r", encoding="utf-8") as f:
            veri = json.load(f)
        return int(veri["photoTakenTime"]["timestamp"])
    except:
        return None

def isimden_zaman_al(dosya_adi):
    try:
        eslesme1 = re.search(r"(\d{4})\.(\d{2})\.(\d{2}) (\d{2})\.(\d{2})\.(\d{2})", dosya_adi)
        if eslesme1:
            dt = datetime.strptime(eslesme1.group(0), "%Y.%m.%d %H.%M.%S")
            return int(dt.timestamp())
        eslesme2 = re.search(r"(\d{8})[_-](\d{6})", dosya_adi)
        if eslesme2:
            dt_str = eslesme2.group(1) + eslesme2.group(2)
            dt = datetime.strptime(dt_str, "%Y%m%d%H%M%S")
            return int(dt.timestamp())
        eslesme3 = re.search(r"(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})", dosya_adi)
        if eslesme3:
            dt_str = f"{eslesme3.group(1)}-{eslesme3.group(2)}-{eslesme3.group(3)} {eslesme3.group(4)}:{eslesme3.group(5)}:{eslesme3.group(6)}"
            dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            return int(dt.timestamp())
    except:
        return None
    return None

def exif_tarihi_guncelle(dosya_yolu, zaman):
    try:
        zaman_str = datetime.utcfromtimestamp(zaman).strftime("%Y:%m:%d %H:%M:%S")
        exif = piexif.load(dosya_yolu)
        exif["Exif"][piexif.ExifIFD.DateTimeOriginal] = zaman_str
        exif["Exif"][piexif.ExifIFD.DateTimeDigitized] = zaman_str
        exif["0th"][piexif.ImageIFD.DateTime] = zaman_str
        exif_bytes = piexif.dump(exif)
        piexif.insert(exif_bytes, dosya_yolu)
        print(f"[EXIF] {dosya_yolu} güncellendi → {zaman_str}")
    except:
        print(f"[HATA] EXIF yazılamadı: {dosya_yolu}")

def dosya_sistem_tarihi_guncelle(dosya_yolu, zaman):
    try:
        os.utime(dosya_yolu, (zaman, zaman))
        print(f"[FSYS] {dosya_yolu} dosya tarihi güncellendi.")
    except:
        print(f"[HATA] Dosya tarihi değiştirilemedi: {dosya_yolu}")

def dosya_isle(dosya_yolu):
    _, uzanti = os.path.splitext(dosya_yolu)
    uzanti = uzanti.lower()
    json_yolu = dosya_yolu + ".supplemental-meta.json"
    zaman = None
    if os.path.exists(json_yolu):
        zaman = jsondan_zaman_al(json_yolu)
    if not zaman:
        zaman = isimden_zaman_al(os.path.basename(dosya_yolu))
    if not zaman:
        print(f"[GEÇ] Zaman bulunamadı: {dosya_yolu}")
        return
    if uzanti in [".jpg", ".jpeg"]:
        exif_tarihi_guncelle(dosya_yolu, zaman)
        dosya_sistem_tarihi_guncelle(dosya_yolu, zaman)
    elif uzanti in DESTEKLENEN_FOTOLAR + DESTEKLENEN_VIDEOLAR:
        dosya_sistem_tarihi_guncelle(dosya_yolu, zaman)

def klasoru_tara(klasor):
    for kok, _, dosyalar in os.walk(klasor):
        for dosya in dosyalar:
            if any(dosya.lower().endswith(ext) for ext in DESTEKLENEN_FOTOLAR + DESTEKLENEN_VIDEOLAR):
                tam_yol = os.path.join(kok, dosya)
                dosya_isle(tam_yol)

if __name__ == "__main__":
    klasor = input("📁 Medya klasörünün yolunu girin: ").strip()
    if os.path.exists(klasor):
        klasoru_tara(klasor)
    else:
        print("❌ Geçersiz klasör yolu.")
