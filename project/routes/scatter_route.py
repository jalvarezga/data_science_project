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

scatter = Blueprint('scatter', __name__)
#include the helpers function. 
def plot_scatter(df, x_column, y_column, color):
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(df[x_column], df[y_column], color=color)
    ax.set_title(f"Scatter Plot of {x_column} vs {y_column}")
    ax.set_xlabel(x_column)
    ax.set_ylabel(y_column)

    buf = io.BytesIO()
    FigureCanvas(fig).print_png(buf)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

@scatter.route('/show_scatter', methods=['POST'])
def show_scatter():
    file_path = request.form['file_path']
    x_column = request.form['x_column']
    y_column = request.form['y_column']
    color = request.form['color']

    df = read_csv(os.path.join(UPLOAD_FOLDER, file_path))



    ##Restrict to numeric columns only
    column_names = df.select_dtypes(include=['number']).columns.tolist()
    no_numeric = len(column_names) == 0
     ## If no numeric columns, skip plotting and show message
    if no_numeric:
        return render_template('index.html',
                               success=True,
                               filename=file_path,
                               column_names=column_names,
                               first_rows=df.head().to_html(classes='table', index=False),
                               no_numeric=True,
                               scatter_img=None,
                               current_tab='scatter-section')
    


    
    #Continue to plot if there are valid numeric columns
    first_rows = df.head().to_html(classes='table', index=False)
    scatter_img = plot_scatter(df, x_column, y_column, color)

    return render_template('index.html',
                           success=True,
                           filename=file_path,
                           column_names=column_names,
                           first_rows=first_rows,
                           scatter_img=scatter_img,
                           x_column=x_column,
                           y_column=y_column,
                           color=color,
                           no_numeric=False,
                           current_tab='scatter-section')






