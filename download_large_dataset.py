"""
download_large_dataset.py
-------------------------
Downloads a larger balanced AffectNet-style emotion dataset from Kaggle and
organises it into the same 5-class folder layout used by train_5class.py.

Target output:
    data_large/train/Angry
    data_large/train/Fear
    data_large/train/Happy
    data_large/train/Sad
    data_large/train/Neutral
    data_large/test/Angry
    ...

Recommended training command:
    python train_5class.py --train_dir data_large/train --test_dir data_large/test

Prerequisites:
    pip install kagglehub
    OR install/configure Kaggle CLI with kaggle.json
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

DATASET_SLUG = "dollyprajapati182/balanced-affectnet"
RAW_DIR = Path("data_large_raw")
OUT_DIR = Path("data_large")

CLASS_ALIASES = {
    "Angry": {"angry", "anger"},
    "Fear": {"fear", "fearful"},
    "Happy": {"happy", "happiness"},
    "Sad": {"sad", "sadness"},
    "Neutral": {"neutral", "neutrality"},
}

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def normalized(name):
    return name.lower().replace(" ", "_").replace("-", "_")


def download_dataset():
    RAW_DIR.mkdir(exist_ok=True)

    try:
        import kagglehub
        print(f"[*] Downloading large dataset with kagglehub: {DATASET_SLUG}")
        downloaded_path = Path(kagglehub.dataset_download(DATASET_SLUG))
        print(f"[OK] KaggleHub downloaded to: {downloaded_path}")
        return downloaded_path
    except Exception as exc:
        print(f"[WARN] kagglehub download failed: {exc}")
        print("[*] Trying Kaggle CLI fallback...")

    command = [
        "kaggle", "datasets", "download",
        "-d", DATASET_SLUG,
        "-p", str(RAW_DIR),
        "--unzip",
    ]
    result = subprocess.run(command)
    if result.returncode != 0:
        print("\n[ERROR] Dataset download failed. Please check:")
        print("  1. pip install kagglehub kaggle")
        print("  2. Kaggle API token exists at C:/Users/<you>/.kaggle/kaggle.json")
        print("  3. You accepted the dataset page terms on Kaggle")
        print(f"  4. Dataset page: https://www.kaggle.com/datasets/{DATASET_SLUG}")
        sys.exit(1)

    print(f"[OK] Kaggle CLI downloaded to: {RAW_DIR.resolve()}")
    return RAW_DIR


def collect_split_dirs(root):
    split_dirs = {"train": [], "test": []}
    for path in root.rglob("*"):
        if not path.is_dir():
            continue
        name = normalized(path.name)
        if name in {"train", "training"}:
            split_dirs["train"].append(path)
        elif name in {"test", "testing", "val", "valid", "validation"}:
            split_dirs["test"].append(path)
    return split_dirs


def find_class_dir(split_root, aliases):
    alias_set = {normalized(a) for a in aliases}
    for path in split_root.rglob("*"):
        if path.is_dir() and normalized(path.name) in alias_set:
            return path
    return None


def copy_images(src, dst):
    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for file_path in src.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTS:
            target = dst / file_path.name
            if target.exists():
                target = dst / f"{file_path.stem}_{count}{file_path.suffix}"
            shutil.copy2(file_path, target)
            count += 1
    return count


def organise(downloaded_root):
    downloaded_root = Path(downloaded_root)
    split_dirs = collect_split_dirs(downloaded_root)

    if not split_dirs["train"]:
        print(f"[ERROR] Could not find a train/training folder under: {downloaded_root}")
        sys.exit(1)

    if not split_dirs["test"]:
        print("[WARN] No test/validation folder found. Training needs validation data.")

    totals = {"train": 0, "test": 0}
    for split in ("train", "test"):
        roots = split_dirs[split]
        if not roots:
            continue

        for clean_name, aliases in CLASS_ALIASES.items():
            src = None
            for split_root in roots:
                src = find_class_dir(split_root, aliases)
                if src:
                    break

            if not src:
                print(f"[WARN] Missing {split}/{clean_name}; aliases checked: {sorted(aliases)}")
                continue

            dst = OUT_DIR / split / clean_name
            copied = copy_images(src, dst)
            totals[split] += copied
            print(f"  [OK] {split}/{clean_name}: {copied} images")

    print(f"\n[OK] Large dataset ready: {OUT_DIR.resolve()}")
    print(f"[INFO] Train images copied: {totals['train']}")
    print(f"[INFO] Test/val images copied: {totals['test']}")
    print("\nNext step:")
    print("  python train_5class.py --train_dir data_large/train --test_dir data_large/test")


if __name__ == "__main__":
    source = download_dataset()
    organise(source)
