# CR: unused imports
import json
import csv
import logging
import os
from Metadata import Metadata
from custom_exceptions import *
from extract_data.fromJsonToObject import update_list_in_file
from pathlib import Path

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="my_logs.log",
                    filemode="a+",
                    format=Log_Format,
                    level=logging.ERROR)
LOGGER = logging.getLogger()


class UserFunctions:
    def __init__(self, username, password, limit,
                 is_artist):
        self.username = username
        self.password = password
        # CR: is_premium
        self.limit = limit
        self.is_artist = is_artist

    def add_to_playlist(self, song_id=None, playlist_name=None):
        if (song_id and playlist_name) is None:
            # CR: ocp
            song_id = input("song id: ")
            # CR: ocp
            playlist_name = input("playlist name: ")
        try:
            # CR: config
            # CR: put in a method too, get_songs_info(path)
            with open('raw_data\\songs\\song_' + song_id + '.json', 'r') as song:
                song_info = json.load(song)
                # CR: format()
            update_list_in_file(song_info, 'users\\' + self.username + '\\playlists\\' + playlist_name + '.json',
                                limit=self.limit)
        except FileNotFoundError as e:
            LOGGER.error("song id entered was incorrect")
            raise e