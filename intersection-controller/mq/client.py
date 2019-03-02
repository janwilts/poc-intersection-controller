from hbmqtt.client import MQTTClient


class Client(MQTTClient):

    def __init__(self, client_id: str, host: str, port: int) -> None:
        """
        Client constructor.

        :param client_id: MQTT Client ID.
        :param host: Host to connect to.
        :param port: Port to connect to.
        """

        super().__init__(client_id)

        self.host: str = host
        self.port: int = port

        self.client: MQTTClient = MQTTClient(client_id)

        self.connected: bool = False

    async def connect_client(self) -> None:
        """
        Wrapper around connect, automatically fills host and port.
        """

        await self.client.connect(f'mqtt://{self.host}:{self.port}')
