from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import spotipy
import models
import spotipy.util as util
import spotipy.oauth2 as oauth2

# Create your views here.

token=""
auth = models.auth()

def index(request):
    if token=="":
        return HttpResponse('<a href=%s>Login</a>.<br />' % auth.get_authorize_url())
    else:
        playlists = models.getplaylist(token)
        print playlists
        # username = sp.me()
        # print username
        # results = sp.current_user_top_tracks(limit=50)
        # a = ""
        # for item in results['items']:
        #     track = item['name']
        #     a += (track + " \n ")
        return HttpResponse(playlists)


def callback(request, code):
    global token
    token = auth.get_access_token(request.GET["code"])["access_token"]
    print token
    return redirect('index')