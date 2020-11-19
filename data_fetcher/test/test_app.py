import os

import pytest
from pymongo import MongoClient
from decouple import config

from ..app import App
from .. import country_db_fields as fields

cluster = MongoClient(config('CONNECTION_STRING'))
database = cluster[config('DATABASE')]
collection = database[config('COLLECTION')]


class TestApp:

    ####################
    # FILES DOWNLOADED #
    ####################
    def test_file_downloaded(self):
        test_app = App()
        test_app._download_csv_file()

        files_exists = os.path.isfile('data_fetcher/data/' + test_app.csv_file_name)

        assert files_exists is True

    #################################
    # CONFIRMED DATA IS SAVED TO DB #
    #################################
    def test_data_confirmed_is_saved(self):
        test_app = App()
        test_app._download_csv_file()

        test_app._create_country_objects()
        test_app._populate_country_objects()
        test_app._save_data_to_db()

        country = 'Netherlands'
        country_data = (collection.find_one({fields.name(): country}))

        confirmed_is_populated = False
        if int(country_data.get(fields.confirmed())) > 0:
            confirmed_is_populated = True

        assert confirmed_is_populated is True

    ##############################
    # DEATHS DATA IS SAVED TO DB #
    ##############################
    def test_data_deaths_is_saved(self):
        test_app = App()
        test_app._download_csv_file()

        test_app._create_country_objects()
        test_app._populate_country_objects()
        test_app._save_data_to_db()

        country = 'Netherlands'
        country_data = (collection.find_one({fields.name(): country}))

        deaths_is_populated = False
        if int(country_data.get(fields.deaths())) > 0:
            deaths_is_populated = True

        assert deaths_is_populated is True

    ##############################
    # ACTIVE DATA IS SAVED TO DB #
    ##############################
    def test_data_active_is_saved(self):
        test_app = App()
        test_app._download_csv_file()

        test_app._create_country_objects()
        test_app._populate_country_objects()
        test_app._save_data_to_db()

        country = 'Netherlands'
        country_data = (collection.find_one({fields.name(): country}))

        active_is_populated = False
        if int(country_data.get(fields.active())) > 0:
            active_is_populated = True

        assert active_is_populated is True

    #################################
    # RECOVERED DATA IS SAVED TO DB #
    #################################
    def test_data_recovered_is_saved(self):
        test_app = App()
        test_app._download_csv_file()

        test_app._create_country_objects()
        test_app._populate_country_objects()
        test_app._save_data_to_db()

        country = 'Netherlands'
        country_data = (collection.find_one({fields.name(): country}))

        recovered_is_populated = False
        if int(country_data.get(fields.active())) > 0:
            recovered_is_populated = True

        assert recovered_is_populated is True

    ###########################
    # CLEANUP AFTER EACH TEST #
    ###########################
    @pytest.fixture(autouse=True)
    def cleanup(self):
        yield
        for root, dirs, files in os.walk('data_fetcher/data'):
            for rm_file in files:
                os.remove(os.path.join(root, rm_file))

        cluster.drop_database(database)
