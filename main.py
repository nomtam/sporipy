import json
import os

import logging

from user_functions import user_functions
from metaData import metaData
from extract_Data.fromJsonToObject import from_json_to_object
from search.search import search
from consolemenu import *
from consolemenu.items import *

#metaData('artists')

# Opening JSON file
#for filename in os.listdir("songs"):
 #   from_json_to_object(os.path.join("songs",filename))

#print(search().get_songs_of_album('1EWnkL3u6vzLdWOUz3vyoY'))

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename = "my_logs.log",
                    filemode = "a+",
                    format = Log_Format,
                    level = logging.ERROR)

LOGGER = logging.getLogger()


#Testing our Logger
try:
    result = int(input("1 - i am sign in, 0 - i am not sign in"))
    if result is 0: us = user_functions.sign_user()
    else:us = user_functions.login()
except ValueError as e:
    LOGGER.error("value error")
    raise e

try:
    ser = search(us.limit)
except AttributeError as e:
    LOGGER.error("user name of password entered was incorrect")
    raise e
#us = login()
#ser = search(us.limit)
menu = ConsoleMenu("SPOTIPY <3", "adding,searching and creating staff on your music account the easiest way possible!")
# Create some items

# MenuItem is the base class for all items, it doesn't do anything when selected
menu_item = MenuItem("Menu Item")

# A FunctionItem runs a Python function when selected
function_item = FunctionItem("get songs of album", ser.get_songs_of_album)
function_item2 = FunctionItem("get all artists", ser.get_artists)
function_item3 = FunctionItem("get albums of artist", ser.get_albums)
function_item4 = FunctionItem("get popular songs of artist", ser.get_popular_songs)
function_item5 = FunctionItem("add song to playlist",us.add_to_playlist)

menu.append_item(function_item)
menu.append_item(function_item2)
menu.append_item(function_item3)
menu.append_item(function_item4)
menu.append_item(function_item5)


menu.show()


#print(len(ser.get_songs_of_album('try')))

#us.add_to_playlist('2374M0fQpWi3dLnB54qaLX','songs_to_love')

