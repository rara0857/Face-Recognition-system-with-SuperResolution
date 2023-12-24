# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
import threading
import csv
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
import zipfile
from io import BytesIO
from werkzeug.utils import secure_filename
import shutil
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'downloads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index_and_delete')
def index_and_delete():
    os.system("python delete.py")
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    rel_file_path = os.path.relpath(file_path, app.config['UPLOAD_FOLDER'])
    return redirect(url_for('process', file_path=rel_file_path))

@app.route('/upload_output', methods=['POST'])
def upload_output():
    if 'output_csv' not in request.files:
        return redirect(request.url)

    file = request.files['output_csv']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['OUTPUT_FOLDER'], filename))
        return redirect(url_for('download', filename=filename))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'csv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/process/<file_path>')
def process(file_path):
    global completed
    def button_event():
        print("\n--------------Cut img-----------------\n")
        os.system("python cut.py " + os.path.join(app.config['UPLOAD_FOLDER'], file_path))

        print("\n--------------Filter img--------------\n")
        os.system("python filter.py")

        print("\n--------------Resize img--------------\n")
        os.system("python " + os.path.join("data", "prepare_data.py"))

        print("\n--------------Recognition-------------\n")
        os.system("python test.py")
        
        print("\n--------------SR process--------------\n")
        os.system("python infer.py")
        
        os.system("python merge.py")
        completed.set()

    completed = threading.Event()
    t = threading.Thread(target=button_event)
    t.start()
    return render_template('loading.html')

@app.route('/download')
def download():
    rows = []
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.csv')
    with open(output_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rows.append(row)
    return render_template('download.html', rows=rows)

@app.route('/delete', methods=['POST'])
def delete():
    os.system("python delete.py")
    return redirect(url_for('index'))

@app.route('/output')
def download_output():
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.csv')
    return send_file(output_path, as_attachment=True)

@app.route('/delete_output', methods=['POST'])
def delete_output():
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.csv')
    try:
        os.remove(output_path)
    except OSError:
        print(' ')
    return redirect(url_for('index'))

@app.route('/delete_student', methods=['POST'])
def delete_student():
    name = request.form['name']
    student_id = request.form['student_id']
    folder_name = f'{name}_{student_id}'
    path = os.path.join('Faces', folder_name)

    if os.path.exists(path):
        shutil.rmtree(path)
        print(f'Deleted {folder_name} successfully!')
        if os.path.exists('Faces/representations_facenet512.pkl'):
            os.remove("Faces/representations_facenet512.pkl")
    else:
        print(f'{folder_name} does not exist!')
    return redirect(url_for('index'))

@app.route('/delete_all_students', methods=['POST'])
def delete_all_students():
    folder_path = 'Faces'
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        os.mkdir(folder_path)
        print('Deleted all students successfully!')
    else:
        print('Faces folder does not exist!')
    return redirect(url_for('index'))

@app.route('/upload_faces', methods=['POST'])
def upload_faces():
    name = request.form['name']
    student_id = request.form['student_id']
    folder_name = f"{name}_{student_id}"
    folder_path = os.path.join("Faces", folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    files = request.files.getlist('files')
    for file in files:
        file_path = os.path.join(folder_path, file.filename)
        file.save(file_path)
    if os.path.exists('Faces/representations_facenet512.pkl'):
        os.remove("Faces/representations_facenet512.pkl")
    return redirect(url_for('index'))

def zip_files_and_download(file_folder, zip_name):
    file_paths = [os.path.join(file_folder, f) for f in os.listdir(file_folder) if f.endswith(".png")]

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in file_paths:
            zf.write(file_path, os.path.basename(file_path))
    
    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name=zip_name, mimetype="application/zip")

@app.route('/download_failed_imgs')
def download_failed_imgs():
    failed_img_folder = 'downloads/failed_img'
    return zip_files_and_download(failed_img_folder, 'failed_imgs.zip')

@app.route('/download_merged_imgs')
def download_merged_imgs():
    merged_img_folder = 'downloads/merged_images'
    return zip_files_and_download(merged_img_folder, 'merged_imgs.zip')

@app.route('/check_completed')
def check_completed():
    if completed.is_set():
        return "completed"
    else:
        return 'not completed yet'

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
