from django.db import models
from spotipy.oauth2 import _make_authorization_headers

class Token(models.Model):
    username = models.TextField(primary_key=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

class User(models.Model):
    username= models.CharField(max_length=100)
    id = models.CharField(max_length=150, primary_key=True)
    score = models.IntegerField(default=0)

class Playlist(models.Model):
    id = models.CharField(max_length=150, primary_key=True)
    name = models.CharField(max_length=150)
    
class Result(models.Model):
    user = models.TextField()
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    score = models.IntegerField()

# Create your models here.
