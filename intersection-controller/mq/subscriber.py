from paho.mqtt.client import Client, MQTTMessage

from mq.io import Io


class Subscriber(Io):

    def __init__(self, client_id: str, host: str, port: int):
        super().__init__(client_id, host, port)

        self.on_subscribe = None
        self.on_unsubscribe = None
        self.on_message = None

        self.client.on_subscribe = self.on_subscribe
        self.client.on_unsubscribe = self.on_unsubscribe
        self.client.on_message = self.client_on_message

    def subscribe(self, topic: str):
        self.client.subscribe(topic)

    def unsubscribe(self, topic: str):
        self.client.unsubscribe(topic)

    def client_on_message(self, client: Client, userdata: any, message: MQTTMessage):
        self.on_message(message)

