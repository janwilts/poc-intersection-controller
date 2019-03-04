from __future__ import annotations

from typing import List

from intersection.components.component import Component
from intersection.groups.group import Group
from intersection.intersection import Intersection
from topic_error import TopicError


class TopicParser:
    """
    Topic parser class, fills intersection, group and component from an input list of components and the topic to parse.
    """

    def __init__(self, intersections: List[Intersection], topic: str) -> None:
        """
        TopicParser constructor.

        :param intersections: All intersections that should be checked.
        :param topic: The topic to be parsed.
        """

        self.intersections: List[Intersection] = intersections
        self.topic: str = topic
        self.topic_parts: List[str] = self.topic.split('/')

        self.intersection: Intersection = None
        self.group: Group = None
        self.component: Component = None

        self.timescale: True = None

    def fill_all(self) -> TopicParser:
        """
        Fills all properties.

        :return: Instance for chaining.
        """

        if self.is_features:
            return self.fill_intersection().fill_feature()
        else:
            return self.fill_intersection().fill_group().fill_component()

    def fill_intersection(self) -> TopicParser:
        """
        Loops over all supplied intersections and checks if their ID matches with the topic intersection ID.

        :return: Instance for chaining.
        """

        if not self.intersections:
            raise TopicError('No intersections have been supplied')

        intersection = next(ints for ints in self.intersections if ints.id == self.topic_intersection_id)

        if not intersection:
            raise TopicError(f'Intersection with intersection id {self.topic_intersection_id} was not found in the '
                             'supplied intersections')

        self.intersection = intersection
        return self

    def fill_group(self) -> TopicParser:
        """
        Fills the group by checking all groups in intersection and comparing their ID and type.

        :return: Instance for chaining.
        """

        if not self.intersection:
            raise TopicError('Intersection has not yet been parsed')

        group = next(group for group in self.intersection.groups
                     if group.type.value == self.topic_group_type and group.id == int(self.topic_group_id))

        if not group:
            raise TopicError(f'Group with group id {self.topic_group_id} and type {self.topic_group_type} was not found'
                             f'on intersection with id {self.intersection.id}')

        self.group = group
        return self

    def fill_component(self) -> TopicParser:
        """
        Fills the component by checking all components in group and comparing their ID and type, if no ID is supplied 1
        is used as ID.

        :return: Instance for chaining.
        """

        if not self.group:
            raise TopicError('Group has not yet been parsed')

        component_id: int = 1

        if self.topic_component_id:
            component_id = int(self.topic_component_id)

        component = next(cmpt for cmpt in self.group.components
                         if cmpt.type.value == self.topic_component_type and cmpt.id == component_id)

        if not component:
            raise TopicError(f'Component with component id {component_id} and type {self.topic_component_type} was not'
                             f'found on group with id {self.group.id}')

        self.component = component
        return self

    def fill_feature(self) -> TopicParser:
        if not self.topic_features:
            raise TopicError('Topic is not a features topic.')

        if not self.topic_feature:
            raise TopicError('No feature has been defined')

        if self.topic_feature == 'timescale':
            self.timescale = True

        return self

    @property
    def is_features(self) -> bool:
        """
        When the incoming topic is a features topic, return true
        """

        return self.topic_features == 'features'

    # Topic part alias getters.

    @property
    def topic_intersection_id(self) -> str:
        return self.topic_parts[0]

    @property
    def topic_group_type(self) -> str:
        return self.topic_parts[1]

    @property
    def topic_group_id(self) -> str:
        return self.topic_parts[2]

    @property
    def topic_component_type(self) -> str:
        return self.topic_parts[3]

    @property
    def topic_component_id(self) -> str:
        return self.topic_parts[4]

    @property
    def topic_features(self) -> str:
        return self.topic_parts[1]

    @property
    def topic_feature(self):
        return self.topic_parts[2]
