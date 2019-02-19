from .io import Io


class Publisher(Io):

    def __init__(self, client_id: str, host: str, port: int):
        super().__init__(client_id, host, port)

        self.on_publish = None

        self.client.on_publish = self.on_publish

    def publish(self, topic: str, payload: any):
        self.client.publish(topic, payload)
