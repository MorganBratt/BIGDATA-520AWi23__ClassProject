import requests

class Weather_Client:
    def __init__(self,uri: str,key: str,coords: dict ):
        self.uri = uri
        self.key = key
        self.coords = coords

    def weather_test(self, start: int, end:int):
        url = f"http://{self.uri}/air_pollution/history?lat={self.coords['lat']}&lon={self.coords['lon']}&start={start}&end={end}&appid={self.key}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            #print(data)
            print(response.text)
        else:
            print('Error fetching weather data')