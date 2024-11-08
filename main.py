from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from skimage import io
from skimage.filters import threshold_sauvola, threshold_niblack
import numpy as np
import os
import cv2
from PIL import Image, ImageEnhance
from skimage.util import img_as_uint, img_as_ubyte

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

    return render_template('result.html', original=filename, processed=processed_filename, method = "Увеличение резкости")
@app.route('/sauvola_image/<filename>')
def sauvola_image(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = io.imread(file_path, as_gray=True)
    sauvola_thres = threshold_sauvola(img,45,0.35, 77)
    binary_saulova = img > sauvola_thres
    sauvola_img = img_as_ubyte(binary_saulova)
    sauvola_filename = f"sauvola_{filename}"
    sauvola_path = os.path.join(app.config['UPLOAD_FOLDER'], sauvola_filename)
    cv2.imwrite(sauvola_path, sauvola_img)

    return render_template('result.html', original=filename, processed=sauvola_filename, method = "Метод Сауволы")

@app.route('/niblack_image/<filename>')
def niblack_image(filename):
 file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
 img = io.imread(file_path, as_gray=True)
 niblack_thres = threshold_niblack(img,45,0.35)
 binary_niblack = img > niblack_thres
 niblack_img = img_as_ubyte(binary_niblack)
 niblack_filename = f"niblack_{filename}"
 niblack_path = os.path.join(app.config['UPLOAD_FOLDER'], niblack_filename)
 cv2.imwrite(niblack_path, niblack_img)
 return render_template('result.html', original=filename, processed = niblack_filename, method = "Метод Ниблека")

@app.route('/adaptive_image/<filename>')
def adaptive_image(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = io.imread(file_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    adaptive_thres = cv2.adaptiveThreshold(img_gray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    adaptive_filename = f"adaptive_{filename}"
    adaptive_path = os.path.join(app.config['UPLOAD_FOLDER'], adaptive_filename)
    cv2.imwrite(adaptive_path, adaptive_thres)
    return render_template('result.html', original=filename, processed = adaptive_filename, method = "Гауссовая адаптивная пороговая обработка")

if __name__ == '__main__':
    app.run(debug=True)
