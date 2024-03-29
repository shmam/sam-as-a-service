import requests
import json
import spotipy
import spotipy.util as util

from . import config as keys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import pi

client_id = keys.spotify_client_id
client_secret = keys.spotify_client_secret
grant_type = 'authorization_code'
scopes = "user-read-recently-played user-read-playback-state"
username = "sayuuuummmm"

def write_token_to_file(string): 
    file = open("token.txt","w")
    file.write(string)
    file.close()

def read_token_from_file(filename): 
    file = open(filename, "r")
    data = file.readline()

    if isinstance(data, bytes): 
        data = data.decode('ascii')
        
    return data 

def resolvetoken():
    oauth_token = read_token_from_file("token.txt")

    if not oauth_token:
        oauth_token = client_auth(oauth_token)
        write_token_to_file(oauth_token)
    else: 
        if test_token(oauth_token): 
            return oauth_token
        else: 
            oauth_token = client_auth(oauth_token)
            write_token_to_file(oauth_token)
    return oauth_token


def test_token(oauth_token): 
    url = "https://api.spotify.com/v1/me/player"
    data = requests.get(url, headers={"Authorization": 'Bearer ' + oauth_token})
    return (data.status_code == 200)

def client_auth(oauth_token):
    token = util.prompt_for_user_token(username,scopes,client_id=client_id,client_secret=client_secret,redirect_uri='https://github.com/shmam')
    return token


def getMyCurrentPlayback():
    oauth_token = resolvetoken()
    url = "https://api.spotify.com/v1/me/player"
    data = requests.get(url, headers={"Authorization": 'Bearer ' + oauth_token})
    if data.status_code == 200: 
        data = data.json()
        track_id = data['item']['id']
        track_name = data['item']['name']
        track_uri = data['item']['uri']
        track_external_url = data['item']['external_urls']['spotify']
        artists_name = ""
        for i in data['item']['artists']: 
            artists_name += (i['name'] + ", ")

        current_track  = { 
            "track_id" : track_id, 
            "track_name": track_name, 
            "track_uri": track_uri, 
            "track_external_url": track_external_url, 
            "artists_name": artists_name[:-2]
        }
        return current_track 
    else:
        return "user is not playing any tracks"


def getMyRecentTracks(): 
    oauth_token = resolvetoken()
    url = "https://api.spotify.com/v1/me/player/recently-played"
    data = requests.get(url, headers={"Authorization": 'Bearer ' + oauth_token}).json()
    tracks = []
    for item in data['items']:
        artists_name = ""
        for i in item['track']['artists']: 
            artists_name += (i['name'] + ",")
        track  = { 
            "track_id" : item['track']['id'], 
            "track_name": item['track']['name'], 
            "track_uri": item['track']['uri'], 
            "track_external_url": item['track']['external_urls']['spotify'], 
            "artists_name": artists_name[:-1]
        }
        tracks.append(track) 
    return tracks


def recent_tracks_audio_features(recent_tracks):
    # Resolve that the token works and is most recent
    oauth_token = resolvetoken()
    url = "https://api.spotify.com/v1/audio-features"
    track_ids = ""

    # Cycle through the 5 most recently played tracks
    num = 5
    for idx in range(0,num): 
        track_ids += recent_tracks[idx]["track_id"] + ","
        print(recent_tracks[idx]["track_name"])

    # Make the API call to get the data
    track_ids = track_ids[:-1]
    url = (url + "/?ids=" + track_ids)
    data = requests.get(url , headers={"Authorization": 'Bearer ' + oauth_token}).json()

    # The values to return
    avg_value = {
        "duration_ms" : 0,
        "key" : 0,
        "mode" : 0,
        "time_signature" : 0,
        "acousticness" : 0,
        "danceability" : 0,
        "energy" : 0,
        "instrumentalness" : 0,
        "liveness" : 0,
        "loudness" : 0,
        "speechiness" : 0,
        "valence" : 0,
        "tempo" : 0
    }

    # Summation
    for item in data["audio_features"]: 
        for category in avg_value.keys():
            try: 
                avg_value[category] += item[category]
            except TypeError: 
                avg_value[category] += 0
    
    # Divide by the number of items to get the average
    for category in avg_value.keys(): 
            avg_value[category] /= num

    return avg_value


def generateRadarChart(avg_value):

    display_value = {
        "acousticness" : 0,
        "danceability" : 0,
        "energy" : 0,
        "liveness" : 0,
        "speechiness" : 0,
    }

    for category in display_value.keys(): 
        display_value[category] = avg_value[category]

    categories = list(display_value.keys())
    values = list(display_value.values())

    values += values[:1] # repeat the first value to close the circular graph
    angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
    angles += angles[:1]

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8),subplot_kw=dict(polar=True))

    plt.xticks(angles[:-1], categories, color='grey', size=20)
    plt.yticks(np.arange(1, 2), ['1'],
            color='grey', size=12)
    plt.ylim(0, 1)
    ax.set_rlabel_position(30)
    
    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, 'skyblue', alpha=0.4)
    plt.title("Generated Audio Analysis of Past 5 Tracks", size=20)
    plt.savefig("img.png")

    return None

    

def printPlayButtons(track_array):
    for track in track_array: 
        element = '<iframe src="' + track['track_external_url'] + '" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'
        print(element)

    