"""
Downloads the pre-trained Caffe gender detection model.
Run this once before starting the realtime detector.
"""
import urllib.request
import os

# Gil Levi & Tal Hassner's age/gender model (widely used, well-tested)
FILES = {
    "gender_deploy.prototxt": (
        "https://raw.githubusercontent.com/spmallick/learnopencv/master/"
        "AgeGender/gender_deploy.prototxt"
    ),
    "gender_net.caffemodel": (
        "https://github.com/GilLevi/AgeGenderDeepLearning/releases/download/"
        "v0.1/gender_net.caffemodel"
    ),
}

def download(url, dest):
    print(f"[*] Downloading {dest} ...")
    try:
        urllib.request.urlretrieve(url, dest)
        size_kb = os.path.getsize(dest) / 1024
        print(f"[OK] Saved {dest}  ({size_kb:.0f} KB)")
        return True
    except Exception as e:
        print(f"[FAIL] {e}")
        return False

if __name__ == "__main__":
    ok = True
    for name, url in FILES.items():
        if os.path.exists(name):
            print(f"[OK] {name} already exists — skipping.")
        else:
            ok = download(url, name) and ok

    if ok:
        print("\n[OK] Gender model ready.")
    else:
        print("\n[WARN] Some downloads failed. Will use fallback heuristic gender detection.")
