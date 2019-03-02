import logging
import asyncio
import os

from dotenv import load_dotenv

from controller import Controller
from intersection.groups.cycle_group import CycleGroup
from intersection.groups.mv_group import MotorVehicleGroup
from intersection.groups.vessel_group import VesselGroup
from intersection.intersection import Intersection
from mq.client import Client


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


def main() -> None:
    """
    Intersection controller main function.
    """

    load_dotenv()

    # Set up subscriber / publisher
    subscriber = Client(os.getenv('SUBSCRIBER_ID'), os.getenv('SUBSCRIBER_HOST'), int(os.getenv('SUBSCRIBER_PORT')))
    publisher = Client(os.getenv('PUBLISHER_ID'), os.getenv('PUBLISHER_HOST'), int(os.getenv('PUBLISHER_PORT')))

    # Create a controller object.
    controller = Controller(INTERSECTIONS, subscriber, publisher)

    # Create asyncio loop, runs controller.run() until it stops.
    loop = asyncio.get_event_loop()
    try:
        controller.loop = loop
        loop.run_until_complete(controller.run())
    finally:
        loop.close()


if __name__ == '__main__':
    formatter = '[%(asctime)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=formatter)

    main()
