from flask import Blueprint, render_template, request
from utils.helpers import allowed_file, read_csv, plot_histogram
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
            column_names = df.columns.tolist()
            return render_template('index.html', success=True, first_rows=first_rows,
                                   filename=file.filename, column_names=column_names)
    return render_template('index.html', success=False)

@main.route('/show_histogram', methods=['POST'])



@main.route('/show_histogram', methods=['POST'])
def show_histogram():
    file_path = request.form['file_path']
    column_name = request.form['column_name']
    color = request.form['color']

    full_path = os.path.join(UPLOAD_FOLDER, file_path)
    df = read_csv(full_path)

    # Filter numeric columns only
    column_names = df.select_dtypes(include=['number']).columns.tolist()
    no_numeric = len(column_names) == 0

    # Recalculate first rows to display the table again
    first_rows = df.head().to_html(classes='table', index=False)
    #note that now the show histogram function needs to re-run the first section that contains the show first rows,
    #  so that when we trigger the show histrogram, the first rows don't get lost.

    # Generate histogram image
    img_str = plot_histogram(df, column_name, color)

    return render_template('index.html',
                           success=True,
                           filename=file_path,
                           column_names=column_names,
                           histogram_img=img_str,
                           first_rows=first_rows,
                           column_name=column_name,
                           color=color,
                           no_numeric=no_numeric)

