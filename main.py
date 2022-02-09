import json
import os

from user_login import user_login
from metaData import metaData
from extract_Data.fromJsonToObject import from_json_to_object
from search.search import search
#metaData('artists')
#metaData('songs')
# Opening JSON file
#for filename in os.listdir("songs"):
 #   from_json_to_object(os.path.join("songs",filename))

#print(search().get_songs_of_album('1EWnkL3u6vzLdWOUz3vyoY'))

us = user_login('ofori','123')
ser = search(us.limit)

#print(len(ser.get_songs_of_album('try')))

us.add_to_playlist('2374M0fQpWi3dLnB54qaLX','songs_to_love')


# returns JSON object as
# a dictionary
