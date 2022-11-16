import os
import sys
import configparser
from datetime import datetime, timedelta
from typing import List

import pandas as pd
import requests

from models import Country
from models import Article
from mongo_db import MongoDatabase

config = configparser.RawConfigParser()
config.read('config.ini')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

covid19_data_csv = os.path.join(os.path.dirname(__file__), 'data', 'data.csv')


class App:
    """
    Fetch and save data of each country to a MongoDB database.
    Fetch and save articles related to COVID-19 to a MongoDB database.
    """

    def __init__(self):
        self.__mongodb = MongoDatabase()
        print('Downloading data...')
        self._download_csv()
        countries = self._create_country_models()
        articles = self._create_article_models()
        print('Saving data to database...')
        self._save_countries_to_db(countries)
        self._save_article_data_to_db(articles)
        print('Finished')

    def _download_csv(self):
        """ Download the csv file """

        try_count = 90
        for x in range(0, try_count):
            date_time = datetime.now() - timedelta(x)
            date_time_string = datetime.strftime(date_time, '%m-%d-%Y')
            url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/' \
                  f'csse_covid_19_data/csse_covid_19_daily_reports/{date_time_string}.csv'
            response = requests.get(url, headers=headers)
            if response.ok:
                with open(covid19_data_csv, 'wb') as file:
                    file.write(response.content)
                    return
        else:
            print(f'Unable to find the latest csv file for the last {str(try_count)} days.')
            sys.exit(0)

    def _create_country_models(self) -> List:
        """ Create country models """

        total_confirmed = 0
        total_deaths = 0

        last_update_col = 'Last_Update'
        country_region_col = 'Country_Region'
        deaths_col = 'Deaths'
        confirmed_col = 'Confirmed'

        countries = []

        df = pd.read_csv(covid19_data_csv)
        df = df[[country_region_col, last_update_col, confirmed_col, deaths_col]]

        last_updated_by_source_at_val = df.iloc[0][last_update_col]
        last_updated_by_source_at_val = datetime.strptime(last_updated_by_source_at_val, '%Y-%m-%d %H:%M:%S')
        last_updated_by_source_at_val = last_updated_by_source_at_val.strftime('%Y-%m-%dT%H:%M:%SZ')

        countries_grouped = df.groupby(df.Country_Region)
        for index, country in countries_grouped:
            name_val = country.iloc[0][country_region_col]
            confirmed_val = country[confirmed_col].sum()
            deaths_val = country[deaths_col].sum()

            total_confirmed += confirmed_val
            total_deaths += deaths_val

            country = Country(name=name_val,
                              confirmed=confirmed_val,
                              deaths=deaths_val,
                              last_updated_by_source_at=last_updated_by_source_at_val)
            countries.append(country)

        worldwide = Country(name='Worldwide',
                            confirmed=total_confirmed,
                            deaths=total_deaths,
                            last_updated_by_source_at=last_updated_by_source_at_val)
        countries.append(worldwide)

        return countries

    def _create_article_models(self) -> List:
        """ Fetch articles and create article models """

        articles = []
        news_api_key = config['DEFAULT']['news_api_key']
        news_page_size = config['DEFAULT']['news_page_size']
        url = f'https://newsapi.org/v2/everything?qInTitle=covid OR corona&apiKey={news_api_key}' \
              f'&language=en&sortBy=publishedAt&pageSize={news_page_size}'
        response = requests.get(url, headers=headers)
        if response.ok:
            size = len(response.json()['articles'])
            for x in range(size):
                title_val = response.json()['articles'][x]['title']
                if not title_val:
                    title_val = '-'

                source_name_val = response.json()['articles'][x]['source']['name']
                if not source_name_val:
                    source_name_val = '-'

                author_val = response.json()['articles'][x]['author']
                if not author_val:
                    author_val = '-'

                description_val = response.json()['articles'][x]['description']
                if not description_val:
                    description_val = '-'

                url_val = response.json()['articles'][x]['url']
                if not url_val:
                    url_val = '-'

                date_string = response.json()['articles'][x]['publishedAt']
                date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
                date_utc = date.strftime('%Y-%m-%dT%H:%M:%SZ')

                article = Article(title=title_val,
                                  source_name=source_name_val,
                                  author=author_val,
                                  description=description_val,
                                  url=url_val,
                                  published_at=date_utc)
                articles.append(article)

        return articles

    def _save_countries_to_db(self, countries: List[Country]):
        """ Save each country object to a MongoDB database """

        collection_country = config['DEFAULT']['collection_country']
        self.__mongodb.drop_collection(collection_country)
        for country in countries:
            self.__mongodb.insert_country(country.dict())

    def _save_article_data_to_db(self, articles: List[Article]):
        """ Save each article object to a MongoDB database """

        collection_article = config['DEFAULT']['collection_article']
        self.__mongodb.drop_collection(collection_article)
        for article in articles:
            self.__mongodb.insert_article(article.dict())


if __name__ == '__main__':
    App()
