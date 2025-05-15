import os
import pandas as pd
import base64
import io
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def read_csv(filepath):
    df = pd.read_csv(filepath)
    return df

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
