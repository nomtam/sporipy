import json
import csv
import os

from extract_Data.fromJsonToObject import addToFileList
from pathlib import Path


class user_functions:
    def __init__(self, username, password, limit,
                 is_artist):  # user enter username and password and i check it its correct here
        if username is not None:
            self.username = username
            self.password = password
            self.limit = limit
            self.is_artist = is_artist

    @staticmethod
    def sign_user():
        username = input("enter new user name:")
        if Path('users\\' + username).exists():
            print("username taken, try again"); user_functions.sign_user()
        else:
            password = input("enter password: ")
            is_artist = int(input("1 - am artists , 0 - not artist"))
            if is_artist is 1:
                limit = False
            else:
                limit = input("free - free account, premium - premium account ")
            os.makedirs('users\\' + username)
            os.makedirs('users\\' + username + '\\playlists')
            with open('users\\' + username + '\\user_details.csv', 'w') as user_info:
                header = ['username', 'password', 'account_type', 'artist']
                csvwriter = csv.writer(user_info)
                csvwriter.writerow(header)
                csvwriter.writerow([username, password, limit, is_artist])
            print("succesfully entered system")
            return user_functions(username, password, limit, is_artist)

    @staticmethod
    def validation(username, password):
        path = Path('users\\' + username)
        if path.exists():
            try:
                with open('users\\' + username + '\\user_details.csv', encoding="utf8") as user_info:
                    content = csv.reader(user_info)
                    next(content)  # skip header
                    details = next(content)
                    if password == details[1]: return details
            except FileNotFoundError as e:
                raise e

    def add_to_playlist(self, song_id=None, playlist_name=None):
        if song_id is None and playlist_name is None: song_id = input("song id: "); playlist_name = input("playlist name: ")
        with open('songs\\song_' + song_id + '.json', 'r') as song:
            song_info = json.load(song)
        addToFileList(song_info, 'users\\' + self.username + '\\playlists\\' + playlist_name + '.json',
                      limit=self.limit)
