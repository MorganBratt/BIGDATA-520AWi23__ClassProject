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
                print(f"message:{message}")
                self.producer.produce(self.topic,message, callback=self.deliver_callback, key=key)
            except BufferError as e:
                sys.stderr.write('%% Local Producer queue full (%d message awaiting delivery) try again\n' % len(self.producer))
            self.producer.poll(0)

        sys.stderr.write('%% Waiting for %d deliveries\n' % len(self.producer))
        self.producer.flush()


