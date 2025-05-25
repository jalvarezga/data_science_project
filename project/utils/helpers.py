import os
import pandas as pd
import base64
import io
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
# Global cache for DataFrames
dataframe_cache = {}
def read_csv(filepath):
    if filepath not in dataframe_cache:
        df = pd.read_csv(filepath)
        dataframe_cache[filepath] = df
    return dataframe_cache[filepath]

def clear_cache():
    dataframe_cache.clear()




