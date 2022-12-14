# -*- coding: utf-8 -*-
"""LSTM(final).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1D0KMM-7Qhf7vKHucjPhjEAPBOgNVlXJP
"""

import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.optimizers import RMSprop

from google.colab import drive
drive.mount('/content/drive')

from keras.layers import Conv2D, MaxPooling2D
from keras.layers import BatchNormalization

from imutils import paths
import keras.backend as K

from numpy import mean
from numpy import std
from matplotlib import pyplot
from sklearn.model_selection import KFold
from keras.datasets import fashion_mnist
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from tensorflow.keras.optimizers import SGD
from numpy import array

import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import datasets, layers, models

from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint

"""Image uploading"""

imagepaths = list(paths.list_images("/Users/tharun/Desktop/tn/gb"))

print(len(imagepaths))



# data = []
# labels = []
# for images in tqdm(imagepaths):
#     label = images.split(os.path.sep)[-2]
#     image =cv2.imread(images)
#     image =cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
#     image =cv2.resize(image, (256,256))
#     image = np.asarray(image)
#     image = np.reshape(image,(256,768))
#     data.append(image)
#     labels.append(label)

testpaths = list(paths.list_images("/Users/tharun/Desktop/mlproject/Garbage Dataset/test"))

from tqdm import tqdm

# testdata = []
# testlabels = []
# for images in tqdm(testpaths):
#     label = images.split(os.path.sep)[-2]
#     image =cv2.imread(images)
#     image =cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
#     image =cv2.resize(image, (30,30))
#     image = np.asarray(image)
#     image = np.reshape(image,(30,90))
#     testdata.append(image)
#     testlabels.append(label)

# from sklearn.preprocessing import LabelEncoder
# lb = LabelEncoder()
# labels = lb.fit_transform(labels)
# testlabels = lb.fit_transform(testlabels)

"""# **If having pickle file**"""

import pickle
data = pickle.load(open('/content/drive/MyDrive/Garbage/traindata.pkl','rb'))
labels = pickle.load(open('/content/drive/MyDrive/Garbage/trainlabels.pkl','rb'))
testdata = pickle.load(open('/content/drive/MyDrive/Garbage/testdata.pkl','rb'))
testlabels = pickle.load(open('/content/drive/MyDrive/Garbage/testlabels.pkl','rb'))

#for inclass
import pickle
data = pickle.load(open('/content/drive/MyDrive/Garbage/traindata.pkl','rb'))
labels = pickle.load(open('/content/drive/MyDrive/Garbage/trainlabels.pkl','rb'))
itestdata = pickle.load(open('/content/drive/MyDrive/Garbage/itestdata.pkl','rb'))
itestlabels = pickle.load(open('/content/drive/MyDrive/Garbage/itestlabels.pkl','rb'))

idat = []
for i in data:
    i=np.reshape(i,(32,96))
    idat.append(i)
data = idat

idat = []
for i in itestdata:
    i=np.reshape(i,(32,96))
    idat.append(i)
itestdata = idat

mapping = ['construction debris', 'e waste', 'green waste', 'medical waste', 'ocean waste', 'Papers _ cards', 'Plastics', 'recyclable waste', 'trash']

def index(x):
    for i in range(9):
        if(mapping[i] == x):
            return i;
    return -1;

ilabels = []
for l in labels:
    ilabels.append(index(l))
labels = ilabels

ilabels = []
for l in itestlabels:
    ilabels.append(index(l))
itestlabels = ilabels

def prep_pixels(train, test):
 	# convert from integers to floats
 	train_norm = np.array(train).astype('float32')
 	test_norm = np.array(test).astype('float32')
 	# normalize to range 0-1
 	train_norm = train_norm / 255.0
 	test_norm = test_norm/ 255.0
 	# return normalized images
 	return train_norm, test_norm

data, itestdata = prep_pixels(data, itestdata)

data = np.asarray(data)
labels = np.asarray(labels)
itestdata=np.asarray(itestdata)
itestlabels=np.asarray(itestlabels)

print(data.shape)
print(itestdata.shape)
print(labels.shape)
print(itestlabels.shape)

testdata.shape



"""# **Creating a model and training**






"""

model1 = models.Sequential()
model1.add(layers.LSTM(50, input_shape = (32, 96), activation = 'tanh', return_sequences = True, recurrent_activation='sigmoid', recurrent_dropout = 0.0, unroll=False ,use_bias=True))
model1.add(layers.Dropout(0.15))
model1.add(layers.LSTM(50, activation = 'tanh',recurrent_activation='sigmoid',recurrent_dropout = 0.0,unroll=False ,use_bias=True))
model1.add(layers.Dropout(0.25))
model1.add(layers.Flatten())
model1.add(layers.Dense(50,activation = 'relu'))
model1.add(layers.Dropout(0.04))
model1.add(layers.Dense(9,activation = 'softmax'))
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5 , decay = 1e-6)
model1.compile(loss = tf.keras.losses.SparseCategoricalCrossentropy(),
              optimizer = 'adam',
              metrics = ['accuracy'])
model1.summary()

# from keras.callbacks import EarlyStopping
# from keras.callbacks import ModelCheckpoint
# es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=8)
# mc = ModelCheckpoint('best_model.h5', monitor='val_accuracy', mode='max', verbose=1, save_best_only=True)

es = EarlyStopping(monitor='val_loss', mode='min', verbose=2, patience=15)

mc = ModelCheckpoint('/content/drive/MyDrive/Garbage/model/best_model_8l_normal1.h5', monitor='val_accuracy', mode='max', verbose=2, save_best_only=True)

history = model1.fit(data, labels, validation_data=(testdata, testlabels),  epochs=400, verbose=2, callbacks=[es, mc])

import pandas as pd
import h5py

hist_df = pd.DataFrame(history.history) 
hist_csv_file = '/content/drive/MyDrive/Garbage/csv/LSTM01.csv'
with open(hist_csv_file, mode='w') as f:
    hist_df.to_csv(f)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
model1.save('/content/drive/MyDrive/Garbage/converged_models/LSTM01.h5')

model2 = models.Sequential()
model2.add(layers.LSTM(50, input_shape = (32, 96), activation = 'tanh', return_sequences = True, recurrent_activation='sigmoid', recurrent_dropout = 0.0, unroll=False ,use_bias=True))
model2.add(layers.Dropout(0.15))
model2.add(layers.LSTM(50, activation = 'tanh', return_sequences = True,recurrent_activation='sigmoid',recurrent_dropout = 0.0,unroll=False ,use_bias=True))
model2.add(layers.Dropout(0.25))
model2.add(layers.LSTM(50, activation = 'tanh',recurrent_activation='sigmoid',recurrent_dropout = 0.0,unroll=False ,use_bias=True))
model2.add(layers.Dropout(0.35))
model2.add(layers.Flatten())
model2.add(layers.Dense(50,activation = 'tanh'))
model2.add(layers.Dropout(0.04))
model2.add(layers.Dense(9,activation = 'softmax'))
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5 , decay = 1e-6)
model2.compile(loss = tf.keras.losses.SparseCategoricalCrossentropy(),
              optimizer = 'adam',
              metrics = ['accuracy'])
model2.summary()

es = EarlyStopping(monitor='val_loss', mode='min', verbose=2, patience=15)

mc = ModelCheckpoint('/content/drive/MyDrive/Garbage/model/best_model_8l_normal2.h5', monitor='val_accuracy', mode='max', verbose=2, save_best_only=True)

history = model2.fit(data, labels, validation_data=(testdata, testlabels),  epochs=400, verbose=2, callbacks=[es, mc])

import pandas as pd
import h5py

hist_df = pd.DataFrame(history.history) 
hist_csv_file = '/content/drive/MyDrive/Garbage/csv/LSTM02.csv'
with open(hist_csv_file, mode='w') as f:
    hist_df.to_csv(f)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
model2.save('/content/drive/MyDrive/Garbage/converged_models/LSTM02.h5')

model3 = models.Sequential()
model3.add(layers.LSTM(50, input_shape = (32, 96), activation = 'tanh', return_sequences = True, recurrent_activation='sigmoid', recurrent_dropout = 0.0, unroll=False ,use_bias=True))
model3.add(layers.Dropout(0.15))
model3.add(layers.LSTM(50, activation = 'tanh', return_sequences = True,recurrent_activation='sigmoid',recurrent_dropout = 0.0,unroll=False ,use_bias=True))
model3.add(layers.Dropout(0.25))
model3.add(layers.LSTM(50, activation = 'tanh', return_sequences = True,recurrent_activation='sigmoid',recurrent_dropout = 0.0,unroll=False ,use_bias=True))
model3.add(layers.Dropout(0.35))
model3.add(layers.LSTM(50, activation = 'tanh',recurrent_activation='sigmoid',recurrent_dropout = 0.0,unroll=False ,use_bias=True))
model3.add(layers.Dropout(0.45))
model3.add(layers.Flatten())
model3.add(layers.Dense(50,activation = 'relu'))
model3.add(layers.Dropout(0.04))
model3.add(layers.Dense(9,activation = 'softmax'))
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5 , decay = 1e-6)
model3.compile(loss = tf.keras.losses.SparseCategoricalCrossentropy(),
              optimizer = 'adam',
              metrics = ['accuracy'])
model3.summary()

es = EarlyStopping(monitor='val_loss', mode='min', verbose=2, patience=15)

mc = ModelCheckpoint('/content/drive/MyDrive/Garbage/model/best_model_8l_normal3.h5', monitor='val_accuracy', mode='max', verbose=2, save_best_only=True)

history = model3.fit(data, labels, validation_data=(testdata, testlabels),  epochs=400, verbose=2, callbacks=[es, mc])

import pandas as pd
import h5py

hist_df = pd.DataFrame(history.history) 
hist_csv_file = '/content/drive/MyDrive/Garbage/csv/LSTM03.csv'
with open(hist_csv_file, mode='w') as f:
    hist_df.to_csv(f)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
model3.save('/content/drive/MyDrive/Garbage/converged_models/LSTM03.h5')

saved_model = models.load_model('/content/drive/MyDrive/1,3,4/model/best_model_4layers.h5')
# evaluate the model
_, train_acc = saved_model.evaluate(data, labels, verbose=2)
_, test_acc = saved_model.evaluate(testdata, testlabels, verbose=2)
print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))

from sklearn.metrics import confusion_matrix
#Generate predictions with the model using our X values
y_pred_arr = saved_model.predict(testdata)

y_pred = []
def intonum(pred):
  res = 0
  max = -1
  for i in range(9):
    if pred[i] > max:
      max = pred[i]
      res = i
  return res

for i in y_pred_arr:
  y_pred.append(intonum(i))

y_pred_arr = np.asarray(y_pred_arr)

y_true = testlabels
#Get the confusion matrix
cf_matrix = confusion_matrix(y_true, y_pred)
print(cf_matrix)

def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):

    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    #Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

#print(cm)

    fig, ax = plt.subplots(figsize=(7,7))
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')


    #Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax

np.set_printoptions(precision=2)

#Plotting the confusion matrix
confusion_mtx = confusion_matrix(testlabels, y_pred)

#Defining the class labels
class_names=['construction debris', 'e waste', 'green waste', 'medical waste', 'ocean waste', 'Papers _ cards', 'Plastics', 'recyclable waste', 'trash']
# Plotting non-normalized confusion matrix
plot_confusion_matrix(testlabels, y_pred, classes = class_names, title='Confusion matrix, with normalization')



class attention(layers.Layer):
    def __init__(self,**kwargs):
        super(attention,self).__init__(**kwargs)

    def build(self,input_shape):
        self.W=self.add_weight(name="att_weight",shape=(input_shape[-1],1),initializer="normal")
        self.b=self.add_weight(name="att_bias",shape=(input_shape[1],1),initializer="zeros")        
        super(attention, self).build(input_shape)

    def call(self,x):
        et=K.squeeze(K.tanh(K.dot(x,self.W)+self.b),axis=-1)
        at=K.softmax(et)
        at=K.expand_dims(at,axis=-1)
        output=x*at
        return K.sum(output,axis=1)

    def compute_output_shape(self,input_shape):
        return (input_shape[0],input_shape[-1])

    def get_config(self):
        return super(attention,self).get_config()

model1at = models.Sequential()
model1at.add(layers.LSTM(50, input_shape = (32, 96), activation = 'tanh', return_sequences = True, recurrent_activation='sigmoid', recurrent_dropout = 0.0, unroll=False ,use_bias=True))
model1at.add(layers.Dropout(0.15))
model1at.add(layers.LSTM(50, activation = 'tanh', return_sequences = True,recurrent_activation='sigmoid',recurrent_dropout = 0.0,unroll=False ,use_bias=True))
model1at.add(attention())
model1at.add(layers.Dropout(0.25))
model1at.add(layers.Flatten())
model1at.add(layers.Dense(50,activation = 'tanh'))
model1at.add(layers.Dropout(0.04))
model1at.add(layers.Dense(9,activation = 'softmax'))
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5 , decay = 1e-6)
model1at.compile(loss = tf.keras.losses.SparseCategoricalCrossentropy(),
              optimizer = 'adam',
              metrics = ['accuracy'])
model1at.summary()



es = EarlyStopping(monitor='val_loss', mode='min', verbose=2, patience=15)

mc = ModelCheckpoint('/content/drive/MyDrive/Garbage/model/best_model_8l_normal1at.h5', monitor='val_accuracy', mode='max', verbose=2, save_best_only=True)

history = model1at.fit(data, labels, validation_data=(testdata, testlabels),  epochs=400, verbose=2, callbacks=[es, mc])

import pandas as pd
import h5py

hist_df = pd.DataFrame(history.history) 
hist_csv_file = '/content/drive/MyDrive/Garbage/csv/LSTM04.csv'
with open(hist_csv_file, mode='w') as f:
    hist_df.to_csv(f)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
model1at.save('/content/drive/MyDrive/Garbage/converged_models/LSTM04.h5')

model2at = models.Sequential()
model2at.add(layers.LSTM(50, input_shape = (32, 96), activation = 'tanh', return_sequences = True, recurrent_activation='sigmoid', recurrent_dropout = 0.0, unroll=False ,use_bias=True))
model2at.add(layers.Dropout(0.15))
model2at.add(layers.LSTM(50, activation = 'tanh', return_sequences = True,recurrent_activation='sigmoid',recurrent_dropout = 0.0,unroll=False ,use_bias=True))
model2at.add(layers.Dropout(0.25))
model2at.add(layers.LSTM(50, activation = 'tanh', return_sequences = True,recurrent_activation='sigmoid',recurrent_dropout = 0.0,unroll=False ,use_bias=True))
model2at.add(attention())
model2at.add(layers.Dropout(0.35))
model2at.add(layers.Flatten())
model2at.add(layers.Dense(50,activation = 'tanh'))
model2at.add(layers.Dropout(0.04))
model2at.add(layers.Dense(9,activation = 'softmax'))
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5 , decay = 1e-6)
model2at.compile(loss = tf.keras.losses.SparseCategoricalCrossentropy(),
              optimizer = 'adam',
              metrics = ['accuracy'])
model2at.summary()

es = EarlyStopping(monitor='val_loss', mode='min', verbose=2, patience=15)

mc = ModelCheckpoint('/content/drive/MyDrive/Garbage/model/best_model_8l_normal2at.h5', monitor='val_accuracy', mode='max', verbose=2, save_best_only=True)

history = model2at.fit(data, labels, validation_data=(testdata, testlabels),  epochs=400, verbose=2, callbacks=[es, mc])

import pandas as pd
import h5py

hist_df = pd.DataFrame(history.history) 
hist_csv_file = '/content/drive/MyDrive/Garbage/csv/LSTM05.csv'
with open(hist_csv_file, mode='w') as f:
    hist_df.to_csv(f)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
model2at.save('/content/drive/MyDrive/Garbage/converged_models/LSTM05.h5')

model3at = models.Sequential()
model3at.add(layers.LSTM(50, input_shape = (32, 96), activation = 'tanh', return_sequences = True, recurrent_activation='sigmoid', recurrent_dropout = 0.0, unroll=False ,use_bias=True))
model3at.add(layers.Dropout(0.15))
model3at.add(layers.LSTM(50, activation = 'tanh', return_sequences = True,recurrent_activation='sigmoid',recurrent_dropout = 0.0,unroll=False ,use_bias=True))
model3at.add(layers.Dropout(0.25))
model3at.add(layers.LSTM(50, activation = 'tanh', return_sequences = True,recurrent_activation='sigmoid',recurrent_dropout = 0.0,unroll=False ,use_bias=True))
model3at.add(layers.Dropout(0.35))
model3at.add(layers.LSTM(50, activation = 'tanh', return_sequences = True,recurrent_activation='sigmoid',recurrent_dropout = 0.0,unroll=False ,use_bias=True))
model3at.add(attention())
model3at.add(layers.Dropout(0.45))
model3at.add(layers.Flatten())
model3at.add(layers.Dense(50,activation = 'tanh'))
model3at.add(layers.Dropout(0.04))
model3at.add(layers.Dense(9,activation = 'softmax'))
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5 , decay = 1e-6)
model3at.compile(loss = tf.keras.losses.SparseCategoricalCrossentropy(),
              optimizer = 'adam',
              metrics = ['accuracy'])
model3at.summary()

es = EarlyStopping(monitor='val_loss', mode='min', verbose=2, patience=15)

mc = ModelCheckpoint('/content/drive/MyDrive/Garbage/model/best_model_8l_normal3at.h5', monitor='val_accuracy', mode='max', verbose=2, save_best_only=True)

history = model3at.fit(data, labels, validation_data=(testdata, testlabels),  epochs=400, verbose=2, callbacks=[es, mc])

import pandas as pd
import h5py

hist_df = pd.DataFrame(history.history) 
hist_csv_file = '/content/drive/MyDrive/Garbage/csv/LSTM06.csv'
with open(hist_csv_file, mode='w') as f:
    hist_df.to_csv(f)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
model3at.save('/content/drive/MyDrive/Garbage/converged_models/LSTM06.h5')











model3.pop()
model1pr = models.Sequential()
model1pr.add(layers.LSTM(50, input_shape = (32, 96), activation = 'tanh', return_sequences = True, recurrent_activation='sigmoid', recurrent_dropout = 0.0, unroll=False ,use_bias=True))
model1pr.add(layers.Dropout(0.15))
model1pr.add(layers.LSTM(96, activation = 'tanh', return_sequences = True,recurrent_activation='sigmoid',recurrent_dropout = 0.0,unroll=False ,use_bias=True))
model1pr.add(model3)
model1pr.add(layers.Dropout(0.25))
model1pr.add(layers.Flatten())
model1pr.add(layers.Dense(50,activation = 'tanh'))
model1pr.add(layers.Dropout(0.04))
model1pr.add(layers.Dense(9,activation = 'softmax'))
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-5 , decay = 1e-6)
model1pr.compile(loss = tf.keras.losses.SparseCategoricalCrossentropy(),
              optimizer = 'adam',
              metrics = ['accuracy'])
model1pr.summary()

es = EarlyStopping(monitor='val_loss', mode='min', verbose=2, patience=15)

mc = ModelCheckpoint('/content/drive/MyDrive/1,3,4/model/best_model_8l_normal1pr.h5', monitor='val_accuracy', mode='max', verbose=2, save_best_only=True)

history = model1pr.fit(data, labels, validation_data=(testdata, testlabels),  epochs=400, verbose=2, callbacks=[es, mc])

import pandas as pd
import h5py

hist_df = pd.DataFrame(history.history) 
hist_csv_file = '/content/drive/MyDrive/1,3,4/csv/LSTM07pre.csv'
with open(hist_csv_file, mode='w') as f:
    hist_df.to_csv(f)

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
model1pr.save('/content/drive/MyDrive/1,3,4/converged_models/LSTM07pre.h5')

model3 = models.load_model('/content/drive/MyDrive/1,3,4/model/best_model_4layers.h5')
# evaluate the model
_, train_acc = saved_model.evaluate(data, labels, verbose=2)
_, test_acc = saved_model.evaluate(testdata, testlabels, verbose=2)
print('Train: %.3f, Test: %.3f' % (train_acc, test_acc))

"""**IN CLASS CLASSIFICATION BY USING MODEL3(3 LSTM LAYERS)**



"""

model3 = models.load_model('/content/drive/MyDrive/1,3,4/model/best_model_4layers.h5')
# evaluate the model
_, test_acc = model3.evaluate(itestdata, itestlabels, verbose=2)
print('Test: %.3f' % (test_acc))

