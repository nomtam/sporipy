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


# CR: isNone check is better
def sign_up_user(user_details_header=['username', 'password', 'limited_account', 'artist']):
    # CR: what if I signed up using the API? SRP..
    username = input("enter new user name:")
    # CR: If already decided to use this artist 1/0. Why not use bool as below?
    is_artist = int(input("1 - am artists , 0 - not artist"))
    # CR: config
    if Path('users\\' + username).exists():
        if is_artist is 1 and Path('raw_data\\artists\\' + username + '.json').exists() or is_artist is not 1:
            print("username taken, try again")
            sign_up_user()

    else:
        # CR: same as above. SRP
        password = input("enter password: ")
        # CR: is_artist should be bool
        if is_artist is 1:
            # CR: is_premium = True...
            limit = 0
            create_new_artist(username)
        else:
            limit = bool(int(input("1 - free account, 0 - premium account ")))
        create_new_user_directory(username, [username, password, limit, is_artist],
                                  user_details_header)
        initiate_audio_profile(username)
        return UserFunctions(username, password, limit, is_artist)


def create_new_artist(username):
    # CR: config
    with open('raw_data\\artists\\' + username + '.json', 'w') as artist:
        pass
    # CR: config
    Metadata.add_new_info('artists', [username, username])


# CR: same with defalut vars.. is None etc.
def initiate_audio_profile(username,
                           audio_features=['danceability', 'energy', 'acousticness', 'instrumentalness',
                                           'valence'], row=[0, 0, 0, 0, 0]):
    # CR: config
    with open('users\\' + username + '\\audio_profile.csv', 'w', newline="") as user_details:
        # CR: csv_writer?
        # CR: srp. put it in a method
        csvwriter = csv.writer(user_details)
        csvwriter.writerow(audio_features)
        csvwriter.writerow(row)


def create_new_user_directory(username, user_info: list, user_details_header):
    # CR: config
    os.makedirs('users\\' + username)
    os.makedirs('users\\' + username + '\\playlists')
    with open('users\\' + username + '\\user_details.csv', 'w', newline="") as user_details:
        csvwriter = csv.writer(user_details)
        csvwriter.writerow(user_details_header)
        csvwriter.writerow(user_info)
    # CR: SRP + OCP comment as above
    print("created new user successfully")
    LOGGER.info("created new user successfully")


def login():
    # CR: OCP + SRP
    username = input("username: ")
    password = input("password: ")
    details = validation(username, password)
    if details is None:
        # CR: ocp + SRP
        print("password or username is incorrect")
        LOGGER.info("user entered incorrect details")
        raise PasswordOrUserNameIncorrect
    else:
        # CR: ocp + SRP
        print("succesfully entered system")
        LOGGER.info("user entered correct details")
        # CR: details[2], [3] is not really clear. Read the comment below about dataframes
        return UserFunctions(username, password, bool(int(details[2])), bool(int(details[3])))


# CR: about logging - why bad password is an info log but bad username is an error log? Think about it
def validation(username, password):
    path = Path('users\\' + username)
    if path.exists():
        try:
            # CR: config
            with open('users\\' + username + '\\user_details.csv', encoding="utf8") as user_info:
                content = csv.reader(user_info)
                next(content)  # skip header
                details = next(content)
                try:
                    # CR: unclear. Better to read it to a class or to a dataframe so we'll know what [1] means
                    if password == details[1]:
                        return details
                    else:
                        LOGGER.info("user entered wrong password")
                except InfoNotFoundOnFile as e:
                    raise e
        except PasswordOrUserNameIncorrect as e:
            LOGGER.error("username inncorect")
            raise e
