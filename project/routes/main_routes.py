from flask import Blueprint, render_template, request
from utils.helpers import allowed_file, read_csv, clear_cache
import os
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            df = read_csv(filepath)
            first_rows = df.head().to_html(classes='table', index=False)
            column_names = df.select_dtypes(include=['number']).columns.tolist()
            no_numeric = len(column_names) == 0
            return render_template('index.html', success=True, first_rows=first_rows,
                                   filename=file.filename, column_names=column_names, no_numeric=no_numeric)
    return render_template('index.html', success=False)


@main.route('/reset', methods=['POST'])
def reset():
    clear_cache()
    return render_template('index.html', success=False, current_tab='upload-section')
