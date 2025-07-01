from flask import Blueprint, render_template, request
from utils.helpers import read_csv
import os
import pandas as pd
from config import UPLOAD_FOLDER

data_types = Blueprint('data_types', __name__)

@data_types.route('/show_data_types', methods=['POST'])
def show_data_types():
    file_path = request.form['file_path']

    # Load DataFrame from uploaded CSV
    full_path = os.path.join(UPLOAD_FOLDER, file_path)
    df = read_csv(full_path)

    # Gather columns
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    all_columns = df.columns.tolist()
    no_numeric = len(numeric_columns) == 0

    # Compute first rows for possible reuse
    first_rows = df.head().to_html(classes='table', index=False)

    # Infer and format data types in user-friendly way
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

        data_types_info.append({
            'column_name': col,
            'data_type': inferred_type
        })

    # Turn into HTML table
    data_types_df = pd.DataFrame(data_types_info)
    data_types_html = data_types_df.to_html(classes='table table-striped', index=False)

    return render_template('index.html',
                           success=True,
                           filename=file_path,
                           column_names=numeric_columns,
                           all_column_names=all_columns,
                           first_rows=first_rows,
                           data_types_html=data_types_html,
                           no_numeric=no_numeric,
                           current_tab='data-types-section')
