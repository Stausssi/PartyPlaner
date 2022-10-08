from Darstellung.Fenster import Fenster
from tkinter import Tk
from datenhaltung import data as d
from datenhaltung.data_classes import Person, Room, Table
from management import management as m
from Darstellung.Darstellung import Darstellung
import time
from datetime import datetime


def generate_test_json():
    mul = 2
    p1 = Person("Brigitte", "Börsenmaklerin", person_id=1, desired_distances={1: 0*mul,
                                                                              2: 1.2*mul,
                                                                              3: 2.4*mul,
                                                                              4: 0.6*mul,
                                                                              5: 3.6*mul,
                                                                              6: 1.5*mul,
                                                                              7: 3.6*mul,
                                                                              8: 1.2*mul}, position=(6*mul, 4*mul))
    p2 = Person("Cäsar", "Zahnarzt", person_id=2, desired_distances={1: 0.6*mul,
                                                                     2: 0*mul,
                                                                     3: 1.5*mul,
                                                                     4: 1.2*mul,
                                                                     5: 3.3*mul,
                                                                     6: 3.6*mul,
                                                                     7: 2.7*mul,
                                                                     8: 1.8*mul}, position=(8*mul, 3*mul))
    p3 = Person("Floar", "Fotomodell", person_id=3, desired_distances={1: 2.1*mul,
                                                                       2: 0.9*mul,
                                                                       3: 0*mul,
                                                                       4: 2.7*mul,
                                                                       5: 1.8*mul,
                                                                       6: 3*mul,
                                                                       7: 3.9*mul,
                                                                       8: 1.5*mul}, position=(8*mul, 2*mul))
    p4 = Person("Gero", "Geschäftsmann", person_id=4, desired_distances={1: 0.9*mul,
                                                                         2: 1.8*mul,
                                                                         3: 1.2*mul,
                                                                         4: 0*mul,
                                                                         5: 2.4*mul,
                                                                         6: 1.8*mul,
                                                                         7: 1.2*mul,
                                                                         8: 3*mul}, position=(6*mul, 3*mul))
    p5 = Person("Kuno", "Künstler", person_id=5, desired_distances={1: 2.7*mul,
                                                                    2: 2.1*mul,
                                                                    3: 0.6*mul,
                                                                    4: 4.5*mul,
                                                                    5: 0*mul,
                                                                    6: 1.8*mul,
                                                                    7: 1.2*mul,
                                                                    8: 3.6*mul}, position=(6*mul, 2*mul))
    p6 = Person("Penelope", "Prinzessin", person_id=6, desired_distances={1: 3.3*mul,
                                                                          2: 1.5*mul,
                                                                          3: 4.2*mul,
                                                                          4: 3*mul,
                                                                          5: 0.9*mul,
                                                                          6: 0*mul,
                                                                          7: 2.1*mul,
                                                                          8: 4.5*mul}, position=(4*mul, 7*mul))
    p7 = Person("Viola", "Geigerin", person_id=7, desired_distances={1: 3.9*mul,
                                                                     2: 4.2*mul,
                                                                     3: 3*mul,
                                                                     4: 2.4*mul,
                                                                     5: 2.1*mul,
                                                                     6: 1.2*mul,
                                                                     7: 0*mul,
                                                                     8: 0.9*mul}, position=(3*mul, 4*mul))
    p8 = Person("Willi", "Gewichtheber", person_id=8, desired_distances={1: 2.4*mul,
                                                                         2: 3.9*mul,
                                                                         3: 1.8*mul,
                                                                         4: 2.1*mul,
                                                                         5: 1.8*mul,
                                                                         6: 0.9*mul,
                                                                         7: 2.7*mul,
                                                                         8: 0*mul}, position=(3*mul, 6*mul))

    data = d.Data(room=Room((9*mul, 14*mul), persons=[
                  p1, p2, p3, p4, p5, p6, p7, p8], table=Table(size=(1*mul, 3*mul), position=(4*mul, 4*mul))))
    data.save("test.json")


if __name__ == "__main__":

    global exit_flag
    exit_flag = False

    generate_test_json()
    data = d.Data()
    data.load("test.json")
    data.configuration.delay = 1
    data.configuration.iterationcount = 150
    # ui
    management = m.Management(data)
    fenster = Fenster(data, management, 500, 250,
                      bg_color=(255, 0, 0), title="PartyPlaner")
    management.start()
    while fenster.is_running:
        timestamp_before = datetime.now()
        fenster.draw()
        time.sleep(0.01)
    fenster.window.destroy()
