from enum import Enum


class ComponentType(Enum):
    """
    Component types, used in generating topics.
    """

    LIGHT = 'light'
    SENSOR = 'sensor'
