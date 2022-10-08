import unittest
from . import data_classes as dc
from . import exceptions as e


class DataStructureTests(unittest.TestCase):
    
    def test_table_position_conversion(self):
        table = dc.Table((5,4), (2,2))
        self.assertIsInstance(table.position, dc.Position)

    def test_person_list(self):
        person1 = dc.Person("Hans", "professor", (4,5))
        person2 = dc.Person("Peter", "student", (4,5))
        self.assertTupleEqual(person2.position, (4,5))
        persons = dc.PersonList()
        persons.append(person1)
        self.assertIn(person1, persons)
        def add_person_2():
            persons.append(person2)
        self.assertRaises(e.BadPositionError, add_person_2)
        person2.position = (4,6)
        persons.append(person2)
        def overwrite_bad_person():
            persons[1] = dc.Person("Fred", "arbeitslos", (4,5))
        self.assertRaises(e.BadPositionError, overwrite_bad_person)
        def move_person_bad():
            persons[1].position = (4,5)
        self.assertRaises(e.BadPositionError, move_person_bad)
    
        def add_person_twice():
            person3 = dc.Person("Gunther", "Bauarbeier", (3,2))
            persons.append(person3)
            persons.append(person3)
        add_person_twice()
        
    
    # - - room - -
     
    #+-0-1-2-3-4-#
    #0 p p p p p #
    #1   t t t   #
    #2   t t t   #
    #3           #
    #4         p #
    #+-----------#
    def test_room(self):
        #init
        table = dc.Table((3,2), (1,1))
        room = dc.Room((5,5), table=table)
        for i in range(5):
            room.persons.append(dc.Person(f"Hannes {i}", "testarbeiter", position=(i,0)))
        room.persons.append(dc.Person("Gustav", "aldi", position=(4,4)))

        #persons move
        prev_position = room.persons[3].position
        def walk_into_person():
            room.persons[3].position = (1,0)
        self.assertRaises(e.BadPositionError, walk_into_person)
        self.assertTupleEqual(room.persons[3].position, prev_position) 
        def walk_into_table():
            room.persons[3].position = (3,2)
        self.assertRaises(e.BadPositionError, walk_into_table)
        self.assertTupleEqual(room.persons[3].position, prev_position) 
        def walk_out_of_room():
            room.persons[3].position = (10,3)
        self.assertRaises(e.PositionOutOfBoundsError, walk_out_of_room)
        self.assertTupleEqual(room.persons[3].position, prev_position)
        
        #person replaced
        prev_person = room.persons[3]
        def replace_person_into_person():
            room.persons[3] = dc.Person("Peter", "fauler Sack", position=(1,0))
        self.assertRaises(e.BadPositionError, replace_person_into_person)
        self.assertIs(room.persons[3], prev_person)
        def replace_person_into_table():
            room.persons[3] = dc.Person("Peter", "fauler Sack", position=(2,2))
        self.assertRaises(e.BadPositionError, replace_person_into_table)
        self.assertIs(room.persons[3], prev_person)
        def replace_person_out_of_room():
            room.persons[3] = dc.Person("Peter", "fauler Sack", position=(20,2))
        self.assertRaises(e.PositionOutOfBoundsError, replace_person_out_of_room)
        self.assertIs(room.persons[3], prev_person)

        #table moves
        prev_position = room.table.position
        def move_table_into_persons():
            room.table.position = (1,0)
        self.assertRaises(e.BadPositionError, move_table_into_persons)
        self.assertTupleEqual(prev_position, room.table.position)
        def move_table_into_wall():
            room.table.position = (4,2)
        self.assertRaises(e.PositionOutOfBoundsError, move_table_into_wall)
        self.assertTupleEqual(prev_position, room.table.position)
        #table changes size
        prev_size = room.table.size
        def resize_table_into_persons():
            room.table.size = (4,4)
        self.assertRaises(e.BadPositionError, resize_table_into_persons)
        self.assertTupleEqual(prev_size, room.table.size)
        def resize_table_into_wall():
            room.table.size = (3,5)
        self.assertRaises(e.PositionOutOfBoundsError, resize_table_into_wall)
        self.assertTupleEqual(prev_size, room.table.size)
        #table replaced
        prev_table = room.table
        def replace_table_into_person():
            room.table = dc.Table((1,1), (0,0))
        self.assertRaises(e.BadPositionError, replace_table_into_person)
        self.assertIs(room.table, prev_table)
        def replace_table_into_wall():
            room.table = dc.Table((3,1), (3,2))
        self.assertRaises(e.PositionOutOfBoundsError, replace_table_into_wall)
        self.assertIs(room.table, prev_table)

        #room changes size
        prev_size = room.size
        def change_room_collide_person():
            room.size = (5,3)
        self.assertRaises(e.RoomResizeError, change_room_collide_person)
        self.assertTupleEqual(prev_size, room.size)
        def change_room_collide_table():
            room.persons.pop()
            room.size = (5,2)
        self.assertRaises(e.RoomResizeError, change_room_collide_table)
        self.assertTupleEqual(prev_size, room.size)
        
    
    def test_person_position(self):
        person = dc.Person("Hans", "professor")
        # test setter with negative value
        def set_position_neg():
            person.position = (0,-1)
        self.assertRaises(ValueError, set_position_neg)
        # test invalid tuple dimension
        def set_invalid_tuple_big():
            person.position = (3,4,7)
        self.assertRaises(TypeError, set_invalid_tuple_big)
        def set_invalid_tuple_small():
            person.position = (1)
        self.assertRaises(TypeError, set_invalid_tuple_small)
        # test invalid types
        def set_invalid_type():
            person.position = 5
        self.assertRaises(TypeError, set_invalid_type)
        def set_invalid_tuple_value_type():
            person.position = (3, 5.6) 
        self.assertRaises(TypeError, set_invalid_tuple_value_type)



    def test_person_list(self):
        persons = dc.PersonList() 
        self.assertListEqual(persons, [])
        
        person = dc.Person("Hans", "professor")
        persons.append(person)
        self.assertIn(person, persons)

        persons.pop()
        self.assertListEqual(persons, [])



