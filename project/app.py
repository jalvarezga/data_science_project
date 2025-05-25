from flask import Flask
from routes.main_routes import main
from routes.histogram_route import histogram
from routes.scatter_route import scatter
from routes.summary_route import summary
import matplotlib

matplotlib.use('Agg')  # No GUI for matplotlib

app = Flask(__name__)

app.register_blueprint(main)
app.register_blueprint(histogram)
app.register_blueprint(scatter)
app.register_blueprint(summary)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
