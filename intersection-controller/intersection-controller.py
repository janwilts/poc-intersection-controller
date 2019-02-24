import sys
import os
from dotenv import load_dotenv

from intersection.groups.cycle_group import CycleGroup
from intersection.groups.mv_group import MotorVehicleGroup
from intersection.groups.vessel_group import VesselGroup
from mq.publisher import Publisher
from mq.subscriber import Subscriber
from intersection.intersection import Intersection

GROUPS = [
    CycleGroup(1),
    CycleGroup(2),
    MotorVehicleGroup(1),
    MotorVehicleGroup(2),
    MotorVehicleGroup(3),
    MotorVehicleGroup(4),
    MotorVehicleGroup(5),
    MotorVehicleGroup(6),
    MotorVehicleGroup(7),
    VesselGroup(1)
]

PATTERN = [
    [GROUPS[2], GROUPS[5], GROUPS[6]],
    [GROUPS[8]],
    [GROUPS[0], GROUPS[1], GROUPS[2], GROUPS[7]],
    [GROUPS[8]],
    [GROUPS[3], GROUPS[4]],
    [GROUPS[8]],
]


def main(argv):
    # Load environment variables from .env file
    load_dotenv()

    intersection = Intersection(GROUPS, PATTERN)

    # Set up subscriber
    subscriber = Subscriber(os.getenv('SUBSCRIBER_ID'), os.getenv('SUBSCRIBER_HOST'), int(os.getenv('SUBSCRIBER_PORT')))

    # Set up publisher
    publisher = Publisher(os.getenv('PUBLISHER_ID'), os.getenv('PUBLISHER_HOST'), int(os.getenv('PUBLISHER_PORT')))

    # Connecting
    subscriber.connect()
    publisher.connect()

    subscriber.on_connect = \
        lambda: print(f'Connected to subscriber {subscriber.client_id} on {subscriber.host}:{subscriber.port}')
    publisher.on_connect = \
        lambda: print(f'Connected to publisher {publisher.client_id} on {publisher.host}:{publisher.port}')

    for sensor_topic in intersection.sensor_topics:
        subscriber.subscribe(sensor_topic)

    subscriber.on_message = lambda message: intersection.message(message)
    intersection.on_publish = lambda topic, payload: publisher.publish(topic, payload)

    intersection.run()


if __name__ == '__main__':
    main(sys.argv)
