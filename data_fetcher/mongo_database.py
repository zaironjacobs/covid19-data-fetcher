from pymongo import MongoClient
from decouple import config


class MongoDatabase:
    """
    MongoDB
    """

    def __init__(self):
        self.__client = MongoClient(config('CONNECTION_STRING'))
        self.__database = self.__client[config('DATABASE')]
        self.__collection = self.__database[config('COLLECTION')]

    def insert(self, data):
        """
        Insert data to MongoDB
        """

        self.__collection.insert_one(data)

    def drop_collection(self, collection_name):
        """
        Drop the collection from the MongoDB database
        """

        self.__database.drop_collection(collection_name)
