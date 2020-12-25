# -*- coding: utf-8 -*-
"""ИАД лаба1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hr86YTwzIqJJ16QAK0iZ8YeoVbIiB6qA

**Карпычева Ангелина 18-АС**
"""

from google.colab import drive
drive.mount('/content/drive')

"""# Подключение библиотек"""

!pip install -U keras-tuner
!pip install -U pygal
import pandas as pd
import numpy as np
from tensorflow.keras.datasets import boston_housing
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns
from keras.regularizers import L1, L2
from sklearn.impute import SimpleImputer
from kerastuner.tuners import RandomSearch, Hyperband, BayesianOptimization
from sklearn.preprocessing import MinMaxScaler

"""# Подготовка данных"""

data = pd.read_csv("/content/drive/My Drive/train.csv")
data

"""Получение целевых ответов"""

y = data.get('revenue')
data.drop('revenue', axis='columns', inplace=True)
data.drop('Id', axis='columns', inplace=True)
y = np.array(y)
y

"""Список признаков, зашифрованных буквенно"""

words = [var for var in data.columns if data[var].dtypes == 'O']

data[words]

"""Перевод буквенных признаков в числовые"""

df = pd.DataFrame(data[words])
data[words] = df.apply(preprocessing.LabelEncoder().fit_transform)

data[words]

data

"""# Нормализация данных"""

def normalize(data):
  # Среднее значение
  mean = data.mean(axis=0)
  # Стандартное отклонение
  std = data.std(axis=0)
  data -= mean
  data /= std
  return data

data = normalize(data)
data

"""Разделение на тренировочные и тестовые данные"""

x_train, x_test, y_train, y_test = train_test_split(data, y, test_size=0.2, random_state=2)

"""# Создание сети с двумя крупными слоями и ее тренировка"""

model = Sequential()
model.add(Dense(4096, activation='relu', input_shape=(x_train.shape[1],)))
model.add(Dropout(0.2))
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1))
model.summary()

model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])

history=model.fit(x_train, y_train, epochs=100, batch_size=1, verbose=1, validation_split=0.3)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model mae')
plt.ylabel('mae')
plt.xlabel('epoch')
plt.legend(['train_loss', 'val_loss'], loc='upper right')
plt.show()

"""Предсказание модели, созданной вручную."""

pred = model.predict(x_test)
pred = np.reshape(pred, (pred.shape[0]))
correct = np.reshape(y_test, (y_test.shape[0]))

"""# Подсчет коэффициента корреляции модели, созданной вручную"""

cc = np.corrcoef(pred, correct)
ccc = cc[0][1]
print(f'Correlation Coefficient: {ccc}')

! rm -rf untitled_project/

"""# Поиск лучшей модели с помощью keras tuner"""

def build_model(hp):
  hidden_layers = hp.Choice('hidden_layers', values=[1,2,3])
  activation_choice = hp.Choice('activation', values=['relu', 'selu', 'elu'])
  model = Sequential()
  model.add(Dense(units=hp.Int('units',min_value=16,max_value=256,step=32),activation=activation_choice, input_shape=(x_train.shape[1],)))
  model.add(Dropout(0.2))
  for i in range(hidden_layers):
    model.add(Dense(units=hp.Int(f'layer_{i}_units_',min_value=16//(i+1), max_value=256//(i+1),step=32//(i+1)),activation=activation_choice))
    model.add(Dropout(0.2))
  model.add(Dense(1))  
  model.compile(optimizer='rmsprop', loss="mse", metrics=["mae"])
  return model

def find_best_NN(x_train_main, y_train_main):
  tuner = Hyperband(build_model, objective="loss", max_epochs=10, hyperband_iterations=10)
  tuner.search(x_train, y_train, batch_size=1, epochs=10, validation_split=0.3)
  tuner.results_summary()
  print("\n\n\n")
  print("\n\n\nHERE IS THE BEST MODEL\n\n\n")
  best_params = tuner.get_best_hyperparameters()[0]
  best_model = tuner.hypermodel.build(best_params)
  best_model.summary()
  return best_model
  

best_model = find_best_NN(x_train, y_train)

"""# Обучение лучшей модели"""

best_history = best_model.fit(x_train, y_train, epochs=250, batch_size=1, validation_split=0.2)

plt.plot(best_history.history['loss'])
plt.plot(best_history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train_loss', 'val_loss'], loc='upper right')
plt.show()

pred = best_model.predict(x_test)
pred = np.reshape(pred, (pred.shape[0]))
correct = np.reshape(y_test, (y_test.shape[0]))

"""# Подсчет коэффициента корреляции лучшей модели"""

cc = np.corrcoef(pred, correct)
ccc = cc[0][1]
print(f'Correlation Coefficient: {ccc}')