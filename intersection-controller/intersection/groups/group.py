from typing import List
from intersection.components.light.light import Light
from intersection.components.light.light_state import LightState
from intersection.components.sensor.sensor import Sensor
from intersection.components.sensor.sensor_state import SensorState


class Group:
    group_type = None

    def __init__(self, group_id: int, lights: List[Light] = None, sensors: List[Sensor] = None):
        self.group_id = group_id

        self.lights = []
        self.sensors = []

        if lights:
            self.lights = lights
        else:
            self.lights = [Light()]

        if sensors:
            self.sensors = sensors
        else:
            self.sensors = [Sensor()]

    def set_all_lights(self, state: LightState):
        for light in self.lights:
            light.state = state

    def set_all_sensors(self, state: SensorState):
        for sensor in self.sensors:
            sensor.state = state

    def one_sensor_high(self):
        for sensor in self.sensors:
            if sensor.state == SensorState.HIGH:
                return True

        return False
