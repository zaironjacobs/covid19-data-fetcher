from data_fetcher import news_fields as fields
import datetime


class News:
    """
    News class to store news data
    """

    def __init__(self):
        self.__title = ''
        self.__source_name = ''
        self.__author = ''
        self.__description = ''
        self.__url = ''
        self.__published_at = datetime.datetime.now()

    def to_dict(self):
        return {fields.title(): self.__title, fields.source_name(): self.__source_name,
                fields.author(): self.__author, fields.description(): self.__description,
                fields.url(): self.__url,
                fields.published_at(): self.__published_at}

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def source_name(self):
        return self.__source_name

    @source_name.setter
    def source_name(self, source_name):
        self.__source_name = source_name

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, author):
        self.__author = author

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    @property
    def published_at(self):
        return self.__published_at

    @published_at.setter
    def published_at(self, published_at):
        self.__published_at = published_at
