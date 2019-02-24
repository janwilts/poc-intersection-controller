import paho.mqtt.client as mqtt


class Io:

    def __init__(self, client_id: str, host: str, port: int):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.client = mqtt.Client(client_id)

        self.connected = False

        self.on_connect = None
        self.on_disconnect = None

        self.client.on_connect = self.on_client_connect
        self.client.on_disconnect = self.on_client_disconnect

    def connect(self):
        self.client.connect(self.host, self.port)

    def disconnect(self):
        self.client.disconnect()

    def on_client_connect(self):
        self.connected = True
        self.on_connect()

    def on_client_disconnect(self):
        self.connected = False
        self.on_disconnect()

