import json
import os
from metaData import metaData

def fromJsonToObject(fileName):
    f = open(fileName)
    object_attributes = json.loads(f.read())
    createNewArtistFile(dict(object_attributes).get('track').get('album'),
                        dict(object_attributes).get('track').get('artists'))
    addSongToAlbumFile(dict(object_attributes).get('track').get('album').get('id'),
                       dict(object_attributes).get('track').get('id'))
    f.close()


def createNewArtistFile(album,list_of_artists):
    for artists in list_of_artists:
        unique_file_id = "artists\\" + str(artists.get('id'))+".json"
        metaData.add_row_artists(artists.get('id'),artists.get('name'))

        if os.path.exists(unique_file_id)!= True:
            with open(unique_file_id, 'w') as f:
                listObj = []
                listObj.append(album)
                json.dump(listObj,f,indent=4
                      ,separators=(',', ': '))
        else:
            with open(unique_file_id,'r') as fp:
                listObj = json.load(fp)
                listObj.append(album)
            with open(unique_file_id,'w') as fp:
               json.dump(listObj,fp,indent=4
                      ,separators=(',', ': '))

def addSongToAlbumFile(album_id,song_id):
    unique_file_id = "albums\\" + album_id+ ".json"
    mode = 'a' if os.path.exists(unique_file_id) else 'w'
    with open(unique_file_id, mode) as f:
        f.write(song_id + "\n")