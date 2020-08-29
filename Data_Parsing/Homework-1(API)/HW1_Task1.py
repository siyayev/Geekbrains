import requests
headers = {'User-Agent': 'my-test-app/0.0.2',
           'Accept': '*/*'
           }
apikey = 'Dm7yaAujiG9YCXSoNXWXfuaeGXqq9GTk'
city = input('Введите название города на английском: ')
city_link = 'http://dataservice.accuweather.com/locations/v1/cities/search?apikey='+apikey+'&q='+city
response = requests.get(city_link, headers=headers)
if len(response.json()) == 0:
    print('Город не найден, попробуйте еще раз')
else:
    r = response.json()
    city_code = r[0]['Key']
    forecast_link = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/' + city_code + '?apikey=' + apikey + '&language=ru-ru&metric=true'
    forecast = requests.get(forecast_link, headers=headers)
    f = forecast.json()
    fd = f['DailyForecasts']
    for i in range(len(fd)):
         date = fd[i]['Date']
         temp = fd[i]['Temperature']['Maximum']['Value']
         day = fd[i]['Day']['IconPhrase']
         night = fd[i]['Night']['IconPhrase']
         print(f'{date} Максимальная температура воздуха {temp} градусов, днем {day}, ночью {night}')