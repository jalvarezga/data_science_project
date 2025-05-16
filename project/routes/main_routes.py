from flask import Blueprint, render_template, request
from utils.helpers import (
    allowed_file, read_csv, plot_histogram, plot_scatter,
    compute_summary, store_df_in_session, load_df_from_session
)
import os
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS

main = Blueprint('main', __name__)
@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            df = read_csv(filepath)

            # Store the DataFrame in session
            store_df_in_session(df)

            # Now use it like usual
            first_rows = df.head().to_html(classes='table', index=False)
            column_names = df.select_dtypes(include='number').columns.tolist()
            no_numeric = len(column_names) == 0

            return render_template('index.html',
                                   success=True,
                                   first_rows=first_rows,
                                   filename=file.filename,
                                   column_names=column_names,
                                   no_numeric=no_numeric)
    return render_template('index.html', success=False)

@main.route('/show_histogram', methods=['POST'])
def show_histogram():
    df = load_df_from_session()
    if df is None:
        return redirect('/')

    column_name = request.form['column_name']
    color = request.form['color']

    column_names = df.select_dtypes(include='number').columns.tolist()
    first_rows = df.head().to_html(classes='table', index=False)
    no_numeric = len(column_names) == 0
    img_str = plot_histogram(df, column_name, color)

    return render_template('index.html',
                           success=True,
                           filename='',
                           column_names=column_names,
                           histogram_img=img_str,
                           first_rows=first_rows,
                           column_name=column_name,
                           color=color,
                           no_numeric=no_numeric)
@main.route('/show_scatter', methods=['POST'])
def show_scatter():
    df = load_df_from_session()
    if df is None:
        return redirect('/')

    x_column = request.form['x_column']
    y_column = request.form['y_column']
    color = request.form['color']

    column_names = df.select_dtypes(include='number').columns.tolist()
    no_numeric = len(column_names) == 0
    first_rows = df.head().to_html(classes='table', index=False)

    if no_numeric:
        return render_template('index.html',
                               success=True,
                               column_names=[],
                               first_rows=first_rows,
                               no_numeric=True,
                               scatter_img=None)

    scatter_img = plot_scatter(df, x_column, y_column, color)

    return render_template('index.html',
                           success=True,
                           column_names=column_names,
                           first_rows=first_rows,
                           scatter_img=scatter_img,
                           x_column=x_column,
                           y_column=y_column,
                           color=color,
                           no_numeric=False)


@main.route('/show_summary', methods=['POST'])
def show_summary():
    df = load_df_from_session()
    if df is None:
        return redirect('/')

    col1 = request.form['col1']
    col2 = request.form['col2']

    column_names = df.select_dtypes(include='number').columns.tolist()
    no_numeric = len(column_names) == 0
    first_rows = df.head().to_html(classes='table', index=False)

    if no_numeric:
        return render_template('index.html',
                               success=True,
                               column_names=[],
                               first_rows=first_rows,
                               no_numeric=True,
                               summary_data=None)

    summary_data, correlation = compute_summary(df, col1, col2)

    return render_template('index.html',
                           success=True,
                           column_names=column_names,
                           first_rows=first_rows,
                           summary_data=summary_data,
                           correlation=correlation,
                           col1=col1,
                           col2=col2,
                           no_numeric=False)
