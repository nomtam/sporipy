# CR: bad class naming
# CR: can't in general understand where does this code fit in..
#  You never get data from the user to write to a file, unless it's playlist data to store,
#  but you method naming doesn't match this use-case
import json
import logging
import os

import custom_exceptions
from Metadata import Metadata

# CR: naming conventions
Log_Format = "%(levelname)s %(asctime)s - %(message)s"
# CR: could name the logging file better
logging.basicConfig(filename="my_logs.log",
                    filemode="a+",
                    format=Log_Format,
                    level=logging.ERROR)
LOGGER = logging.getLogger()

# CR: bad method naming. Maybe data_loader?
def from_json_to_object(file_name):
    # CR: why not use
    try:
        f = open(file_name)
        # CR: why not make the songs a dict here? insted of duplicated code later?
        songs = json.loads(f.read())
        try:
            # CR: isn't making a var out of "dict(songs).get('track')" cleaner?
            create_new_artist_file(dict(songs).get('track').get('album'),
                                   dict(songs).get('track').get('artists'))
            add_song_to_album_file(dict(songs).get('track').get('album').get('id'),
                                   dict(songs).get('track').get('id'))
        except custom_exceptions.InfoNotFoundOnFile:
            LOGGER.error("the info on the file was not what expected")
        finally:
            # CR: why not "with open"? so you don't have to close
            f.close()
    except FileNotFoundError as e:
        LOGGER.error("file entered was incorrect")
        raise e


def create_new_artist_file(album, list_of_artists):
    for artists in list_of_artists:
        # CR: config
        unique_file_id = "raw_data\\artists\\" + str(artists.get('id')) + ".json"
        Metadata.add_new_info('artists', [artists.get('id'), artists.get('name')])
        update_list_in_file(album, unique_file_id)


# CR: should be separated to a few methods
# CR: isn't is_premium better name?
def update_list_in_file(add_to_list, unique_file_id, limit=False):
    if os.path.exists(unique_file_id):
        # CR: method #1
        with open(unique_file_id, 'r') as fp:
            current_file_value = json.load(fp)
            current_file_value.append(add_to_list)
        # CR: method #2
        # CR: complex if. Limit is unclear. should be 2 ifs
        if limit is True and len(current_file_value) < 20 or limit is False:
            # CR: duplicated code. Method #4. also - append is 'a', isn't it?
            with open(unique_file_id, 'w') as fp:
                json.dump(current_file_value, fp, indent=4
                          , separators=(',', ': '))
                # CR: uninformative log
                LOGGER.info('appended info to file')
        else:
            # CR: this shouldn't be a print. If you can't add more songs you return an error to the user and explain it.
            #  Like a 403 error for example
            print("BUY PREMIUM TO ADD MORE SONGS")

    else:
        # CR: method #3
        with open(unique_file_id, 'w') as f:
            current_file_value = [add_to_list]
            # CR: duplicated code
            json.dump(current_file_value, f, indent=4
                      , separators=(',', ': '))
            # CR: not indicative log. What info to what file
            LOGGER.info('added info to file')
            LOGGER.info('created file')


def add_song_to_album_file(album_id, song_id):
    # CR: config
    unique_file_id = "raw_data\\albums\\" + album_id + ".json"
    update_list_in_file(song_id, unique_file_id)
