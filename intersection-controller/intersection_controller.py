import logging
import signal
import sys
import os
from typing import List

from dotenv import load_dotenv
from paho.mqtt.client import MQTTMessage

from intersection.groups.cycle_group import CycleGroup
from intersection.groups.mv_group import MotorVehicleGroup
from intersection.groups.vessel_group import VesselGroup
from intersection_thread import IntersectionThread
from mq.publisher import Publisher
from mq.subscriber import Subscriber
from intersection.intersection import Intersection

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s')

subscriber: Subscriber = None
publisher: Publisher = None

INTERSECTION_GROUPS = [
    CycleGroup(1),
    CycleGroup(2),
    MotorVehicleGroup(1),
    MotorVehicleGroup(2),
    MotorVehicleGroup(3),
    MotorVehicleGroup(4),
    MotorVehicleGroup(5),
    MotorVehicleGroup(6),
]

INTERSECTION_PATTERN = [
    [INTERSECTION_GROUPS[2], INTERSECTION_GROUPS[5], INTERSECTION_GROUPS[6]],
    [INTERSECTION_GROUPS[0], INTERSECTION_GROUPS[1], INTERSECTION_GROUPS[2], INTERSECTION_GROUPS[7]],
    [INTERSECTION_GROUPS[3], INTERSECTION_GROUPS[4]],
]

BRIDGE_GROUPS = [
    MotorVehicleGroup(1),
    VesselGroup(1)
]

BRIDGE_PATTERN = [
    [BRIDGE_GROUPS[1]]
]

INTERSECTIONS = [
    Intersection('intersection', INTERSECTION_GROUPS, INTERSECTION_PATTERN),
    Intersection('bridge', BRIDGE_GROUPS, BRIDGE_PATTERN)
]

THREADS = [
    IntersectionThread(INTERSECTIONS[0]),
    IntersectionThread(INTERSECTIONS[1])
]


def on_sigint(signum, frame):
    logging.debug('Received signal SIGINT')

    for ints in INTERSECTIONS:
        ints.stop = True

        for topic in ints.sensor_topics:
            subscriber.unsubscribe(topic)

    logging.debug('Disconnecting subscriber and publisher.')

    subscriber.disconnect()
    publisher.disconnect()

    for thread in THREADS:
        thread.join()


def on_message(message: MQTTMessage):
    logging.debug(f'Received message {message.payload} on {message.topic}')

    topic_parts = message.topic.split('/')

    intersections: List[Intersection] = [INTERSECTIONS for ints in INTERSECTIONS if ints.id == topic_parts[0]]

    for ints in intersections:
        ints.message(message)


def main(argv):
    # Load environment variables from .env file
    load_dotenv()

    global subscriber
    global publisher

    # Set up subscriber
    subscriber = Subscriber(os.getenv('SUBSCRIBER_ID'), os.getenv('SUBSCRIBER_HOST'), int(os.getenv('SUBSCRIBER_PORT')))

    # Set up publisher
    publisher = Publisher(os.getenv('PUBLISHER_ID'), os.getenv('PUBLISHER_HOST'), int(os.getenv('PUBLISHER_PORT')))

    logging.info('Connecting subscriber and publisher.')

    subscriber.connect()
    publisher.connect()

    signal.signal(signal.SIGINT, on_sigint)
    signal.signal(signal.SIGTERM, on_sigint)

    for intersection in INTERSECTIONS:
        intersection.on_publish = lambda topic, payload: publisher.publish(topic, payload)

        for sensor_topic in intersection.sensor_topics:
            logging.info(f'Subscribing on: {sensor_topic}')
            subscriber.subscribe(sensor_topic)

    subscriber.on_message = on_message

    for intersection in INTERSECTIONS:
        intersection.init()

    for thread in THREADS:
        thread.start()


if __name__ == '__main__':
    main(sys.argv)
