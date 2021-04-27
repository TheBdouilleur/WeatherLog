import os
import time
import requests
from bs4 import BeautifulSoup


API_KEY = os.environ['API_KEY']
WS_URL = "http://api.weatherstack.com/current"

weather_places=[{"place":"Clermont-Ferrand","url":WS_URL},
        {"place":"Paris","url":WS_URL},
        {"place":"Grenoble","url":WS_URL},
        {"place":"Mont-Blanc","url":"https://www.meteoblue.com/en/weather/current/mont-blanc_france"},
        {"place":"South-Pole","url":"https://www.meteoblue.com/en/weather/current/amundsen-scott-south-pole-station_antarctica"}]

while True:
    for weather_place in weather_places:
        print(weather_place)
        if weather_place['url']==WS_URL:
            parameters = {'access_key': API_KEY, 'query': weather_place['place']}
            response = requests.get(weather_place['url'], parameters)
            js = response.json()
            print(js)
            with open(f"{weather_place['place']}_log.csv","a") as file:
                file.write(f"{js['location']['localtime']},{js['location']['localtime_epoch']},{js['current']['temperature']},{js['current']['feelslike']},{js['current']['wind_speed']},{js['current']['weather_descriptions']}\n")
        else:
            response = requests.get(weather_place['url'])
            html = response.text

            soup = BeautifulSoup(html, "html.parser")
            
            
            temperature_list_fahrenheit_string = [s  for div in soup.select('.temperatures .cell') for s in div.stripped_strings][1:]
            temperature_list_fahrenheit = [int(i[:-1]) for i in temperature_list_fahrenheit_string]
            temperature_fahrenheit=sum(temperature_list_fahrenheit)/len(temperature_list_fahrenheit)
            temperature=str(int(1.8*temperature_fahrenheit+32))

            feelslike_list_fahrenheit_string = [s  for div in soup.select('.windchills .cell') for s in div.stripped_strings][1:]
            feelslike_list_fahrenheit = [int(i[:-1]) for i in feelslike_list_fahrenheit_string]
            feelslike_fahrenheit = sum(feelslike_list_fahrenheit)/len(feelslike_list_fahrenheit)
            feelslike = str(int(1.8*feelslike_fahrenheit+32))

            with open(f"{weather_place['place']}_log.csv","a") as file:
                file.write(f"{js['location']['localtime']},{js['location']['localtime_epoch']},{temperature},{feelslike},\n")
                
    time.sleep(86400)