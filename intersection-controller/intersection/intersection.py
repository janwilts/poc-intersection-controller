import time
from typing import List

from paho.mqtt.client import MQTTMessage

from intersection.components.light.light_state import LightState
from intersection.components.sensor.sensor import Sensor
from intersection.components.sensor.sensor_state import SensorState
from intersection.groups.group import Group


class Intersection:
    def __init__(self, groups: List[Group], pattern: List[List[Group]]):
        self.groups = groups
        self.pattern = pattern

        self.on_publish = None

    def message(self, message: MQTTMessage):
        component = self.get_component_from_topic(message.topic)

        if not component:
            return

        if not isinstance(component, Sensor):
            return

        component.state = SensorState.HIGH

    def run(self):
        while True:
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
            group.set_all_lights(LightState.GO)
            self.on_publish(f'intersection/{group.group_type.value}/{group.group_id}/light', LightState.GO.value)

        time.sleep(10)

        for group in pattern:
            group.set_all_lights(LightState.WAIT)
            self.on_publish(f'intersection/{group.group_type.value}/{group.group_id}/light', LightState.WAIT.value)

        time.sleep(2)

        for group in pattern:
            group.set_all_lights(LightState.STOP)
            self.on_publish(f'intersection/{group.group_type.value}/{group.group_id}/light', LightState.STOP.value)
            group.set_all_sensors(SensorState.LOW)

    def get_component_from_topic(self, topic: str):
        topic_parts = topic.split('/')

        correct_group_type_groups = []

        for group in self.groups:
            if group.group_type == topic_parts[1]:
                correct_group_type_groups.append(group)

        correct_id_group = None

        for group in correct_group_type_groups:
            if group.group_id == topic_parts[2]:
                correct_id_group = group

        components = []

        if topic_parts[3] == 'sensor':
            components = correct_id_group.sensors
        elif topic_parts[3] == 'light':
            components = correct_id_group.lights

        correct_component_id = 1

        if topic_parts[4]:
            correct_component_id = topic_parts[4]

        for component in components:
            if component.component_id == correct_component_id:
                return component

        return None

    @property
    def sensor_topics(self):
        topics = []

        for group in self.groups:
            for sensor in group.sensors:
                topics.append(f'intersection/{group.group_type.value}/{group.group_id}/sensor/{sensor.component_id}')

        return topics
