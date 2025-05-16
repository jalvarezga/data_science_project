import os
import pandas as pd
import base64
import io
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import session

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def read_csv(filepath):
    df = pd.read_csv(filepath)
    return df


def store_df_in_session(df):
    session['df'] = df.to_json()  # Save as JSON string

def load_df_from_session():
    if 'df' in session:
        return pd.read_json(session['df'])
    return None




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

def compute_summary(df, col1, col2):
    summary = {}
    for col in [col1, col2]:
        summary[col] = {
            'mean': round(df[col].mean(), 3),
            'std': round(df[col].std(), 3),
            '25%': round(df[col].quantile(0.25), 3),
            '50%': round(df[col].median(), 3),
            '75%': round(df[col].quantile(0.75), 3),
            'missing': int(df[col].isnull().sum())
        }
    corr = round(df[[col1, col2]].corr().iloc[0, 1], 3)
    return summary, corr

