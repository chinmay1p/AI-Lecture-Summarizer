import cv2
import numpy as np
import tensorflow as tf
import os
import gc

_model = tf.keras.applications.MobileNetV2(
    include_top=False,
    weights='imagenet',
    input_shape=(224, 224, 3),
    pooling='avg'
)

def _prep(frame):
    img = cv2.resize(frame, (224, 224))
    arr = tf.keras.preprocessing.image.img_to_array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = tf.keras.applications.mobilenet_v2.preprocess_input(arr)
    return arr

def _emb(frame):
    p = _prep(frame)
    e = _model.predict(p)
    return e.flatten()

def _cos(v1, v2):
    d = np.dot(v1, v2)
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    return d / (n1 * n2)

def extract_keyframes(video_path, output_dir, sim_th=0.98):
    print(f"Starting keyframe extraction for {video_path}...")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return []

    paths = []
    last = None
    i = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if i % 15 == 0:
            cur = _emb(frame)
            if last is None:
                is_new = True
            else:
                sim = _cos(cur, last)
                is_new = sim < sim_th
            if is_new:
                saved += 1
                name = f"keyframe_{saved:04d}.png"
                path = os.path.join(output_dir, name)
                cv2.imwrite(path, frame)
                paths.append(path)
                print(f"  - New slide detected. Saved {name} (Similarity: {sim if last is not None else 'N/A'})")
                last = cur
                gc.collect()
        i += 1

    cap.release()
    print(f"Keyframe extraction complete. Found {saved} unique slides.")
    return paths

