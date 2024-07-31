import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import pandas as pd
import os

# Load the dataset
if os.path.isdir("./tensorflow/"):
    data = pd.read_csv("./tensorflow/math_operations_dataset.csv")
else:
    data = pd.read_csv("math_operations_dataset.csv")

# Tokenize the operations
tokenizer = Tokenizer()
tokenizer.fit_on_texts(data['operation'])
sequences = tokenizer.texts_to_sequences(data['operation'])

# Pad the sequences
max_length = max(len(seq) for seq in sequences)
X = pad_sequences(sequences, maxlen=max_length, padding='post')

# Encode the labels
label_map = {'correct': 0, 'addition_error': 1, 'subtraction_error': 2, 'multiplication_error': 3, 'division_error': 4}
y = data['label'].map(label_map).values

# Split the data into training and validation sets
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the model
''' 
'''
# Sequential Model
model = Sequential([
    Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=128), 
    Bidirectional(LSTM(128, return_sequences=True)),
    Dropout(0.5),
    Bidirectional(LSTM(128)),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(5, activation='softmax')
])
'''
# Convolutional Neural Networks (CNNs) for Text Classification
model = Sequential([
    Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=128, input_length=max_length),
    Conv1D(128, kernel_size=3, padding='same', activation='relu'),
    MaxPooling1D(pool_size=2),
    Conv1D(128, kernel_size=3, padding='same', activation='relu'),
    MaxPooling1D(pool_size=2),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(5, activation='softmax')
])
'''
'''
# GRU (Gated Recurrent Unit) Layers
model = Sequential([
    Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=128, input_length=max_length),
    Bidirectional(GRU(128, return_sequences=True)),
    Dropout(0.5),
    Bidirectional(GRU(128)),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(5, activation='softmax')
])
'''
'''
# Transformer Models
from tensorflow.keras.layers import MultiHeadAttention, LayerNormalization, Dense, Dropout, Input, Embedding
from tensorflow.keras.models import Model
import tensorflow as tf

inputs = Input(shape=(max_length,))
x = Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=128)(inputs)
x = MultiHeadAttention(num_heads=4, key_dim=128)(x, x)
x = LayerNormalization()(x)
x = Dropout(0.5)(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(5, activation='softmax')(x)

model = Model(inputs=inputs, outputs=x)
'''
'''
# Recurrent Convolutional Neural Networks
model = Sequential([
    Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=128, input_length=max_length),
    Conv1D(128, 5, activation='relu'),
    MaxPooling1D(5),
    Bidirectional(LSTM(128, return_sequences=True)),
    Dropout(0.5),
    Bidirectional(LSTM(128)),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(5, activation='softmax')
])
'''
'''
# Attention Mechanism
from tensorflow.keras.layers import Attention

sequence_input = Input(shape=(max_length,), dtype='int32')
embedded_sequences = Embedding(len(tokenizer.word_index) + 1, 128)(sequence_input)
lstm = Bidirectional(LSTM(128, return_sequences=True))(embedded_sequences)
attention = Attention()([lstm, lstm])
flatten = Flatten()(attention)
dense1 = Dense(128, activation='relu')(flatten)
dropout = Dropout(0.5)(dense1)
outputs = Dense(5, activation='softmax')(dropout)

model = Model(inputs=sequence_input, outputs=outputs)
'''



# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=0.0001)

# Train the model
history = model.fit(X_train, y_train, epochs=50, validation_data=(X_val, y_val), batch_size=32, callbacks=[early_stopping, reduce_lr])

# Evaluate the model
loss, accuracy = model.evaluate(X_val, y_val)
print(f'Validation Accuracy: {accuracy:.2f}')

# Save the model
if os.path.isdir("./tensorflow/"):
    model.save('./tensorflow/math_error_detection_model.keras')
else:
    model.save('math_error_detection_model.keras')
