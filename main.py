import json
import os
from metaData import metaData
from extract_Data.fromJsonToObject import fromJsonToObject

me = metaData()
# Opening JSON file
for filename in os.listdir("songs"):
    fromJsonToObject(os.path.join("songs",filename))

# returns JSON object as
# a dictionary
