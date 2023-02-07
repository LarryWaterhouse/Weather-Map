# load csv of Game Data via CFBD
import numpy as np
import pandas as pd
import cfbd
from __future__ import print_function
import time
from cfbd.rest import ApiException
from pprint import pprint


configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'API KEY'
configuration.api_key_prefix['Authorization'] = 'Bearer'
api_config = cfbd.ApiClient(configuration)

#get game results
response = games = cfbd.GamesApi(api_config).get_games(year=year, season_type='both', division='fbs')

game_data = pd.DataFrame(response, columns=['team', 'id', 'season','week', 'start_date',	'date', 'time',	'neutral_site','venue',	'home_team','home_points'.	'away_team',	'away_points'])

# create an instance of the API class
api_instance = cfbd.TeamsApi(cfbd.ApiClient(configuration))
year = 56 # int | Year filter (optional)

try:
    # FBS team list
    api_response = api_instance.get_fbs_teams(year=year)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TeamsApi->get_fbs_teams: %s\n" % e)
    
geo_df = pd.DataFrame(api_response)

game_data =  pd.merge(game_data,geo_df,left_index=True, right_index=True)

#Function to get the weather using Open Meteo's API
def get_weather_results(lat, long, date):
    url ='https://archive-api.open-meteo.com/v1/archive?latitude=' + str(lat) + '&longitude=' + str(long) + '&start_date=' + str(date) + '&end_date=' + str(date) + '&hourly=temperature_2m,apparent_temperature,precipitation,weathercode,windspeed_10m,winddirection_10m&timezone=America%2FNew_York&temperature_unit=fahrenheit&windspeed_unit=ms&precipitation_unit=inch'
    r = requests.get(url)
    data = r.json()
    weather_data = data['hourly']
    weather_data = {
        'time': weather_data['time'],
        'temperature_2m': weather_data['temperature_2m'],
        'apparent_temperature': weather_data['apparent_temperature'],
        'precipitation': weather_data['precipitation'],
        'weathercode': weather_data['weathercode'],
        'windspeed_10m': weather_data['windspeed_10m'],
        'winddirection_10m': weather_data['winddirection_10m']
    }

    df = pd.DataFrame(weather_data)

    return df


get_data = get_weather_results(lat,long,date)

results = []
#Loop through Game_data for the Lat, Long, Date

for x in range(0, len(game_data)):
    try:
        results.append(get_weather_results(game_data['lat'][x], game_data['long'][x], game_data['date'][x]))
    except KeyError:
        continue

result_df = pd.concat(results, ignore_index=True)

merge_df = pd.merge(game_data,result_df,left_index=True, right_index=True)


