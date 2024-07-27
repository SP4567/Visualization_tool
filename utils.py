import os
import logging
from flask import flash

def setup_logging(log_file='app.log'):
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    logger = logging.getLogger(__name__)
    return logger

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_file(file, upload_folder):
    if file and allowed_file(file.filename, {'h5', 'txt'}):
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path
    else:
        flash('Invalid file type. Only .h5 and .txt files are allowed.')
        return None

def secure_filename(filename):
    return os.path.basename(filename)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in the {getattr(form, field).label.text} field - {error}")

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def handle_uploaded_file(request, upload_folder):
    model_file = request.files.get('model')
    text_file = request.files.get('text')
    model_path, text_content = None, None

    if model_file:
        model_path = save_file(model_file, upload_folder)
    if text_file:
        text_file_path = save_file(text_file, upload_folder)
        text_content = read_text_file(text_file_path)

    return model_path, text_content
