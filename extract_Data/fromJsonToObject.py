import json
import logging
import os
from metaData import metaData
import custom_exceptions

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "my_logs.log",
                    filemode = "a+",
                    format = Log_Format,
                    level = logging.ERROR)
LOGGER = logging.getLogger()

def from_json_to_object(fileName):
    try:
        f = open(fileName)
        songs = json.loads(f.read())
        try:
            createNewArtistFile(dict(songs).get('track').get('album'),
                                dict(songs).get('track').get('artists'))
            addSongToAlbumFile(dict(songs).get('track').get('album').get('id'),
                                dict(songs).get('track').get('id'))
        except custom_exceptions.InfoNotFoundOnFile:
            LOGGER.error("the info on the file was not what expected")
        finally:
            f.close()
    except FileNotFoundError as e:
        LOGGER.error("file entered was inncorect")
        raise e

def createNewArtistFile(album, list_of_artists):
    for artists in list_of_artists:
        unique_file_id = "artists\\" + str(artists.get('id')) + ".json"
        metaData.add_row_artists(artists.get('id'), artists.get('name'),'artists')
        addToFileList(album, unique_file_id)

def addToFileList(add_to_list, unique_file_id,limit = False):
    if os.path.exists(unique_file_id):
        with open(unique_file_id, 'r') as fp:
            listObj = json.load(fp)
            listObj.append(add_to_list)
        if limit is True and len(listObj)<20 or limit is False:
            with open(unique_file_id, 'w') as fp:
                json.dump(listObj, fp, indent=4
                        , separators=(',', ': '))
                LOGGER.info('appended info to file')
        else: print("BUY PREMIUM TO ADD MORE SONGS")

    else:
        with open(unique_file_id, 'w') as f:
            listObj = []
            listObj.append(add_to_list)
            json.dump(listObj, f, indent=4
                      , separators=(',', ': '))
            LOGGER.info('added info to file')
            LOGGER.info('created file')


def addSongToAlbumFile(album_id, song_id):
    unique_file_id = "albums\\" + album_id + ".json"
    addToFileList(song_id, unique_file_id)
