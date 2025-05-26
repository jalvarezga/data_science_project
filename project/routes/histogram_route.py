from flask import Blueprint, render_template, request,g
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

histogram = Blueprint('histogram', __name__)
#put the function from helpers

def plot_histogram(df, column_name, color):
    fig, ax = plt.subplots()
    df[column_name].dropna().hist(bins=20, color=color, edgecolor='black', ax=ax)
    ax.set_title(f"Histogram of {column_name}")
    ax.set_xlabel(column_name)
    ax.set_ylabel('Frequency')
    buf = io.BytesIO()
    FigureCanvas(fig).print_png(buf)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@histogram.route('/show_histogram', methods=['POST'])
def show_histogram():
    file_path = request.form['file_path']
    g.file_path = file_path 
    column_name = request.form['column_name']
    color = request.form['color']

    full_path = os.path.join(UPLOAD_FOLDER, file_path)
    df = read_csv(full_path)

    # Filter numeric columns only
    column_names = df.select_dtypes(include=['number']).columns.tolist()
    no_numeric = len(column_names) == 0

    # Recalculate first rows to display the table again
    #first_rows = df.head().to_html(classes='table', index=False)
    #note that now the show histogram function needs to re-run the first section that contains the show first rows,
    #  so that when we trigger the show histrogram, the first rows don't get lost.

    

    # Generate histogram image
    img_str = plot_histogram(df, column_name, color)

    return render_template('index.html',
                           success=True,
                           filename=file_path,
                           column_names=column_names,
                           histogram_img=img_str,
                           #first_rows=first_rows,#note that we need to return the show first rows of the table here too. otherwise when we plot a histogram the table will not be rendered in the website
                           column_name=column_name,
                           color=color,
                           no_numeric=no_numeric,
                           current_tab='histogram-section')
