# CR: I am assuming you didn't finish this class so I am not reviewing it too much
import csv
import os
import json

import pandas as pd

from Metadata import Metadata
# CR: missing empty line
# CR: many unused vars.
def update_user_audio_profile(song_id,user_preferences:list):
    # CR: config
    songs_info = pd.read_csv('raw_data\\songs\\Metadata.csv')
    # CR: format here too
    quer = 'id == "'+song_id+'"'
    df = pd.DataFrame(songs_info)
    newdf = songs_info.query(quer)
    header = [header for header in newdf][:-1]
    song_feature_values = [value for value in newdf.iloc[0]][:-1]
    df2 = df.mean(axis=0)
    list = []
    query = "danceability > {} & energy > {} & acousticness > {} & instrumentalness> {} & valence > {}".format()
    newdf = df.query('danceability > 0.5 & danceability > 0.8')

    song_grouped = df.sort_values(by=list)

    #all avgs of the feature
    print(df2.get('energy'))


def find_user_most_liked_feature(username):
    pass
mt = Metadata('songs', header=["danceability", "energy", "acousticness", "instrumentalness", "valence", "id"])
for filename in os.listdir("audio_features"):
    try:
        f = open(os.path.join("audio_features", filename))
        features = json.loads(f.read())
        f.close()
        add_to_metadata = []
        for feature in features.keys():
            add_to_metadata.append(features.get(feature))
        mt.add_new_info('songs', add_to_metadata)
    except FileNotFoundError as e:
        raise e

update_user_audio_profile('03DcpryHcONqKi2uKXK5Ow','rr')

#df = pd.read_csv('raw_data\\songs\\Metadata.csv')
#df = df.sort_values(["danceability", "energy"], ascending = (False, False))
#newdf = df.query('danceability > 0.5 & danceability > 0.8')
#song_grouped = songmetadata.sort_values(['instrumentalness'], ascending=True)

#print(songmetadata)
