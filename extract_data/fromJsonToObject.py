import json
import logging
import os

import custom_exceptions
from Metadata import Metadata

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="my_logs.log",
                    filemode="a+",
                    format=Log_Format,
                    level=logging.ERROR)
LOGGER = logging.getLogger()


def from_json_to_object(file_name):
    try:
        f = open(file_name)
        songs = json.loads(f.read())
        try:
            create_new_artist_file(dict(songs).get('track').get('album'),
                                   dict(songs).get('track').get('artists'))
            add_song_to_album_file(dict(songs).get('track').get('album').get('id'),
                                   dict(songs).get('track').get('id'))
        except custom_exceptions.InfoNotFoundOnFile:
            LOGGER.error("the info on the file was not what expected")
        finally:
            f.close()
    except FileNotFoundError as e:
        LOGGER.error("file entered was incorrect")
        raise e


def create_new_artist_file(album, list_of_artists):
    for artists in list_of_artists:
        unique_file_id = "raw_data\\artists\\" + str(artists.get('id')) + ".json"
        Metadata.add_new_info('artists', [artists.get('id'), artists.get('name')])
        update_list_in_file(album, unique_file_id)


def update_list_in_file(add_to_list, unique_file_id, limit=False):
    if os.path.exists(unique_file_id):
        with open(unique_file_id, 'r') as fp:
            current_file_value = json.load(fp)
            current_file_value.append(add_to_list)
        if limit is True and len(current_file_value) < 20 or limit is False:
            with open(unique_file_id, 'w') as fp:
                json.dump(current_file_value, fp, indent=4
                          , separators=(',', ': '))
                LOGGER.info('appended info to file')
        else:
            print("BUY PREMIUM TO ADD MORE SONGS")

    else:
        with open(unique_file_id, 'w') as f:
            current_file_value = [add_to_list]
            json.dump(current_file_value, f, indent=4
                      , separators=(',', ': '))
            LOGGER.info('added info to file')
            LOGGER.info('created file')


def add_song_to_album_file(album_id, song_id):
    unique_file_id = "raw_data\\albums\\" + album_id + ".json"
    update_list_in_file(song_id, unique_file_id)
