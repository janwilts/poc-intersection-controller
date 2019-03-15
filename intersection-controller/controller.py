import time
from typing import List

from paho.mqtt.client import MQTTMessage, Client

from intersection.intersection import Intersection
from topic_parser import TopicParser


class Controller:
    """
    Main controller class.
    """

    def __init__(self, intersections: List[Intersection], subscriber: Client, publisher: Client, qos: int) -> None:
        """
        Controller constructor.

        :param intersections List of intersections with defined pattern.
        :param subscriber A connected MQTT subscriber.
        :param publisher A connected MQTT publisher.
        :param qos MQTT Quality of Service.
        """

        self.intersections: List[Intersection] = intersections
        self.subscriber: Client = subscriber
        self.publisher: Client = publisher
        self.qos: int = qos

        self.stop: bool = False

    def init(self) -> None:
        """
        Starts the controller by first connecting the subscriber and publisher, then runs their coroutines.
        """

        # Sets up the message listener
        self.subscriber.on_message = self.on_message

        for intersection in self.intersections:
            # Subscribe on all sensor topics in a intersection
            self.subscriber.subscribe([(topic, self.qos) for topic in intersection.sensor_topics])
            self.subscriber.subscribe(f'{intersection.topic}/features/timescale')

            # Intersection publish handler
            intersection.on_publish = self.on_publish

    def start(self) -> None:
        self.subscriber.loop_forever()

    def run_intersections(self) -> None:
        """
        Starts all intersections, by iterating over their patterns.
        """

        for intersection in self.intersections:
            intersection.init()

        while not self.stop:
            for intersection in self.intersections:
                intersection.iterate_patterns()

    def on_message(self, _client: Client, _userdata: any, message: MQTTMessage) -> None:
        """
        Listens for incoming messages then parses them in the intersections.

        :param _client: Unused.
        :param _userdata: Unused.
        :param message: Incoming MQTT message object.
        """

        parser = TopicParser(self.intersections, message.topic).fill_all()

        if parser.is_features:
            if parser.timescale:
                parser.intersection.timescale = float(message.payload)
        else:
            parser.intersection.on_message(parser, message.payload)

    def on_publish(self, topic: str, payload: any = None) -> None:
        """
        Publish callback, to be called from the intersections.

        :param topic: Topic to send payload on.
        :param payload: The message contents.
        """

        if payload is None:
            self.publisher.publish(topic)
        else:
            self.publisher.publish(topic, payload)
