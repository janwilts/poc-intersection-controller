import logging
import os
import time
from concurrent.futures.thread import ThreadPoolExecutor

from dotenv import load_dotenv
from paho.mqtt.client import Client

from controller import Controller
from intersection.components.light.light import Light
from intersection.components.sensor.sensor import Sensor
from intersection.groups.cycle_group import CycleGroup
from intersection.groups.foot_group import FootGroup
from intersection.groups.mv_group import MotorVehicleGroup
from intersection.groups.vessel_group import VesselGroup
from intersection.intersection import Intersection

# Schematic depiction of the intersections used in the proof of concept.
#
# MV = motor_vehicle
# F = foot
# C = cycle
# V = vessel
#
# L = light
# S = sensor
#                                                         |   |   |      |
#                                                         |       |      |
#                                                  F1S1   | F1L1  |      |                  |  |   ~       |
#                                                  C1S1   | C1L1  |      |                  |  |           |
# ────────────────────────────────────────────────────────┘              |                  |  v ~      ~  |
#                                                                         \                 |              |
#    <──                                   MV3L1 MV3S1     <──             \                | V1S2  ~      |
#                                                                           \               |  ~           |
# ───────────────────┤                       ──  ──  ──  ──                  └────────
#                                                         |   |   |      |
#                                                         |   v   |      |──────┘ V1L2         └────────────
#
#    ──>     MV2S1 MV2L1                   MV4L1 MV4S1     ┌──                   <──                        MV1L2    <──
#                                                          v
#   ──  ──  ──  ──  ──                       ├────────────┤              ├──────────────────┤              ├────────────
#
#    ──┐     MV1S1 MV1L1                                                         ──>    MV1L1                        ──>
#      v
# ───────────────────┐       ┬ MV6L1 | MV5L1 ┌────────────┐       ┬ C1L2 ┌──────────────────┐         V1L1 ┌────────────
#                    |       |               |            |       | F1L2 | C1S2             |   ~          |
#                    |       | MV6S1 | MV5S1 |            |       |      | F1S2             |         V1S1 |
#                    |       |               |            |       |      |                  |      ~      ~|
#                    |   |   |  <┐   |   ┌>  |            |       |   ^  |                  |          ^   |
#                    |   |   |   |       |   |            |       |   |  |                  |   ~      |   |
#                    |   v   |   |   |   |   |            |       |   |  |                  |          |   |

INTERSECTION_GROUPS = [
    CycleGroup(1, [Light(1), Light(2), Sensor(1), Sensor(2)]),
    FootGroup(1, [Light(1), Light(2), Sensor(1), Sensor(2)]),
    MotorVehicleGroup(1),
    MotorVehicleGroup(2),
    MotorVehicleGroup(3),
    MotorVehicleGroup(4),
    MotorVehicleGroup(5),
    MotorVehicleGroup(6),
]

INTERSECTION_PATTERN = [
    [INTERSECTION_GROUPS[0], INTERSECTION_GROUPS[1], INTERSECTION_GROUPS[2], INTERSECTION_GROUPS[7]],
    [INTERSECTION_GROUPS[2], INTERSECTION_GROUPS[3], INTERSECTION_GROUPS[4]],
    [INTERSECTION_GROUPS[5], INTERSECTION_GROUPS[6]],
]

BRIDGE_GROUPS = [
    MotorVehicleGroup(1),
    VesselGroup(1),
]

BRIDGE_PATTERN = [
    [BRIDGE_GROUPS[1]],
]

def main() -> None:
    """
    Intersection controller main function.
    """

    logging_formatter = '[%(asctime)s] [%(levelname)s] %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_formatter)

    # Load environment variables from .env file
    load_dotenv()

    intersection = Intersection(os.getenv('TEAM_ID'), INTERSECTION_GROUPS, INTERSECTION_PATTERN)

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

    # Create a controller object.
    controller = Controller([intersection], subscriber, publisher, qos)
    controller.init()

    with ThreadPoolExecutor(2) as executor:
        executor.submit(controller_start, controller),
        executor.submit(controller_run_intersections, controller)


def controller_start(controller: Controller) -> None:
    controller.start()


def controller_run_intersections(controller: Controller) -> None:
    controller.run_intersections()
    time.sleep(1)


if __name__ == '__main__':
    main()
