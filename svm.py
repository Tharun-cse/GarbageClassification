# -*- coding: utf-8 -*-
"""SVM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xNNA-O28WR-p1W8X3lASnzpbdqlokNdI

<h2><center>Import modules</center></h2>
"""

import os
import cv2
import numpy as np
from imutils import paths

imagepaths = list(paths.list_images("/content/drive/MyDrive/ml/train"))

from google.colab import drive
drive.mount('/content/drive')

imagepaths

from tqdm import tqdm

data = []
labels = []
for images in tqdm(imagepaths):
    label = images.split(os.path.sep)[-2]
    image =cv2.imread(images)
    image =cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    image =cv2.resize(image, (100,100))
    image = np.asarray(image)
    image = np.reshape(image,(30000))
    data.append(image)
    labels.append(label)

# import pickle
# pickle.dump(data, open('/content/drive/MyDrive/ml/final/svm/data.pkl', 'wb'))
# pickle.dump(labels, open('/content/drive/MyDrive/ml/final/svm/labels.pkl', 'wb'))

"""<h2><center>Loading pickles</center></h2>"""

import pickle
data = pickle.load(open('/content/drive/MyDrive/ml/final/svm/data.pkl', 'rb'))
labels = pickle.load(open('/content/drive/MyDrive/ml/final/svm/labels.pkl', 'rb'))

mapping = ['construction debris', 'e waste', 'green waste', 'medical waste', 'ocean waste', 'Papers', 'Plastics', 'recyclable waste', 'trash']

def index(x):
    for i in range(9):
        if(mapping[i] == x):
            return i;
    return -1;

ilabels = []
for l in labels:
    ilabels.append(index(l))
labels = ilabels

labels

data = np.asarray(data)
labels = np.asarray(labels)

print(data.shape)
print(labels.shape)

def prep_pixels(test):
 	# convert from integers to floats
 	test_norm = np.array(test).astype('float32')
 	# normalize to range 0-0
 	test_norm = test_norm/ 255.0
 	# return normalized images
 	return test_norm

data = prep_pixels(data)

from sklearn.model_selection import train_test_split
traindata, testdata, trainlabels, testlabels = train_test_split(data, labels, random_state = 32, test_size=0.15)

print(traindata.shape)
print(testdata.shape)
print(trainlabels.shape)
print(testlabels.shape)

"""<h2><center>Linear Kernel</center></h2>"""

from sklearn.svm import SVC
#model = SVC(probability=True)

"""model = SVC()"""

model = SVC(kernel='linear')

model.fit(traindata, trainlabels)



from sklearn.metrics import accuracy_score
pred_labels = model.predict(testdata)
print(pred_labels)

pred_labels = np.asarray(pred_labels)

#Get the confusion matrix
from sklearn.metrics import confusion_matrix
cf_matrix = confusion_matrix(testlabels, pred_labels)
print(cf_matrix)

import matplotlib.pyplot as plt
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
        print('Confusion matrix, with normalization')

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

"""<h2><center>Confusion matrix</center></h2>"""

#Plotting the confusion matrix
confusion_mtx = confusion_matrix(testlabels, pred_labels)

#Defining the class labels
class_names=['construction debris', 'e waste', 'green waste', 'medical waste', 'ocean waste', 'Papers _ cards', 'Plastics', 'recyclable waste', 'trash']
# Plotting non-normalized confusion matrix
plot_confusion_matrix(testlabels, pred_labels, classes = class_names, title='Confusion matrix, with normalization')

accuracy_score(pred_labels,testlabels)



"""<h2><center>Poly Kernel</center></h2>"""

model = SVC(kernel='poly',degree=4)

model.fit(traindata, trainlabels)

sets = set()
count = [0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in testlabels:
  sets.add(i)
  count[i] += 1

count

sets = set()
count = [0, 0, 0, 0, 0, 0, 0, 0, 0]
for i in trainlabels:
  sets.add(i)
  count[i] += 1

count



from sklearn.metrics import accuracy_score
pred_labels = model.predict(testdata)
print(pred_labels)

accuracy_score(pred_labels,testlabels)

#Get the confusion matrix
from sklearn.metrics import confusion_matrix
cf_matrix = confusion_matrix(testlabels, pred_labels)
print(cf_matrix)

import matplotlib.pyplot as plt
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
        print('Confusion matrix, with normalization')

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

"""<h2><center>Confusion matrix</center></h2>"""

#Plotting the confusion matrix
confusion_mtx = confusion_matrix(testlabels, pred_labels)

#Defining the class labels
class_names=['construction debris', 'e waste', 'green waste', 'medical waste', 'ocean waste', 'Papers _ cards', 'Plastics', 'recyclable waste', 'trash']
# Plotting non-normalized confusion matrix
plot_confusion_matrix(testlabels, pred_labels, classes = class_names, title='Confusion matrix, with normalization')



"""<h2><center>Linear Kernel</center></h2>"""

model = SVC(kernel='linear', C=0.6)
model.fit(traindata, trainlabels)

from sklearn.metrics import accuracy_score
pred_labels = model.predict(testdata)
print(pred_labels)

print("Accuracy: ",accuracy_score(pred_labels,testlabels)*100,"%")

