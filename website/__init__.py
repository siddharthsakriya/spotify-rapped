from flask import Flask
from .spotify_init import spotify_init
def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    app.register_blueprint(spotify_init, url_prefix='/')

    return app