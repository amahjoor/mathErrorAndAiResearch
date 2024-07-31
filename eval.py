# Save the model architecture
with open('model_architecture.json', 'w') as f:
    f.write(model.to_json())

# Save the model weights
model.save_weights('model_weights.h5')
