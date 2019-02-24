from intersection.components.component import Component
from intersection.components.component_type import ComponentType
from intersection.components.light.light_state import LightState


class Light(Component):
    type = ComponentType.LIGHT

    def __init__(self, component_id=1):
        super().__init__(component_id)
        self.state = LightState.STOP
