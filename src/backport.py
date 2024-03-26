import os, json, time
from kafka.kafka import Kafka_Client
from openweathermap.openweathermap import Weather_Client
from util.util import Utility
from data.data_store import DataRepository

# load required configuration and repositories
conf_json = os.getenv('PROJECT_CONF')
configuration = json.loads(conf_json)

kafka_client = Kafka_Client(configuration["kafka"]["conf"],configuration["kafka"]["topic"])
data_repository = DataRepository()
weather_client = Weather_Client(configuration["openweathermap"]["uri"], configuration["openweathermap"]["key"],configuration["openweathermap"]["coordinates"])    


weather_calls = 0
# last year in months
month_epochs = [
    (1706745600,1709247600),
    (1704067200,1706742000),
    (1701388800,1704063600),
    (1698796800,1701385200),
    (1696118400,1698793200),
    (1693526400,1696114800),
    (1690848000,1693522800),
    (1688169600,1690844400),
    (1685577600,1688166000),
    (1682899200,1685574000),
    (1680307200,1682895600),
    (1677628800,1680303600),
]

for month in month_epochs:
    start_epoch = month[0]
    end_epoch = month[1]
    data = weather_client.weather_test(start_epoch,end_epoch)
    kafka_client.write(str(data["coord"]), [str(data["list"])])
    print(f"Finished kafka publish for AQI from {Utility.epoch_to_datetime(start_epoch)} to {Utility.epoch_to_datetime(end_epoch)}")
    weather_calls +=1
    time.sleep(15)

print(f"Finished, {weather_calls} calls to the weather api.")
