from flask import Flask
from flask_session import Session
import secrets

app = Flask(__name__)

# Secure secret key
app.secret_key = secrets.token_hex(32)  # Or manually paste a fixed value below e.g. '9f1a4e9dfe3b49e6a75b632a52f59eb4c2836a95bb4b8499a25b5dcce71dd1ef'

# Session config
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
