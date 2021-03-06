# -*- coding: utf-8 -*-
"""ИАД лаба 2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-qw4DKmtnPK_32hYcwMuzVkxj94G3Fk_

**Карпычева Ангелина 18-АС**
"""

from google.colab import drive
drive.mount('/content/drive')

"""Загрузка датасета"""

from keras.datasets import cifar10 as cifar

(x_train, y_train), (x_test, y_test) = cifar.load_data()

"""Получение части данных для валидации"""

from sklearn.model_selection import train_test_split
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.3, random_state=0)

"""Предобработка данных"""

from keras.datasets import cifar10
from keras.utils import to_categorical
import matplotlib.pyplot as plt

x_train.astype('float32')
x_val.astype('float32')
x_test.astype('float32')

y_train.astype('float32')
y_val.astype('float32')
y_test.astype('float32')

y_train = to_categorical(y_train)
y_val = to_categorical(y_val)
y_test = to_categorical(y_test)

"""Оригинальная архитектура VGG16"""

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
import keras.regularizers as regularizers
!pip install -U pydot-ng, graphviz
from keras.applications import VGG16
from keras.optimizers import Adam
import cv2
from google.colab.patches import cv2_imshow
from keras.utils import plot_model

model = Sequential()
weight_decay = 0.0005
x_shape = [32,32,3]


model.add(Conv2D(64, (3, 3), padding='same', input_shape=x_shape, activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(Dropout(0.3))
model.add(Conv2D(64, (3, 3), padding='same', activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))


model.add(Conv2D(128, (3, 3), padding='same', activation='relu',kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(Dropout(0.4))
model.add(Conv2D(128, (3, 3), padding='same', activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(256, (3, 3), padding='same', activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(Dropout(0.4))
model.add(Conv2D(256, (3, 3), padding='same', activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(Dropout(0.4))
model.add(Conv2D(256, (3, 3), padding='same', activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))


model.add(Conv2D(512, (3, 3), padding='same', activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(Dropout(0.4))
model.add(Conv2D(512, (3, 3), padding='same', activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(Dropout(0.4))
model.add(Conv2D(512, (3, 3), padding='same', activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))


model.add(Conv2D(512, (3, 3), padding='same', activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(Dropout(0.4))
model.add(Conv2D(512, (3, 3), padding='same', activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(Dropout(0.4))
model.add(Conv2D(512, (3, 3), padding='same', activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(4096, activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(4096, activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(10))
model.add(Activation('softmax'))

model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
plot_model(model, to_file='model.png', show_shapes=True)  
cv2_imshow(cv2.imread('model.png'))

"""Создание генераторов"""

from keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        rescale=1./255
)

batch_size = 32
epochs = 50

train_generator = datagen
train_generator.fit(x_train)
train_generator = datagen.flow(x_train, y_train, batch_size=batch_size)
val_generator = ImageDataGenerator(rescale=1./255)
val_generator.fit(x_val)
val_generator = val_generator.flow(x_val, y_val, batch_size=batch_size)
test_generator = ImageDataGenerator(rescale=1./255)
test_generator.fit(x_test)
test_generator = test_generator.flow(x_test, y_test, batch_size=batch_size)

"""Тренировка базовой модели с аугментацией


"""

history = model.fit(
    train_generator,
    steps_per_epoch=x_train.shape[0]//batch_size,
    epochs=epochs,
    validation_data=val_generator,
    validation_steps=250
).history

model.save('/content/drive/MyDrive/ИАД_ЛАБЫ/base_model.h5')

"""График тренировки"""

import matplotlib.pyplot as plt

def smooth_curve(points, factor=0.8):
  smoothed_points = []
  for point in points:
    if smoothed_points:
      previous = smoothed_points[-1]
      smoothed_points.append(previous * factor + point * (1 - factor))
    else:
      smoothed_points.append(point)
  return smoothed_points

def draw_smooth_graph(history):
    loss_values = history["loss"]
    validation_loss_values = history["val_loss"]

    epochs = range(1, len(history['loss']) + 1)

    plt.plot(epochs, smooth_curve(loss_values), 'b', label='Training loss')
    plt.plot(epochs, smooth_curve(validation_loss_values), 'r', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Value')
    plt.legend()
    plt.show()

draw_smooth_graph(history)

"""Создание новой архитектуры (уменьшенной)

"""

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
import keras.regularizers as regularizers

model_2 = Sequential()
weight_decay = 0.0005
x_shape = [32,32,3]

model_2.add(Conv2D(64, (3, 3), padding='same', input_shape=x_shape, activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model_2.add(BatchNormalization())
model_2.add(Dropout(0.3))
model_2.add(Conv2D(64, (3, 3), padding='same', activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model_2.add(BatchNormalization())
model_2.add(MaxPooling2D(pool_size=(2, 2)))

model_2.add(Conv2D(128, (3, 3), padding='same', activation='relu',kernel_regularizer=regularizers.l2(weight_decay)))
model_2.add(BatchNormalization())
model_2.add(Dropout(0.4))
model_2.add(Conv2D(128, (3, 3), padding='same', activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model_2.add(BatchNormalization())
model_2.add(MaxPooling2D(pool_size=(2, 2)))

model_2.add(Flatten())
model_2.add(Dense(4096, activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model_2.add(BatchNormalization())
model_2.add(Dropout(0.5))
model_2.add(Dense(4096, activation='relu', kernel_regularizer=regularizers.l2(weight_decay)))
model_2.add(BatchNormalization())
model_2.add(Dropout(0.5))
model_2.add(Dense(10))
model_2.add(Activation('softmax'))

model_2.summary()

model_2.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

history_2 = model_2.fit(
    train_generator,
    steps_per_epoch=x_train.shape[0]//batch_size,
    epochs=epochs,
    validation_data=val_generator,
    validation_steps=250
).history

model_2.save('/content/drive/MyDrive/ИАД_ЛАБЫ/model_2.h5')

(loss_2, accuracy_2) = model_2.evaluate(test_generator, verbose=1)
print(f'Loss is {loss_2}')
print(f'Accuracy is {accuracy_2}')

def smooth_curve(points, factor=0.8):
  smoothed_points = []
  for point in points:
    if smoothed_points:
      previous = smoothed_points[-1]
      smoothed_points.append(previous * factor + point * (1 - factor))
    else:
      smoothed_points.append(point)
  return smoothed_points

def draw_smooth_graph(history):
    loss_values = history["loss"]
    validation_loss_values = history["val_loss"]

    epochs = range(1, len(history['loss']) + 1)

    plt.plot(epochs, smooth_curve(loss_values), 'b', label='Training loss')
    plt.plot(epochs, smooth_curve(validation_loss_values), 'r', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Value')
    plt.legend()
    plt.show()

draw_smooth_graph(history_2)

from keras.models import load_model
best_model = load_model('/content/drive/MyDrive/ИАД_ЛАБЫ/model_2.h5')

"""Предсказание новой модели без шума"""

import random
import numpy as np
import matplotlib.pyplot as plt

img = x_train[random.randint(0, len(x_train)-1)]
img = np.expand_dims(img, axis=0)

img_to_show = img.copy().astype('float32')
img_to_show /= 255
plt.imshow(img_to_show[0])

classes = ['airplane', 'automobile','bird','cat','deer','dog','frog','horse','ship','truck']
predictions = list(best_model.predict(img)[0])
sorted_predictions = sorted(predictions)[::-1]
for i, pred in enumerate(sorted_predictions):
  if (i < 1) and (pred != 0.):
    print(f'Top {i+1} prediction is {classes[predictions.index(pred)]} ({str(pred*100)[:5]}%) (on standart picture)')

"""С шумом"""

def apply_noise(img, SNR=5):
  signal_power = np.square(img)
  signal_average_power = np.mean(signal_power)
  max_noise = signal_average_power / SNR
  mean_noise = 0
  noise = np.random.normal(mean_noise, np.sqrt(max_noise), size = img.shape)
  noised_img = img + noise
  return noised_img

noised_img = apply_noise(img, 5)

img_to_show = noised_img.copy()
img_to_show /= 255
plt.imshow(img_to_show[0])

classes = ['airplane', 'automobile','bird','cat','deer','dog','frog','horse','ship','truck']
predictions = list(best_model.predict(noised_img)[0])
sorted_predictions = sorted(predictions)[::-1]
for i, pred in enumerate(sorted_predictions):
  if (i < 1) and (pred != 0.):
    print(f'Top {i+1} prediction is {classes[predictions.index(pred)]} ({str(pred*100)[:5]}%) (on noisy picture)')

"""Точность на зашумленном датасете"""

def apply_noise_on_dataset(data):
  noisy_data = np.zeros((data.shape))
  i = 0
  for img in data:
    noisy_img = apply_noise(img, 5)
    noisy_data[i] = noisy_img
    i += 1
  return noisy_data

noisy_test_generator = ImageDataGenerator(rescale=1./255)
noisy_test_generator = noisy_test_generator.flow(apply_noise_on_dataset(x_test), y_test, batch_size=32)

(loss, accuracy) = best_model.evaluate(test_generator,verbose=1)
print(f'On raw dataset accuracy is {accuracy}')

(loss, accuracy) = best_model.evaluate(noisy_test_generator, verbose=1)
print(f'On noisy dataset accuracy is {accuracy}')

"""Карты признаков слоев новой сети"""

from keras.models import Model

layer_outputs = [layer.output for layer in best_model.layers]
activation_model = Model(inputs=best_model.input, outputs=layer_outputs)

best_model.summary()

activations = activation_model.predict(img)
layer_names = [layer.name for layer in best_model.layers]

images_per_row = 16
for layer_name, layer_activation in zip(layer_names, activations):
  if 'conv' not in layer_name:
    continue
  n_features = layer_activation.shape[-1]
  size = layer_activation.shape[1]

  n_cols = n_features // images_per_row
  display_grid = np.zeros((size * n_cols, size * images_per_row))

  for col in range(n_cols):
    for row in range(images_per_row):
      channel_image = layer_activation[0, :, :, col * images_per_row + row]
      channel_image -= channel_image.mean()
      channel_image /= channel_image.std()
      channel_image *= 64
      channel_image += 128
      channel_image = np.clip(channel_image, 0, 255).astype('uint8')
      display_grid[col * size : (col + 1) * size, row * size : (row + 1) * size] = channel_image
  
  scale = 1. / size
  plt.figure(figsize=(scale * display_grid.shape[1], scale * display_grid.shape[0]))
  plt.title(layer_name)
  plt.grid(False)
  plt.imshow(display_grid, aspect='auto', cmap='viridis')

"""Матрицы свертки слоев новой сети"""

def visualise_layer_filters(model, layer_name, num_filters):
  import matplotlib.pyplot as plt
  layer = model.get_layer(layer_name)
  layer_filters, _ = layer.get_weights()
  channels = 3
  num_cells = channels * num_filters
  place = plt.figure(figsize=(10, 30))
  for i in range(1, num_cells + 1):
    f = layer_filters[:, :, :, i-1]
    for j in range(channels):
      fig = place.add_subplot(num_cells, channels, i)
      fig.set_xticks([]) 
      fig.set_yticks([])
      plt.imshow(f[:, :, j], cmap='viridis')  
  plt.show()    

# последний сверточный слой
visualise_layer_filters(best_model, best_model.layers[-12].name, 6)