import csv
import logging
import os
import custom_exceptions
# CR: same as on other places about logging
Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="my_logs.log",
                    filemode="a+",
                    format=Log_Format,
                    level=logging.ERROR)
LOGGER = logging.getLogger()


class Metadata:
    # CR: better practice is to check if None on headers
    def __init__(self, directory_name, header=['name', 'id']):
        # CR: config
        if os.path.exists('raw_data\\'+directory_name + '\\Metadata.csv') is False:
            # CR: put this in a method. You are coupled to csv
            with open(directory_name + '\\Metadata.csv', 'x', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)

    @staticmethod
    def add_new_info(directory_name, values_to_add):
        # CR: same for csv coupling
        try:
            # CR: config
            with open('raw_data\\'+directory_name + '\\Metadata.csv', 'a+', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(values_to_add)
        except custom_exceptions.DirectoryNotFound:
            LOGGER.error("Directory was not found")
