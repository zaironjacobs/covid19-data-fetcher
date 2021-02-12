from pymongo import MongoClient
from decouple import config


class MongoDatabase:
    """
    MongoDB
    """

    def __init__(self):
        self.__client = MongoClient(config('CONNECTION_STRING'))
        self.__database = self.__client[config('DATABASE')]
        self.__collection_country = self.__database[config('COLLECTION_COUNTRY')]
        self.__collection_news = self.__database[config('COLLECTION_NEWS')]

    def insert_country(self, data):
        """
        Insert data to MongoDB
        """

        self.__collection_country.insert_one(data)

    def insert_news(self, data):
        """
        Insert data to MongoDB
        """

        self.__collection_news.insert_one(data)

    def drop_collection(self, collection_name):
        """
        Drop the collection from the MongoDB database
        """

        self.__database.drop_collection(collection_name)
