COVID-19 Data Fetcher
=================

Fetch and save data of each country to a local MongoDB database. 

Data will be fetched from: https://github.com/CSSEGISandData/COVID-19

## Download
```console
$ git clone https://github.com/zaironjacobs/covid19-python-data-fetcher
```

## Usage

Make sure you have MongoDB installed on your system before running the script.

Copy the file .env.example to .env and a database name and a collection name to the environment variables.

To use:
```console
$ cd covid19-python-data-fetcher
$ pipenv install --dev
$ pipenv run python run_data_fetcher.py
```