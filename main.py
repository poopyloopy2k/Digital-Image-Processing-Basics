from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from PIL import Image, ImageEnhance

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создание папки uploads, если она не существует
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return redirect(url_for('uploaded_file', filename=filename))

@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    return render_template('process.html', filename=filename)

@app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/apply_filter/<filename>')
def apply_filter(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = Image.open(file_path)

    # Применение фильтра увеличения резкости
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(7)

    processed_filename = f"processed_{filename}"
    processed_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
    img.save(processed_path)

    return render_template('result.html', original=filename, processed=processed_filename)


if __name__ == '__main__':
    app.run(debug=True)
