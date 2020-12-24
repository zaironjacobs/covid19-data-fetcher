from data_fetcher import country_db_fields as fields
import datetime


class Country:
    """
    Country class to store data of a country
    """

    def __init__(self):
        self.__name = ''
        self.__confirmed = 0
        self.__deaths = 0
        self.__active = 0
        self.__recovered = 0
        self.__last_updated_by_source_at = datetime.datetime.now()

    def increment_confirmed(self, confirmed):
        self.__confirmed += confirmed

    def increment_deaths(self, deaths):
        self.__deaths += deaths

    def increment_active(self, active):
        self.__active += active

    def increment_recovered(self, recovered):
        self.__recovered += recovered

    def to_dict(self):
        return {fields.name(): self.__name, fields.confirmed(): self.__confirmed,
                fields.deaths(): self.__deaths, fields.active(): self.__active,
                fields.recovered(): self.__recovered,
                fields.last_updated_by_source_at(): self.__last_updated_by_source_at}

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def confirmed(self):
        return self.__confirmed

    @property
    def deaths(self):
        return self.__deaths

    @property
    def active(self):
        return self.__active

    @property
    def recovered(self):
        return self.__recovered

    @property
    def last_updated_by_source_at(self):
        return self.__last_updated_by_source_at

    @last_updated_by_source_at.setter
    def last_updated_by_source_at(self, last_updated_by_source_at):
        self.__last_updated_by_source_at = last_updated_by_source_at
