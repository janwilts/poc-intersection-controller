import logging

from intersection.components.component import Component
from intersection.components.component_type import ComponentType
from intersection.components.light.light_state import LightState


class Light(Component):
    """
    Light component class.
    """

    type = ComponentType.LIGHT

    def __init__(self, component_id: int = 1) -> None:
        """
        Light constructor.

        :param component_id: Light component id.
        """

        super().__init__(component_id)

        self._state = LightState.STOP

    @property
    def state(self) -> LightState:
        return self._state

    @state.setter
    def state(self, state: LightState):
        self._state = state

        logging.debug(f'Set component {self.topic} to {state}')

