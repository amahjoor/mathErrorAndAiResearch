# Code to generate equations -> generates to math_operations_dataset.csv

import random
import pandas as pd

# Define the range for the numbers in the operations
num_range = range(1, 100)

# Define the number of samples per category
num_samples_per_category = 1000

# Initialize lists to hold the data
operations = []
labels = []

# Function to generate correct, addition error, and subtraction error operations
def generate_operations(num_samples):
    for _ in range(num_samples):
        a = random.choice(num_range)
        b = random.choice(num_range)
        correct_result = a + b
        
        # Correct operation
        operations.append(f"{a} + {b} = {correct_result}")
        labels.append("correct")
        
        # Addition error
        addition_error = correct_result + random.randint(1, 10)
        operations.append(f"{a} + {b} = {addition_error}")
        labels.append("addition_error")
        
        # Subtraction error
        subtraction_error = correct_result - random.randint(1, 10)
        operations.append(f"{a} + {b} = {subtraction_error}")
        labels.append("subtraction_error")

# Generate the operations
generate_operations(num_samples_per_category)

# Create a DataFrame
data = pd.DataFrame({
    "operation": operations,
    "label": labels
})

# Shuffle the dataset
data = data.sample(frac=1).reset_index(drop=True)

# Save the dataset to a CSV file
data.to_csv("math_operations_dataset.csv", index=False)

print("Dataset created successfully.")
