import logging
import threading
import time
from typing import List

from paho.mqtt.client import MQTTMessage

from intersection.components.component import Component
from intersection.components.light.light_state import LightState
from intersection.components.sensor.sensor import Sensor
from intersection.components.sensor.sensor_state import SensorState
from intersection.groups.group import Group


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

    def message(self, message: MQTTMessage):
        component = self.get_component_from_topic(message.topic)

        if not component:
            return

        if not isinstance(component, Sensor):
            return

        self.sensor_lock.acquire()
        component.state = SensorState.HIGH
        self.sensor_lock.release()

    def init(self):
        for group in self.groups:
            for light in group.lights:
                logging.debug(f'Set light {group.id}:{light.id} to STOP')

                light.state = LightState.STOP
                self.on_publish(light.topic, light.state.value)

    def run(self):
        while True:
            if self.stop:
                break

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
            for light in group.lights:
                logging.debug(f'Set light {group.id}:{light.id} to GO')

                light.state = LightState.GO
                self.on_publish(light.topic, light.state.value)

        time.sleep(10)

        for group in pattern:
            for light in group.lights:
                logging.debug(f'Set light {group.id}:{light.id} to WAIT')

                light.state = LightState.WAIT
                self.on_publish(light.topic, light.state.value)

        time.sleep(2)

        for group in pattern:

            logging.debug(f'Set all sensors in  {group.id} to LOW')

            self.sensor_lock.acquire()
            group.set_all_sensors(SensorState.LOW)
            self.sensor_lock.release()

            for light in group.lights:
                logging.debug(f'Set light {group.id}:{light.id} to STOP')

                light.state = LightState.STOP
                self.on_publish(light.topic, light.state.value)

    def get_component_from_topic(self, topic: str):
        topic_parts = topic.split('/')

        group = self.get_group_from_topic(topic)

        if not group:
            return None

        components: List[Component] = [group.components for cpt in group.components if cpt.type.value == topic_parts[3]]

        if topic_parts[4]:
            components = [components for cpt in components if cpt.id == topic_parts[4]]

        if len(components) != 1:
            return None

        return components[0]

    def get_group_from_topic(self, topic: str):
        topic_parts = topic.split('/')

        groups: List[Group] = [self.groups for grp in self.groups if grp.type.value == topic_parts[1]]
        groups: List[Group] = [groups for grp in groups if grp.id == topic_parts[2]]

        if len(groups) != 1:
            return None

        return groups[0]

    @property
    def sensor_topics(self):
        for group in self.groups:
            for sensor in group.sensors:
                yield sensor.topic

    @property
    def topic(self):
        return self.id
