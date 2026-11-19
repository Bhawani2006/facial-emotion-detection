"""
Demonstration of Integrated Emotion Detection System
Shows how all components work together.
"""

import os
import cv2
import sqlite3
import json
import time
import threading
import queue
from datetime import datetime
import numpy as np

print("=" * 60)
print("INTEGRATED EMOTION DETECTION SYSTEM DEMONSTRATION")
print("=" * 60)
print()

# Check if essential files exist
print("[1] Checking essential components...")
essential_files = {
    'emotion_model.keras': 'Emotion CNN model',
    'gender_model.keras': 'Gender CNN model',
    'realtime_detector_with_glasses.py': 'Glasses detection module'
}

all_exist = True
for file, desc in essential_files.items():
    exists = os.path.exists(file)
    status = "✓ FOUND" if exists else "✗ MISSING"
    print(f"  {status} - {file} ({desc})")
    if not exists:
        all_exist = False

print()

# Demonstrate database initialization
print("[2] Initializing database...")
try:
    import sqlite3
    
    # Initialize database
    conn = sqlite3.connect('emotion_detection.db')
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS demo_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS demo_detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            emotion TEXT,
            confidence REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    print("  ✓ Database initialized successfully")
    
    # Insert demo data
    cursor.execute("INSERT INTO demo_users (username) VALUES ('DemoUser')")
    user_id = cursor.lastrowid
    
    # Insert some demo detections
    demo_emotions = ['Happy', 'Fear', 'Sad', 'Happy', 'Fear']
    for i, emotion in enumerate(demo_emotions):
        cursor.execute(
            "INSERT INTO demo_detections (user_id, emotion, confidence) VALUES (?, ?, ?)",
            (user_id, emotion, 70 + (i * 5))
        )
    
    conn.commit()
    
    # Show demo data
    cursor.execute('''
        SELECT emotion, COUNT(*) as count, AVG(confidence) as avg_conf
        FROM demo_detections 
        GROUP BY emotion 
        ORDER BY count DESC
    ''')
    
    print("\n  Demo Statistics:")
    for row in cursor.fetchall():
        print(f"    {row[0]}: {row[1]} detections, avg {row[2]:.1f}% confidence")
    
    conn.close()
    
except Exception as e:
    print(f"  ✗ Database initialization failed: {e}")

print()

# Demonstrate OpenCV face detection
print("[3] Demonstrating OpenCV face detection...")
try:
    print("  ✓ OpenCV imported successfully")

    # Initialize the Haar cascade bundled with OpenCV.
    cascade_path = os.path.join(
        cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'
    )
    face_detector = cv2.CascadeClassifier(cascade_path)
    if face_detector.empty():
        raise RuntimeError(f"Could not load face cascade: {cascade_path}")

    # Smoke-test detection without requiring a webcam or model files.
    sample_frame = np.zeros((100, 100), dtype=np.uint8)
    face_detector.detectMultiScale(
        sample_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )
    print("  ✓ OpenCV Haar cascade face detection initialized")
    print("  Note: Full detection requires webcam input")

except (cv2.error, RuntimeError, AttributeError) as e:
    print(f"  ✗ OpenCV face detection initialization failed: {e}")

print()

# Demonstrate Streamlit dashboard
print("[4] Checking Streamlit dashboard...")
try:
    import streamlit
    print("  ✓ Streamlit available")
    print("  Run dashboard with: streamlit run dashboard.py")
except ImportError as e:
    print(f"  ✗ Streamlit not installed: {e}")
    print("  Install with: pip install streamlit")

print()

# Show complete workflow
print("[5] COMPLETE WORKFLOW:")
print("""
  1. Setup Environment:
     • Run: setup_enhanced.bat  (or manually install packages)
     • This demo uses: OpenCV, NumPy, Streamlit and SQLite.

  2. Initialize Database:
     • Run: python enhanced_emotion_detector.py --mode test
     • Creates SQLite database with all tables

  3. Run Dashboard:
     • Run: streamlit run dashboard.py
     • Opens browser at http://localhost:8501
     • Provides analytics, user management, session tracking

  4. Run Live Detection:
     • Run: python enhanced_emotion_detector.py --mode detect --username "YourName"
     • Starts webcam, detects faces, logs to database
     • Real-time emotion, gender, and glasses detection

  5. View Results:
     • Access dashboard during/after detection
     • View real-time statistics
     • Analyze session history
     • Export data for further analysis
""")

print()

# System architecture summary
print("[6] SYSTEM ARCHITECTURE SUMMARY:")
print("""
  ┌─────────────────────────────────────────────────────────┐
  │                    Streamlit Dashboard                    │
  │  • Real-time visualization                              │
  │  • User management & analytics                           │
  │  • Session tracking & reporting                          │
  └───────────────┬─────────────────────────────────────────┘
                  │ HTTP/WebSocket
  ┌───────────────▼─────────────────────────────────────────┐
  │               Enhanced Emotion Detector                   │
  │  • OpenCV Haar cascade (face detection)                 │
  │  • Filtered CNN: Sad, Happy, Fear only                  │
  │  • Gender CNN/heuristic (gender detection)              │
  │  • Glasses detection (eyeglasses/sunglasses)            │
  └───────────────┬─────────────────────────────────────────┘
                  │ SQLite Database
  ┌───────────────▼─────────────────────────────────────────┐
  │                     SQLite Database                       │
  │  • users: User profiles                                  │
  │  • sessions: Detection sessions                          │
  │  • emotion_logs: Timestamped detections                 │
  │  • emotion_stats: Aggregated statistics                  │
  └─────────────────────────────────────────────────────────┘
""")

print()

# Quick test
print("[7] Quick Test - Creating essential files...")

# Create a simple test image for detection
test_image = np.zeros((100, 100, 3), dtype=np.uint8)
cv2.rectangle(test_image, (20, 20), (80, 80), (255, 255, 255), -1)
cv2.imwrite('test_face.png', test_image)
print("  ✓ Created test image: test_face.png")

# Create a simple config file
config = {
    "system_version": "2.0",
    "components": ["OpenCV", "Streamlit", "SQLite", "CNN"],
    "database_path": "emotion_detection.db",
    "default_port": 8501
}

with open('system_config.json', 'w') as f:
    json.dump(config, f, indent=2)
print("  ✓ Created config: system_config.json")

print()

print("=" * 60)
print("DEMONSTRATION COMPLETE!")
print("=" * 60)
print()
print("Next steps:")
print("1. Install requirements: pip install -r requirements_enhanced.txt")
print("2. Initialize: python enhanced_emotion_detector.py --mode test")
print("3. Run dashboard: streamlit run dashboard.py")
print("4. Run detection: python enhanced_emotion_detector.py --mode detect")
print()
print("For help, run: python enhanced_emotion_detector.py --help")
