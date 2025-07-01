from flask import Blueprint, render_template, request
<<<<<<< HEAD
from utils.helpers import read_csv
import os
import pandas as pd
from config import UPLOAD_FOLDER
=======
import pandas as pd
import os
from config import UPLOAD_FOLDER
from utils.helpers import read_csv # Assuming read_csv can handle both CSV and Excel
>>>>>>> parent of b59f28a (standardize buttons and some files of data types and show rows)

data_types = Blueprint('data_types', __name__)
@data_types.route('/show_data_types', methods=['POST'])

<<<<<<< HEAD
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
=======

def show_data_types():
    file_path = request.form['file_path']
    df = read_csv(os.path.join(UPLOAD_FOLDER, file_path))
    # Get data types and convert to a more readable format
>>>>>>> parent of b59f28a (standardize buttons and some files of data types and show rows)
    data_types_info = []
    for col in df.columns:
        dtype = df[col].dtype
        # Infer more user-friendly types
        if pd.api.types.is_numeric_dtype(dtype):
            inferred_type = 'Numeric (Float/Integer)'
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            inferred_type = 'Date/Time'
        elif pd.api.types.is_bool_dtype(dtype):
            inferred_type = 'Boolean'
        elif pd.api.types.is_object_dtype(dtype):
            # Try to infer if it's categorical or just general text
            #Gamini did this part! I don't like this specific part beacasue it 'guessses' if a variable is likely categorical or not.
            #that's ambiguous!! I will refine it later
            if df[col].nunique() / len(df[col]) < 0.5: # Simple heuristic for categorical
                inferred_type = 'Categorical (Text/Mixed)'
            else:
                inferred_type = 'Text/String'
        else:
            inferred_type = str(dtype) # Fallback to pandas dtype string

        data_types_info.append({
            'column_name': col,
            'data_type': inferred_type
        })

<<<<<<< HEAD
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
=======
    # Prepare data for HTML table
    # You can convert this list of dicts to a pandas DataFrame for easy HTML conversion
    data_types_df = pd.DataFrame(data_types_info)
    data_types_html = data_types_df.to_html(classes='table table-striped', index=False)

    all_columns = df.columns.tolist()
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    # You'll likely need the filename and first_rows to maintain context in the main index.html
    first_rows = df.head().to_html(classes='table', index=False)

    return render_template('index.html',
                           success=True,
                           filename=file_path,
                           first_rows=first_rows,
                           column_names=numeric_columns,          # For summary/histogram/etc.
                           all_column_names=all_columns,          # For View Data Types display
                           data_types_html=data_types_html,
>>>>>>> parent of b59f28a (standardize buttons and some files of data types and show rows)
                           current_tab='data-types-section')
