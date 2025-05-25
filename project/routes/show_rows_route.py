# show_rows_route.py
from flask import Blueprint, render_template, request
from config import UPLOAD_FOLDER
from utils.helpers import read_csv
import os

show_rows = Blueprint('show_rows', __name__)

@show_rows.route('/show_rows', methods=['POST'])
def show_rows_func():
    file_path = request.form['file_path']
    df = read_csv(os.path.join(UPLOAD_FOLDER, file_path))
    
    first_rows = df.head().to_html(classes='table', index=False)
    column_names = df.columns.tolist()

    # Optional: check for numeric data
    no_numeric = df.select_dtypes(include='number').empty

    return render_template('index.html',
                           success=True,
                           filename=file_path,
                           column_names=column_names,
                           first_rows=first_rows,
                           current_tab='table-section',
                           no_numeric=no_numeric)
