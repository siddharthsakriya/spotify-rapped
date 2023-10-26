import base64
from flask import request, redirect, session, render_template, Blueprint, g
import requests

spotify_login = Blueprint('spotify_login', __name__)

CLIENT_ID = '36aafcd436fd4b5696fa262f0cbc4d3c'
CLIENT_SECRET = '2f8abf7c56f14ce7bd40021beb4b539c'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
base64_encoded_client_credentials = base64.b64encode(credentials.encode()).decode()


@spotify_login.route('/')
def home():
    return render_template('base.html')


@spotify_login.route('/login')
def login():
    # Construct the Spotify authorization URL
    auth_url = (f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri="
                f"{REDIRECT_URI}&scope=user-library-read")
    return redirect(auth_url)


@spotify_login.route('/callback')
def callback():
    code = request.args.get('code')
    token_response = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }, headers={
        'Authorization': f'Basic {base64_encoded_client_credentials}'
    })
    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data.get('access_token')
        session['access_token'] = access_token
        return redirect('/my_playlists')
    else:
        return 'Authentication failed.'


@spotify_login.route('/my_playlists')
def my_playlists():
    access_token = session.get('access_token')
    if not access_token:
        return redirect('/login')

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.spotify.com/v1/me/playlists', headers =headers)

    if response.status_code == 200:
        playlists = response.json()
        print(playlists)
        g.access_token = access_token
        return render_template('home.html')
    else:
        return "<h1>error</h1>"
