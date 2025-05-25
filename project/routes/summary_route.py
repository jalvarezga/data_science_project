from flask import Blueprint, render_template, request
from utils.helpers import allowed_file, read_csv, clear_cache
import os
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS


#helpers modules
import os
import pandas as pd
import base64
import io
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

summary = Blueprint('summary', __name__)
  
  
#include the function from helpers
def compute_summary(df, col1, col2):
    summary = {}
    for col in [col1, col2]:
        summary[col] = {
            'mean': round(df[col].mean(), 3),
            'std': round(df[col].std(), 3),
            "Min": df[col].min(),
            '25%': round(df[col].quantile(0.25), 3),
            '50%': round(df[col].median(), 3),
            '75%': round(df[col].quantile(0.75), 3),
            "Max": df[col].max(),
            'missing': int(df[col].isnull().sum())
        }
    corr = round(df[[col1, col2]].corr().iloc[0, 1], 3)
    return summary, corr


@summary.route('/show_summary', methods=['POST'])
def show_summary():
    file_path = request.form['file_path']
    col1 = request.form['col1']
    col2 = request.form['col2']

    df = read_csv(os.path.join(UPLOAD_FOLDER, file_path))

    column_names = df.select_dtypes(include=['number']).columns.tolist()
    no_numeric = len(column_names) == 0
    first_rows = df.head().to_html(classes='table', index=False)

    if no_numeric:
        return render_template('index.html',
                               success=True,
                               filename=file_path,
                               column_names=[],
                               first_rows=first_rows,
                               no_numeric=True,
                               summary_data=None,
                               current_tab='summary-section')

    summary_data, correlation = compute_summary(df, col1, col2)

    return render_template('index.html',
                           success=True,
                           filename=file_path,
                           column_names=column_names,
                           first_rows=first_rows,
                           summary_data=summary_data,
                           correlation=correlation,
                           col1=col1,
                           col2=col2,
                           no_numeric=False,
                           current_tab='summary-section')
