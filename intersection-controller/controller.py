import asyncio
import logging
from concurrent.futures.process import ProcessPoolExecutor
from typing import List

from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1
from hbmqtt.session import ApplicationMessage

from intersection.intersection import Intersection
from mq.client import Client


class Controller:
    """
    Main controller class, runs tasks asynchronously.
    """

    def __init__(self, intersections: List[Intersection], subscriber: Client, publisher: Client) -> None:
        """
        Controller constructor.

        :param intersections List of intersections with defined pattern.
        :param subscriber Subscriber MQTT Client.
        :param publisher Publisher MQTT Client.
        """

        self.intersections: List[Intersection] = intersections
        self.subscriber: Client = MQTTClient()
        self.publisher: Client = MQTTClient()

        self.loop: asyncio.AbstractEventLoop = None
        self.stop: bool = False

    async def run(self) -> None:
        """
        Starts the controller by first connecting the subscriber and publisher, then runs their coroutines.
        """

        await self.subscriber.connect('mqtt://82.73.55.235:6969')
        await self.publisher.connect('mqtt://82.73.55.235:6969')

        for intersection in self.intersections:
            topics = []

            for topic in intersection.sensor_topics:
                topics.append((topic, QOS_1))

            await self.subscriber.subscribe(topics)
            intersection.on_publish = self.on_publish

        executor = ProcessPoolExecutor(2)

        await asyncio.ensure_future(self.loop.run_in_executor(executor, self.on_message))
        await self.loop.run_in_executor(executor, self.run_intersections)

    async def run_intersections(self) -> None:
        """
        Starts all intersections, by iterating over their patterns.
        """

        while not self.stop:
            for intersection in self.intersections:
                await intersection.iterate_patterns()

    async def on_message(self) -> None:
        """
        Listens for incoming messages then parses them in the intersections.
        """

        while not self.stop:
            message: ApplicationMessage = await self.subscriber.deliver_message()

            for intersection in self.intersections:
                intersection.parse_topic(message.topic)

    async def on_publish(self, topic: str, payload: any) -> None:
        """
        Publish callback, to be called from the intersections.

        :param topic: Topic to send payload on.
        :param payload: The message contents.
        """

        if not payload:
            await self.publisher.publish(topic)
        else:
            await self.publisher.publish(topic, payload)
