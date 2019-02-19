import paho.mqtt.client as mqtt


class Io:

    def __init__(self, client_id: str, host: str, port: int):
        self.host = host
        self.port = port
        self.client = mqtt.Client(client_id)

        self.on_connect = None
        self.on_disconnect = None

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    def connect(self):
        self.client.connect(self.host, self.port)

    def disconnect(self):
        self.client.disconnect()
