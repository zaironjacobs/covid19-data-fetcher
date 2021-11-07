COVID-19 Data Fetcher
=================

* Fetch and save data of each country to a MongoDB database.
* Fetch and save articles related to COVID-19 to a MongoDB database.

Source of data: [CSSEGISandData](https://github.com/CSSEGISandData/COVID-19) & [News API](https://newsapi.org/).

## Dependencies

- [MongoDB](https://www.mongodb.com/)
- [Python 3](https://www.python.org/downloads/)
- [News API Key](https://newsapi.org/)

## Download

```console
$ git clone https://github.com/zaironjacobs/covid19-data-fetcher
```

## Usage

Copy the file config-example.ini to config.ini and fill in the environment variables. A local connection example:

```
database = covid19
collection_country = country
collection_article = article
connection_string = mongodb://localhost:27017
news_api_key = 1234567890
news_page_size = 5
```

To use:

```console
$ pipenv install
$ pipenv run python run.py
```

An example of a country document:

```javascript
{
    "_id": {
        "$oid": "60250f5b1ae25397d00c706c"
    },
    "name": "Netherlands",
    "confirmed": 1027023,
    "deaths": 14710,
    "active": 998836,
    "recovered": 13477,
    "last_updated_by_source_at": {
        "$date": "2021-02-11T05:23:55.000Z"
    }
}
```

An example of an article document:

```javascript
{
    "_id": {
        "$oid": "60252065ac79b69102f2183c"
    },
    "title": "Coping With COVID Redundancy",
    "source_name": "Mindtools.com",
    "author": "Steven Edwards",
    "description": "If we fail to pivot and transition successfully through...",
    "url": "https://www.mindtools.com/blog/coping-with-covid-redundancy/",
    "published_at": "2021-02-11T12:01:00Z"
}
```

## Crontab

At minute 0 and 30:

```
0,30 * * * * cd ~/covid19-data-fetcher && /usr/local/bin/pipenv run python run.py
```
