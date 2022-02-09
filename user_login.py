import json
import csv
from extract_Data.fromJsonToObject import addToFileList
from pathlib import Path

class user_login:
    def __init__(self, username, password):#user enter username and password and i check it its correct here
        user_info = self.validation(username,password)
        if user_info is None:
            print("password or username is incorrect")
        else:
            self.limit = user_info[2]
            self.username = username
            self.is_artist = bool(user_info[3])
            print("succesfully entered system")
        #try:
         #   with open('users\\' + self.username + '\\user_details.csv', encoding="utf8") as user_info:
          #      content = csv.reader(user_info)
           #     next(content)#skip header

            #    limit = next(content)[2]=='free'
        #except FileNotFoundError as e:
         #   raise e


    def validation(self,username,password):
        path = Path('users\\'+username)
        if path.exists() :
            try:
                with open('users\\' + username + '\\user_details.csv', encoding="utf8") as user_info:
                    content = csv.reader(user_info)
                    next(content)  # skip header
                    details = next(content)
                    if password == details[1]:return details
            except FileNotFoundError as e:
                raise e



    def add_to_playlist(self, song_id, playlist_name):
        with open('songs\\song_'+song_id+'.json','r') as song:
            song_info = json.load(song)
        addToFileList(song_info, 'users\\' + self.username + '\\playlists\\' + playlist_name+'.json',limit=self.limit)
