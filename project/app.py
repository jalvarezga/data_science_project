from flask import Flask, g
from routes.main_routes import main
from routes.histogram_route import histogram
from routes.scatter_route import scatter
from routes.summary_route import summary
from routes.show_rows_route import show_rows  
from utils.helpers import read_csv
from config import UPLOAD_FOLDER
import os
import matplotlib

matplotlib.use('Agg')

app = Flask(__name__)

app.register_blueprint(main)
app.register_blueprint(histogram)
app.register_blueprint(scatter)
app.register_blueprint(summary)
app.register_blueprint(show_rows) 



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
