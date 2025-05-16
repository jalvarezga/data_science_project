# app.py
from flask import Flask
from flask_session import Session

app = Flask(__name__)

# Store session data in filesystem
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'your_really_strong_secret_key_here'  # Use secrets.token_hex(32)
Session(app)

# Import and register blueprint
from routes.main_routes import main
app.register_blueprint(main)
