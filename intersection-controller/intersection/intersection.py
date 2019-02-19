from .groups.cycle_group import CycleGroup
from .groups.foot_group import FootGroup
from .groups.mv_group import MotorVehicleGroup
from .groups.psv_group import PublicServiceVehicleGroup
from .groups.vessel_group import VesselGroup
from .user_type import UserType


class Intersection:
    def __init__(self, group_ids):
        self.group_ids = group_ids
        self.groups = []

        for user_type, groups in self.group_ids.items():
            for group in groups:
                if isinstance(group, int):
                    self.groups.append(self.group_from_user_type(user_type, group))
                else:
                    self.groups.append(self.group_from_user_type(user_type, group.id, group.components))

    @staticmethod
    def group_from_user_type(user_type: UserType, group_id: int, components=None):
        if user_type == UserType.CYCLE:
            return CycleGroup(group_id, components)
        elif user_type == UserType.FOOT:
            return FootGroup(group_id, components)
        elif user_type == UserType.MOTOR_VEHICLE:
            return MotorVehicleGroup(group_id, components)
        elif user_type == UserType.PUBLIC_SERVICE_VEHICLE:
            return PublicServiceVehicleGroup(group_id, components)
        elif user_type == UserType.VESSEL:
            return VesselGroup(group_id, components)

    @property
    def light_topics(self):
        topics = []

        for group in self.groups:
            for light in group.lights:
                topics.append(f'intersection/{group.user_type.value}/{group.group_id}/light/{light.component_id}')

        return topics

    @property
    def sensor_topics(self):
        topics = []

        for group in self.groups:
            for sensor in group.sensors:
                topics.append(f'intersection/{group.user_type.value}/{group.group_id}/sensor/{sensor.component_id}')

        return topics

