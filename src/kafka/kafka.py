# producer.py
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient
import sys

class Kafka_Client:
    def __init__(self,conf, topic):
        self.conf = conf
        self.topic = topic
        self.producer = Producer(**self.conf)
        self.admin_client = AdminClient

    def deliver_callback(self, err, msg):
        """Callback to handle message delivery reports."""
        if err:
            sys.stderr.write('%% Message failed delivery: %s\n' % err)
        else:
            sys.stderr.write('%% Message delivered to %s [%d] @ %o\n' % (msg.topic(), msg.partition(), msg.offset()))

    def write(self,key, messages):

        for message in messages:
            try:
                self.producer.produce(self.topic,message, callback=self.deliver_callback, key=key)
            except BufferError as e:
                sys.stderr.write('%% Local Producer queue full (%d message awaiting delivery) try again\n' % len(self.producer))
            self.producer.poll(0)

        sys.stderr.write('%% Waiting for %d deliveries\n' % len(self.producer))
        self.producer.flush()

if __name__ == "__main__":
    import os, json
    conf_json = os.getenv('PROJECT_CONF')
    configuration = json.loads(conf_json)
    messages = ["[{'main': {'aqi': 2}, 'components': {'co': 226.97, 'no': 0.09, 'no2': 1.59, 'o3': 65.8, 'so2': 0.07, 'pm2_5': 0.5, 'pm10': 0.91, 'nh3': 0.36}, 'dt': 1711224000}, {'main': {'aqi': 2}, 'components': {'co': 226.97, 'no': 0.06, 'no2': 1.23, 'o3': 77.96, 'so2': 0.07, 'pm2_5': 0.5, 'pm10': 0.79, 'nh3': 0.32}, 'dt': 1711227600}, {'main': {'aqi': 2}, 'components': {'co': 226.97, 'no': 0.07, 'no2': 0.78, 'o3': 94.41, 'so2': 0.06, 'pm2_5': 0.5, 'pm10': 0.64, 'nh3': 0.21}, 'dt': 1711231200}, {'main': {'aqi': 2}, 'components': {'co': 230.31, 'no': 0.06, 'no2': 0.85, 'o3': 94.41, 'so2': 0.08, 'pm2_5': 0.5, 'pm10': 0.63, 'nh3': 0.24}, 'dt': 1711234800}]"]
    kafka_client = Kafka_Client(configuration["kafka"]["conf"],configuration["kafka"]["topic"])
    kafka_client.write("test", messages)