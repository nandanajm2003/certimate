from flask import Flask, render_template, request, jsonify, send_file
import base64
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
from flask_resize import resize

app = Flask(__name__)


UPLOAD_FOLDER = 'static/uploads'  # Specify the upload directory
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    # Save the file to the specified upload folder
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(upload_path)

    return 'File uploaded successfully'

@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.get_json()
    image_data = data['image']

    # Convert base64 image data to bytes
    image_bytes = base64.b64decode(image_data.split(',')[1])

    # Save the edited image
    with open('static/edited_image.jpg', 'wb') as f:
        f.write(image_bytes)

    return jsonify({'message': 'Image saved successfully'})



UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'
    else:
        return 'Invalid file format'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/generate_certificates', methods=['POST'])
def generate_certificates():
    name_column = request.form.get('nameColumn')
    x_coord = int(request.form.get('xCoord'))
    y_coord = int(request.form.get('yCoord'))
    font_size = int(request.form.get('fontSize'))
    font_family = request.form.get('fontFamily')

    if not name_column:
        return jsonify({'error': 'Invalid request'}), 400

    # Assuming namesData is accessible and contains the Excel data
    names = []  # Populate names from namesData based on name_column

    for name in names:
        # Load the uploaded image
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')  # Adjust the path as necessary
        image = Image.open(image_path)

        # Create a drawing context
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_family, font_size)

        # Calculate text size for positioning
        text_width, text_height = draw.textsize(name, font=font)

        # Calculate coordinates for centering text
        text_x = x_coord - text_width / 2
        text_y = y_coord - text_height / 2

        # Add the name at the specified coordinates
        draw.text((text_x, text_y), name, font=font, fill='black')

        # Save the edited image with the name as JPG
        edited_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'edited_{name}.jpg')
        image.save(edited_image_path)

    # Return success message or list of edited image paths
    return jsonify({'message': 'Images edited and saved successfully', 'edited_images': edited_image_path})


if __name__ == '__main__':
    app.run(debug=True)