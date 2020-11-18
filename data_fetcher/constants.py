from decouple import config

csse_covid_19_daily_reports_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/' \
                                  'csse_covid_19_data/csse_covid_19_daily_reports/{}.csv'

github_api_csse_covid_19_daily_reports = 'https://api.github.com/repos/CSSEGISandData/COVID-19/commits?path=' \
                                         'csse_covid_19_data%2Fcsse_covid_19_daily_reports%2F{}.csv'

data_dir = 'data_fetcher/data/'

worldwide = 'Worldwide'

province_state_column = 'Province_State'
country_region_column = 'Country_Region'
deaths_column = 'Deaths'
confirmed_column = 'Confirmed'
recovered_column = 'Recovered'
active_column = 'Active'

cases_columns = [confirmed_column, deaths_column, recovered_column, active_column]
unwanted_columns = ['FIPS', 'Admin2', 'Province_State', 'Last_Update', 'Lat', 'Long_',
                    'Combined_Key', 'Incident_Rate', 'Case_Fatality_Ratio']
