import sys, os, json
from kafka.kafka import Kafka_Client

conf_json = os.getenv('PROJECT_CONF')
configuration = json.loads(conf_json)

messages = [str(i) for i in range(100)]  # Generating a list of messages to send

kafka_client = Kafka_Client(configuration["kafka"]["conf"],configuration["kafka"]["topic"])
kafka_client.write("test", messages)