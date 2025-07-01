from flask import Blueprint, request, jsonify
import pandas as pd
import os
from config import UPLOAD_FOLDER
from utils.helpers import read_csv

data_types = Blueprint('data_types', __name__)

@data_types.route('/get_data_types', methods=['POST'])
def get_data_types():
    data = request.get_json()
    file_path = data.get('file_path')
    df = read_csv(os.path.join(UPLOAD_FOLDER, file_path))

    # Build data type info
    data_types_info = []
    for col in df.columns:
        dtype = df[col].dtype
        if pd.api.types.is_numeric_dtype(dtype):
            inferred_type = 'Numeric (Float/Integer)'
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            inferred_type = 'Date/Time'
        elif pd.api.types.is_bool_dtype(dtype):
            inferred_type = 'Boolean'
        elif pd.api.types.is_object_dtype(dtype):
            if df[col].nunique() / len(df[col]) < 0.5:
                inferred_type = 'Categorical (Text/Mixed)'
            else:
                inferred_type = 'Text/String'
        else:
            inferred_type = str(dtype)

        data_types_info.append({'column_name': col, 'data_type': inferred_type})

    data_types_df = pd.DataFrame(data_types_info)
    data_types_html = data_types_df.to_html(classes='table table-striped', index=False)

    return jsonify({'html': data_types_html})
