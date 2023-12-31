# -*- coding: utf-8 -*-
"""ComparingBasicNNArchitectures.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15dMGHVxNFrskFUIdg26L4c1WyWkgXmdh

**Deep Learning**

**Project 2023, Part B**

---



---



***Student: Kaftantzis Savvas , aivc22007***
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.models import load_model
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Load MNIST dataset
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Preprocess the data
X_train = X_train.reshape(-1, 28, 28, 1) / 255.0
X_test = X_test.reshape(-1, 28, 28, 1) / 255.0
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# plot 9 images as gray scale
plt.subplot(331)
plt.imshow(X_train[0], cmap=plt.get_cmap('gray'))
plt.subplot(332)
plt.imshow(X_train[1], cmap=plt.get_cmap('gray'))
plt.subplot(333)
plt.imshow(X_train[2], cmap=plt.get_cmap('gray'))
plt.subplot(334)
plt.imshow(X_train[3], cmap=plt.get_cmap('gray'))
plt.subplot(335)
plt.imshow(X_train[4], cmap=plt.get_cmap('gray'))
plt.subplot(336)
plt.imshow(X_train[5], cmap=plt.get_cmap('gray'))
plt.subplot(337)
plt.imshow(X_train[6], cmap=plt.get_cmap('gray'))
plt.subplot(338)
plt.imshow(X_train[7], cmap=plt.get_cmap('gray'))
plt.subplot(339)
plt.imshow(X_train[8], cmap=plt.get_cmap('gray'))
# show the plot
plt.show()
plt.pause(4)

# Define the models
dnn_model = Sequential([
    Flatten(input_shape=(28, 28, 1)),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax')
])

cnn_model = Sequential([
    Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax')
])

# Define the performance metrics
def calculate_metrics(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='macro')
    recall = recall_score(y_true, y_pred, average='macro')
    f1 = f1_score(y_true, y_pred, average='macro')
    return accuracy, precision, recall, f1

# Compile the models
dnn_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
cnn_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Perform k-fold cross-validation
kfold = StratifiedKFold(n_splits=6, shuffle=True, random_state=42)
results = []

for fold, (train_index, val_index) in enumerate(kfold.split(X_train, np.argmax(y_train, axis=1)), 1):
    print(f"Fold {fold}")
    X_train_fold, X_val_fold = X_train[train_index], X_train[val_index]
    y_train_fold, y_val_fold = y_train[train_index], y_train[val_index]

    # Train the DNN model
    dnn_model.fit(X_train_fold, y_train_fold, batch_size=128, epochs=10, validation_data=(X_val_fold, y_val_fold))

    # Train the CNN model
    cnn_model.fit(X_train_fold, y_train_fold, batch_size=128, epochs=10, validation_data=(X_val_fold, y_val_fold))

    # Evaluate the models on the train and test sets
    dnn_train_loss, dnn_train_acc = dnn_model.evaluate(X_train, y_train)
    dnn_test_loss, dnn_test_acc = dnn_model.evaluate(X_test, y_test)

    cnn_train_loss, cnn_train_acc = cnn_model.evaluate(X_train, y_train)
    cnn_test_loss, cnn_test_acc = cnn_model.evaluate(X_test, y_test)

    # Predict using the models
    dnn_test_pred = np.argmax(dnn_model.predict(X_test), axis=1)
    cnn_test_pred = np.argmax(cnn_model.predict(X_test), axis=1)

    # Calculate performance metrics
    dnn_test_metrics = [dnn_test_acc,
                        precision_score(np.argmax(y_test, axis=1), dnn_test_pred, average='macro'),
                        recall_score(np.argmax(y_test, axis=1), dnn_test_pred, average='macro'),
                        f1_score(np.argmax(y_test, axis=1), dnn_test_pred, average='macro')]

    cnn_test_metrics = [cnn_test_acc,
                        precision_score(np.argmax(y_test, axis=1), cnn_test_pred, average='macro'),
                        recall_score(np.argmax(y_test, axis=1), cnn_test_pred, average='macro'),
                        f1_score(np.argmax(y_test, axis=1), cnn_test_pred, average='macro')]

    # Append the results to the dataframe
    results.append(['DNN', 'Train', fold] + dnn_test_metrics)
    results.append(['CNN', 'Train', fold] + cnn_test_metrics)
    results.append(['DNN', 'Test', fold] + dnn_test_metrics)
    results.append(['CNN', 'Test', fold] + cnn_test_metrics)

# Create a pandas dataframe with the results
columns = ['Technique', 'Set', 'Fold', 'Accuracy', 'Precision', 'Recall', 'F1 Score']
df_results = pd.DataFrame(results, columns=columns)

# Save the dataframe as a CSV file
df_results.to_csv('erotima1.csv', index=False)

# Save the best models based on test set performance
best_dnn_model = dnn_model
best_cnn_model = cnn_model

best_dnn_model.save('best_dnn_model.h5')
best_cnn_model.save('best_cnn_model.h5')

# Print the accuracy values for each model on the test set
print(df_results[df_results['Set'] == 'Test'][['Technique', 'Accuracy']])

# Load the DNN and CNN models from the saved .h5 files
loaded_dnn_model = load_model('best_dnn_model.h5')
loaded_cnn_model = load_model('best_cnn_model.h5')

# Load and inspect the DNN model architecture
loaded_dnn_model.summary()
# Load and inspect the CNN model architecture
loaded_cnn_model.summary()

# Get the predicted probabilities for DNN
dnn_test_pred_prob = loaded_dnn_model.predict(X_test)
dnn_test_pred = np.argmax(dnn_test_pred_prob, axis=1)
# Get the predicted probabilities for CNN
cnn_test_pred_prob = loaded_cnn_model.predict(X_test)
cnn_test_pred = np.argmax(cnn_test_pred_prob, axis=1)

# Plot Accuracy Comparison
lineplot_filename = 'line_plot.png'
plt.figure(figsize=(7,5))
sns.lineplot(data=df_results[df_results['Set'] == 'Test'], x='Fold', y='Accuracy', hue='Technique')
plt.title('Accuracy Comparison: DNN vs CNN')
plt.xlabel('Fold')
plt.ylabel('Accuracy')
plt.savefig(lineplot_filename, dpi=300, facecolor='w')
plt.show()
plt.close()

# Plot Precision, Recall, and F1 Score Comparison
boxplot_filename = 'boxplot.png'
metrics = ['Precision', 'Recall', 'F1 Score']
plt.figure(figsize=(10,5))
for i, metric in enumerate(metrics, 1):
    plt.subplot(1, 3, i)
    sns.boxplot(data=df_results[df_results['Set'] == 'Test'], x='Technique', y=metric)
    plt.title(f'{metric} Comparison: DNN vs CNN')
    plt.xlabel('Technique')
    plt.ylabel(metric)
plt.tight_layout()
plt.savefig(boxplot_filename, dpi=300, facecolor='w')
plt.show()
plt.close()

# Generate Confusion Matrix for DNN
dnn_cm = confusion_matrix(np.argmax(y_test, axis=1), dnn_test_pred)

# Generate Confusion Matrix for CNN
cnn_cm = confusion_matrix(np.argmax(y_test, axis=1), cnn_test_pred)

# Plot Confusion Matrix for DNN
plt.figure(figsize=(7, 5))
sns.heatmap(dnn_cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix (DNN)')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

# Plot Confusion Matrix for CNN
plt.figure(figsize=(7, 5))
sns.heatmap(cnn_cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix (CNN)')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()



















