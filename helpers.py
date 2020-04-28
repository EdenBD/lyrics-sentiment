import pandas as pd
import numpy as np
import os 

import json
import urllib.request
from urllib.request import Request
from pandas.io.json import json_normalize
from urllib.parse import quote
import time
import sys

# need to keep quering "Get Token" button here: https://developer.spotify.com/console/get-audio-features-track/?id=06AKEBrKUckW0KREUWRnvT
def get_spotify_valence(song_title, artist_name, spotify_api_key):
  """
  Returns the a 0-1 real value number that represents the song's valence of None if not found.
  """
  # Format given information
  song = quote(song_title)
  artist = quote(artist_name) 

  # Get song URI from artist and song (https://developer.spotify.com/documentation/web-api/reference/search/search/)
  request = Request('https://api.spotify.com/v1/search?q=track:' + song + '%20artist:' + artist + '&type=track&limit=1')
  request.add_header('Accept', 'application/json')
  request.add_header('Content-Type', 'application/json')
  request.add_header('Authorization', 'Bearer ' + spotify_api_key)
  res = urllib.request.urlopen(request)
  resObject = json.load(res)
  # if not found
  if (len(resObject["tracks"]["items"]) == 0):
    print("Song {} not found".format(song_title))
    return None
  else:
    songURI = resObject["tracks"]["items"][0]["id"]
    audioRequest = Request('https://api.spotify.com/v1/audio-features/' + songURI)
    audioRequest.add_header('Accept', 'application/json')
    audioRequest.add_header('Content-Type', 'application/json')
    audioRequest.add_header('Authorization', 'Bearer ' + spotify_api_key)
    audioRes = urllib.request.urlopen(audioRequest)
    jsonObject = json.load(audioRes)
    valence = jsonObject["valence"]
    print("Found valence: {:.2f} of the song: {} - {}".format(valence, song_title, artist_name))
    return valence
