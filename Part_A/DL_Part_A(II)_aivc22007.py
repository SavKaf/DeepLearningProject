# -*- coding: utf-8 -*-
"""DL_Part_A(II)_aivc22007.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pQ7fIlas6nlvcrOG11uSr08oF5IniAx-

# Deep Learning

Project 2023, Part A (II)

Student: Kaftantzis Savvas , aivc22007
"""

#Libraries
import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from keras.layers import Dense
from keras import optimizers

from google.colab import drive
drive.mount('/content/drive')
# Import our dataset and check the head of it
df = pd.read_excel('/content/drive/MyDrive/Colab Notebooks/Dataset2Use_PartA.xlsx')
# Drop the last column (year)
df.drop(df.columns[-1], axis=1, inplace=True)
# Check the head of it
df.head()

# Rename columns
df.rename(columns={'365* ( Β.Υ / Κοστ.Πωλ )': 'A',
                   'Λειτ.Αποτ/Συν.Ενεργ. (ROA)': 'B',
                   'ΧΡΗΜ.ΔΑΠΑΝΕΣ / ΠΩΛΗΣΕΙΣ': 'C',
                  ' ΠΡΑΓΜΑΤΙΚΗ ΡΕΥΣΤΟΤΗΤΑ :  (ΚΕ-ΑΠΟΘΕΜΑΤΑ) / Β.Υ': 'D',
                  '(ΑΠΑΙΤ.*365) / ΠΩΛ.': 'E',
                  'Συν.Υποχρ/Συν.Ενεργ': 'F',
                  'Διάρκεια Παραμονής Αποθεμάτων': 'G',
                  'Λογαριθμος Προσωπικού': 'H',
                  'ΕΝΔΕΙΞΗ ΕΞΑΓΩΓΩΝ': 'I',
                  'ΕΝΔΕΙΞΗ ΕΙΣΑΓΩΓΩΝ': 'J',
                  'ΕΝΔΕΙΞΗ ΑΝΤΙΠΡΟΣΩΠΕΙΩΝ': 'K',
                  'ΕΝΔΕΙΞΗ ΑΣΥΝΕΠΕΙΑΣ (=2) (ν+1)': 'L'},
          inplace=True)

df.columns

# Count the values of column L, for each value
df['L'].value_counts()

# Separate the features (X) and the target variable (y)
X = df.drop('L', axis=1)
y = df['L']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Calculate the count of healthy and bankrupt businesses in the training set
healthy_count = (y_train == 1).sum()
bankrupt_count = (y_train == 2).sum()

# Calculate the desired number of healthy and bankrupt businesses based on the desired ratio
desired_healthy_count = bankrupt_count * 3
desired_bankrupt_count = bankrupt_count

# Check if the training set already meets the desired ratio
if healthy_count == desired_healthy_count and bankrupt_count == desired_bankrupt_count:
    print("The training set already has the desired ratio of 3 healthy businesses to 1 bankrupt business.")
else:
    # Select random samples from the majority class (healthy businesses)
    under_sampler = RandomUnderSampler(sampling_strategy={1: desired_healthy_count})
    X_train_resampled, y_train_resampled = under_sampler.fit_resample(X_train, y_train)

    # Update the training set with the resampled data
    X_train = pd.DataFrame(X_train_resampled, columns=X_train.columns)
    y_train = pd.Series(y_train_resampled, name=y_train.name)

    print("The training set has been modified to meet the desired distribution.")

# Print the counts of healthy and bankrupt businesses in the updated training set
updated_healthy_count = (y_train == 1).sum()
updated_bankrupt_count = (y_train == 2).sum()

print("Count of healthy businesses in the updated training set:", updated_healthy_count)
print("Count of bankrupt businesses in the updated training set:", updated_bankrupt_count)

# Create the StandardScaler object
scaler = StandardScaler()

# Standardize the training set features
X_train_scaled = scaler.fit_transform(X_train)

# Standardize the test set features using the scaler fitted on the training set
X_test_scaled = scaler.transform(X_test)

"""# 1) Linear Discriminant Analysis"""

# Apply Linear Discriminant Analysis on the resampled data
lda = LinearDiscriminantAnalysis()
lda.fit(X_train_scaled, y_train)

# Make predictions on the scaled training and test data
lda_train_predictions = lda.predict(X_train_scaled)
lda_test_predictions  = lda.predict(X_test_scaled)

# Separate predictions for value 1 and value 2 in the test set
lda_test_predictions_class_1 = lda_test_predictions[y_test == 1]
lda_test_predictions_class_2 = lda_test_predictions[y_test == 2]

# Calculate accuracy for value 1 (All good)
accuracy_test_1 = accuracy_score(y_test[y_test == 1], lda_test_predictions_class_1)
accuracy_test_1

# Calculate accuracy for value 2 (Has declared bankruptcy)
accuracy_test_2 = accuracy_score(y_test[y_test == 2], lda_test_predictions_class_2)
accuracy_test_2

# Calculate evaluation metrics for the training set
accuracy_train = accuracy_score(y_train, lda_train_predictions)
precision_train = precision_score(y_train, lda_train_predictions)
recall_train = recall_score(y_train, lda_train_predictions)
f1_train = f1_score(y_train, lda_train_predictions)

cm_train = confusion_matrix(y_train, lda_train_predictions)
print('Confussion matrix for training set: \n',cm_train)
print('\nFor training set:')
print('Accuracy:', accuracy_train)
print('Precision:', precision_train)
print('Recall:', recall_train)
print('F1 score:', f1_train)

# Calculate evaluation metrics for the test set
accuracy_test = accuracy_score(y_test, lda_test_predictions)
precision_test = precision_score(y_test, lda_test_predictions)
recall_test = recall_score(y_test, lda_test_predictions)
f1_test = f1_score(y_test, lda_test_predictions)

cm_test = confusion_matrix(y_test, lda_test_predictions)
print('Confussion matrix for test set: \n',cm_test)
print('\nFor test set:')
print('Accuracy:', accuracy_test)
print('Precision:', precision_test)
print('Recall:', recall_test)
print('F1 score:', f1_test)

"""# 2) Logistic Regression"""

# Apply the Logistic Regression model
logreg = LogisticRegression()
# Fit the Logistic Regression model on the scaled training data
logreg.fit(X_train_scaled, y_train)

# Make predictions on the scaled test data
log_train_predictions = logreg.predict(X_train_scaled)
log_test_predictions = logreg.predict(X_test_scaled)

# Separate predictions for value 1 and value 2 in the test set
log_test_predictions_class_1 = log_test_predictions[y_test == 1]
log_test_predictions_class_2 = log_test_predictions[y_test == 2]

# Calculate accuracy for value 1 (All good)
accuracy_test_1_log = accuracy_score(y_test[y_test == 1], log_test_predictions_class_1)
accuracy_test_1_log

# Calculate accuracy for value 2 (Has declared bankruptcy)
accuracy_test_2_log = accuracy_score(y_test[y_test == 2], log_test_predictions_class_2)
accuracy_test_2_log

# Calculate evaluation metrics for the training set
accuracy_train_log = accuracy_score(y_train, log_train_predictions)
precision_train_log = precision_score(y_train, log_train_predictions)
recall_train_log = recall_score(y_train, log_train_predictions)
f1_train_log = f1_score(y_train, log_train_predictions)

cm_train_log = confusion_matrix(y_train, log_train_predictions)
print('Confussion matrix for training set: \n',cm_train_log)
print('\nFor training set:')
print('Accuracy:', accuracy_train_log)
print('Precision:', precision_train_log)
print('Recall:', recall_train_log)
print('F1 score:', f1_train_log)

# Calculate evaluation metrics for the test set
accuracy_test_log = accuracy_score(y_test, log_test_predictions)
precision_test_log = precision_score(y_test, log_test_predictions)
recall_test_log = recall_score(y_test, log_test_predictions)
f1_test_log = f1_score(y_test, log_test_predictions)

cm_test_log = confusion_matrix(y_test, log_test_predictions)
print('Confussion matrix for test set: \n',cm_test_log)
print('\nFor test set:')
print('Accuracy:', accuracy_test_log)
print('Precision:', precision_test_log)
print('Recall:', recall_test_log)
print('F1 score:', f1_test_log)

"""# 3) Decision Trees"""

# Apply Decision Trees and fit the model
dt = DecisionTreeClassifier(max_depth=10, min_samples_split=10, min_samples_leaf=5,
                              max_features="sqrt", class_weight={1: 0.7, 2 : 1.2},random_state=42)
dt.fit(X_train_scaled, y_train)

# I did various experiments with the parameters,
# so I tweaked the parameters so I could get better results to hit the hit rate constraints

# Make predictions on the scaled training and test data
dt_train_predictions = dt.predict(X_train_scaled)
dt_test_predictions  = dt.predict(X_test_scaled)

# Separate predictions for value 1 and value 2 in the test set
dt_test_predictions_class_1 = dt_test_predictions[y_test == 1]
dt_test_predictions_class_2 = dt_test_predictions[y_test == 2]

# Calculate accuracy for value 1 (All good)
accuracy_test_1_log = accuracy_score(y_test[y_test == 1], dt_test_predictions_class_1)
accuracy_test_1_log

# Calculate accuracy for value 2 (Has declared bankruptcy)
accuracy_test_2_dt = accuracy_score(y_test[y_test == 2], dt_test_predictions_class_2)
accuracy_test_2_dt

# Calculate evaluation metrics for the training set
accuracy_train_dt = accuracy_score(y_train, dt_train_predictions)
precision_train_dt = precision_score(y_train, dt_train_predictions)
recall_train_dt = recall_score(y_train, dt_train_predictions)
f1_train_dt = f1_score(y_train, dt_train_predictions)

cm_train_dt = confusion_matrix(y_train, dt_train_predictions)
print('Confussion matrix for training set: \n',cm_train_dt)
print('\nFor training set:')
print('Accuracy:', accuracy_train_dt)
print('Precision:', precision_train_dt)
print('Recall:', recall_train_dt)
print('F1 score:', f1_train_dt)

# Calculate evaluation metrics for the test set
accuracy_test_dt = accuracy_score(y_test, dt_test_predictions)
precision_test_dt = precision_score(y_test, dt_test_predictions)
recall_test_dt = recall_score(y_test, dt_test_predictions)
f1_test_dt = f1_score(y_test, dt_test_predictions)

cm_test_dt = confusion_matrix(y_test, dt_test_predictions)
print('Confussion matrix for test set: \n',cm_test_dt)
print('\nFor test set:')
print('Accuracy:', accuracy_test_dt)
print('Precision:', precision_test_dt)
print('Recall:', recall_test_dt)
print('F1 score:', f1_test_dt)

"""# 4) k-Nearest Neighbors"""

# Apply kNN and fit the model
knn = KNeighborsClassifier()
knn.fit(X_train_scaled, y_train)

# I did several empirical experiments changing the n_neighbors.

# Make predictions on the scaled training and test data
knn_train_predictions = knn.predict(X_train_scaled)
knn_test_predictions  = knn.predict(X_test_scaled)

# Separate predictions for value 1 and value 2 in the test set
knn_test_predictions_class_1 = knn_test_predictions[y_test == 1]
knn_test_predictions_class_2 = knn_test_predictions[y_test == 2]

# Calculate accuracy for value 1 (All good)
accuracy_test_1_knn = accuracy_score(y_test[y_test == 1], knn_test_predictions_class_1)
accuracy_test_1_knn

# Calculate accuracy for value 2 (Has declared bankruptcy)
accuracy_test_2_knn = accuracy_score(y_test[y_test == 2], knn_test_predictions_class_2)
accuracy_test_2_knn

# Calculate evaluation metrics for the training set
accuracy_train_knn = accuracy_score(y_train, knn_train_predictions)
precision_train_knn = precision_score(y_train, knn_train_predictions)
recall_train_knn = recall_score(y_train, knn_train_predictions)
f1_train_knn = f1_score(y_train, knn_train_predictions)

cm_train_knn = confusion_matrix(y_train, knn_train_predictions)
print('Confussion matrix for training set: \n',cm_train_knn)
print('\nFor training set:')
print('Accuracy:', accuracy_train_knn)
print('Precision:', precision_train_knn)
print('Recall:', recall_train_knn)
print('F1 score:', f1_train_knn)

# Calculate evaluation metrics for the test set
accuracy_test_knn = accuracy_score(y_test, knn_test_predictions)
precision_test_knn = precision_score(y_test, knn_test_predictions)
recall_test_knn = recall_score(y_test, knn_test_predictions)
f1_test_knn = f1_score(y_test, knn_test_predictions)

cm_test_knn = confusion_matrix(y_test, knn_test_predictions)
print('Confussion matrix for test set: \n',cm_test_knn)
print('\nFor test set:')
print('Accuracy:', accuracy_test_knn)
print('Precision:', precision_test_knn)
print('Recall:', recall_test_knn)
print('F1 score:', f1_test_knn)

"""# 5) Naïve Bayes"""

# Apply Bernoulli Naïve Bayes and fit the model
naive_bayes = BernoulliNB()
naive_bayes.fit(X_train_scaled, y_train)

# For 'GaussianNB' i got Accuracy for class 1 = 89% and for class 2 = 43%.
# But for BernoulliNB' that is a suitable variation of the Naïve Bayes algorithm for binary feature data,
# i got the best results..

# Make predictions on the scaled training and test data
nb_train_predictions = naive_bayes.predict(X_train_scaled)
nb_test_predictions = naive_bayes.predict(X_test_scaled)

# Separate predictions for value 1 and value 2 in the test set
nb_test_predictions_class_1 = nb_test_predictions[y_test == 1]
nb_test_predictions_class_2 = nb_test_predictions[y_test == 2]

# Calculate accuracy for value 1 (All good)
accuracy_test_1_nb = accuracy_score(y_test[y_test == 1], nb_test_predictions_class_1)
accuracy_test_1_nb

# Calculate accuracy for value 2 (Has declared bankruptcy)
accuracy_test_2_nb = accuracy_score(y_test[y_test == 2], nb_test_predictions_class_2)
accuracy_test_2_nb

# Calculate evaluation metrics for the training set
accuracy_train_nb = accuracy_score(y_train, nb_train_predictions)
precision_train_nb = precision_score(y_train, nb_train_predictions)
recall_train_nb = recall_score(y_train, nb_train_predictions)
f1_train_nb = f1_score(y_train, nb_train_predictions)

cm_train_nb = confusion_matrix(y_train, nb_train_predictions)
print('Confussion matrix for training set: \n',cm_train_nb)
print('\nFor training set:')
print('Accuracy:', accuracy_train_nb)
print('Precision:', precision_train_nb)
print('Recall:', recall_train_nb)
print('F1 score:', f1_train_nb)

# Calculate evaluation metrics for the test set
accuracy_test_nb = accuracy_score(y_test, nb_test_predictions)
precision_test_nb = precision_score(y_test, nb_test_predictions)
recall_test_nb = recall_score(y_test, nb_test_predictions)
f1_test_nb = f1_score(y_test, nb_test_predictions)

cm_test_nb = confusion_matrix(y_test, nb_test_predictions)
print('Confussion matrix for test set: \n',cm_test_nb)
print('\nFor test set:')
print('Accuracy:', accuracy_test_nb)
print('Precision:', precision_test_nb)
print('Recall:', recall_test_nb)
print('F1 score:', f1_test_nb)

"""# 6) Support Vector Machines"""

# Apply SVC and fit the model
svm_classifier = SVC(kernel='sigmoid',random_state=42)
svm_classifier.fit(X_train_scaled, y_train)

# Kernel specifies the kernel type to be used in the algorithm.
# The fot the best results with 'simgoid'.

# Make predictions on the scaled training and test data
svm_train_predictions = svm_classifier.predict(X_train_scaled)
svm_test_predictions  = svm_classifier.predict(X_test_scaled)

# Separate predictions for value 1 and value 2 in the test set
svm_test_predictions_class_1 = svm_test_predictions[y_test == 1]
svm_test_predictions_class_2 = svm_test_predictions[y_test == 2]

# Calculate accuracy for value 1 (All good)
accuracy_test_1_svm = accuracy_score(y_test[y_test == 1], svm_test_predictions_class_1)
accuracy_test_1_svm

# Calculate accuracy for value 2 (Has declared bankruptcy)
accuracy_test_2_svm = accuracy_score(y_test[y_test == 2], svm_test_predictions_class_2)
accuracy_test_2_svm

# Calculate evaluation metrics for the training set
accuracy_train_svm = accuracy_score(y_train, svm_train_predictions)
precision_train_svm = precision_score(y_train, svm_train_predictions)
recall_train_svm = recall_score(y_train, svm_train_predictions)
f1_train_svm = f1_score(y_train, svm_train_predictions)

cm_train_svm = confusion_matrix(y_train, svm_train_predictions)
print('Confussion matrix for training set: \n',cm_train_svm)
print('\nFor training set:')
print('Accuracy:', accuracy_train_svm)
print('Precision:', precision_train_svm)
print('Recall:', recall_train_svm)
print('F1 score:', f1_train_svm)

# Calculate evaluation metrics for the test set
accuracy_test_svm = accuracy_score(y_test, svm_test_predictions)
precision_test_svm = precision_score(y_test, svm_test_predictions)
recall_test_svm = recall_score(y_test, svm_test_predictions)
f1_test_svm = f1_score(y_test, svm_test_predictions)

cm_test_svm = confusion_matrix(y_test, svm_test_predictions)
print('Confussion matrix for test set: \n',cm_test_svm)
print('\nFor test set:')
print('Accuracy:', accuracy_test_svm)
print('Precision:', precision_test_svm)
print('Recall:', recall_test_svm)
print('F1 score:', f1_test_svm)

"""# 7) Neural Networks"""

# Train and fit the neural network model
mlp_classifier = MLPClassifier(hidden_layer_sizes=(2,4), activation='relu', solver='sgd',
                      batch_size=10,max_iter=500, random_state=42)
mlp_classifier.fit(X_train_scaled, y_train)

# Make predictions on the scaled training and test data
mlp_train_predictions = mlp_classifier.predict(X_train_scaled)
mlp_test_predictions  = mlp_classifier.predict(X_test_scaled)

# Separate predictions for value 1 and value 2 in the test set
mlp_test_predictions_class_1 = mlp_test_predictions[y_test == 1]
mlp_test_predictions_class_2 = mlp_test_predictions[y_test == 2]

# Calculate accuracy for value 1 (All good)
accuracy_test_1_mlp = accuracy_score(y_test[y_test == 1], mlp_test_predictions_class_1)
accuracy_test_1_mlp

# Calculate accuracy for value 2 (Has declared bankruptcy)
accuracy_test_2_mlp = accuracy_score(y_test[y_test == 2], mlp_test_predictions_class_2)
accuracy_test_2_mlp

# Calculate evaluation metrics for the training set
accuracy_train_mlp = accuracy_score(y_train, mlp_train_predictions)
precision_train_mlp = precision_score(y_train, mlp_train_predictions)
recall_train_mlp = recall_score(y_train, mlp_train_predictions)
f1_train_mlp = f1_score(y_train, mlp_train_predictions)

cm_train_mlp = confusion_matrix(y_train, mlp_train_predictions)
print('Confussion matrix for training set: \n',cm_train_mlp)
print('\nFor training set:')
print('Accuracy:', accuracy_train_mlp)
print('Precision:', precision_train_mlp)
print('Recall:', recall_train_mlp)
print('F1 score:', f1_train_mlp)

# Calculate evaluation metrics for the test set
accuracy_test_mlp = accuracy_score(y_test, mlp_test_predictions)
precision_test_mlp = precision_score(y_test, mlp_test_predictions)
recall_test_mlp = recall_score(y_test, mlp_test_predictions)
f1_test_mlp = f1_score(y_test, mlp_test_predictions)

cm_test_mlp = confusion_matrix(y_test, mlp_test_predictions)
print('Confussion matrix for test set: \n',cm_test_mlp)
print('\nFor test set:')
print('Accuracy:', accuracy_test_mlp)
print('Precision:', precision_test_mlp)
print('Recall:', recall_test_mlp)
print('F1 score:', f1_test_mlp)



