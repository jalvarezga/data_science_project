from flask import Flask
from routes.main_routes import main
import matplotlib

matplotlib.use('Agg')  # No GUI for matplotlib

app = Flask(__name__)
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')