import os
import sys
import configparser
import shutil
from datetime import datetime, timedelta

import pandas as pd
import requests
from requests.exceptions import RequestException
from requests.exceptions import HTTPError

from .models.country import Country
from .models.article import Article
from . import constants
from .mongo_database import MongoDatabase
from . import retriever

# Read config file
config = configparser.RawConfigParser()
config.read('config.ini')

# Get configs
collection_country = config['DEFAULT']['collection_country']
collection_article = config['DEFAULT']['collection_article']
news_api_key = config['DEFAULT']['news_api_key']
news_page_size = config['DEFAULT']['news_page_size']


class App:
    """
    Fetch and save data of each country to a MongoDB database.
    Fetch and save articles related to COVID-19 to a MongoDB database.
    """

    def __init__(self):
        self.__csv_file_name = ''

        self.__article_objects_list = []
        self.__country_objects_dict = {}

        self.__total_confirmed = 0
        self.__total_deaths = 0
        self.__total_recovered = 0
        self.__total_active = 0

        self.__mongodb = MongoDatabase()

    def init(self):
        """
        Main function for initialization
        """

        print('Downloading data...')
        self._download_csv_file()
        self._fetch_articles()

        print('Saving data to database...')
        self._create_country_objects()
        self._populate_country_objects()
        self._save_country_data_to_db()
        self._save_article_data_to_db()

        print('Finished')

    def __download(self, url):
        """
        Download any file to the data dir
        """

        try:
            output_path, downloaded_file_name = retriever.download(url, output_path=constants.data_dir)
        except (OSError, HTTPError, RequestException) as err:
            raise err
        else:
            return downloaded_file_name

    def _download_csv_file(self):
        """
        Download the csv file
        """

        if not os.path.exists(constants.data_dir):
            os.makedirs(constants.data_dir)
        else:
            shutil.rmtree(constants.data_dir)

        tries = 90
        for num in range(0, tries):
            date_time = datetime.now() - timedelta(num)
            date_time_string = datetime.strftime(date_time, '%m-%d-%Y')
            try:
                url = constants.csse_covid_19_daily_reports_url.format(date_time_string) + '.csv'
                file_name = self.__download(url)
                self.__csv_file_name = file_name
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

        last_updated_by_source_at = self.__get_last_updated_time()

        country_names_list = self._get_country_names_list()

        for country_name in country_names_list:
            country = Country()
            country.name = country_name
            country.last_updated_by_source_at = last_updated_by_source_at
            self.__country_objects_dict.update({country.name: country})

    def _populate_country_objects(self):
        """
        Populate all country objects with data retrieved from the csv file
        """

        df = pd.read_csv(constants.data_dir + self.__csv_file_name)

        # Remove all ".0" from numbers
        df.fillna(0, inplace=True, downcast='infer')

        row_count = len(df.index)

        def get_case_count(dataframe, column_name):
            case = int(dataframe.at[count, column_name])
            if case < 0:
                case = abs(case)
            return case

        for count in range(row_count):
            country_name = df.at[count, constants.country_region_column]

            try:
                deaths = get_case_count(df, constants.deaths_column)
                recovered = get_case_count(df, constants.recovered_column)
                active = get_case_count(df, constants.active_column)
                confirmed = get_case_count(df, constants.confirmed_column)
            except ValueError as err:
                print('Value error: ' + str(err))
            else:
                country = self.__country_objects_dict.get(country_name)

                country.increment_deaths(deaths)
                self.__total_deaths += deaths

                country.increment_recovered(recovered)
                self.__total_recovered += recovered

                country.increment_active(active)
                self.__total_active += active

                country.increment_confirmed(confirmed)
                self.__total_confirmed += confirmed

        country_worldwide = self.__country_objects_dict.get(constants.worldwide)
        country_worldwide.increment_deaths(self.__total_deaths)
        country_worldwide.increment_recovered(self.__total_recovered)
        country_worldwide.increment_active(self.__total_active)
        country_worldwide.increment_confirmed(self.__total_confirmed)

    def __get_last_updated_time(self):
        """
        Return the last updated time of the data
        """

        df = pd.read_csv(constants.data_dir + self.__csv_file_name, nrows=1)
        date_string = df.at[0, constants.last_update]
        date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

        # Add UTC to time
        date_utc = date.strftime('%Y-%m-%dT%H:%M:%SZ')

        return date_utc

    def _fetch_articles(self):
        """
        Fetch articles and save them to a list
        """

        url = constants.news_api_url.format(news_api_key, news_page_size)
        response = requests.get(url)
        if response.status_code == 200:
            size = len(response.json()['articles'])
            for x in range(size):
                article = Article()

                title = '-'
                if response.json()['articles'][x]['title'] is not None:
                    title = response.json()['articles'][x]['title']
                article.title = title

                source_name = '-'
                if response.json()['articles'][x]['source']['name'] is not None:
                    source_name = response.json()['articles'][x]['source']['name']
                article.source_name = source_name

                author = '-'
                if response.json()['articles'][x]['author'] is not None:
                    author = response.json()['articles'][x]['author']
                article.author = author

                description = '-'
                if response.json()['articles'][x]['description'] is not None:
                    description = response.json()['articles'][x]['description']
                article.description = description

                url = '-'
                if response.json()['articles'][x]['url'] is not None:
                    url = response.json()['articles'][x]['url']
                article.url = url

                date_string = response.json()['articles'][x]['publishedAt']
                date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')

                # Add UTC to time
                date_utc = date.strftime('%Y-%m-%dT%H:%M:%SZ')

                article.published_at = date_utc

                self.__article_objects_list.append(article)
        else:
            print('Error: could not fetch articles')

    def _save_country_data_to_db(self):
        """
        Save each country object to a MongoDB database
        """

        self.__mongodb.drop_collection(collection_country)
        for key, value in self.__country_objects_dict.items():
            self.__mongodb.insert_country(value.to_dict())

    def _save_article_data_to_db(self):
        """
        Save each article object to a MongoDB database
        """

        self.__mongodb.drop_collection(collection_article)
        for article in self.__article_objects_list:
            self.__mongodb.insert_article(article.to_dict())

    @property
    def csv_file_name(self):
        return self.__csv_file_name
