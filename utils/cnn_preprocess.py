import cv2
import numpy as np
from tensorflow.keras.models import load_model
import json
import os

MODEL_PATH = "models/cnn_mobilenet.h5"
CLASS_INDEX_PATH = "models/class_indices.json"
IMG_SIZE = 224

# =====================
# LOAD MODEL (SEKALI)
# =====================
model = load_model(MODEL_PATH)

with open(CLASS_INDEX_PATH, "r") as f:
    class_indices = json.load(f)

# balik index → label
index_to_label = {v: k for k, v in class_indices.items()}

# =====================
# PREDICT FUNCTION
# =====================
def predict_image(image_path):
    # [TAMBAHAN] validasi path
    if not os.path.exists(image_path):
        raise ValueError("File gambar tidak ditemukan")

    img = cv2.imread(image_path)

    # [TAMBAHAN] validasi file gambar
    if img is None:
        raise ValueError("File bukan gambar atau rusak")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img.astype("float32") / 255.0
    img = np.expand_dims(img, axis=0)

    preds = model.predict(img, verbose=0)[0]
    class_idx = int(np.argmax(preds))
    confidence = float(preds[class_idx])

    return {
        "label": index_to_label[class_idx],
        "confidence": round(confidence * 100, 2)
    }
