from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'php', 'py'}
app.secret_key = 'your_secret_key'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_image(file):
    try:
        Image.open(file)
        return True
    except Exception:
        return False
    
@app.route('/')
def index():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    print(os.listdir(app.config['UPLOAD_FOLDER']))
    return render_template('index.html', images=images)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file Selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file Selected', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename) and is_valid_image(file):
        filename = secure_filename(str(uuid.uuid4()) + os.path.splitext(file.filename)[1])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Upload Success', 'success')
    else:
        flash('unsupported extension or invalid content', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5000, debug=True)