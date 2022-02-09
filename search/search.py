import csv
import json


class search:
    def __init__(self,user_limit):
        self.user_limit = user_limit

    def get_artists(self):
        try:
            with open('artists\\metaData.csv', encoding="utf8") as file:
                content = csv.reader(file)
                artists = []
                next(content)
                for row in content:
                    if row: artists.append(row)  # if row is an empty list it will be false
            if self.user_limit : return artists[:5]
            else:return artists

        except FileNotFoundError as e:
            raise e

    def get_albums(self,artist_id):
        try:
            with open('artists\\' + artist_id + '.json') as artist:
                list_of_albums = json.load(artist)
                if self.user_limit : return list_of_albums[:5]
                else: return list_of_albums
        except FileNotFoundError as e:
            raise e

    def get_popular_songs(self,artist_id):
        all_songs = []
        list_of_artists_albums = search.get_albums(artist_id)

        for album in list_of_artists_albums:
            try:
                all_songs.extend(search.get_songs_of_album(album.get('id')))
            except FileNotFoundError as e:
                raise e
        sorted_songs = sorted(all_songs, key=lambda d: d['popularity'], reverse=True)
        if self.user_limit:return sorted_songs[:5]
        else: return sorted_songs

    def get_songs_of_album(self,album_id):
        try:
            with open('albums\\' + album_id + '.json', 'r') as File:
                list_of_all_songs_ids = json.load(File)
        except FileNotFoundError as e:
            raise e
        songs = self.create_list_of_songs(list_of_all_songs_ids)
        if self.user_limit:return songs[:5]
        else: return songs

    @staticmethod
    def create_list_of_songs(list_of_all_songs_ids):
        all_songs = []
        for song_id in list_of_all_songs_ids:
            with open('songs\\song_' + song_id + '.json', 'r')as song:
                all_songs.append(json.load(song).get('track'))
        return all_songs
