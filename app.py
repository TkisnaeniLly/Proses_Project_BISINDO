from flask import Flask, render_template, request, jsonify, Response
import os
import cv2

# =====================
# IMPORT LOGIC ML
# =====================
from utils.cnn_preprocess import predict_image
from utils.lstm_predict import process_frame

# =====================
# FLASK CONFIG
# =====================
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# =====================
# CAMERA (LSTM)
# =====================
camera = cv2.VideoCapture(0)

# =====================
# STATE ML
# =====================
latest_lstm_prediction = "..."

# =====================
# PAGE ROUTES
# =====================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload")
def upload_page():
    return render_template("translate_upload.html")

@app.route("/realtime")
def realtime_page():
    return render_template("translate_realtime.html")

@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")

# =====================
# API ENDPOINTS
# =====================

@app.route("/predict-upload", methods=["POST"])
def predict_upload():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)

    try:
        result = predict_image(path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get-realtime-prediction")
def get_realtime_prediction():
    return jsonify({"label": latest_lstm_prediction})

# =====================
# LSTM - REALTIME STREAM
# =====================

def generate_frames():
    global latest_lstm_prediction
    while True:
        if not camera.isOpened():
            continue

        success, frame = camera.read()
        if not success:
            continue

        try:
            # Update: Sekarang mengembalikan (frame, label)
            frame, label = process_frame(frame)
            latest_lstm_prediction = label
            if frame is None:
                continue
        except Exception as e:
            print(f"Error processing frame: {e}")
            continue

        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            buffer.tobytes() +
            b"\r\n"
        )

@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

# =====================
# MAIN
# =====================

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
