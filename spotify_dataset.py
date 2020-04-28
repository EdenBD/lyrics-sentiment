# -*- coding: utf-8 -*-
"""Spotify Dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17NWbYNiSXYfoCipbn9qXmkIL1SvCFOah

# Preparing Lyrics - Sentiment dataset

In this notebook I am using [Spotify API](https://developer.spotify.com/documentation/web-api/) and an existing [Song/Band/Lyrics Kaggle Dataset](https://www.kaggle.com/detkov/lyrics-dataset) to get a sentiment analysis dataset, where I use valence to measure positiveness. The valence ranges from 0 to 1, where higher valence corresponds to [a happier sentiment](https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/). 

Results in a total of ~156,000 non-null rows.

## Taken Steps to Prepare Dataset:

1. Get songs lyrics database (with columns: Band, Lyrics, Song).
2. Query Spotify for a song ID and songs valence (i.e hapiness), done in chunks of 99 songs per query.
3. Integrate to one dataframe, where each song has a corresponding valence value, or np.nan if song not found.
"""

import pandas as pd
import numpy as np
import os 

# Mount google Drive
from google.colab import drive
drive.mount('/content/gdrive/')

# Download Lyrics file from Kaggle place it in your drive.
# Change MY_FOLDER to your folder in the derive.
ROOT_DIRECTORY = "/content/gdrive/My Drive"
MY_FOLDER = "6864"
FILE_NAME = "Lyrics1.csv"

# Path to save new df to.
OUTPUT_FILENAME = "labeled_lyrics.csv"
SAVE_PATH = os.path.join(ROOT_DIRECTORY, MY_FOLDER, OUTPUT_FILENAME)

path_to_data = os.path.join(ROOT_DIRECTORY, MY_FOLDER, FILE_NAME)
print("Verify your path: ",path_to_data,end='\n\n')
df = pd.read_csv(path_to_data, error_bad_lines=False)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Report the number of sentences.
print('Number of training sentences: {:,}\n'.format(df.shape[0]))

# Display random rows from the data.
df.sample(5)

# Reomove non-english songs.
for column in df.columns:
  mask_nonAscii = df[column].str.len().ne(df[column].str.encode('ascii',errors = 'ignore').str.len())
  df = df[~mask_nonAscii & df[column].notnull()]

# Rename.
df.rename({"Lyrics": "seq", "Song": 'song', "Band":'artist'}, axis=1, inplace=True)

# Create nan column for label.
df['label'] = np.nan

# Drop duplicates
df.drop_duplicates(['song','seq','artist'], keep='first', inplace=True)

# Reset index after deleting Nan and duplicate rows
df = df.reset_index(drop= True)

# Display df information after changes.
df.info()

"""### Accessing Spotify API"""

import json
import urllib.request
from urllib.request import Request
from pandas.io.json import json_normalize
from urllib.parse import quote
import time
import sys

# need to keep quering "Get Token" button here: https://developer.spotify.com/console/get-audio-features-track/?id=06AKEBrKUckW0KREUWRnvT
current_token = 'PLACE_YOUR_TOKEN_HERE'

artists = df.artist.values
songs = df.song.values

print(len(songs))
print(len(artists))
print(df.shape)

"""Thank you [Madeline Zhang](https://github.com/madelinez820) for the detailed [Spotify access example code](https://github.com/EdenBD/How-To-Win-Eurovision/blob/master/data-wrangling-scripts/spotify_script.ipynb)."""

songURIS = ""
max_tracks_count = 99
successful_i = []
nulls_count = 0

# If range bigger than 35,000 need to do in chunks.
for i in range(0,len(songs)):
    # formatting spaces
    song = quote(songs[i])
    artist = quote(artists[i]) 

    # going from artist / song name to song URIs (https://developer.spotify.com/documentation/web-api/reference/search/search/)
    # Can make more efficient by increasing limit to 50.
    request = Request('https://api.spotify.com/v1/search?q=track:' + song + '%20artist:' + artist + '&type=track&limit=1')
    request.add_header('Accept', 'application/json')
    request.add_header('Content-Type', 'application/json')
    request.add_header('Authorization', 'Bearer ' + current_token)
    try: 
      res = urllib.request.urlopen(request)
      resObject = json.load(res)

      if (len(resObject["tracks"]["items"]) == 0):
          nulls_count += 1
      else:
          songURI = resObject["tracks"]["items"][0]["id"]

          if len(successful_i)<max_tracks_count:
            songURIS+=songURI + ','
            successful_i.append(i)
          else:
            songURIS+=songURI
            successful_i.append(i)
            print("Got {} Successful songs".format(len(successful_i)))
            songURIS = quote(songURIS)
            # Getting 99 songs URI -> audio features (https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/)
            audioRequest = Request('https://api.spotify.com/v1/audio-features?ids=' + songURIS)
            audioRequest.add_header('Accept', 'application/json')
            audioRequest.add_header('Content-Type', 'application/json')
            audioRequest.add_header('Authorization', 'Bearer ' + current_token)
            audioRes = urllib.request.urlopen(audioRequest)
            jsonObject = json.load(audioRes)
            tracks_objects = jsonObject["audio_features"]
            for idx,trackObject in zip(successful_i, tracks_objects):
              # Set value at specified row/column pair.
              if trackObject:
                df['label'].iat[idx] = trackObject["valence"]
            # Reset. 
            successful_i = []
            songURIS = ""
        

    except urllib.error.HTTPError as e:
      if int(e.code) == 429: # Maxed requests, need to wait 
        wait_time = float(e.info()['Retry-After'])
      else:
        wait_time = 3

      if int(e.code) == 400:
        print("Invalid request at song: ",song)
      if int(e.code) == 401:
        print("Need to refresh Token from i: ",i)
        break
        
      print("For {} Sleeping {} seconds at {}".format(e.code,wait_time,i))
      time.sleep(wait_time)

print(df.sample(5))

# Remove nulls for songs not found in Spotify.
print("df Length before removing Spotify unfound songs: ", len(df))
df.dropna(inplace=True)
print("df Length after: ", len(df))

"""Only needed if dataset is large (above 35K) and we are building dataset in chunks. Stack current and previously computed dfs."""

# Size of the chunk that was computed now. 
done_chunk = 35000

# Read the previously calculated df file.
prev = pd.read_csv(SAVE_PATH, error_bad_lines=False)

prev = prev.loc[:done_chunk, ~prev.columns.str.contains('^Unnamed')]
current = df.loc[done_chunk:, ~df.columns.str.contains('^Unnamed')]
df = pd.concat([prev, current], axis=0)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

"""Save current df to file."""

df.to_csv(SAVE_PATH)

"""Get Sentiment of one song"""

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

artist_name ="grande"
song_title = "breathin" 
label = get_spotify_valence(song_title, artist_name , current_token)