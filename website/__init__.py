from flask import Flask
from .spotify_login import spotify_login


def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    app.register_blueprint(spotify_login, url_prefix='/')
    return app


