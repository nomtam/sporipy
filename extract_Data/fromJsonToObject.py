import json
import logging
import os

from metaData import metaData

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


def from_json_to_object(fileName):
    f = open(fileName)
    songs = json.loads(f.read())
    createNewArtistFile(dict(songs).get('track').get('album'),
                        dict(songs).get('track').get('artists'))
    addSongToAlbumFile(dict(songs).get('track').get('album').get('id'),
                       dict(songs).get('track').get('id'))
  #  metaData.add_row_artists(songs.get('id'), songs.get('name'),'songs')
    f.close()


def createNewArtistFile(album, list_of_artists):
    for artists in list_of_artists:
        unique_file_id = "artists\\" + str(artists.get('id')) + ".json"
        metaData.add_row_artists(artists.get('id'), artists.get('name'),'artists')
        addToFileList(album, unique_file_id)

def addToFileList(add_to_list, unique_file_id,limit = False):
    if os.path.exists(unique_file_id) != True:
        with open(unique_file_id, 'w') as f:
            listObj = []
            listObj.append(add_to_list)
            json.dump(listObj, f, indent=4
                      , separators=(',', ': '))
            logging.info('added info to file')
            logging.info('created file')

    else:
        with open(unique_file_id, 'r') as fp:
            listObj = json.load(fp)
            listObj.append(add_to_list)
        if limit is True and len(listObj)<20 or limit is False:
            with open(unique_file_id, 'w') as fp:
                json.dump(listObj, fp, indent=4
                        , separators=(',', ': '))
                logging.info('appended info to file')
        else: print("BUY PREMIUM TO ADD MORE SONGS")


def addSongToAlbumFile(album_id, song_id):
    unique_file_id = "albums\\" + album_id + ".json"
    addToFileList(song_id, unique_file_id)
