from intersection.groups.group import Group
from intersection.groups.group_type import GroupType


class PublicServiceVehicleGroup(Group):
    type = GroupType.PUBLIC_SERVICE_VEHICLE
    go_time: int = 2
    transition_time: int = 2
