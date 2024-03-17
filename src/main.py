import sys, os, json
from kafka.kafka import Kafka_Client
from openweathermap.openweathermap import Weather_Client

conf_json = os.getenv('PROJECT_CONF')
configuration = json.loads(conf_json)

messages = [str(i) for i in range(1)]  # Generating a list of messages to send

weather_client = Weather_Client(configuration["openweathermap"]["uri"], configuration["openweathermap"]["key"],configuration["openweathermap"]["coordinates"])
weather_client.weather_test(1606266000,1606269600)

exit()

kafka_client = Kafka_Client(configuration["kafka"]["conf"],configuration["kafka"]["topic"])
kafka_client.write("test", messages)

