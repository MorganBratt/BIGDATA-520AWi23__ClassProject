import os, json
from kafka.kafka import Kafka_Client
from openweathermap.openweathermap import Weather_Client
from datetime import datetime, timezone
from util.util import Utility
from data.data_store import DataRepository




def lambda_handler(event, context):
    print("Hello from Lambda!")
    
    # load required configuration and repositories
    conf_json = os.getenv('PROJECT_CONF')
    configuration = json.loads(conf_json)
    
    kafka_client = Kafka_Client(configuration["kafka"]["conf"],configuration["kafka"]["topic"])
    data_repository = DataRepository()
    weather_client = Weather_Client(configuration["openweathermap"]["uri"], configuration["openweathermap"]["key"],configuration["openweathermap"]["coordinates"])    

    bookmark_before = data_repository.get_bookmark()
    print(f"bookmark get: {bookmark_before}")

    start_epoch = Utility.datetime_to_epoch("2024-3-21 00:00:00", "%Y-%m-%d %H:%M:%S", "UTC")
    end_epoch = int(Utility.get_utc_rounded_down(datetime.now(timezone.utc)).timestamp())


    current_time_start = start_epoch
    while current_time_start < end_epoch:
        data = weather_client.weather_test(current_time_start,current_time_start+10800)
        kafka_client.write(str(data["coord"]), [str(data["list"])])
        current_time_start += 14400 ## take 4 1 hour samples
        print("loop")

    # todo: bookmarking


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }



if __name__ == "__main__":

    lambda_handler(event=[],context=[])

    exit()

