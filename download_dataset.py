"""
download_dataset.py
-------------------
Downloads FER-2013 via kaggle CLI and organises it into the
5-class folder structure that train_5class.py expects.

Prerequisites:
    pip install kaggle
    Put kaggle.json in  C:/Users/<you>/.kaggle/kaggle.json
    (Download from  kaggle.com -> Account -> Create API Token)

Usage:
    python download_dataset.py
"""

import os
import sys
import shutil
import zipfile

# Classes we KEEP (Disgust and Surprise are dropped)
KEEP = {'angry': 'Angry', 'fear': 'Fear', 'happy': 'Happy',
        'sad': 'Sad', 'neutral': 'Neutral'}

RAW_DIR = 'data_raw'
OUT_DIR = 'data'


def download_via_kaggle():
    print("[*] Downloading FER-2013 from Kaggle ...")
    ret = os.system(
        f'kaggle datasets download -d msambare/fer2013 -p {RAW_DIR} --unzip'
    )
    if ret != 0:
        print("\n[ERROR] kaggle download failed. Make sure:")
        print("  1. You have  pip install kaggle")
        print("  2. kaggle.json is at  C:/Users/<you>/.kaggle/kaggle.json")
        print("  3. You accepted the dataset terms on kaggle.com")
        sys.exit(1)


def organise():
    """
    FER-2013 raw layout (after kaggle unzip):
        data_raw/train/<classname>/<img>.jpg
        data_raw/test/<classname>/<img>.jpg

    We copy only the 5 classes we want into:
        data/train/<ClassName>/
        data/test/<ClassName>/
    """
    for split in ('train', 'test'):
        src_root = os.path.join(RAW_DIR, split)
        if not os.path.isdir(src_root):
            # Some kaggle zips use 'validation' for test
            alt = os.path.join(RAW_DIR, 'validation')
            if split == 'test' and os.path.isdir(alt):
                src_root = alt
            else:
                print(f"[WARN] Source folder not found: {src_root}  (skipping)")
                continue

        for raw_name, clean_name in KEEP.items():
            src = os.path.join(src_root, raw_name)
            # Some releases capitalise the folder
            if not os.path.isdir(src):
                src = os.path.join(src_root, raw_name.capitalize())
            if not os.path.isdir(src):
                print(f"[WARN] Class folder not found: {src}  (skipping)")
                continue

            dst = os.path.join(OUT_DIR, split, clean_name)
            os.makedirs(dst, exist_ok=True)
            count = 0
            for fname in os.listdir(src):
                if fname.lower().endswith(('.jpg', '.png', '.jpeg')):
                    shutil.copy2(os.path.join(src, fname),
                                 os.path.join(dst, fname))
                    count += 1
            print(f"  [OK] {split}/{clean_name}: {count} images")

    print(f"\n[OK] Dataset ready in: {os.path.abspath(OUT_DIR)}")
    print("     Run:  python train_5class.py")


if __name__ == '__main__':
    if not os.path.isdir(RAW_DIR):
        download_via_kaggle()
    else:
        print(f"[INFO] Found existing raw folder: {RAW_DIR}  (skipping download)")

    organise()
