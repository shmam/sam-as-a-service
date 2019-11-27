import requests
import json
import spotipy
import spotipy.util as util

client_id = "3dc7c13790354801bf68fe78f07d35da"
client_secret = "c80bcac20daa4132905e93bc52f81fdc"
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
            artists_name += (i['name'] + ",")

        current_track  = { 
            "track_id" : track_id, 
            "track_name": track_name, 
            "track_uri": track_uri, 
            "track_external_url": track_external_url, 
            "artists_name": artists_name
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
            "artists_name": artists_name
        }
        tracks.append(track) 

    # print(tracks)
    return tracks

def printPlayButtons(track_array):
    for track in track_array: 
        element = '<iframe src="' + track['track_external_url'] + '" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'
        print(element)

def main():
    oauth_token = resolvetoken()
    current_track = getMyCurrentPlayback(oauth_token)
    past_tracks = getMyRecentTracks(oauth_token)
    print(current_track)
    return 0

if __name__ == '__main__':
    main()
    