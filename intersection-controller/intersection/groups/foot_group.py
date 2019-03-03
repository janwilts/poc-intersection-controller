from intersection.groups.group import Group
from intersection.groups.group_type import GroupType


class FootGroup(Group):
    type = GroupType.FOOT
    go_time: int = 7
    transition_time: int = 2
