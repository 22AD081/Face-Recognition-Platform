from flask import Flask, request, jsonify
from flask_cors import CORS
import face_recognition
import cv2
import numpy as np
import datetime
import os
import pickle

app = Flask(__name__)
CORS(app)

ENCODINGS_PATH = "encodings.pkl"
encodings_db = {}

# Load existing encodings
if os.path.exists(ENCODINGS_PATH):
    with open(ENCODINGS_PATH, 'rb') as f:
        encodings_db = pickle.load(f)

@app.route('/register', methods=['POST'])
def register_face():
    name = request.form['name']
    file = request.files['image']
    
    # Read image from uploaded file
    in_memory_file = np.frombuffer(file.read(), np.uint8)
    img_bgr = cv2.imdecode(in_memory_file, cv2.IMREAD_COLOR)
    
    if img_bgr is None:
        return jsonify({'status': 'error', 'message': 'Image could not be decoded'})

    # Convert to RGB and ensure C-contiguous memory layout
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_rgb = np.ascontiguousarray(img_rgb)

    print(f"[DEBUG] Image shape: {img_rgb.shape}, dtype: {img_rgb.dtype}, Contiguous: {img_rgb.flags['C_CONTIGUOUS']}")

    try:
        encodings = face_recognition.face_encodings(img_rgb)
        if len(encodings) == 0:
            return jsonify({'status': 'error', 'message': 'No face detected in the image'})
        
        encodings_db[name] = encodings[0].tolist()
        #save_known_faces()
        return jsonify({'status': 'success', 'message': f'Face registered for {name}'})
    
    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/recognize', methods=['POST'])
def recognize_faces():
    file = request.files['image']

    # Read and decode image
    in_memory_file = np.frombuffer(file.read(), np.uint8)
    img_bgr = cv2.imdecode(in_memory_file, cv2.IMREAD_COLOR)

    if img_bgr is None:
        return jsonify({'status': 'error', 'message': 'Image could not be decoded'})

    # Convert to RGB and ensure it's C-contiguous
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_rgb = np.ascontiguousarray(img_rgb)

    print(f"[DEBUG] Image shape: {img_rgb.shape}, dtype: {img_rgb.dtype}, Contiguous: {img_rgb.flags['C_CONTIGUOUS']}")

    try:
        unknown_encodings = face_recognition.face_encodings(img_rgb)
        if not unknown_encodings:
            return jsonify({'status': 'error', 'message': 'No face detected in the image'})

        results = []
        for unknown_encoding in unknown_encodings:
            for name, data in encodings_db.items():
                known_encoding = data['encoding']
                match = face_recognition.compare_faces([known_encoding], unknown_encoding)[0]
                if match:
                    results.append(name)

        if results:
            return jsonify({'status': 'success', 'recognized': list(set(results))})
        else:
            return jsonify({'status': 'success', 'recognized': [], 'message': 'No known faces matched.'})

    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/stats', methods=['GET'])
def stats():
    return jsonify({
        "count": len(encodings_db),
        "last_registered": max(encodings_db.items(), key=lambda x: x[1]['timestamp'])[0] if encodings_db else None,
        "registrations": encodings_db
    })
@app.route('/', methods=['GET'])
def home():
    return "Face Recognition API is running."

if __name__ == '__main__':
    app.run(port=5001)
