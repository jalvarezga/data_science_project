# routes/show_rows_route.py

from flask import Blueprint, render_template, request, g
from utils.helpers import read_csv
from config import UPLOAD_FOLDER
import os

show_rows = Blueprint('show_rows', __name__)

@show_rows.route('/show_rows', methods=['POST'])
def show_rows_view():
    file_path = request.form.get('file_path')
    g.file_path = file_path

    full_path = os.path.join(UPLOAD_FOLDER, file_path)
    try:
        df = read_csv(full_path)
        first_rows = df.head().to_html(classes='table', index=False)

        column_names = df.select_dtypes(include=['number']).columns.tolist()
        no_numeric = len(column_names) == 0

        return render_template('index.html',
                               success=True,
                               filename=file_path,
                               first_rows=first_rows,
                               no_numeric=no_numeric,
                               current_tab='table-section')
    except Exception:
        return render_template('index.html',
                               success=True,
                               filename=file_path,
                               first_rows="<p>Could not load data.</p>",
                               no_numeric=True,
                               current_tab='table-section')
