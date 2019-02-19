from .component import Component
from .sensor_state import SensorState


class Sensor(Component):
    def __init__(self, component_id=1):
        super().__init__(component_id)
        self.state = SensorState.LOW
