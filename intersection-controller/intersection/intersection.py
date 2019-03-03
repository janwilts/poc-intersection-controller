import threading
import time
from typing import List, Generator

from intersection.components.light.light_state import LightState
from intersection.components.sensor.sensor import Sensor
from intersection.components.sensor.sensor_state import SensorState
from intersection.groups.group import Group
from topic_error import TopicError


class Intersection:
    def __init__(self, id: str, groups: List[Group], pattern: List[List[Group]]):
        self.id = id
        self.groups = groups
        self.pattern = pattern
        self.stop = False

        for group in groups:
            group.intersection = self

        self.on_publish = None

        self.sensor_lock = threading.Lock()

    def on_message(self, parser, payload: bytes) -> None:
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

        for group in pattern:
            self.set_all_lights_in_group(group, LightState.GO)

        time.sleep(3)

        for group in pattern:
            self.set_all_lights_in_group(group, LightState.TRANSITIONING)

        time.sleep(1)

        for group in pattern:
            # Turn off all sensors
            for _ in group.set_all_sensors(SensorState.LOW):
                pass

            # Red to all lights
            self.set_all_lights_in_group(group, LightState.STOP)

    def set_all_lights_in_group(self, group: Group, state: LightState) -> None:
        if not group.one_sensor_high() and state == LightState.GO:
            return

        for topic, state in group.set_all_lights(state):
            self.on_publish(topic, state.value)

    @property
    def sensor_topics(self) -> Generator:
        for group in self.groups:
            for sensor in group.sensors:
                yield sensor.topic

    @property
    def topic(self):
        return self.id
