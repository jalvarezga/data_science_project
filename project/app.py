from flask import Flask, g
from routes.main_routes import main
from routes.histogram_route import histogram
from routes.scatter_route import scatter
from routes.summary_route import summary
from routes.show_table_route import show_table
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
app.register_blueprint(show_table)


@app.context_processor
def inject_first_rows():
    file_path = getattr(g, 'file_path', None)
    if file_path:
        full_path = os.path.join(UPLOAD_FOLDER, file_path)
        try:
            df = read_csv(full_path)
            return {'first_rows': df.head().to_html(classes='table', index=False)}
        except Exception:
            return {'first_rows': "<p>Could not load data.</p>"}
    return {'first_rows': ""}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
