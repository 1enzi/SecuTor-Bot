import pymongo
from pymongo import MongoClient

import strings

cluster = MongoClient(strings.clusterURL)

db = cluster["SecuTor"]
collection = db["SecuTor"]

post1 = {
    "name": "Tim",
    "age": 23
}

collection.insert_one(post1)