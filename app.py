from flask import Flask, render_template, request, redirect
import numpy as np
import json
import uuid
import os
import base64
import tensorflow as tf
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
UPLOAD_FOLDER = './uploadimages'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ── Models ────────────────────────────────────────────────────────────────────
model = tf.keras.models.load_model("models/plant_health_mobilenetv2_model.keras")
cnn_model = tf.keras.models.load_model("models/plant_health_cnn_model.keras")

with open("models/class_names.txt", 'r') as f:
    class_names = [line.strip() for line in f.readlines()]

with open("plant_disease.json", 'r') as file:
    plant_disease_list = json.load(file)

# Build a lookup dict for fast access: {"Tomato___Early_blight": {...}, ...}
disease_lookup = {entry['name']: entry for entry in plant_disease_list}

# ── Helpers ───────────────────────────────────────────────────────────────────
def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )

def extract_features(image_path):
    image = tf.keras.utils.load_img(image_path, target_size=(160, 160))
    feature = tf.keras.utils.img_to_array(image)
    return np.array([feature])

def model_predict(image_path, selected_model):
    img = extract_features(image_path)
    prediction = selected_model.predict(img)[0]

    # Top-3 predictions
    top3_idx = prediction.argsort()[::-1][:3]
    top3 = []
    for idx in top3_idx:
        class_name = class_names[idx]
        parts = class_name.split('___')
        label = f"{parts[0].replace('_', ' ').title()}"
        if len(parts) > 1:
            label += f" — {parts[1].replace('_', ' ').title()}"
        top3.append({
            'label': label,
            'confidence': f"{prediction[idx] * 100:.1f}%"
        })

    # Top prediction
    top_idx = top3_idx[0]
    top_class = class_names[top_idx]
    confidence = prediction[top_idx] * 100

    # Handle background class
    if 'background' in top_class.lower():
        return {
            'status': 'UNRECOGNIZED',
            'plant': 'Not a plant leaf',
            'condition': 'Please upload a clear leaf image',
            'confidence': f"{confidence:.1f}%",
            'cause': None,
            'cure': None,
            'top3': top3
        }

    parts = top_class.split('___')
    plant = parts[0].replace('_', ' ').title()
    condition = parts[1].replace('_', ' ').title() if len(parts) > 1 else "Unknown"
    status = "HEALTHY" if "healthy" in condition.lower() else "DISEASED"

    # Look up disease info
    disease_info = disease_lookup.get(top_class, {})

    return {
        'status': status,
        'plant': plant,
        'condition': condition,
        'confidence': f"{confidence:.1f}%",
        'cause': disease_info.get('cause', None),
        'cure': disease_info.get('cure', None),
        'top3': top3
    }

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/upload/', methods=['POST', 'GET'])
def uploadimage():
    if request.method != "POST":
        return redirect('/')

    image = request.files.get('img')

    if not image or image.filename == '':
        return render_template('home.html', error="No file selected.")

    if not allowed_file(image.filename):
        return render_template('home.html', error="Only PNG and JPEG images are allowed.")

    model_choice = request.form.get('model_choice', 'mobilenet')
    selected_model = model if model_choice == 'mobilenet' else cnn_model

    image_bytes = image.read()
    ext = image.filename.rsplit('.', 1)[1].lower()
    mime = 'image/png' if ext == 'png' else 'image/jpeg'
    image_data_url = f"data:{mime};base64,{base64.b64encode(image_bytes).decode('utf-8')}"

    safe_name = secure_filename(image.filename)
    unique_name = f"{uuid.uuid4().hex}_{safe_name}"
    temp_path = os.path.join(UPLOAD_FOLDER, unique_name)

    try:
        with open(temp_path, 'wb') as f:
            f.write(image_bytes)
        prediction = model_predict(temp_path, selected_model)
    except Exception as e:
        return render_template('home.html', error=f"Prediction failed: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return render_template('home.html',
                           result=True,
                           image_data_url=image_data_url,
                           prediction=prediction)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))