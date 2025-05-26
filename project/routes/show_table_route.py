from flask import Blueprint, request, render_template, g
import os
from config import UPLOAD_FOLDER
from utils.helpers import read_csv

show_table = Blueprint('show_table', __name__)

@show_table.route('/show_first_rows', methods=['POST'])
def show_first_rows():
    file_path = request.form['file_path']
    g.file_path = file_path  # Make file path available to context processor

    return render_template('index.html',
                           success=True,
                           filename=file_path,
                           current_tab='table-section')  # This activates the "Show First Rows" tab
