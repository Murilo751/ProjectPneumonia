# import os
# import warnings
# from keras.src.applications.vgg16 import VGG16
# from keras.src.legacy.preprocessing.image import ImageDataGenerator
# from tensorflow import keras
# from tensorflow.keras import layers
#
# warnings.filterwarnings('ignore')
#
# # Caminho para o conjunto de dados
# dataset_path = os.path.join(os.getcwd(), "dataset", "chest_xray")
#
# train_dir = os.path.join(dataset_path, "train")
# test_dir = os.path.join(dataset_path, "test")
# print(f"Train directory: {train_dir}")
# print(f"Test directory: {test_dir}")
#
#
# # Verifica se os diretórios existem
# if not os.path.exists(train_dir):
#     raise FileNotFoundError(f"Diretório de treino não encontrado: {train_dir}")
# if not os.path.exists(test_dir):
#     raise FileNotFoundError(f"Diretório de teste não encontrado: {test_dir}")
#
# # Parâmetros de configuração
# image_size = (224, 224)
# batch_size = 50
# epochs = 20
#
# # Configuração dos geradores de dados
# data_datagen = ImageDataGenerator(
#     rescale=1.0/255,
#     validation_split=0.20,
#     featurewise_center=False,
#     samplewise_center=False,
#     rotation_range=10,
#     zoom_range=0.1,
#     width_shift_range=0.1,
#     height_shift_range=0.1,
#     horizontal_flip=True,
#     vertical_flip=False
# )
#
# train_ds = data_datagen.flow_from_directory(
#     train_dir,
#     target_size=image_size,
#     batch_size=batch_size,
#     class_mode='binary',
#     subset='training'
# )
#
# val_ds = data_datagen.flow_from_directory(
#     train_dir,
#     target_size=image_size,
#     batch_size=batch_size,
#     class_mode='binary',
#     subset='validation'
# )
#
# test_datagen = ImageDataGenerator(rescale=1.0/255)
#
# test_ds = test_datagen.flow_from_directory(
#     test_dir,
#     target_size=image_size,
#     batch_size=batch_size,
#     class_mode='binary',
#     shuffle=True
# )
#
# # Definição do modelo com VGG16
# def my_model_with_vgg(input_size=(224, 224, 3), num_classes=1):
#     base_model = VGG16(weights='imagenet', include_top=False, input_shape=input_size)
#     base_model.trainable = False  # Congela os pesos da base
#
#     model = keras.Sequential([
#         base_model,
#         layers.BatchNormalization(),
#         layers.Flatten(),
#         layers.Dense(256, activation="relu"),
#         layers.Dense(num_classes, activation="sigmoid")
#     ])
#
#     return model
#
# model_vgg = my_model_with_vgg(input_size=(224, 224, 3), num_classes=1)
# model_vgg.summary()
#
# model_vgg.compile(
#     loss="binary_crossentropy",
#     optimizer="adam",
#     metrics=["accuracy"]
# )
#
# # Treinamento do modelo
# history = model_vgg.fit(train_ds, validation_data=val_ds, batch_size=batch_size, epochs=epochs)
#
#
# # Salvamento do modelo treinado
# model_vgg.save('model.h5')
