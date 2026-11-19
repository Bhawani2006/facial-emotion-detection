"""Emotion Monitor Pro: local webcam emotion display, no MediaPipe.

Run: python emotion_monitor_pro.py
Optional: python emotion_monitor_pro.py --camera 1
Requires: tensorflow, opencv-contrib-python, numpy.
Keep emotion_model.h5 (or emotion_model.hdf5) beside this file.
Q/Esc quit, T toggles theme, F toggles fullscreen.

The seven bars are FER2013 model scores, not medical or mental-state
measurements. Gender, fatigue and frustration are not inferred. Frames stay
in memory; this script does not record video or save dashboard sessions.
"""

import argparse
from pathlib import Path
import time

import cv2
import numpy as np

LABELS = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]
COLORS = [(85, 94, 245), (158, 178, 70), (208, 134, 178),
          (137, 216, 95), (230, 165, 85), (89, 206, 244), (190, 181, 168)]
WINDOW = "Emotion Monitor Pro"
WIDTH, HEIGHT = 1280, 800


def text(image, message, xy, size, color, thickness=1):
    cv2.putText(image, message, xy, cv2.FONT_HERSHEY_SIMPLEX,
                size, color, thickness, cv2.LINE_AA)


def load_model():
    # Delay TensorFlow startup until main, so layout can be tested separately.
    from tensorflow import keras

    def load_compatible(path):
        try:
            return keras.models.load_model(str(path), compile=False)
        except (TypeError, ValueError) as original_error:
            # Some model configs mix newer initializer axes and inactive
            # legacy batch-renormalization metadata. Strip only no-op fields
            # in a temporary copy. The model and trained weights stay intact.
            import json
            import shutil
            import tempfile
            import h5py  # Installed as a TensorFlow dependency.

            with h5py.File(str(path), "r") as handle:
                config = json.loads(handle.attrs["model_config"])
            changed = False

            def clean(node):
                nonlocal changed
                if isinstance(node, dict):
                    if node.get("class_name") == "GlorotUniform":
                        fields = node.get("config", {})
                        for key in ("input_axes", "output_axes"):
                            if key in fields and fields[key] is None:
                                del fields[key]
                                changed = True
                    if node.get("class_name") == "BatchNormalization":
                        fields = node.get("config", {})
                        if fields.get("renorm") is False:
                            for key in ("renorm", "renorm_clipping", "renorm_momentum"):
                                fields.pop(key, None)
                            changed = True
                    if node.get("class_name") == "Dense":
                        fields = node.get("config", {})
                        if "quantization_config" in fields and fields["quantization_config"] is None:
                            del fields["quantization_config"]
                            changed = True
                    for value in node.values():
                        clean(value)
                elif isinstance(node, list):
                    for value in node:
                        clean(value)

            clean(config)
            if not changed:
                raise original_error
            with tempfile.TemporaryDirectory() as temp:
                copy = Path(temp) / path.name
                shutil.copyfile(str(path), str(copy))
                with h5py.File(str(copy), "r+") as handle:
                    handle.attrs["model_config"] = json.dumps(config)
                return keras.models.load_model(str(copy), compile=False)

    folder = Path(__file__).resolve().parent
    for name in ("emotion_model.h5", "emotion_model.hdf5"):
        path = folder / name
        if path.is_file():
            print("Loading", path, "(the first TensorFlow startup can take a while)")
            model = load_compatible(path)
            shape = model.input_shape
            if (isinstance(shape, list) or len(shape) != 4 or shape[-1] != 1
                    or int(model.output_shape[-1]) != len(LABELS)):
                raise RuntimeError("Expected a grayscale, seven-class FER2013 model.")
            return model, int(shape[1]), int(shape[2])
    raise FileNotFoundError("Put emotion_model.h5 or emotion_model.hdf5 beside this script.")


def predict_face(model, gray, box, in_h, in_w):
    x, y, w, h = box
    roi = cv2.resize(gray[y:y+h, x:x+w], (in_w, in_h))
    batch = (roi.astype(np.float32) / 255.0).reshape(1, in_h, in_w, 1)
    scores = np.asarray(model(batch, training=False)).reshape(-1)
    if scores.size != 7 or not np.all(np.isfinite(scores)):
        raise RuntimeError("The emotion model returned invalid scores.")
    return scores


def render(frame, scores, box, fps, dark=True):
    """Compose a fixed-size canvas; bars describe only the largest face."""
    bg = (20, 17, 15) if dark else (244, 241, 235)
    panel = (32, 28, 25) if dark else (255, 255, 255)
    ink = (243, 239, 233) if dark else (45, 38, 30)
    muted = (157, 150, 141) if dark else (116, 104, 91)
    track = (53, 46, 40) if dark else (231, 226, 219)
    accent = (192, 224, 97) if dark else (100, 117, 28)
    canvas = np.full((HEIGHT, WIDTH, 3), bg, dtype=np.uint8)
    text(canvas, "EMOTION MONITOR PRO", (28, 42), 0.85, ink, 2)
    text(canvas, "LOCAL WEBCAM  /  FER2013 EXPRESSION MODEL", (29, 68), 0.40, muted)
    text(canvas, f"{fps:4.1f} FPS", (1136, 42), 0.55, accent, 1)
    cv2.line(canvas, (28, 88), (1252, 88), track, 1)

    cv2.rectangle(canvas, (24, 108), (350, 716), panel, -1)
    text(canvas, "EMOTION ANALYTICS", (44, 144), 0.60, ink, 1)
    text(canvas, "LIVE MODEL SCORES", (44, 169), 0.37, muted)
    for i, name in enumerate(LABELS):
        y = 214 + i * 57
        text(canvas, name.upper(), (44, y), 0.42, ink)
        value = float(np.clip(scores[i], 0, 1)) if scores is not None else 0.0
        label = f"{100 * value:.1f}%" if scores is not None else "--"
        text(canvas, label, (263, y), 0.43, muted)
        cv2.rectangle(canvas, (44, y + 10), (326, y + 20), track, -1)
        if value > 0:
            cv2.rectangle(canvas, (44, y + 10),
                          (44 + max(1, int(282 * value)), y + 20), COLORS[i], -1)
    text(canvas, "Largest face is analyzed", (44, 643), 0.40, muted)
    text(canvas, "Scores are not a diagnosis.", (44, 670), 0.39, muted)
    text(canvas, "No recording. No uploads.", (44, 694), 0.39, muted)

    cv2.rectangle(canvas, (370, 108), (1256, 716), panel, -1)
    text(canvas, "LIVE CAMERA", (392, 143), 0.46, ink)
    view = frame.copy()
    if box is not None and scores is not None:
        x, y, w, h = [int(v) for v in box]
        best = int(np.argmax(scores))
        color = COLORS[best]
        cv2.rectangle(view, (x, y), (x+w, y+h), color, 2)
        title = f"{LABELS[best]} {scores[best]*100:.1f}%"
        # Put the label inside the image even when the face touches the top.
        tx, ty = max(4, x), max(22, y - 9)
        text(view, title, (tx, ty), 0.65, (10, 10, 10), 4)
        text(view, title, (tx, ty), 0.65, color, 2)
    fh, fw = view.shape[:2]
    scale = min(844 / fw, 480 / fh)
    vw, vh = max(1, round(fw * scale)), max(1, round(fh * scale))
    view = cv2.resize(view, (vw, vh))
    vx, vy = 392 + (844-vw)//2, 164 + (480-vh)//2
    canvas[vy:vy+vh, vx:vx+vw] = view
    if scores is None:
        status = "NO FACE  |  Look toward the camera"
        status_color = muted
    else:
        best = int(np.argmax(scores))
        status = f"{LABELS[best].upper()}  |  Model score {scores[best]*100:.1f}%"
        status_color = COLORS[best]
    text(canvas, status, (392, 685), 0.56, status_color, 1)
    text(canvas, "Q / ESC  QUIT       T  THEME       F  FULLSCREEN", (29, 758), 0.46, ink)
    text(canvas, "Expression estimates can be wrong. Lighting and pose affect results.",
         (29, 785), 0.40, muted)
    return canvas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--camera", type=int, default=0, help="Webcam index (default 0)")
    args = parser.parse_args()
    model, in_h, in_w = load_model()
    cascade = cv2.CascadeClassifier(str(Path(cv2.data.haarcascades) /
                                       "haarcascade_frontalface_default.xml"))
    if cascade.empty():
        raise RuntimeError("OpenCV's face cascade could not be loaded.")
    cap = cv2.VideoCapture(args.camera)
    try:
        if not cap.isOpened():
            raise RuntimeError("Cannot open webcam. Close other camera apps, allow camera "
                               "access in Windows, or try --camera 1.")
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(WINDOW, WIDTH, HEIGHT)
        dark, fullscreen, fps = True, False, 0.0
        previous = time.perf_counter()
        print("Camera ready. Q/Esc: quit | T: theme | F: fullscreen")
        while True:
            ok, frame = cap.read()
            if not ok:
                raise RuntimeError("Webcam stopped returning frames. Reconnect it and retry.")
            frame = cv2.flip(frame, 1)
            gray = cv2.equalizeHist(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            faces = cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5,
                                            minSize=(48, 48))
            box = max(faces, key=lambda b: b[2]*b[3]) if len(faces) else None
            scores = predict_face(model, gray, box, in_h, in_w) if box is not None else None
            now = time.perf_counter()
            current_fps = 1.0 / max(now - previous, 0.001)
            fps = current_fps if fps == 0 else 0.9*fps + 0.1*current_fps
            previous = now
            cv2.imshow(WINDOW, render(frame, scores, box, fps, dark))
            key = cv2.waitKey(1) & 0xFF
            if key in (ord('q'), ord('Q'), 27):
                break
            if key in (ord('t'), ord('T')):
                dark = not dark
            if key in (ord('f'), ord('F')):
                fullscreen = not fullscreen
                cv2.setWindowProperty(WINDOW, cv2.WND_PROP_FULLSCREEN,
                                      cv2.WINDOW_FULLSCREEN if fullscreen else cv2.WINDOW_NORMAL)
            if cv2.getWindowProperty(WINDOW, cv2.WND_PROP_VISIBLE) < 1:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        print(f"Emotion Monitor Pro: {exc}")
        raise SystemExit(1)
