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
            return data

        else:
            print('Error fetching weather data')


# Example usage
if __name__ == "__main__":
    import os, json, pytz
    from datetime import datetime, timezone
    conf_json = os.getenv('PROJECT_CONF')
    configuration = json.loads(conf_json)

    def epoch_to_datetime(epoch_time):
        """Convert epoch time to a human-readable datetime."""
        # The epoch time should be in seconds. If you have milliseconds, divide by 1000.
        #date_time = datetime.fromtimestamp(epoch_time)
        date_time = datetime.fromtimestamp(epoch_time, pytz.utc)
        return date_time.strftime('%Y-%m-%d %H:%M:%S')
    
    


    start_epoch = 1706745600
    end_epoch = 1709251200
    weather_client = Weather_Client(configuration["openweathermap"]["uri"], configuration["openweathermap"]["key"],configuration["openweathermap"]["coordinates"])
    data = weather_client.weather_test(start_epoch,end_epoch - 3600)


    first_entry = data["list"][0]["dt"]
    last_entry = data["list"][-1]["dt"]
    count = len(data["list"])

    print("First entry:", epoch_to_datetime(first_entry))
    print("Last entry:", epoch_to_datetime(last_entry))
    print("Count:", count)

    