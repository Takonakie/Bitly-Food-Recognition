from flask import Flask, render_template, request, redirect, url_for, flash
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os
from ultralytics import YOLO
from werkzeug.utils import secure_filename
import openai
import re

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flashing messages
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load model and classes
model = YOLO('food_detection_model.pt')

class_names = model.model.names

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

        # Bangun prompt ke GPT
        prompt = f"What is the estimated calorie count for the food item {label}? Explain it in two ways: one per typical serving (e.g., per piece or per scoop), and one per 100 grams. Provide me with only the calorie numbers in two formats: per serving and per 100 grams. Do not include any other text. Format the answer as: '... per piece' for per serving and '... per 100g' for per 100 grams."

        # Panggil OpenAI API
        client = openai.OpenAI(api_key = "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")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # atau "gpt-4" jika kamu punya akses
            messages=[
                {"role": "system", "content": "You are a nutritionist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        # Ambil hasil dari GPT
        calorie_answer = response.choices[0].message.content

        numbers = re.findall(r'\d+', calorie_answer)

        calorie_answer1 = numbers[0] if len(numbers) > 0 else "N/A"
        calorie_answer2 = numbers[1] if len(numbers) > 1 else "N/A"

    return render_template(
        'estimateshowcalorie.html',
        image_filename=image_filename,
        detections=detections,
        calorie_estimate1=calorie_answer1,
        unit1="per piece",
        calorie_estimate2=calorie_answer2,
        unit2="per 100 grams"
    )

#run normal
if __name__ == '__main__':
    app.run(debug=True)
