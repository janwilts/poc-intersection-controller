from intersection.groups.group import Group
from intersection.groups.group_type import GroupType


class VesselGroup(Group):
    type = GroupType.VESSEL
    go_time: int = 60
    transition_time: int = 20
