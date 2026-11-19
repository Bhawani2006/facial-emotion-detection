"""
Download and organize UTKFace dataset for gender/age detection training.

UTKFace filename format: age_gender_race_date.jpg
  age: integer (0-116)
  gender: 0=Male, 1=Female
  race: 0=White, 1=Black, 2=Asian, 3=Indian, 4=Other
  date: timestamp

Dataset: https://www.kaggle.com/datasets/nipunarora8/utkface-new

After downloading from Kaggle, extract all images into ./data_utkface/
Then run: python download_utkface.py
"""

import os
from pathlib import Path

def organize_utkface():
    """
    Parse UTKFace filenames and organize into train/val/test splits
    with Male/Female subdirectories.
    """
    src_dir = Path('./data_utkface')
    if not src_dir.exists():
        print(f"[ERROR] {src_dir} does not exist.")
        print("Please download UTKFace from Kaggle and extract to ./data_utkface/")
        print("https://www.kaggle.com/datasets/nipunarora8/utkface-new")
        return False
    
    # Create output structure
    out_base = Path('./utkface_organized')
    for split in ['train', 'val', 'test']:
        for gender in ['Male', 'Female']:
            (out_base / split / gender).mkdir(parents=True, exist_ok=True)
    
    images = list(src_dir.glob('*.jpg'))
    if not images:
        print(f"[ERROR] No .jpg files found in {src_dir}")
        return False
    
    print(f"[*] Found {len(images)} images in {src_dir}")
    
    males   = []
    females = []
    
    for img_path in images:
        try:
            # Parse filename: age_gender_race_date.jpg
            parts = img_path.stem.split('_')
            if len(parts) < 2:
                continue
            gender = int(parts[1])
            
            if gender == 0:
                males.append(img_path)
            elif gender == 1:
                females.append(img_path)
        except (ValueError, IndexError):
            continue
    
    print(f"[*] Parsed: {len(males)} Male, {len(females)} Female")
    
    # Split: 70% train, 15% val, 15% test
    def split_data(images, name):
        n = len(images)
        n_train = int(n * 0.70)
        n_val   = int(n * 0.15)
        
        import random
        random.shuffle(images)
        
        train = images[:n_train]
        val   = images[n_train:n_train+n_val]
        test  = images[n_train+n_val:]
        
        return train, val, test
    
    male_train, male_val, male_test = split_data(males, 'Male')
    fem_train,  fem_val,  fem_test  = split_data(females, 'Female')
    
    # Copy files
    for split, datasets in [
        ('train', (male_train, fem_train)),
        ('val',   (male_val,   fem_val)),
        ('test',  (male_test,  fem_test)),
    ]:
        male_files, fem_files = datasets
        
        for src in male_files:
            dst = out_base / split / 'Male' / src.name
            os.link(str(src), str(dst))  # hardlink to save space
        
        for src in fem_files:
            dst = out_base / split / 'Female' / src.name
            os.link(str(src), str(dst))
        
        print(f"[OK] {split:5s}: {len(male_files):5d} Male  {len(fem_files):5d} Female")
    
    print(f"\n[OK] Organized dataset saved to {out_base}")
    return True

if __name__ == '__main__':
    organize_utkface()
