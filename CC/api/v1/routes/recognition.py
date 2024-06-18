from flask import Flask,Blueprint, render_template, request, Response
import cv2
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

recognition = Blueprint('recognition', __name__)

# Load model
model = load_model('https://storage.googleapis.com/ccoba/model_trained_20bclass.h5')

clean_labels = pd.read_csv('https://storage.googleapis.com/ccoba/data_bersih.csv')

def predict_image_cv(model, image, label_map):
    # Ubah gambar menjadi skala abu-abu
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Resize gambar ke ukuran yang diharapkan oleh model
    resized_img = cv2.resize(gray, (32, 32))
    # Normalisasi nilai pixel
    resized_img = resized_img / 255.0
    # Ubah gambar menjadi array numpy dan tambahkan dimensi batch
    img_array = np.expand_dims(img_to_array(resized_img), axis=0)
    img_array = np.expand_dims(img_array, axis=-1)

    # Melakukan prediksi menggunakan model
    predictions = model.predict(img_array)

    # Mendapatkan kelas prediksi
    predicted_class = np.argmax(predictions[0])

    # Mendapatkan label dari kelas prediksi
    predicted_label = None
    predicted_menu = None
    for label, (recipe_name,class_id) in label_map.items():
        if class_id == predicted_class:
            predicted_label = label
            predicted_menu = recipe_name 
            break

    return predicted_label, predicted_menu




@recognition.route('/predict', methods=['POST'])
def predict():
    image = request.files['image']
    img_np = np.frombuffer(image.read(), np.uint8)
    frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    predicted_label, predicted_menu = predict_image_cv(model, frame, data_bersih)

    if predicted_label is not None and predicted_menu is not None:
        cv2.putText(frame, f'Prediksi: {predicted_label} ({predicted_menu})', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    ret, buffer = cv2.imencode('.jpg', frame)
    img_str = buffer.tobytes()

    return img_str