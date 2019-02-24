from intersection.components.component import Component
from intersection.components.sensor.sensor_state import SensorState


class Sensor(Component):
    def __init__(self, component_id=1):
        super().__init__(component_id)
        self.state = SensorState.LOW
