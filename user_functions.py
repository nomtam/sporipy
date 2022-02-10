import json
import csv
import logging
import os

import metaData
from custom_exceptions import *
from extract_Data.fromJsonToObject import addToFileList
from pathlib import Path

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "my_logs.log",
                    filemode = "a+",
                    format = Log_Format,
                    level = logging.ERROR)
LOGGER = logging.getLogger()


class user_functions:
    def __init__(self, username, password, limit,
                 is_artist):
        self.username = username
        self.password = password
        self.limit = limit
        self.is_artist = is_artist

    @staticmethod
    def sign_user(user_details_header =['username', 'password', 'limited_account', 'artist']):
        username = input("enter new user name:")
        is_artist = int(input("1 - am artists , 0 - not artist"))

        if Path('users\\' + username).exists():
            if is_artist is 1 and Path('artists\\'+username+'.json').exists() or is_artist is not 1:
                print("username taken, try again"); user_functions.sign_user()

        else:
            password = input("enter password: ")
            if is_artist is 1:limit = 0; user_functions.create_new_artist(username)
            else: limit = bool(int(input("1 - free account, 0 - premium account ")))
            user_functions.create_new_user_directory(username,[username, password, limit, is_artist],
                                                     user_details_header)
            return user_functions(username, password, limit, is_artist)

    @staticmethod
    def create_new_artist(username):
        with open('artists\\'+username+'.json','w') as artist:
            pass
        metaData.add_row_artists(username, username)


    @staticmethod
    def create_new_user_directory(username,user_info:list,user_details_header):
        os.makedirs('users\\' + username)
        os.makedirs('users\\' + username + '\\playlists')
        with open('users\\' + username + '\\user_details.csv', 'w',newline="") as user_details:
            csvwriter = csv.writer(user_details)
            csvwriter.writerow(user_details_header)
            csvwriter.writerow(user_info)
        print("succesfully created new user")
        LOGGER.info("created new user successfully")

    @staticmethod
    def login():
        username = input("username: ")
        password = input("password: ")
        details = user_functions.validation(username, password)
        if details is None:
            print("password or username is incorrect")
            LOGGER.info("user entered incorrect details")
            raise PasswordOrUserNameIncorrect
        else:
            print("succesfully entered system")
            LOGGER.info("user entered correct details")
            return user_functions(username, password, bool(int(details[2])), bool(int(details[3])))

    @staticmethod
    def validation(username, password):
        path = Path('users\\' + username)
        if path.exists():
            try:
                with open('users\\' + username + '\\user_details.csv', encoding="utf8") as user_info:
                    content = csv.reader(user_info)
                    next(content)  # skip header
                    details = next(content)
                    try:
                        if password == details[1]: return details
                        else: LOGGER.info("user entered wrong password")
                    except InfoNotFoundOnFile as e:
                        raise e
            except PasswordOrUserNameIncorrect as e:
                LOGGER.error("username inncorect")
                raise e


    def add_to_playlist(self, song_id=None, playlist_name=None):
        if (song_id and playlist_name) is None:
            song_id = input("song id: ")
            playlist_name = input("playlist name: ")
        try:
            with open('songs\\song_' + song_id + '.json', 'r') as song:
                song_info = json.load(song)
            addToFileList(song_info, 'users\\' + self.username + '\\playlists\\' + playlist_name + '.json',
                        limit=self.limit)
        except FileNotFoundError as e:
            LOGGER.error("soing id entered was incorrect")
            raise e
