"""
Analyze dataset for glasses presence and model performance with glasses
"""
import os
import random
import cv2
import numpy as np

def check_glasses_in_dataset():
    """Check if dataset contains images with glasses"""
    base_path = 'data_balanced_small/train'
    emotions = ['Angry', 'Fear', 'Happy', 'Neutral', 'Sad']
    
    total_images = 0
    glasses_count = 0
    sample_with_glasses = []
    
    print("Analyzing dataset for glasses presence...")
    
    for emotion in emotions:
        emotion_path = os.path.join(base_path, emotion)
        if not os.path.exists(emotion_path):
            continue
            
        files = os.listdir(emotion_path)
        total_images += len(files)
        
        # Sample 10 random images from each emotion to check for glasses
        sample_files = random.sample(files, min(10, len(files)))
        
        for file in sample_files:
            img_path = os.path.join(emotion_path, file)
            try:
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    # Simple heuristic for glasses detection: look for dark horizontal lines in eye region
                    h, w = img.shape
                    eye_region = img[int(h*0.25):int(h*0.4), int(w*0.25):int(w*0.75)]
                    
                    # Calculate variance - glasses often create darker horizontal lines
                    if eye_region.size > 0:
                        variance = np.var(eye_region)
                        # Low variance might indicate uniform dark areas (glasses frames)
                        if variance < 500:  # Arbitrary threshold
                            glasses_count += 1
                            sample_with_glasses.append(img_path)
            except Exception as e:
                continue
    
    print(f"\nDataset Analysis:")
    print(f"Total images sampled: {total_images}")
    print(f"Estimated glasses images (heuristic): {glasses_count}")
    print(f"Approximate percentage with glasses: {(glasses_count/total_images*100 if total_images>0 else 0):.1f}%")
    
    return sample_with_glasses

def test_haar_glasses_detection():
    """Test OpenCV's glasses Haar Cascade"""
    print("\nTesting OpenCV glasses detection...")
    
    # Check if glasses cascade exists in OpenCV
    cascade_path = cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml'
    if os.path.exists(cascade_path):
        print(f"Found glasses cascade: {cascade_path}")
        glasses_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Test with a sample image
        test_dir = 'data_balanced_small/train/Happy'
        if os.path.exists(test_dir):
            files = os.listdir(test_dir)
            if files:
                test_img = cv2.imread(os.path.join(test_dir, files[0]))
                if test_img is not None:
                    gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
                    glasses = glasses_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                    print(f"Test detection found {len(glasses)} potential glasses regions")
    else:
        print("No dedicated glasses cascade found in OpenCV")
        # List available cascades
        cascades_dir = cv2.data.haarcascades
        print(f"Available cascades in {cascades_dir}:")
        if os.path.exists(cascades_dir):
            cascades = [f for f in os.listdir(cascades_dir) if f.endswith('.xml')]
            for cascade in cascades[:10]:
                print(f"  - {cascade}")

if __name__ == '__main__':
    check_glasses_in_dataset()
    test_haar_glasses_detection()
