from typing import List

from intersection.components.component import Component
from intersection.components.light.light import Light
from intersection.components.light.light_state import LightState
from intersection.components.sensor.sensor import Sensor
from intersection.components.sensor.sensor_state import SensorState


class Group:
    type = None

    def __init__(self, id: int, components: List[Component] = None):
        self.id = id
        self.intersection = None

        if components:
            self.components = components
        else:
            self.components = [Light(), Sensor()]

        for component in self.components:
            component.group = self

    def set_all_lights(self, state: LightState):
        for light in self.lights:
            prev_state = light.state

            light.state = state

            if prev_state != light.state:
                yield light.topic, light.state

    def set_all_sensors(self, state: SensorState):
        for sensor in self.sensors:
            prev_state = sensor.state
            sensor.state = state

            if prev_state != sensor.state:
                yield sensor.topic, sensor.state

    def one_sensor_high(self):
        for sensor in self.sensors:
            if sensor.state == SensorState.HIGH:
                return True

        return False

    @property
    def lights(self):
        return [component for component in self.components if isinstance(component, Light)]

    @property
    def sensors(self):
        return [component for component in self.components if isinstance(component, Sensor)]

    @property
    def topic(self):
        return f'{self.intersection.topic}/{self.type.value}/{self.id}'
