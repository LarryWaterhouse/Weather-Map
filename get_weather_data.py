geo_df = pd.read_csv('LOAD DATA')

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
for x in range(0, len(game_data)):
    try:
        results.append(get_weather_results(game_data['lat'][x], game_data['long'][x], game_data['date'][x]))
    except KeyError:
        continue

result_df = pd.concat(results, ignore_index=True)
