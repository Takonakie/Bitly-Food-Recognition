from flask import Flask, render_template, request, redirect, url_for, flash
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os
from ultralytics import YOLO
from werkzeug.utils import secure_filename

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flashing messages
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load model and classes
model = YOLO('models/food_detection_model.pt')

# Hardcoded class names (order must match the training .yaml file)
class_names = [
    "baklava", "beignets", "chocolate_cake", "churros", "cup_cakes",
    "donuts", "ice_cream", "macarons", "red_velvet_cake", "waffles"
]
calorie_mapping = {
    "baklava": [290, "per piece", 430, "per 100g"],
    "beignets": [250, "per piece", 390, "per 100g"],
    "chocolate_cake": [370, "per slice", 350, "per 100g"],
    "churros": [116, "per stick (15cm)", 330, "per 100g"],
    "cup_cakes": [180, "per cupcake", 305, "per 100g"],
    "donuts": [452, "per donut", 452, "per 100g"],
    "ice_cream": [137, "per scoop (1/2 cup)", 207, "per 100g"],
    "macarons": [70, "per piece", 440, "per 100g"],
    "red_velvet_cake": [410, "per slice", 370, "per 100g"],
    "waffles": [218, "per waffle (plain)", 290, "per 100g"]
}
# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estimate')
def estimate():
    return render_template('estimate.html')

@app.route('/aboutpage')
def aboutpage():
    return render_template('aboutpage.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

# Image upload and redirect to description page
@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        flash("No file part in the request.")
        return redirect(url_for('index'))

    file = request.files['image']
    if file.filename == '':
        flash("No file selected.")
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Redirect to estimatedescription page with the image path
        return redirect(url_for('estimatedescription', image_filename=filename))

    else:
        flash("Invalid file type. Only PNG, JPG, and JPEG files are allowed.")
        return redirect(url_for('index'))

# Show uploaded image on estimatedescription page
@app.route('/estimatedescription')
def estimatedescription():
    image_filename = request.args.get('image_filename')
    return render_template('estimatedescription.html', image_filename=image_filename)

# Predict calorie information after description is reviewed
@app.route('/calculate_calorie', methods=['POST'])
def calculate_calorie():
    #description = request.form['description']
    image_filename = request.form['image_filename']

    # Predict using YOLO model
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    results = model(image_path, save=False)[0]

    # Parse predictions
    detections = []
    calorie_estimate = "Unknown"

    for box in results.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        #label = f"{class_names[class_id]}: {confidence:.2f}"
        label = f"{class_names[class_id]}"
        detections.append(label)

        # Lookup calories from mapping
        calorie_value1, unit1, calorie_value2, unit2 = calorie_mapping.get(label, ["N/A", "Unknown"])
        calorie_estimate1 = f"{calorie_value1} kcal"
        calorie_estimate2 = f"{calorie_value2} kcal"

    return render_template('estimateshowcalorie.html', image_filename=image_filename, calorie_estimate1=calorie_estimate1, unit1=unit1, calorie_estimate2=calorie_estimate2, unit2=unit2, detections=detections[0])

#run normal
if __name__ == '__main__':
    app.run(debug=True)
