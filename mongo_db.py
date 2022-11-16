import configparser

from pymongo import MongoClient

# Read config file
config = configparser.RawConfigParser()
config.read('config.ini')


class MongoDatabase:
    """ MongoDB """

    def __init__(self):
        database = config['DEFAULT']['database']
        collection_country = config['DEFAULT']['collection_country']
        collection_article = config['DEFAULT']['collection_article']
        connection_string = config['DEFAULT']['connection_string']

        self.__client = MongoClient(connection_string)
        self.__database = self.__client[database]
        self.__collection_country = self.__database[collection_country]
        self.__collection_articles = self.__database[collection_article]

    def insert_country(self, data):
        """ Insert data to MongoDB """

        self.__collection_country.insert_one(data)

    def insert_article(self, data):
        """ Insert data to MongoDB """

        self.__collection_articles.insert_one(data)

    def drop_collection(self, collection_name):
        """ Drop the collection from the MongoDB database """

        self.__database.drop_collection(collection_name)
