import csv
import json
import logging
# CR: looks the same as fromJsonToObject. Why not make a file for that?
Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="my_logs.log",
                    filemode="a+",
                    format=Log_Format,
                    level=logging.ERROR)
LOGGER = logging.getLogger()


class Search:
    # CR: why not is_premium? Limit is general and might sound like a number and not bool
    def __init__(self, user_limit: bool):
        self.user_limit = user_limit

    def get_artists(self):
        try:
            # CR: config
            with open('raw_data\\artists\\Metadata.csv', encoding="utf8") as file:
                content = csv.reader(file)
                artists = []
                next(content)

                for row in content:
                    # CR: should brake line after :
                    # CR: could use also len(artists) == 0 for more readable code
                    if row: artists.append(row)  # if row is an empty list it will be false
            if self.user_limit:
                # CR: you shouldn't be printing the results from the method.
                #  What about OCP? What if I would prefer to return them as an API result?
                #  The whole point of making a search class is to use it with different outputs,
                #  like console and api, and you couple it to console
                # CR: also, 5 is hard codded
                print(artists[:5])
            else:
                # CR: same as above
                print(artists)

        except FileNotFoundError as e:
            LOGGER.error("file meta data of artists not found")
            raise e

    def get_albums(self, artist_id=None):
        # CR: new line in if again...
        # CR: breaking OCP and SRP by using input here. Same explanation as above
        if artist_id is None: artist_id = input("artist id to Search:")
        try:
            # CR: counfig
            with open('raw_data\\artists\\' + artist_id + '.json') as artist:
                albums = json.load(artist)
                if self.user_limit:
                    # CR: here you return as you should. So why do you print?
                    print(albums[:5])
                    return albums[:5]
                else:
                    # CR: ;?
                    # CR: same question about printing
                    print(albums);
                    return albums

        except FileNotFoundError as e:
            LOGGER.error("artist id not correct")
            raise e

    def get_popular_songs(self, artist_id=None):
        # CR: same as about for if with new line and input with OCP SRP
        if artist_id is None: artist_id = input("artist id to Search:")
        all_songs = []
        artists_albums = self.get_albums(artist_id=artist_id)

        for album in artists_albums:
            try:
                # CR: append is a more common use to add to list
                all_songs.extend(self.get_songs_of_album(album_id=album.get('id')))
            except FileNotFoundError as e:
                LOGGER.error("album id not correct")
                raise e
        sorted_songs = sorted(all_songs, key=lambda d: d['popularity'], reverse=True)
        if self.user_limit:
            # CR: again with the prints
            print(sorted_songs[:5])
        else:
            print(sorted_songs)

    def get_songs_of_album(self, album_id=None):
        # CR: same with if and input
        if album_id is None: album_id = input("album id to Search:")
        try:
            # CR: config
            with open('raw_data\\albums\\' + album_id + '.json', 'r') as File:
                songs_ids = json.load(File)
        except FileNotFoundError as e:
            LOGGER.error("album id not correct")
            raise e
        songs = self.create_list_of_songs(songs_ids)
        if self.user_limit:
            # CR: semicolon and also print comment
            print(songs[:5]);
            return songs[:5]
        else:
            print(songs);return songs

    # CR: why static?
    # CR: this method is super used. you repeat this code at every method in this class.
    #  Why not make it more generic and use it everywhere? Put the path as config,
    #  and maybe send back the data and append it from the caller method
    @staticmethod
    def create_list_of_songs(list_of_all_songs_ids):
        all_songs = []
        for song_id in list_of_all_songs_ids:
            try:
                # CR: config
                with open('raw_data\\songs\\song_' + song_id + '.json', 'r')as song:
                    all_songs.append(json.load(song).get('track'))
            except FileNotFoundError as e:
                LOGGER.error("file of song not found")
                raise e
        return all_songs
