from flask import Blueprint, request, jsonify
import os
from config import UPLOAD_FOLDER
from utils.helpers import read_csv

show_rows = Blueprint('show_rows', __name__)

@show_rows.route('/show_rows', methods=['POST'])
def get_first_rows():
    data = request.get_json()
    file_path = data['file_path']
    df = read_csv(os.path.join(UPLOAD_FOLDER, file_path))
    first_rows_html = df.head().to_html(classes='table table-striped', index=False)
    return jsonify({'html': first_rows_html})
