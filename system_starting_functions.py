import csv
import logging
import os
from pathlib import Path

from Metadata import Metadata
from userfunctions import UserFunctions, PasswordOrUserNameIncorrect, InfoNotFoundOnFile

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="my_logs.log",
                    filemode="a+",
                    format=Log_Format,
                    level=logging.ERROR)
LOGGER = logging.getLogger()


def sign_up_user(user_details_header=['username', 'password', 'limited_account', 'artist']):
    username = input("enter new user name:")
    is_artist = int(input("1 - am artists , 0 - not artist"))

    if Path('users\\' + username).exists():
        if is_artist is 1 and Path('raw_data\\artists\\' + username + '.json').exists() or is_artist is not 1:
            print("username taken, try again")
            sign_up_user()

    else:
        password = input("enter password: ")
        if is_artist is 1:
            limit = 0
            create_new_artist(username)
        else:
            limit = bool(int(input("1 - free account, 0 - premium account ")))
        create_new_user_directory(username, [username, password, limit, is_artist],
                                  user_details_header)
        initiate_audio_profile(username)
        return UserFunctions(username, password, limit, is_artist)


def create_new_artist(username):
    with open('raw_data\\artists\\' + username + '.json', 'w') as artist:
        pass
    Metadata.add_new_info('artists', [username, username])


def initiate_audio_profile(username,
                           audio_features=['danceability', 'energy', 'acousticness', 'instrumentalness',
                                           'valence'],row=[0,0,0,0,0]):
    with open('users\\' + username + '\\audio_profile.csv', 'w', newline="") as user_details:
        csvwriter = csv.writer(user_details)
        csvwriter.writerow(audio_features)
        csvwriter.writerow(row)


def create_new_user_directory(username, user_info: list, user_details_header):
    os.makedirs('users\\' + username)
    os.makedirs('users\\' + username + '\\playlists')
    with open('users\\' + username + '\\user_details.csv', 'w', newline="") as user_details:
        csvwriter = csv.writer(user_details)
        csvwriter.writerow(user_details_header)
        csvwriter.writerow(user_info)
    print("created new user successfully")
    LOGGER.info("created new user successfully")


def login():
    username = input("username: ")
    password = input("password: ")
    details = validation(username, password)
    if details is None:
        print("password or username is incorrect")
        LOGGER.info("user entered incorrect details")
        raise PasswordOrUserNameIncorrect
    else:
        print("succesfully entered system")
        LOGGER.info("user entered correct details")
        return UserFunctions(username, password, bool(int(details[2])), bool(int(details[3])))


def validation(username, password):
    path = Path('users\\' + username)
    if path.exists():
        try:
            with open('users\\' + username + '\\user_details.csv', encoding="utf8") as user_info:
                content = csv.reader(user_info)
                next(content)  # skip header
                details = next(content)
                try:
                    if password == details[1]:
                        return details
                    else:
                        LOGGER.info("user entered wrong password")
                except InfoNotFoundOnFile as e:
                    raise e
        except PasswordOrUserNameIncorrect as e:
            LOGGER.error("username inncorect")
            raise e
