"""
live_detector.py - Real-time webcam emotion detection for this repo.

Uses the trained model files already in this repo:
  - emotion_model.h5    (48x48 grayscale CNN, 7-class FER2013 softmax output)
  - emotion_model.hdf5  (64x64 grayscale CNN, used as fallback)

Setup (run once, inside your venv):
    pip install tensorflow opencv-python numpy

Run:
    python live_detector.py

Press Q to quit.

Notes:
  - Face detection uses OpenCV's Haar cascade (no extra downloads needed).
  - Preprocessing matches the repo docs: grayscale -> histogram
    equalization -> resize to the model's input size -> scale to 0-1.
  - The 7-class model uses the standard FER2013 label order
    [Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral]. Per the repo
    guide, results are shown in the 5-emotion system view (indices
    [0, 2, 3, 4, 6] -> Angry, Fear, Happy, Sad, Neutral). Set
    SHOW_ALL_7 = True below to display all 7 raw classes instead.
"""

import os
import sys

import cv2
import numpy as np
from tensorflow import keras

PRIMARY_MODEL = "emotion_model.h5"
FALLBACK_MODEL = "emotion_model.hdf5"

SHOW_ALL_7 = False  # True = show all 7 FER2013 classes, False = 5-emotion view

FER2013_LABELS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
FIVE_VIEW_INDICES = [0, 2, 3, 4, 6]  # Angry, Fear, Happy, Sad, Neutral
FIVE_VIEW_LABELS = ["Angry", "Fear", "Happy", "Sad", "Neutral"]

# BGR colors per emotion (from the repo guide)
EMOTION_COLORS = {
    "Angry": (48, 59, 255),
    "Disgust": (120, 60, 0),
    "Fear": (214, 86, 88),
    "Happy": (89, 199, 52),
    "Sad": (227, 113, 0),
    "Surprise": (0, 200, 255),
    "Neutral": (166, 161, 161),
}


def load_emotion_model():
    """Load the primary model, falling back to the secondary one."""
    for path in (PRIMARY_MODEL, FALLBACK_MODEL):
        if os.path.exists(path):
            print(f"Loading model: {path}")
            return keras.models.load_model(path), path
    sys.exit(
        f"No model file found. Put {PRIMARY_MODEL} (or {FALLBACK_MODEL}) "
        "in the same folder as this script."
    )


def main():
    model, model_path = load_emotion_model()

    # Input size and class count come from the model itself, so this works
    # with either model file.
    in_h, in_w = int(model.input_shape[1]), int(model.input_shape[2])
    n_classes = int(model.output_shape[-1])
    print(f"Model input: {in_w}x{in_h} grayscale, {n_classes} output classes")

    if n_classes == len(FER2013_LABELS):
        labels = FER2013_LABELS
    elif n_classes == len(FIVE_VIEW_LABELS):
        labels = FIVE_VIEW_LABELS
    else:
        labels = [f"Class {i}" for i in range(n_classes)]

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    if face_cascade.empty():
        sys.exit("Could not load Haar cascade. Check your opencv-python install.")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        sys.exit("Could not open webcam (device 0). Close other camera apps and retry.")

    print("Webcam started. Press Q to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame, exiting.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)  # repo docs: histogram equalization

        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(48, 48)
        )

        for (x, y, w, h) in faces:
            roi = gray[y : y + h, x : x + w]
            roi = cv2.resize(roi, (in_w, in_h))
            roi = roi.astype("float32") / 255.0
            roi = roi.reshape(1, in_h, in_w, 1)

            probs = model.predict(roi, verbose=0)[0]

            if n_classes == len(FER2013_LABELS) and not SHOW_ALL_7:
                # 5-emotion system view per the repo guide
                kept = probs[FIVE_VIEW_INDICES]
                idx = FIVE_VIEW_INDICES[int(np.argmax(kept))]
                conf = float(kept.max())
            else:
                idx = int(np.argmax(probs))
                conf = float(probs[idx])

            emotion = labels[idx]
            color = EMOTION_COLORS.get(emotion, (0, 255, 0))
            text = f"{emotion} {conf * 100:.0f}%"

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(
                frame,
                text,
                (x, y - 10 if y - 10 > 20 else y + h + 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2,
            )

        cv2.imshow("Live Emotion Detection (Q to quit)", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
