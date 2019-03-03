import logging

from intersection.components.component_state import ComponentState


class Component:
    """
    Component base class.
    """

    type = None

    def __init__(self, id: int = 1) -> None:
        self.id: int = id

        self.group = None
        self._state: ComponentState = None

    @property
    def topic(self) -> str:
        base_topic = f'{self.group.topic}/{self.type.value}'

        if self.id:
            return f'{base_topic}/{self.id}'

        return base_topic
