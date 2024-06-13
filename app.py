from flask import Flask, request, redirect, render_template
from keras.src.saving import load_model
from keras.src.utils import load_img, img_to_array
import numpy as np
import os

app = Flask(__name__)

# Verifica se o arquivo model.h5 existe e carrega o modelo
model_path = 'model/model.h5'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Modelo não encontrado no caminho: {model_path}")

model = load_model(model_path)


# Processamento da imagem
def process_image(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image /= 255.0
    return image

@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        try:
            # Assegura que o diretório de uploads exista
            uploads_dir = 'uploads'
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)

            # Codificação do nome do arquivo para evitar problemas de caracteres
            filename = file.filename.encode('utf-8').decode('utf-8')
            image_path = os.path.join(uploads_dir, filename)
            file.save(image_path)

            if not os.path.exists(image_path):
                return "An error occurred: file was not saved properly."

            processed_image = process_image(image_path)
            prediction = model.predict(processed_image)
            class_idx = int(prediction[0][0] > 0.5)  # 0.5 é o threshold para classes binárias
            class_label = 'Pneumonia' if class_idx == 1 else 'Normal'

            # Remover a imagem após a predição
            os.remove(image_path)

            return f'Prediction: {class_label}'
        except Exception as e:
            return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True)