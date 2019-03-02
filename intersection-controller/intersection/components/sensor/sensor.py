from intersection.components.component import Component
from intersection.components.component_type import ComponentType
from intersection.components.sensor.sensor_state import SensorState


class Sensor(Component):
    type = ComponentType.SENSOR

    def __init__(self, component_id=1):
        super().__init__(component_id)
        self._state = SensorState.LOW
