from django.shortcuts import redirect, render
from django.http import HttpResponse
from requests.models import Response
from requests.sessions import Request
from django.utils import timezone
from quizify.settings import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth
from django.contrib.sites.models import Site
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from requests import Request, post
from django.db.models import *
import requests
import json
from .models import *
from datetime import timedelta
from .song import Song
import urllib

import test


def AuthUrl_get():
    scopes ="playlist-read-private, playlist-modify-public"
    url = Request(method="GET", url="https://accounts.spotify.com/authorize", 
    params={'scopes':scopes, 'response_type':'code','redirect_uri':REDIRECT_URI, 'client_id':CLIENT_ID}).prepare().url
    r = Response({'url':url}, status=status.HTTP_200_OK)
    return r.data['url']

def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type':'authorization_code',
        'code':code,
        'redirect_uri':REDIRECT_URI,
        'client_id':CLIENT_ID,
        'client_secret':CLIENT_SECRET}).json()

    token = response.get("access_token")
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')
    
    if not request.session.exists(request.session.session_key):
        request.session.create()

    expire = timezone.now() + timedelta(seconds=expires_in)

    if Token.objects.filter(username=request.session.session_key):
        Token.objects.filter(username=request.session.session_key).update(access_token=token, refresh_token=refresh_token, token_type=token_type, expires_in=expire)
    else:
        Token.objects.create(username=request.session.session_key, access_token=token, refresh_token=refresh_token, token_type=token_type, expires_in=expire)
    return redirect('http://127.0.0.1:8000/home/')

def refresh_spotify(session_id):

    rtoken = Token.objects.filter(username=session_id).order_by('expires_in')[0].refresh_token
    print("HERE3", rtoken)


    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': rtoken,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    print(response)
    
    token = response.get("access_token")
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    error = response.get('error')
  

    expire = timezone.now() + timedelta(seconds=expires_in)
    Token.objects.filter(username=session_id).update(access_token=token, token_type=token_type, expires_in=expire)

def is_authenticated(session_id):
    print("HERE1")
    if Token.objects.filter(username=session_id):
        tokens = Token.objects.filter(username=session_id).order_by('expires_in')
        token = tokens[0]
        if token.expires_in <= timezone.now():
            print("HERE 2")
            refresh_spotify(session_id)
        return True
    return False



def landing(request):    
    return render(request, "quiz/land.html")

def quiz(request, playlist_id):
    submit: bool = False
    quiz_score: int = 0
    user: User

    if 'user' in request.session:
            user = User.objects.get(pk = request.session['user'])
            user.score += quiz_score

    token = Token.objects.get(username=request.session.session_key).access_token


    headers = {
        'Authorization': 'Bearer {token}'.format(token=token)
    }
    songs_json = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers=headers).json()
    name, songs = test.parse_songs(songs_json)
    songs = [Song(id=id, name=songs[id][0]) for id in songs][:min(len(songs), 10)]

    if 'submit' in request.GET:
        submit = True
        print(request.path_info)

        for song in songs:
            print(request.GET[song.id])
            if song.name.lower() == request.GET[song.id].lower():
                quiz_score += 10
        
        if 'user' in request.session:
            user.score += quiz_score
            user.save()

        

        
            
        print(quiz_score)
            
    # id = request.get('id')
    return render(request, 'quiz/quiz.html', context={'name':name, 'playlist':songs, 'results':submit, 'score':quiz_score, 'user':user})


def login(request):

    if not is_authenticated(request.session.session_key):
        return redirect(AuthUrl_get())

    
    
    return redirect('http://127.0.0.1:8000/home/')



def home(request):

    print("HERE")

    token = Token.objects.get(username=request.session.session_key).access_token
    
    headers = {
        'Authorization': 'Bearer {token}'.format(token=token)
    }

    user = requests.get('https://api.spotify.com/v1/me', headers=headers).json()
    print("JSON READY")
    if not User.objects.filter(id=user['id']):
        u = User.objects.create(id=user['id'], username=user['display_name'])
    else:
        u = User.objects.get(id=user['id'])

    request.session['user'] = u.id

    
    json_var = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers).json()
    
    playlists = test.parse(json_var)

    plays = Playlist.objects.bulk_create(
        [Playlist(name=playlists[id], id=id) for id in playlists.keys()],
        ignore_conflicts=True
    )
  

    return render(request, "quiz/home.html", context={'playlists': plays,
                                                        'user': u})



# Create your views here.
