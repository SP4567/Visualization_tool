from flask import Flask, request, render_template, redirect, url_for, flash
import os
from dashboard import create_dash_app
from utils import setup_logging, handle_uploaded_file

app = Flask(__name__)

logger = setup_logging()

# Initialize Dash app
dash_app = create_dash_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    model_path, text_content = handle_uploaded_file(request, app.config['UPLOAD_FOLDER'])
    if model_path and text_content:
        flash('Files uploaded successfully.')
        app.config['MODEL_PATH'] = model_path
        app.config['TEXT_CONTENT'] = text_content
    else:
        flash('File upload failed.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
