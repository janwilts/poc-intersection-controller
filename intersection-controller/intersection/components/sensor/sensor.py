import logging

from intersection.components.component import Component
from intersection.components.component_type import ComponentType
from intersection.components.sensor.sensor_state import SensorState


class Sensor(Component):
    """
    Sensor component class.
    """

    type = ComponentType.SENSOR

    def __init__(self, component_id: int = 1) -> None:
        """
        Sensor constructor.

        :param component_id: Sensor component id.
        """

        super().__init__(component_id)

        self._state = SensorState.LOW

    @property
    def state(self) -> SensorState:
        return self._state

    @state.setter
    def state(self, state: SensorState) -> None:
        if self._state == state:
            return

        self._state = state

        logging.debug(f'Set component {self.topic} to {state}')
