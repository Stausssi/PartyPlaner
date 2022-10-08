from math import sqrt
import random

class Satisfaction:
    def __init__(self, data):
        self.data = data

    def get_happiest_move(self, p, x, y):
        discomfort = 0
        # return random.randint(0,10)
        for person in self.data.room.persons:
            distance = sqrt((x - person.position.x)**2 + (y - person.position.y)**2)
            difference = abs(distance - p.desired_distances[person.id])
            discomfort += difference
        return discomfort
