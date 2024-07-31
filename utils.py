import os
from flask import flash
from werkzeug.utils import secure_filename
from log_config import logger

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_file(file, upload_folder):
    if file and allowed_file(file.filename, {'h5', 'txt'}):
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        try:
            file.save(file_path)
            logger.info(f"File saved successfully: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}", exc_info=True)
            flash(f"Error saving file: {str(e)}")
            return None
    else:
        flash('Invalid file type. Only .h5 and .txt files are allowed.')
        return None

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        logger.info(f"Text file read successfully: {file_path}")
        return content
    except Exception as e:
        logger.error(f"Error reading text file: {str(e)}", exc_info=True)
        return None

def handle_uploaded_file(request, upload_folder):
    logger.info("Handling uploaded file")
    model_file = request.files.get('model')
    text_file = request.files.get('text')
    model_path, text_content = None, None

    if model_file:
        logger.info(f"Received model file: {model_file.filename}")
        model_path = save_file(model_file, upload_folder)
    else:
        logger.warning("No model file received")

    if text_file:
        logger.info(f"Received text file: {text_file.filename}")
        text_file_path = save_file(text_file, upload_folder)
        if text_file_path:
            text_content = read_text_file(text_file_path)
    else:
        logger.warning("No text file received")

    logger.info(f"Returning model_path: {model_path}, text_content length: {len(text_content) if text_content else 0}")
    return model_path, text_content
