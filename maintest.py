from datenhaltung import data_classes as dc
from datenhaltung import exceptions as e
from datenhaltung import data

if __name__ == "__main__":
    person1 = dc.Person("Hans", "professor", 0, (4,5))
    person1.position = (4,6)
    person2 = dc.Person("Peter", "student", 0, (4,5))
    persons = dc.PersonList()
    table = dc.Table((5,4), (2,2))
    persons.append(person1)
    persons.append(person2)
    room = dc.Room((10,10), table=table, persons=persons)
    daten = data.Data(room)
    daten.save(path="test.json")
    print(data)
    person2.position = (4,6)
    persons.append(person2)
    persons[1] = dc.Person("Fred", "arbeitslos", 0, (4,5))
    persons[1].position = (4,8)
    
