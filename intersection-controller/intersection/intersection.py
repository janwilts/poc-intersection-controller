import asyncio
import logging
import time
from typing import List, Callable, Awaitable, Generator

from intersection.components.light.light_state import LightState
from intersection.components.sensor.sensor import Sensor
from intersection.components.sensor.sensor_state import SensorState
from intersection.groups.group import Group


class Intersection:
    """
    Intersection class, represents one intersection that has its own groups and a pattern.
    """

    def __init__(self, id: str, groups: List[Group], pattern: List[List[Group]]) -> None:
        """
        Intersection constructor.

        :param id: Unique ID of the intersection, first part of the topic.
        :param groups: List of groups in this intersection.
        :param pattern:
        """

        self.id: str = id
        self.groups: List[Group] = groups
        self.pattern: List[List[Group]] = pattern

        # Dependency injection.
        for group in groups:
            group.intersection = self

        # Publish callback.
        self.on_publish: Callable[[str, any], Awaitable[None]] = None

    def parse_topic(self, topic: str) -> None:
        component = self.get_component_from_topic(topic)

        if not component:
            return

        if not isinstance(component, Sensor):
            return

        component.state = SensorState.HIGH

    async def init(self):
        for group in self.groups:
            for light in group.lights:
                light.state = LightState.STOP
                await self.on_publish(light.topic, light.state.value)

    async def iterate_patterns(self):
        for pattern in self.pattern:
            await self.handle_pattern_part(pattern)

    async def handle_pattern_part(self, pattern: List[Group]):
        should_go = False

        for group in pattern:
            if group.one_sensor_high():
                should_go = True

        if not should_go:
            return

        for group in pattern:
            for light in group.lights:
                light.state = LightState.GO
                self.on_publish(light.topic, light.state.value)

        await asyncio.sleep(10)

        for group in pattern:
            for light in group.lights:
                light.state = LightState.WAIT
                self.on_publish(light.topic, light.state.value)

        await asyncio.sleep(2)

        for group in pattern:
            group.set_all_sensors(SensorState.LOW)

            for light in group.lights:
                light.state = LightState.STOP
                self.on_publish(light.topic, light.state.value)

    def get_component_from_topic(self, topic: str):
        topic_parts = topic.split('/')

        group = self.get_group_from_topic(topic)

        if not group:
            return None

        type_components = []

        for component in group.components:
            if component.type.value == topic_parts[3]:
                type_components.append(component)

        id_components = []

        if topic_parts[4]:
            for component in type_components:
                if component.id == int(topic_parts[4]):
                    id_components.append(component)

        if len(id_components) != 1:
            return None

        return id_components[0]

    def get_group_from_topic(self, topic: str):
        topic_parts = topic.split('/')

        type_groups = []

        for group in self.groups:
            if group.type.value == topic_parts[1]:
                type_groups.append(group)

        id_groups = []

        for group in type_groups:
            if group.id == int(topic_parts[2]):
                id_groups.append(group)

        if len(id_groups) != 1:
            return None

        return id_groups[0]

    @property
    def sensor_topics(self):
        """
        Loops over all groups, and its sensors, returns their topics.

        :return: All sensor topics belonging to this intersection.
        """

        for group in self.groups:
            for sensor in group.sensors:
                yield sensor.topic

    @property
    def topic(self):
        """
        :return: Intersection topic prefix.
        """

        return self.id
