import base64
from flask import Flask, jsonify, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

CLIENT_ID = '36aafcd436fd4b5696fa262f0cbc4d3c'
CLIENT_SECRET = '33a0fe4a229d4bc599b2c0f9ab59370b'
REDIRECT_URI = 'http://127.0.0.1:8000/callback'
credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
base64_encoded_client_credentials = base64.b64encode(credentials.encode()).decode()

@app.route('/')
def hello():
    return '<h1>hello world</h1>'

@app.route('/login')
def login():
    # Construct the Spotify authorization URL
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=user-library-read"
    return redirect(auth_url)

@app.route('/callback')
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

@app.route('/my_playlists')
def my_playlists():
    return '<h1>SUCCESS</h1>'

if __name__ == '__main__':
    app.run(debug=True, port = 8000)