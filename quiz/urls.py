from django.shortcuts import redirect
from . import views
from django.urls import path

urlpatterns = [
    path('', views.landing, name='land'),
    path('home/', views.home, name='home'), 
    path('login/', views.login, name='login'),
    path('redirect/', views.spotify_callback),
    path('quiz/<str:playlist_id>', views.quiz, name='quiz'),
]