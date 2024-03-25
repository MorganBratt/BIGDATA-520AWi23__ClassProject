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

    start_epoch = data_repository.get_bookmark()
    print(f"start_epoch get: {start_epoch}")

    if start_epoch == 0:
        start_epoch = data_repository.get_start_date_epoch()
    end_epoch = int(Utility.get_utc_rounded_down(datetime.now(timezone.utc)).timestamp())


    current_time_start = start_epoch
    while current_time_start < end_epoch:
        data = weather_client.weather_test(current_time_start,current_time_start+10800)
        kafka_client.write(str(data["coord"]), [str(data["list"])])
        current_time_start += 14400 ## take 4 1 hour samples
        data_repository.set_bookmark(current_time_start)
        print("loop")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }



if __name__ == "__main__":

    lambda_handler(event=[],context=[])

    exit()

