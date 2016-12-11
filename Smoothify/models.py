from __future__ import unicode_literals
import spotipy.oauth2 as oauth2
import spotipy
import matplotlib.pyplot as plt
import numpy as np
from django.db import models

# Create your models here.

import sys
global SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI
global SCOPE


SCOPE = 'user-read-private user-top-read'
SPOTIPY_CLIENT_ID = '087ebe015e4d43d38e1d9f8039bd8713'
SPOTIPY_CLIENT_SECRET = 'ef8e52fe87314aa891219d033a3c1ad8'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/callback'

def auth():
    auth = oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,
                               SPOTIPY_REDIRECT_URI, state=None, scope=SCOPE, cache_path=None)
    return auth

def getplaylist(token):
    if token:
        sp = spotipy.Spotify(auth=token)
        username = sp.me()['id']
        playlist_full = sp.user_playlists(username)
        playlist_items = playlist_full['items']
        playlist_user = {}
        for playlist_item in playlist_items:
            if playlist_item['owner']['id'] == username:
                key = playlist_item['name']
                id = playlist_item['id']
                playlist_user[key] = id

        return playlist_user

def gettracks(token,playlistid):
    if token:
        sp = spotipy.Spotify(auth=token)
        username = sp.me()['id']
        tracks = sp.user_playlist(username, playlistid,
                    fields="tracks,next")['tracks']['items']
        track_info = []
        for track in tracks:
            item = track['track']
            b = {'name':item['name'],'artist':[x['name'] for x in item['artists']],
                          'album':item['album']['name'],'id':item['id']}
            id = item['id']
            features = sp.audio_features([id])[0]
            f = {'acousticness':features['acousticness'],'danceability':features['danceability'],
                            'energy':features['energy'],'instrumentalness':features['instrumentalness'],
                            'key':features['key']/10,'loudness':(features['loudness']+60)/60}
            combine = {'basic':b,'feature':f}
            track_info.append(combine)

        return track_info

def statistic(tracks):
    acousticness = [x['feature']['acousticness'] for x in tracks]
    danceability = [x['feature']['danceability'] for x in tracks]
    energy = [x['feature']['energy'] for x in tracks]
    instrumentalness = [x['feature']['instrumentalness'] for x in tracks]
    key = [x['feature']['key'] for x in tracks]
    loudness = [x['feature']['loudness'] for x in tracks]

    plt.figure(1)
    plt.subplot(231)
    acousticness = np.sort(acousticness)
    plt.plot(acousticness)
    plt.ylabel('acousticness')

    plt.subplot(232)
    danceability = np.sort(danceability)
    plt.plot(danceability)
    plt.ylabel('danceability')

    plt.subplot(233)
    energy = np.sort(energy)
    plt.plot(energy)
    plt.ylabel('energy')

    plt.subplot(234)
    instrumentalness = np.sort(instrumentalness)
    plt.plot(instrumentalness)
    plt.ylabel('instrumentalness')

    plt.subplot(235)
    key = np.sort(key)
    plt.plot(key)
    plt.ylabel('key')

    plt.subplot(236)
    loudness = np.sort(loudness)
    plt.plot(loudness)
    plt.ylabel('loudness')

    plt.show()

def svd(tracks):
    a = []
    for track in tracks:
        f = track['feature']
        p = []
        for key,value in f.items():
            p.append(value)
        a.append(p)
    matrix = np.array(a)
    U, s, V = np.linalg.svd(matrix, full_matrices=True)
    return U

token = 'BQCxGe-0JVEQReyu5eKktBiXlc8IKT3ysMGTC28Atgh9iO-JR3J0m-62Gma_BIXFm4zKk4X09GLMr0xUGNlT7c8_vdaH9Ga5XrYUA03A9NUOGF7wyQkm-jRALBxWaHerP5GRqEvInBBCJ9fTGRI09wM4U-RJRsdDPFYGVT10FBFegWpREwDNXJ0XnJGJosMsy_slJXc9Y7_HSpeZP-YQa-4Mkg3g9OQp_UFOwXDwU6JFI4DOYzbN5gkLDj44UjP174KgIiTIQ3uYu3E9YoTsM7FT4CH35jIdjGMi1wEd6YxjMiwbReYLcZbP21-LPirDtJhHdf85PeE'
# a = getplaylist(token)

track_info = gettracks(token,'0QEeiTRJrI2GzAO2dpyDJW')
for i in xrange(len(track_info)):
    print track_info[i]['basic']['name']
# statistic(track_info)
U = svd(track_info)
n = len(track_info)
name = np.linspace(1,n,n)
for i in xrange(len(track_info)):
    plt.text(U[i,0],U[i,1],name[i])

plt.axis([-0.5,0.5,-0.5,0.5])
plt.show()