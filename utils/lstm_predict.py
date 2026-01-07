import cv2
import numpy as np
import mediapipe as mp
import json
from collections import deque
from tensorflow.keras.models import load_model

# =====================
# KONFIGURASI (TETAP)
# =====================
MODEL_PATH = "models/lstm_realtime.h5"
CLASS_INDEX_PATH = "models/class_index_lstm.json"

SEQUENCE_LEN = 10
NUM_FEATURES = 126
CONF_THRESHOLD = 0.6
STABLE_FRAMES = 5

# =====================
# LOAD MODEL
# =====================
model = load_model(MODEL_PATH)

with open(CLASS_INDEX_PATH) as f:
    class_to_idx = json.load(f)

idx_to_class = {v: k for k, v in class_to_idx.items()}

# =====================
# MEDIAPIPE
# =====================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# =====================
# BUFFER (TETAP)
# =====================
sequence_buffer = deque(maxlen=SEQUENCE_LEN)
prediction_buffer = deque(maxlen=STABLE_FRAMES)

# =====================
# FUNGSI ASLI (TETAP)
# =====================
def normalize_landmarks(landmarks):
    lm = np.array(landmarks)
    lm -= lm[0]
    lm /= np.max(np.linalg.norm(lm, axis=1)) + 1e-6
    return lm.flatten()

def sort_hands(hand_landmarks):
    hands_with_x = []
    for h in hand_landmarks:
        avg_x = np.mean([lm.x for lm in h.landmark])
        hands_with_x.append((avg_x, h))
    hands_with_x.sort(key=lambda x: x[0])
    return [h for _, h in hands_with_x]

# =====================
# FUNGSI WRAPPER UNTUK FLASK
# =====================
def process_frame(frame):
    # [TAMBAHAN] proteksi frame kosong
    if frame is None:
        return None, "..."

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    all_landmarks = []

    if result.multi_hand_landmarks:
        sorted_hands = sort_hands(result.multi_hand_landmarks)

        for hand_lms in sorted_hands:
            mp_draw.draw_landmarks(
                frame, hand_lms, mp_hands.HAND_CONNECTIONS
            )
            for lm in hand_lms.landmark:
                all_landmarks.append([lm.x, lm.y, lm.z])

    # =====================
    # HANDLE 1 / 2 TANGAN (TETAP)
    # =====================
    if len(all_landmarks) == 21:
        all_landmarks += [[0, 0, 0]] * 21

    if len(all_landmarks) == 42:
        features = normalize_landmarks(all_landmarks)
        sequence_buffer.append(features)
    else:
        sequence_buffer.clear()
        prediction_buffer.clear()

    label = "..."

    # =====================
    # PREDIKSI (TETAP)
    # =====================
    if len(sequence_buffer) == SEQUENCE_LEN:
        seq = np.expand_dims(sequence_buffer, axis=0)
        pred = model.predict(seq, verbose=0)[0]

        conf = float(np.max(pred))
        cls = int(np.argmax(pred))

        if conf > CONF_THRESHOLD:
            prediction_buffer.append(cls)

        if len(prediction_buffer) == STABLE_FRAMES:
            final_cls = max(
                set(prediction_buffer),
                key=prediction_buffer.count
            )
            label = f"{idx_to_class[final_cls]} ({conf*100:.1f}%)"

    # =====================
    # DISPLAY (UI handles this now)
    # =====================
    # We no longer draw on the frame as per user request
    # frame = ... (keeping frame as is from mediapipe drawing)

    return frame, label
