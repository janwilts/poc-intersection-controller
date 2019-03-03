import logging
import os
from concurrent.futures.thread import ThreadPoolExecutor

from dotenv import load_dotenv
from paho.mqtt.client import Client

from controller import Controller
from intersection.groups.cycle_group import CycleGroup
from intersection.groups.mv_group import MotorVehicleGroup
from intersection.groups.vessel_group import VesselGroup
from intersection.intersection import Intersection

# Schematic depiction of the intersections used in the proof of concept.
#
# MV = motor_vehicle
# C = cycle
# V = vessel
#
# L = light
# S = sensor
#                                                         |   |   |      |
#                                                         |   |   |      |
#                                                         |   v   |      |
#                                                         |       |      |
#                                                    C1S1 |       |      |                  |  |   ~       |
#                                                         | C1L1  |      |                  |  |           |
# ────────────────────────────────────────────────────────┘              |                  |  v ~      ~  |
#                                                                         \                 |              |
#    <──                                   MV3L1 MV3S1     <──             \                | V1S2  ~      |
#                                                                           \               |  ~           |
# ───────────────────┤                       ──  ──  ──  ──                  └──────────────┘ V1L2         └────────────
#
#    ──>     MV2S1 MV2L1                   MV4L1 MV4S1     ┌──                   <──                        MV1L2    <──
#                                                          v
#   ──  ──  ──  ──  ──                       ├────────────┤              ├──────────────────┤              ├────────────
#
#    ──┐     MV1S1 MV1L1                                                         ──>    MV1L1                        ──>
#      v
# ───────────────────┐       ┬ MV6L1 | MV5L1 ┌────────────┐       ┬ C2L1 ┌──────────────────┐         V1L1 ┌────────────
#                    |       |               |            |       |      | C2S1             |   ~          |
#                    |       | MV6S1 | MV5S1 |            |       |      |                  |         V1S1 |
#                    |       |               |            |       |      |                  |      ~      ~|
#                    |   |   |  <┐   |   ┌>  |            |       |   ^  |                  |          ^   |
#                    |   |   |   |       |   |            |       |   |  |                  |   ~      |   |
#                    |   v   |   |   |   |   |            |       |   |  |                  |          |   |

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
    VesselGroup(1),
]

BRIDGE_PATTERN = [
    [BRIDGE_GROUPS[1]],
]

INTERSECTIONS = [
    Intersection('intersection', INTERSECTION_GROUPS, INTERSECTION_PATTERN),
    Intersection('bridge', BRIDGE_GROUPS, BRIDGE_PATTERN),
]


def main() -> None:
    """
    Intersection controller main function.
    """

    logging_formatter = '[%(asctime)s] [%(levelname)s] %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_formatter)

    # Load environment variables from .env file
    load_dotenv()

    # Set up subscriber / publisher
    subscriber = Client(os.getenv('SUBSCRIBER_ID'))
    publisher = Client(os.getenv('PUBLISHER_ID'))

    # Enable MQTT logging
    subscriber.enable_logger()
    publisher.enable_logger()

    # Connect subscriber and publisher
    subscriber.connect(os.getenv('SUBSCRIBER_HOST'), int(os.getenv('SUBSCRIBER_PORT')))
    publisher.connect(os.getenv('PUBLISHER_HOST'), int(os.getenv('PUBLISHER_PORT')))

    qos = int(os.getenv('QUALITY_OF_SERVICE'))

    executor = ThreadPoolExecutor(3)

    # Create a controller object.
    controller = Controller(INTERSECTIONS, subscriber, publisher, qos)
    controller.init()

    executor.submit(controller_start, controller)
    executor.submit(controller_run_intersections, controller)


def controller_start(controller: Controller) -> None:
    controller.start()


def controller_run_intersections(controller: Controller) -> None:
    controller.run_intersections()


if __name__ == '__main__':
    main()
