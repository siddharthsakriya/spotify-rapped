import base64
from flask import request, redirect, session, render_template, Blueprint
import requests

spotify_init = Blueprint('spotify_init', __name__)

CLIENT_ID = '36aafcd436fd4b5696fa262f0cbc4d3c'
CLIENT_SECRET = '33a0fe4a229d4bc599b2c0f9ab59370b'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
base64_encoded_client_credentials = base64.b64encode(credentials.encode()).decode()

@spotify_init.route('/')
def home():
    return render_template('base.html')

@spotify_init.route('/login')
def login():
    # Construct the Spotify authorization URL
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=user-library-read"
    return redirect(auth_url)

@spotify_init.route('/callback')
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

@spotify_init.route('/my_playlists')
def my_playlists():
    access_token = session.get('access_token')
    if not access_token:
        return redirect('/login')

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers)

    if response.status_code == 200:
        playlists = response.json()
        print(playlists)
        return "<h1>hi</h1>"
    else:
        return "<h1>error</h1>"
