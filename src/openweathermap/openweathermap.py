import requests

class Weather_Client:
    def __init__(self,uri,key):
        self.uri = uri
        self.key = key


    def hello_world(self):
        print(F"uri:{self.uri} key:{self.key}")

    def weather_test(self):

        city = "Seattle"
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.key}'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            desc = data['weather'][0]['description']
            print(f'Temperature: {temp} K')
            print(f'Description: {desc}')
        else:
            print('Error fetching weather data')