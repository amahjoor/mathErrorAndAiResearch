# Code to test the accuracy of the model

import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Load the dataset
#data = pd.read_csv("./tensorflow/math_operations_dataset.csv")
data = pd.read_csv("./math_operations_dataset.csv")

# Tokenize the operations
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
tokenizer = Tokenizer()
tokenizer.fit_on_texts(data['operation'])
sequences = tokenizer.texts_to_sequences(data['operation'])

# Pad the sequences
max_length = max(len(seq) for seq in sequences)
X = pad_sequences(sequences, maxlen=max_length, padding='post')

# Encode the labels
label_map = {'correct': 0, 'addition_error': 1, 'subtraction_error': 2, 'multiplication_error': 3, 'division_error': 4}
y = data['label'].map(label_map).values

# Split the data into training and test sets
_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load the trained model
#model = tf.keras.models.load_model('./tensorflow/math_error_detection_model.h5')
model = tf.keras.models.load_model('./math_error_detection_model.keras')

# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f'Test Accuracy: {test_accuracy:.2f}')

# Make predictions on the test set
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)

# Print classification report
print("Classification Report: ")
print(classification_report(y_test, y_pred_classes, target_names=['correct', 'addition_error', 'subtraction_error', 'multiplication_error', 'division_error']))

# Print confusion matrix
print("Confusion Matrix: ")
conf_matrix = confusion_matrix(y_test, y_pred_classes)
print(conf_matrix)
