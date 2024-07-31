from flask import Flask, request, render_template, redirect, url_for, flash, session
import os
from dashboard import create_dash_app
from utils import handle_uploaded_file
from log_config import logger

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.secret_key = 'supersecretkey'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Dash app
dash_app = create_dash_app(app)
app = dash_app.server

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    logger.info("Upload route accessed")
    try:
        logger.info(f"Files in request: {request.files}")
        model_path, text_content = handle_uploaded_file(request, app.config['UPLOAD_FOLDER'])
        logger.info(f"Model path: {model_path}, Text content length: {len(text_content) if text_content else 0}")
        if model_path and text_content:
            flash('Files uploaded successfully.')
            session['MODEL_PATH'] = model_path
            session['TEXT_CONTENT'] = text_content
            logger.info(f"Session after upload: {session}")
            return redirect(url_for('index'))  # Redirect to Dash app
        else:
            flash('File upload failed.')
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        flash(f"An error occurred: {str(e)}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
