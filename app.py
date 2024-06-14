from flask import Flask, request, redirect, render_template
from keras.src.saving import load_model
from keras.src.utils import load_img, img_to_array
import numpy as np
import os

app = Flask(__name__)

model_path = 'model/model.h5'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Modelo não encontrado no caminho: {model_path}")

model = load_model(model_path)


def process_image(image_path):
    image = load_img(image_path, target_size=(150, 150))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image /= 255.0
    return image

@app.route('/')
def index():
    return render_template('layout.html')


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        try:
            uploads_dir = 'uploads'
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)

            filename = file.filename.encode('utf-8').decode('utf-8')
            image_path = os.path.join(uploads_dir, filename)
            file.save(image_path)

            if not os.path.exists(image_path):
                error_message = "An error occurred: file was not saved properly."
                with open('error_log.txt', 'w', encoding='utf-8') as f:
                    print(error_message, file=f)
                return error_message

            processed_image = process_image(image_path)
            prediction = model.predict(processed_image)
            class_idx = int(prediction[0][0] > 0.5)  # 0.5 é o threshold para classes binárias
            class_label = 'Pneumonia' if class_idx == 1 else 'Normal'

            os.remove(image_path)

            prediction_message = f'Prediction: {class_label}'
            with open('prediction_log.txt', 'w', encoding='utf-8') as f:
                print(prediction_message, file=f)

            return prediction_message
        except Exception as e:
            error_message = f"An error occurred: {e}"
            with open('error_log.txt', 'w', encoding='utf-8') as f:
                print(error_message, file=f)
            return error_message

if __name__ == "__main__":
    app.run(debug=True)