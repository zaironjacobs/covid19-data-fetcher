import os
import configparser

import pytest
from pymongo import MongoClient

from fetcher import Fetcher

# Read config file
config = configparser.RawConfigParser()
config.read('config.ini')

# Get configs and setup database
cluster = MongoClient(config['DEFAULT']['connection_string'])
database = cluster[config['DEFAULT']['database']]
collection = database[config['DEFAULT']['collection_country']]

covid19_data_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.csv')


class TestApp:

    ####################
    # FILES DOWNLOADED #
    ####################
    def test_file_downloaded(self):
        fetcher = Fetcher()
        fetcher._download_csv()

        files_exists = os.path.isfile(covid19_data_csv)

        assert files_exists is True

    #################################
    # CONFIRMED DATA IS SAVED TO DB #
    #################################
    def test_data_confirmed_is_saved(self):
        fetcher = Fetcher()
        fetcher._download_csv()

        countries = fetcher._create_country_models()

        fetcher._save_countries_to_db(countries)

        country = 'Netherlands'
        country_data = collection.find_one({'name': country})

        confirmed_is_populated = False
        if int(country_data.get('confirmed')) > 0:
            confirmed_is_populated = True

        assert confirmed_is_populated is True

    ##############################
    # DEATHS DATA IS SAVED TO DB #
    ##############################
    def test_data_deaths_is_saved(self):
        fetcher = Fetcher()
        fetcher._download_csv()

        countries = fetcher._create_country_models()

        fetcher._save_countries_to_db(countries)

        country = 'Netherlands'
        country_data = collection.find_one({'name': country})

        deaths_is_populated = False
        if int(country_data.get('deaths')) > 0:
            deaths_is_populated = True

        assert deaths_is_populated is True

    ###########################
    # CLEANUP AFTER EACH TEST #
    ###########################
    @pytest.fixture(autouse=True)
    def cleanup(self):
        yield
        if os.path.isfile(covid19_data_csv):
            os.remove(covid19_data_csv)
        cluster.drop_database(database)
