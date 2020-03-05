import json
import requests
from secret import spotify_token, spotify_user_id, playlist_id
from selenium import webdriver #could be used to fully automate by getting new spotify api token

#returns songs_to_keep array
def get_songs():
    #get playlist we want to choose songs from
    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

    headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(spotify_token)
    }

    resp = requests.get(query, headers=headers)
    resp_json = resp.json() #make sure response is json format

    items = resp_json['items']  #item = every track item from json
    print('type "y" or "n" if you want song to be kept in new playlist')
    
    songs_to_keep = []
    #loop through items and add track to songs to keep arr
    for i in range(len(items)):
        track = items[i]['track']['name']
        user_input = input(track + " ")
        if(user_input == "y"):
            songs_to_keep.append(items[i]['track']['uri'])

    return songs_to_keep



def createplaylist(playlist_name):
    request_body = json.dumps({
        "name": playlist_name,
        "description": "Songs I listened to in " + playlist_name,
        "public": True
    })

    query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
    response = requests.post(
        query, data=request_body, 
        headers={
            "Content-Type":"application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }
    )

    response_json = response.json()
    return response_json["id"]

def add_songs_to_playlist(playlistName):
    playlist = createplaylist(playlistName)
    songs_to_add = get_songs()  #uris of songs to add

    request_data = json.dumps(songs_to_add)

    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist)

    resp = requests.post(
        query,
        data = request_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        }

    )
    response_json = resp.json()
    return response_json

add_songs_to_playlist("Spring/Summer 2020")