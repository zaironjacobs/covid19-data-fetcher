from pymongo import MongoClient

from . import constants


class MongoDB:
    """
    MongoDB
    """

    def __init__(self):
        self.__cluster = MongoClient()
        self.__database = self.__cluster[constants.database]
        self.__collection = self.__database[constants.collection]

    def insert(self, data):
        """
        Insert data to MongoDB
        """

        self.__collection.insert_one(data)

    def drop_collection(self, collection_name):
        """
        Drop a collection from the MongoDB database
        """

        self.__database.drop_collection(collection_name)
