import cv2
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

# Load the model
model = load_model('integral_model.h5')

# Function to preprocess the image and extract features
def extract_features(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    features = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        features.append([x, y, w, h])
    
    return features

# Function to make predictions on extracted features
def predict(image_path):
    # Extract features from the image
    features = extract_features(image_path)
    
    # Convert features to numpy array
    X_test = np.array(features)
    
    # Ensure the input shape matches the model's expected input shape
    if X_test.shape[1] != model.input_shape[1]:
        raise ValueError(f"Expected input shape: {model.input_shape[1]}, but got {X_test.shape[1]}")

    # Make predictions
    predictions = model.predict(X_test)
    predicted_classes = (predictions > 0.5).astype("int32").flatten()
    
    # Load the class labels
    labels = {0: 'not_integral', 1: 'integral'}

    # Display the image with the prediction results
    img = cv2.imread(image_path)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Prediction Results')
    for (x, y, w, h), label in zip(features, predicted_classes):
        plt.text(x, y - 10, labels[label], color='red' if label else 'blue')
        plt.gca().add_patch(plt.Rectangle((x, y), w, h, edgecolor='red' if label else 'blue', facecolor='none', linewidth=2))
    plt.axis('off')
    plt.show()

    return [labels[label] for label in predicted_classes]

# Example usage
image_path = 'intt.png'  # Replace with the path to your image
result = predict(image_path)
print(f'The image is predicted to be: {result}')
