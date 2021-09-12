import spotipy
from quizify.settings import CLIENT_ID, CLIENT_SECRET
from spotipy.oauth2 import SpotifyOAuth

def parse_songs(json_var):
    song_dict = {}

    playname = json_var['name']
    
    for i in json_var['tracks']['items']:
        name = i['track']['name']
        uri = i['track']['uri'][14:]
        song_dict[uri] = [name]

    return playname, song_dict

def parse(playlists):
    
    playlist_dict = {}

    for num, playlist in enumerate(playlists['items']):
        # print()
        # print(f"{num} " + playlist['id'] + " " + playlist['name'])
        playlist_dict[playlist['id']] = playlist['name']

    # print("")
    # for x in playlist_dict:
    #     print(x, playlist_dict.get(x)) #creates dictionary of playlists, choose which one

    # choose_playlist = int(input("\nType playlist number: "))
    # print(playlist_dict.get(choose_playlist))
    # results = sp.playlist(playlist_dict.get(choose_playlist), fields="tracks,next")
    # tracks = results['tracks']

    # song_dict = {}
    # show_tracks(tracks, song_dict)
    # for x in song_dict:
    #     print(x, song_dict.get(x))

    # choose_song = int(input("\nType song num: "))
    # song = song_dict.get(choose_song)[2]
    # print("this is the song uri to access api:", song_dict.get(choose_song)[2])
    print(playlist_dict)
    return playlist_dict



