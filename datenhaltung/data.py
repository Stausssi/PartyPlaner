import json
import jsonschema
from .data_classes import *

class Data:
    def __init__(self, room=None, configuration=None, json_path=None):
        self.room = room
        self.configuration = configuration
        self.statistics = None

        if self.configuration is None:
            self.configuration = Configuration(0,0)
        
        if self.room is None:
            self.room = Room(size=(0,0), table=Table(size=(0,0), position=(0,0)))
            
        if json_path is not None:
            self.load(json_path)     

    def load(self, path):
        with open("datenhaltung/jsonschema.json") as f:
            schema = json.load(f)

        with open(path) as f:
            try:
                data = json.load(f)
                jsonschema.validate(data, schema)

            except jsonschema.exceptions.ValidationError as e:
                print("well-formed but invalid JSON:", e)
            except json.decoder.JSONDecodeError as e:
                print("poorly-formed text, not JSON:", e)

            room = data["room"]
            room_size = (room["size"][0], room["size"][1]) # needs to be a tuple
            new_room = Room(size=room_size)

            table = room["table"]
            table_size = (table["size"][0], table["size"][1]) # needs to be a tuple
            table_position = (table["position"][0], table["position"][1]) # needs to be a tuple
            new_table = Table(size=table_size, position=table_position)

            new_room.table = new_table

            persons = room["persons"]

            for person in persons:
                person_id = person["id"]
                name = person["name"]
                job = person["job"]
                desired_distances = person["desired_distances"]
                desired_distances = {int(k):v for k,v in desired_distances.items()}
                position = (person["position"][0], person["position"][1]) # needs to be a tuple
                happiness = person["happiness"]
                new_room.persons.append(Person(name, job, person_id, desired_distances, position, happiness))

            self.room = new_room

    def save(self, path):
        print('data: ', self.room)
        data = {
            'room': self.room.room_to_dict()
            # 'configuration': self.configuration,
            # 'statistics': self.statistics
        }

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
