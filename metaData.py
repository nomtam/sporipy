import csv
import os

class metaData:
    def __init__(self):
        if os.path.exists("artists\\metaData.csv")!= True:
            header = ['name', 'id']
            with open('artists\\metaData.csv', 'x', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(header)


    @staticmethod
    def add_row_artists(id,name):
        with open('artists\\metaData.csv', 'a+', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow([id,name])