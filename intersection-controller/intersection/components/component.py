import logging

from intersection.components.state import State


class Component:
    type = None

    def __init__(self, id=1):
        self.id = id
        self.group = None

        self._state: State = None

    @property
    def topic(self) -> str:
        base_topic = f'{self.group.topic}/{self.type.value}'

        if self.id:
            return f'{base_topic}/{self.id}'

        return base_topic

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, state: State) -> None:
        logging.debug(f'Set state on component {self.id} to {state.value}')

        self._state = state
