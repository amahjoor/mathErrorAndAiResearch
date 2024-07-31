import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt

# Load and inspect the JSON data    
try:
    with open('./integrals.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"Could not find the JSON file at the specified path: {json_file_path}")

# Extract features and labels from the data
features = []
labels = []

for item in data:
    for annotation in item['annotations']:
        for result in annotation['result']:
            value = result['value']
            #print(value)
            x = value['x']
            y = value['y']
            width = value['width']
            height = value['height']
            label = result.get('rectanglelabels', [None])[0]  # Assuming single label per annotation
            if label is not None:
                    # Feature vector: [x, y, width, height]
                    features.append([x, y, width, height])
                    
                    # Label: 1 if 'integral', else 0 (adjust based on your specific use case)
                    labels.append(1 if label == 'integral' else 0)
            
            # Feature vector: [x, y, width, height]
            features.append([x, y, width, height])
            
            # Label: 1 if 'integral', else 0 (adjust based on your specific use case)
            labels.append(1 if label == 'integral' else 0)

# Check if features and labels were extracted successfully
if not features or not labels:
    raise ValueError("No features or labels were extracted from the JSON data. Please check the structure of your JSON file.")

# Convert lists to numpy arrays
X = np.array(features)
y = np.array(labels)

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Define your model architecture
model = Sequential([
    Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    #Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')  # Assuming binary classification
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Model training code
history = model.fit(
    X_train,
    y_train,
    epochs=20,
    validation_data=(X_val, y_val)
)

def visualizeModel():
    # Plot training & validation accuracy values
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')

    # Plot training & validation loss values
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')

    plt.show()

visualizeModel()

# Save the model in the new format
model.save('integral_model.keras')

# Save the model architecture
with open('model_architecture.json', 'w') as f:
    f.write(model.to_json())

# Save the model weights
model.save_weights('model.weights.h5')