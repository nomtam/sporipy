import csv
import json
import logging

Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="my_logs.log",
                    filemode="a+",
                    format=Log_Format,
                    level=logging.ERROR)
LOGGER = logging.getLogger()


class Search:
    def __init__(self, user_limit: bool):
        self.user_limit = user_limit

    def get_artists(self):
        try:
            with open('raw_data\\artists\\Metadata.csv', encoding="utf8") as file:
                content = csv.reader(file)
                artists = []
                next(content)
                for row in content:
                    if row: artists.append(row)  # if row is an empty list it will be false
            if self.user_limit:
                print(artists[:5])
            else:
                print(artists)

        except FileNotFoundError as e:
            LOGGER.error("file meta data of artists not found")
            raise e

    def get_albums(self, artist_id=None):
        if artist_id is None: artist_id = input("artist id to Search:")
        try:
            with open('raw_data\\artists\\' + artist_id + '.json') as artist:
                albums = json.load(artist)
                if self.user_limit:
                    print(albums[:5])
                    return albums[:5]
                else:
                    print(albums);
                    return albums

        except FileNotFoundError as e:
            LOGGER.error("artist id not correct")
            raise e

    def get_popular_songs(self, artist_id=None):
        if artist_id is None: artist_id = input("artist id to Search:")
        all_songs = []
        artists_albums = self.get_albums(artist_id=artist_id)

        for album in artists_albums:
            try:
                all_songs.extend(self.get_songs_of_album(album_id=album.get('id')))
            except FileNotFoundError as e:
                LOGGER.error("album id not correct")
                raise e
        sorted_songs = sorted(all_songs, key=lambda d: d['popularity'], reverse=True)
        if self.user_limit:
            print(sorted_songs[:5])
        else:
            print(sorted_songs)

    def get_songs_of_album(self, album_id=None):
        if album_id is None: album_id = input("album id to Search:")
        try:
            with open('raw_data\\albums\\' + album_id + '.json', 'r') as File:
                songs_ids = json.load(File)
        except FileNotFoundError as e:
            LOGGER.error("album id not correct")
            raise e
        songs = self.create_list_of_songs(songs_ids)
        if self.user_limit:
            print(songs[:5]);
            return songs[:5]
        else:
            print(songs);return songs

    @staticmethod
    def create_list_of_songs(list_of_all_songs_ids):
        all_songs = []
        for song_id in list_of_all_songs_ids:
            try:
                with open('raw_data\\songs\\song_' + song_id + '.json', 'r')as song:
                    all_songs.append(json.load(song).get('track'))
            except FileNotFoundError as e:
                LOGGER.error("file of song not found")
                raise e
        return all_songs
