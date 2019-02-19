from .component_type import ComponentType
from .light import Light
from .sensor import Sensor


class Group:

    def __init__(self, group_id: int, components: any = None):
        self.group_id = group_id

        self.lights = []
        self.sensors = []

        if components:
            for component_type, component_ids in components.values():
                for component_id in component_ids:
                    if component_type == ComponentType.LIGHT:
                        self.lights.append(Light(component_id))
                    elif component_type == ComponentType.SENSOR:
                        self.sensors.append(Sensor(component_id))

        else:
            self.lights = [Light()]
            self.sensors = [Sensor()]

