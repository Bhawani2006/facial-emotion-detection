"""
live_detector.py - Real-time webcam emotion detection for this repo.

Uses the trained model files already in this repo:
  - emotion_model.hdf5  (trained 64x64 grayscale CNN, preferred)
  - emotion_model.h5    (legacy 48x48 CNN, used only as fallback)

Setup (run once, inside your venv):
    pip install tensorflow opencv-python numpy

Run:
    python live_detector.py --username "YourName"

Press Q to quit.

Notes:
  - Face detection uses OpenCV's Haar cascade (no extra downloads needed).
  - Preprocessing matches the repo docs: grayscale -> histogram
    equalization -> resize to the model's input size. The preferred .hdf5
    uses 0-1 input; the legacy .h5 retains its existing 0-255 scale.
  - The 7-class model uses the standard FER2013 label order
    [Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral]. Per the repo
    guide, results are shown in the 5-emotion system view (indices
    [0, 2, 3, 4, 6] -> Angry, Fear, Happy, Sad, Neutral). Set
    SHOW_ALL_7 = True below to display all 7 raw classes instead.
"""

import argparse
import os
from pathlib import Path
import sqlite3
import sys
import time

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "emotion_detection.db"
PRIMARY_MODEL = BASE_DIR / "emotion_model.hdf5"
FALLBACK_MODEL = BASE_DIR / "emotion_model.h5"

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


def init_database(db_path=DATABASE_PATH):
    """Create the dashboard schema without replacing existing data."""
    conn = sqlite3.connect(str(db_path), timeout=10, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE,
            age INTEGER, gender TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, end_time TIMESTAMP,
            device_info TEXT, FOREIGN KEY(user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS emotion_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, face_id INTEGER,
            emotion TEXT, confidence REAL, gender TEXT, gender_confidence REAL,
            glasses_type TEXT, glasses_confidence REAL,
            x INTEGER, y INTEGER, w INTEGER, h INTEGER,
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        );
    """)
    conn.commit()
    return conn


class DetectionRecorder:
    """Record each detected face; flush once a second and on exit."""

    def __init__(self, username="Guest", age=None, gender=None, db_path=DATABASE_PATH):
        self.conn = init_database(db_path)
        self.conn.execute(
            "INSERT OR IGNORE INTO users (username, age, gender) VALUES (?, ?, ?)",
            (username.strip() or "Guest", age, gender),
        )
        user_id = self.conn.execute(
            "SELECT id FROM users WHERE username = ?", (username.strip() or "Guest",)
        ).fetchone()[0]
        cursor = self.conn.execute(
            "INSERT INTO sessions (user_id, device_info) VALUES (?, ?)",
            (user_id, "live_detector.py / OpenCV webcam 0"),
        )
        self.session_id = cursor.lastrowid
        self.conn.commit()
        self.last_flush = time.monotonic()

    def record(self, face_id, emotion, confidence, box):
        self.conn.execute(
            """INSERT INTO emotion_logs
               (session_id, face_id, emotion, confidence, x, y, w, h)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (self.session_id, int(face_id), emotion, float(confidence),
             *(int(v) for v in box)),
        )
        if time.monotonic() - self.last_flush >= 1:
            self.conn.commit()
            self.last_flush = time.monotonic()

    def close(self):
        try:
            self.conn.execute(
                "UPDATE sessions SET end_time = CURRENT_TIMESTAMP WHERE id = ?",
                (self.session_id,),
            )
            self.conn.commit()
        finally:
            self.conn.close()


def load_emotion_model():
    """Load the primary model, falling back to the secondary one."""
    from tensorflow import keras

    for path in (PRIMARY_MODEL, FALLBACK_MODEL):
        if os.path.exists(path):
            print(f"Loading model: {path}")
            if path == FALLBACK_MODEL:
                print("WARNING: using legacy .h5; its saved weights did not pass expression tests.")
            return keras.models.load_model(path, compile=False), path
    sys.exit(
        f"No model file found. Put {PRIMARY_MODEL} (or {FALLBACK_MODEL}) "
        "in the same folder as this script."
    )


def main():
    import cv2
    import numpy as np

    parser = argparse.ArgumentParser(description="Webcam emotion detection with SQLite recording")
    parser.add_argument("--username", default="Guest")
    parser.add_argument("--age", type=int, default=None)
    parser.add_argument("--gender", choices=["Male", "Female", "Other"], default=None)
    args = parser.parse_args()
    if args.age is not None and not 0 <= args.age <= 120:
        parser.error("--age must be between 0 and 120")
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

    try:
        recorder = DetectionRecorder(args.username, args.age, args.gender)
    except Exception:
        cap.release()
        raise
    print(f"Recording session {recorder.session_id} to {DATABASE_PATH}")
    print("Webcam started. Press Q to quit. Refresh the dashboard to see saved results.")

    try:
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

            for face_id, (x, y, w, h) in enumerate(faces):
                roi = gray[y : y + h, x : x + w]
                roi = cv2.resize(roi, (in_w, in_h))
                roi = roi.astype("float32")
                if model_path == PRIMARY_MODEL:
                    roi /= 255.0  # Trained .hdf5 model uses 0-1 pixels.
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
                recorder.record(face_id, emotion, conf, (x, y, w, h))
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

    finally:
        try:
            recorder.close()
        finally:
            cap.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
