# Code to generate equations -> generates to math_operations_dataset.csv

import random
import pandas as pd
import os

# Define the range for the numbers in the operations
num_range = range(1, 100)

# Define the number of samples per category
num_samples_per_category = 20000

# Initialize lists to hold the data
operations = []
labels = []

# Helper function for generating division operations
def has_finite_decimal_denominator(num):
    """ Returns True if the denominator has only 2 and 5 as prime factors, else False """
    while num % 2 == 0:
        num //= 2
    while num % 5 == 0:
        num //= 5
    return num == 1


# Function to generate correct, addition error, and subtraction error operations
def generate_operations(num_samples):
    for _ in range(num_samples):
        a = random.choice(num_range)
        b = random.choice(num_range)
        # Ensure b is not zero and has a finite decimal representation in division
        while b == 0 or not has_finite_decimal_denominator(b):
            b = random.randint(1, 100)



        # ADDITION
        correct_result_add = a + b
        operations.append(f"{a} + {b} = {correct_result_add}")
        labels.append("correct")
        addition_error_offset = random.randint(-10, 10)
        while addition_error_offset == 0:
            addition_error_offset = random.randint(-10, 10)
        addition_error = correct_result_add + addition_error_offset
        operations.append(f"{a} + {b} = {addition_error}")
        labels.append("addition_error")
        
        # SUBTRACTION
        correct_result_sub = a - b
        operations.append(f"{a} - {b} = {correct_result_sub}")
        labels.append("correct")
        subtraction_error_offset = random.randint(-10, 10)
        while subtraction_error_offset == 0:
            subtraction_error_offset = random.randint(-10, 10)
        subtraction_error = correct_result_sub - subtraction_error_offset
        operations.append(f"{a} - {b} = {subtraction_error}")
        labels.append("subtraction_error")

        # MULTIPLICATION
        correct_result_multiplication = a * b
        operations.append(f"{a} * {b} = {correct_result_multiplication}")
        labels.append("correct")
        multiplication_error_offset = random.randint(-10, 10)
        while multiplication_error_offset == 0:
            multiplication_error_offset = random.randint(-10, 10)
        multiplication_error = correct_result_sub - multiplication_error_offset
        operations.append(f"{a} * {b} = {multiplication_error}")
        labels.append("multiplication_error")

        # DIVISION
        correct_result_division = a / b
        operations.append(f"{a} / {b} = {correct_result_division}")
        labels.append("correct")
        # Generate a random error for the division
        division_error_offset = random.randint(-10, 10)
        while division_error_offset == 0:
            division_error_offset = random.randint(-10, 10)
        division_error = correct_result_division - division_error_offset
        operations.append(f"{a} / {b} = {division_error}")
        labels.append("division_error")

        
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
if os.path.isdir("./tensorflow/"):
    data.to_csv("./tensorflow/math_operations_dataset.csv", index=False)
else: 
    data.to_csv("math_operations_dataset.csv", index=False)

print("Dataset created successfully.")