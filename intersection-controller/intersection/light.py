from .component import Component
from .light_state import LightState


class Light(Component):
    def __init__(self, component_id=1):
        super().__init__(component_id)
        self.state = LightState.STOP
