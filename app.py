import io

import numpy as np
from IPython.core.display import Image
from flask import Flask, render_template

#Webserver gateway interface
app = Flask(__name__)

model = load_model('model.h5')

def process_image(image):
    image = Image.open(io.BytesIO(image))
    image = image.resize((128, 128))
    image = np.array(image) / 255.0  # Normalizar a imagem
    image = np.expand_dims(image, axis=0)  # Adiciona dimensão de batch
    return image

@app.route('/')
def index():
    return render_template('layout.html')

@app.route('/predict', methods=['POST'])
def predict():


if __name__ == "__main__":
    app.run(debug=True)
