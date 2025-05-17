from flask import Blueprint, render_template, request
from flask import session, redirect, url_for# for the reset button
from utils.helpers import allowed_file, read_csv, plot_histogram, plot_scatter, compute_summary
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
            first_rows = df.head().to_html(classes='table', index=False)
            column_names = df.select_dtypes(include=['number']).columns.tolist()
            no_numeric = len(column_names) == 0
            return render_template('index.html', success=True, first_rows=first_rows,
                                   filename=file.filename, column_names=column_names, no_numeric=no_numeric)
    return render_template('index.html', success=False)


@main.route('/show_histogram', methods=['POST'])
def show_histogram():
    file_path = request.form['file_path']
    column_name = request.form['column_name']
    color = request.form['color']

    full_path = os.path.join(UPLOAD_FOLDER, file_path)
    df = read_csv(full_path)

    # Filter numeric columns only
    column_names = df.select_dtypes(include=['number']).columns.tolist()
    no_numeric = len(column_names) == 0

    # Recalculate first rows to display the table again
    first_rows = df.head().to_html(classes='table', index=False)
    #note that now the show histogram function needs to re-run the first section that contains the show first rows,
    #  so that when we trigger the show histrogram, the first rows don't get lost.

    # Generate histogram image
    img_str = plot_histogram(df, column_name, color)

    return render_template('index.html',
                           success=True,
                           filename=file_path,
                           column_names=column_names,
                           histogram_img=img_str,
                           first_rows=first_rows,#note that we need to return the show first rows of the table here too. otherwise when we plot a histogram the table will not be rendered in the website
                           column_name=column_name,
                           color=color,
                           no_numeric=no_numeric,
                           current_tab='histogram-section')

@main.route('/show_scatter', methods=['POST'])
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

@main.route('/show_summary', methods=['POST'])
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




@main.route('/reset', methods=['GET'])
def reset():
    session.clear()  # Clears all session data
    return redirect(url_for('main.index'))
