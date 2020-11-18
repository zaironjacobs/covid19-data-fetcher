import os
import sys
import shutil
from datetime import datetime, timedelta

from decouple import config
import pandas as pd
import requests
from requests.exceptions import RequestException
from requests.exceptions import HTTPError

from .country import Country
from . import constants
from .mongodb import MongoDB
from . import helper
from . import retriever


class App:
    """
    Save data from the downloaded csv file inside the data dir to a local MongoDB database
    """

    def __init__(self):
        self.__date_time_string = ''
        self.__csv_file_name = ''

        self.__country_objects_list = []

        self.__total_confirmed = 0
        self.__total_deaths = 0
        self.__total_recovered = 0
        self.__total_active = 0

        self.__mongodb = MongoDB()

    def init(self):
        """
        Main function for initialization
        """

        print('Downloading data...')
        self._download_csv_file()

        print('Cleaning data...')
        helper.clean_data(self.__csv_file_name)

        print('Saving data to database...')
        self._create_country_objects()
        self._populate_country_objects()
        self._save_data_to_db()

        print('Finished')

    def _download_csv_file(self):
        """
        Download csv file
        """

        def download(url, date_time_string):
            try:
                output_path, downloaded_file_name = retriever.download(url.format(date_time_string),
                                                                       output_path=constants.data_dir)
            except (OSError, HTTPError, RequestException) as err:
                raise err
            else:
                return downloaded_file_name

        if not os.path.exists(constants.data_dir):
            os.makedirs(constants.data_dir)
        else:
            shutil.rmtree(constants.data_dir)

        tries = 30
        for num in range(0, tries):
            date_time = datetime.now() - timedelta(num)
            self.__date_time_string = datetime.strftime(date_time, '%m-%d-%Y')
            try:
                file_name = download(constants.csse_covid_19_daily_reports_url, self.__date_time_string)
                self.__csv_file_name = file_name
                print('Download completed: ' + file_name)
            except (OSError, HTTPError, RequestException):
                pass
            else:
                break
        else:
            print('Download failed: Unable to find the latest csv file for the last ' + str(tries) + ' days')
            sys.exit(0)

    def _get_country_names_list(self):
        """
        Return a list with all country names
        """
        df = pd.read_csv(constants.data_dir + self.__csv_file_name)
        row_count = len(df.index)

        country_names_list = []

        for count in range(row_count):
            country = df.at[count, constants.country_region_column]
            country_names_list.append(country)

        country_names_list.append(constants.worldwide)

        # Remove duplicate countries and return
        return list(dict.fromkeys(country_names_list))

    def _create_country_objects(self):
        """
        Create country objects
        """

        last_updated_by_source_at = self._get_last_updated_time()

        country_names_list = self._get_country_names_list()

        for country_name in country_names_list:
            country = Country()
            country.name = country_name
            country.last_updated_by_source_at = last_updated_by_source_at
            self.__country_objects_list.append(country)

    def _populate_country_objects(self):
        """
        Populate all country objects with data retrieved from the csv file
        """

        for country in self.__country_objects_list:

            df = pd.read_csv(constants.data_dir + self.__csv_file_name)
            row_count = len(df.index)
            for count in range(row_count):
                country_name = df.at[count, constants.country_region_column]
                if country.name == country_name:
                    try:
                        deaths = int(df.at[count, constants.deaths_column])
                        country.increment_deaths(deaths)
                        self.__total_deaths += deaths

                        recovered = int(df.at[count, constants.recovered_column])
                        country.increment_recovered(recovered)
                        self.__total_recovered += recovered

                        active = int(df.at[count, constants.active_column])
                        country.increment_active(active)
                        self.__total_active += active

                        confirmed = int(df.at[count, constants.confirmed_column])
                        country.increment_confirmed(confirmed)
                        self.__total_confirmed += confirmed
                    except ValueError as err:
                        print('Value error: ' + str(err))

        for country in self.__country_objects_list:
            if country.name == constants.worldwide:
                country.increment_deaths(self.__total_deaths)
                country.increment_recovered(self.__total_recovered)
                country.increment_active(self.__total_active)
                country.increment_confirmed(self.__total_confirmed)

    def _get_last_updated_time(self):
        """
        Return the last updated time of the data source
        """

        res = requests.get(constants.github_api_csse_covid_19_daily_reports.format(self.__date_time_string))
        date_updated_by_source = res.json()[0]['commit']['committer']['date']
        return datetime.strptime(date_updated_by_source, '%Y-%m-%dT%H:%M:%SZ')

    def _save_data_to_db(self):
        """
        Save each country object to a local MongoDB database
        """

        self.__mongodb.drop_collection(config('COLLECTION'))
        for country in self.__country_objects_list:
            self.__mongodb.insert(country.to_dict())

    @property
    def csv_file_name(self):
        return self.__csv_file_name
