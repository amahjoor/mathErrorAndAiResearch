import os
from flask import Flask, request, render_template, redirect, url_for
import requests
import base64
from config import APP_ID, APP_KEY  # Import the credentials

# Replace these with your Mathpix API credentials
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Function to read an image file and convert it to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to send image to Mathpix API and get text response
def convert_image_to_text(image_path):
    image_base64 = image_to_base64(image_path)
    headers = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'Content-type': 'application/json'
    }
    data = {
        'src': f'data:image/jpeg;base64,{image_base64}',
        'formats': ['text']
    }
    response = requests.post('https://api.mathpix.com/v3/text', headers=headers, json=data)
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            result = convert_image_to_text(file_path)
            return render_template('result.html', result=result)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
