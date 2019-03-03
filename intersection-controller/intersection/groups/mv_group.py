from intersection.groups.group import Group
from intersection.groups.group_type import GroupType


class MotorVehicleGroup(Group):
    type = GroupType.MOTOR_VEHICLE
    go_time: int = 2
    transition_time: int = 2

