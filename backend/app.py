from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import requests
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        return None

    json_result = response.json()
    return json_result.get("access_token")

@app.route('/search_artist', methods=['GET'])
def search_artist():
    token = get_token()
    if not token:
        return jsonify({"error": "Unable to get token"}), 500

    artist_name = request.args.get('artist_name')
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Unable to search artist"}), 500

    artist_data = response.json().get("artists", {}).get("items", [])
    if not artist_data:
        return jsonify({"error": "No artist found"}), 404

    artist = artist_data[0]
    artist_info = {
        "id": artist["id"],
        "name": artist["name"],
        "image_url": artist["images"][0]["url"] if artist["images"] else None
    }
    return jsonify(artist_info)

@app.route('/top_tracks', methods=['GET'])
def top_tracks():
    token = get_token()
    if not token:
        return jsonify({"error": "Unable to get token"}), 500

    artist_id = request.args.get('artist_id')
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Unable to get top tracks"}), 500

    tracks_data = response.json().get("tracks", [])
    tracks = [
        {"name": track["name"], "url": track["external_urls"]["spotify"]}
        for track in tracks_data
    ]
    return jsonify(tracks)

if __name__ == '__main__':
    app.run(debug=True)
