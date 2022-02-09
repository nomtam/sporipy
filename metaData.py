import csv
import os


class metaData:
    def __init__(self, directory_name):
        if os.path.exists(directory_name + '\\metaData.csv') is False:
            header = ['name', 'id']
            with open(directory_name + '\\metaData.csv', 'x', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(header)

    @staticmethod
    def add_row_artists(id, name, directory_name):
        with open(directory_name + '\\metaData.csv', 'a+', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow([id, name])
