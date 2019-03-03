from intersection.groups.group import Group
from intersection.groups.group_type import GroupType


class CycleGroup(Group):
    type = GroupType.CYCLE
    go_time: int = 3
    transition_time: int = 2
