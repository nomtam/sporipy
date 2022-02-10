import csv
import logging
import os

import custom_exceptions


Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "my_logs.log",
                    filemode = "a+",
                    format = Log_Format,
                    level = logging.ERROR)
LOGGER = logging.getLogger()

class metaData:
    def __init__(self, directory_name,header = ['name','id']):
        if os.path.exists(directory_name + '\\metaData.csv') is False:
            with open(directory_name + '\\metaData.csv', 'x', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)

    @staticmethod
    def add_row_artists(directory_name,*args):
        try:
            with open(directory_name + '\\metaData.csv', 'a+', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(args)
        except custom_exceptions.DirectoryNotFound:
            LOGGER.error("Directory was not found")

