import threading
import time
from typing import List, Generator

from intersection.components.light.light_state import LightState
from intersection.components.sensor.sensor import Sensor
from intersection.components.sensor.sensor_state import SensorState
from intersection.groups.group import Group
from topic_error import TopicError


class Intersection:
    """
    Intersection class, depicts one intersection, e.g. the traffic lights or the bridge.
    """

    def __init__(self, id: str, groups: List[Group], pattern: List[List[Group]]) -> None:
        """
        Intersection constructor.

        :param id: Intersection ID, topic prefix.
        :param groups: All groups.
        :param pattern: The pattern in which the intersection should be executed.
        """

        self.id = id
        self.groups = groups
        self.pattern = pattern

        self.on_publish = None
        self.sensor_lock = threading.Lock()

        self.stop = False
        self.timescale = 1

        for group in groups:
            group.intersection = self

    def on_message(self, parser, payload: bytes) -> None:
        """
        Message handler, gets the component and then checks if its a sensor, if so changes its state.

        :param parser: Topic parser.
        :param payload: Message payload.
        :return:
        """

        component = parser.component

        if not isinstance(component, Sensor):
            raise TopicError('Found component is not a sensor')

        self.sensor_lock.acquire()

        payload = int(payload)

        if payload == SensorState.HIGH.value:
            component.state = SensorState.HIGH
        elif payload == SensorState.LOW.value:
            component.state = SensorState.LOW

        self.sensor_lock.release()

    def init(self):
        """
        Set all lights to STOP.
        """

        for group in self.groups:
            for light in group.lights:
                light.state = LightState.STOP
                self.on_publish(light.topic, light.state.value)

    def iterate_patterns(self) -> None:
        """
        Loop over all pattern part in the patterns property.
        """

        for pattern in self.pattern:
            self.handle_pattern_part(pattern)

    def handle_pattern_part(self, pattern: List[Group]):
        should_go = False

        for group in pattern:
            if group.one_sensor_high():
                should_go = True

        if not should_go:
            return

        # Green
        [self.set_all_lights_in_group(group, LightState.GO) for group in pattern]
        self.timescale_sleep(max([group.go_time for group in pattern]) / self.timescale)

        # Orange
        [self.set_all_lights_in_group(group, LightState.TRANSITIONING) for group in pattern]
        self.timescale_sleep(max([group.transition_time for group in pattern]) / self.timescale)

        for group in pattern:
            # Turn off all sensors
            for _ in group.set_all_sensors(SensorState.LOW):
                pass

            # Red
            self.set_all_lights_in_group(group, LightState.STOP)

        self.timescale_sleep(max([group.go_time for group in pattern]) / self.timescale)

    def timescale_sleep(self, duration: float) -> None:
        for _ in range(0, 100):
            time.sleep((duration / 100) / self.timescale)

    def set_all_lights_in_group(self, group: Group, state: LightState) -> None:
        for topic, state in group.set_all_lights(state):
            self.on_publish(topic, state.value)

    @property
    def sensor_topics(self) -> Generator:
        """
        All sensor topics in this intersection.

        :return: Sensor topics.
        """

        for group in self.groups:
            for sensor in group.sensors:
                yield sensor.topic

    @property
    def topic(self):
        """
        Intersection topic part (ID).

        :return: Topic part.
        """

        return self.id
