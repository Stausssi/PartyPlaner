from typing import overload
from .exceptions import BadPositionError, PersonAlreadyPresentError, PositionOutOfBoundsError, RoomResizeError
from collections import namedtuple


class Position(namedtuple("Position", ["x", "y"], defaults=(0,) * 2)):
    pass


class Size(namedtuple("Size", ["x", "y"], defaults=(0,) * 2)):
    pass


class Validateable:
    """Interface for validation checking

        this interface implements the method validate(), 
        which will be called by children to inform the parent that a value in one of its properties changed, so it can revalidate.
    """
    _parent = None

    def validate(self, child, requested_changes):
        """Validates the current change meets the requirements

        - params
            child: instance of the caller of this method

        by passing the child parameter, the parent should be able to minimize the validation checking, which should increase the performance
        """
        pass

    def parent_validate(self, child, requested_changes):
        if not self._parent:
            return
        self._parent.validate(child, requested_changes)


class PositionPropertyInterface(Validateable):
    """Interface for reusing position property

        this interface contains the property "position", which will always be:
        - type tuple
        - exactly len 2
        - contains only positive ints
    """
    _position = Position(0, 0)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: tuple):
        validation.validate_position_structure(position)
        x, y = position
        changes = {
            "position": Position(x, y)
        }
        self.parent_validate(self, changes)
        self._position = Position(x, y)


class SizePropertyInterface(Validateable):
    """Interface for reusing size property

        this interface contains the property "size", which will always be:
        - type tuple
        - exactly len 2
        - contains only positive ints

    """
    _size = Size(0, 0)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: tuple):
        validation.validate_size_structure(size)
        x, y = size
        changes = {
            "size": Size(x, y)
        }
        self.parent_validate(self, changes)
        self._size = Size(x, y)


class Person(PositionPropertyInterface):

    def __init__(self, name, job, person_id=None, desired_distances={}, position=(0, 0), happiness=0, parent=None):
        if person_id is None:
            person_id = id(self)
        self._id = person_id
        self.name = name
        self.job = job
        self.desired_distances = desired_distances
        self.position = position
        self.happiness = happiness
        self._parent = parent

    def __str__(self):
        return f"Person({self.name} [{self.job}] at {self.position})"

    def add_desired_distance_for_person(self, distance, person):
        self.desired_distances[person.id] = distance

    def person_to_dict(self):
        return {"id": self._id, "name": self.name, "job": self.job, "desired_distances": self.desired_distances, "position": self.position, "happiness": self.happiness}

    @property
    def id(self):
        return self._id


class PersonList(list, Validateable):
    """Validated list for Persons

        A list, with some additional validation when changing / setting items

        Example: 
            This list will raise an Exception when somebody tries to append a person with 
            a position which is already taken by another person in this list
    """

    def __init__(self, parent=None):
        self._parent = parent
        super().__init__()

    def append(self, person):
        validation.validate_person_added_to_list(self, person)
        person._parent = self
        self.parent_validate(person, {})  # no changes, just adding person
        super().append(person)

    def __setitem__(self, index, person):
        validation.validate_person_replace_in_list(self, self[index], person)
        changes = {"current": self[index], "new": person}
        self.parent_validate(self, changes)
        person._parent = self
        super().__setitem__(index, person)

    def validate(self, child, changes):
        if child not in self:
            return
        validation.validate_person_changed_in_list(self, child, changes)
        self.parent_validate(child, changes)

    def persons_to_array(self):
        persons = []
        for person in self:
            persons.append(person.person_to_dict())
        return persons


class Table(PositionPropertyInterface, SizePropertyInterface):
    """Table

        fields:
        - size: Size (namedtuple)
        - position: Position (namedtuple)
    """

    def __init__(self, size, position, parent=None):
        self.size = size
        self.position = position
        self._parent = parent

    def table_to_dict(self):
        return {
            "size": self.size,
            "position": self.position
        }

    def __str__(self) -> str:
        return f"Table({self.size} at {self.position})"


class Room(SizePropertyInterface):
    """Room
        fields:
        - size: Size (namedtuple)
        - table: Table
        - persons: PersonList
    """
    _persons: PersonList
    _table: Table

    def __init__(self, size, table: Table = None, persons: list = []):
        self.size = size
        self._parent = self
        self._persons = PersonList(self)
        if not table:
            self.table = Table(size=(0,0), position=(0,0), parent=self)
        else:
            self.table = table
        self.persons = persons

    @property
    def persons(self):
        return self._persons

    @persons.setter
    def persons(self, persons: list):
        self._persons.clear()
        for person in persons:
            self._persons.append(person)

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, table):
        validation.validate_table_changed_in_room(self, table, {})
        self._table = table
        self._table._parent = self

    def validate(self, child, changes):
        child_type = type(child)
        if child_type == Person:
            validation.validate_person_changed_in_room(self, child, changes)
        elif child_type == Table:
            validation.validate_table_changed_in_room(self, child, changes)
        elif child_type == PersonList:
            validation.validate_person_replaced_in_room(self, child, changes)
        elif child_type == Room:
            validation.validate_room_size_change(self, changes)

    def room_to_dict(self):
        print(self.persons)
        return {
            "size": self.size,
            "table": self.table.table_to_dict(),
            "persons": self.persons.persons_to_array()
        }


class Configuration:
    def __init__(self, iterationcount, delay):
        self.iterationcount = iterationcount
        self.delay = delay

    def configuration_to_dict(self):
        return {
            "iterationcount": self.iterationcount,
            "delay": self.delay
        }


class Statistic:
    def __init__(self):
        self.persons = {}

class Simulation:
    def __init__(self, configuration):
        self.configuration = configuration
        self.iterations= []

    def simulation_to_dict(self):
        return {
            "configuration": self.configuration,
            "room": self.iterations
        }
       


############################## Validation ################################################


class validation:

    @staticmethod
    def validate_position_structure(position: tuple):
        if type(position) != tuple:
            raise TypeError(
                f"Expected position to be tuple, got {type(position)}")
        if len(position) != 2:
            raise TypeError(
                f"Expected position to be len 2, got len {len(position)}")
        for coordinate in position:
            if type(coordinate) != int:
                raise TypeError(
                    f"Expected position to contain values of type int, got ({type(position[0])}, {type(position[1])})")
            if coordinate < 0:
                raise ValueError(
                    f"Expected position to contain only positive values, got {str(position)}")

    @staticmethod
    def validate_size_structure(size: tuple):
        if type(size) != tuple:
            raise TypeError(f"Expected size to be tuple, got {type(size)}")
        if len(size) != 2:
            raise TypeError(f"Expected size to be len 2, got len {len(size)}")
        for coordinate in size:
            if type(coordinate) != int:
                raise TypeError(
                    f"Expected size to contain values of type int, got ({type(size[0])}, {type(size[1])})")
            if coordinate < 0:
                raise ValueError(
                    f"Expected size to contain only positive values, got {str(size)}")

    @staticmethod
    def validate_person_added_to_list(prev_list, person):
        if type(person) != Person:
            raise TypeError(
                f"Expected person to be {Person}, got {type(person)}")
        for list_person in prev_list:
            if list_person is person:
                raise PersonAlreadyPresentError(prev_list, person)
            if list_person.position == person.position:
                raise BadPositionError(list_person, person, person.position)

    @staticmethod
    def validate_person_changed_in_list(prev_list, person, changes):
        if type(person) != Person:
            raise TypeError(
                f"Expected person to be {Person}, got {type(person)}")
        for list_person in prev_list:
            if list_person is person:
                continue
            if list_person.position == changes["position"]:
                raise BadPositionError(list_person, person, person.position)

    @staticmethod
    def validate_person_replace_in_list(prev_list, current, new):
        if type(new) != Person:
            raise TypeError(f"Expected person to be {Person}, got {type(new)}")
        for list_person in prev_list:
            if list_person is current:
                continue
            if list_person is new:
                raise PersonAlreadyPresentError(prev_list, new)
            if list_person.position == new.position:
                raise BadPositionError(list_person, new, new.position)

    @staticmethod
    def validate_person_changed_in_room(room, person, changes):
        new_position = changes.get("position", person.position)
        if room.size.x <= new_position.x or room.size.y <= new_position.y:
            raise PositionOutOfBoundsError(room, person, new_position)
        if table := room.table:
            collides_with_table_x = table.position.x <= new_position.x and new_position.x < table.position.x + table.size.x
            collides_with_table_y = table.position.y <= new_position.y and new_position.y < table.position.y + table.size.y
            if collides_with_table_x and collides_with_table_y:
                raise BadPositionError(table, person, new_position)

    @staticmethod
    def validate_person_replaced_in_room(room, prev_list, changes):
        new_person = changes["new"]
        if room.size.x <= new_person.position.x or room.size.y <= new_person.position.y:
            raise PositionOutOfBoundsError(
                room, new_person, new_person.position)
        if table := room.table:
            collides_with_table_x = table.position.x <= new_person.position.x and new_person.position.x < table.position.x + table.size.x
            collides_with_table_y = table.position.y <= new_person.position.y and new_person.position.y < table.position.y + table.size.y
            if collides_with_table_x and collides_with_table_y:
                raise BadPositionError(table, new_person, new_person.position)

    @staticmethod
    def validate_table_changed_in_room(room, table, changes):
        size, position = changes.get("size", table.size), changes.get(
            "position", table.position)
        table_outside_room_x = position.x + size.x > room.size.x
        table_outside_room_y = position.y + size.y > room.size.y
        if table_outside_room_x or table_outside_room_y:
            raise PositionOutOfBoundsError(room, table, position)
        for person in room.persons:
            collides_with_table_x = position.x <= person.position.x and person.position.x < position.x + size.x
            collides_with_table_y = position.y <= person.position.y and person.position.y < position.y + size.y
            if collides_with_table_x and collides_with_table_y:
                raise BadPositionError(table, person, person.position)

    @staticmethod
    def validate_room_size_change(room, changes):
        size = changes.get("size", room.size)
        table_outside_room_x = room.table.position.x + room.table.size.x > size.x
        table_outside_room_y = room.table.position.y + room.table.size.y > size.y
        if table_outside_room_x or table_outside_room_y:
            raise RoomResizeError(room, room.table, size)
        for person in room.persons:
            person_outside_x = person.position.x >= size.x
            person_outside_y = person.position.y >= size.y
            if person_outside_x or person_outside_y:
                raise RoomResizeError(room, person, size)
