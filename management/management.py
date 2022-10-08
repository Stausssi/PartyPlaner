import sys
import threading
from time import sleep
import time
from satisfaction.calculations import Satisfaction
from datenhaltung.data import Data
from datetime import datetime

class Management:
    def __init__(self, data):
        self.data = data
        self.satisfaction = Satisfaction(data)
        self.is_running = False
        self.is_paused = False
        self.is_single_iteration_step = False
        self.do_single_guest_step = False
        self.iteration = 0
        self.moves_on_last_iteration = 0

    def start(self):
        if self.is_running:
            raise RuntimeError("Game thread already running!")

        t = threading.Thread(target=self.__start_game_logic)
        t.start()

    def __start_game_logic(self):
        self.is_running = True
        i = 0
        while self.is_running and i < self.data.configuration.iterationcount:
            
            if not self.is_paused:
                timestamp_before = datetime.now()
                for guest in self.data.room.persons:

                    # wenn single gast modus und nciht nächsteer knopf gedrückt, dann warte
                    while self.is_paused:
                        if self.do_single_guest_step:
                            self.do_single_guest_step = False
                            break
                        else:
                            sleep(0.01)

                    new_x ,new_y = guest.position 
                    least_discomfort = sys.maxsize
                    for a in range(-1, 2):
                        for b in range(-1, 2):
                            if a == 0 and b == 0:
                                continue
                            x = guest.position.x + a
                            y = guest.position.y + b

                            # is in field and not in table
                            if self.is_valid_field(x, y):
                                result = self.satisfaction.get_happiest_move(guest, x, y)

                                if result < least_discomfort:
                                    new_x = x
                                    new_y = y
                                    least_discomfort = result

                    guest.position = (new_x, new_y)
                    guest.happiness = least_discomfort

                if not self.is_single_iteration_step:
                    time_elapsed = (datetime.now() - timestamp_before).microseconds / 1000000
                    time.sleep(self.data.configuration.delay - time_elapsed)
                    # Refresh visualization
                    # Refresh statistic module

                # Increase iteration counter
                i += 1
                if self.is_single_iteration_step:
                   self.is_paused = True
            else:
                time.sleep(0.01)

            
            
    def move_persons(self):
        if self.iteration > self.data.configuration.iterationcount:
            return
        if self.iteration > 0 and self.moves_on_last_iteration == 0:
            return
        self.moves_on_last_iteration = 0
        for guest in self.data.room.persons:
            # wenn single gast modus und nciht nächsteer knopf gedrückt, dann warte
            while self.is_paused:
                if self.do_single_guest_step:
                    self.do_single_guest_step = False
                    break
                else:
                    sleep(0.01)

            new_position = guest.position 
            least_discomfort = sys.maxsize
            for a in range(-1, 1):
                
                for b in range(-1, 1):
                    if a == 0 and b == 0:
                        continue
                    x = guest.position.x + a
                    y = guest.position.y + b

                    # is in field and not in table
                    if self.is_valid_field(x, y):
                        result = self.satisfaction.get_happiest_move(guest, x, y)

                        if result < least_discomfort:
                            new_position = (x,y)

                            least_discomfort = result
                            
            if not new_position == guest.position:
                guest.position = new_position
                self.moves_on_last_iteration += 1
        
            guest.happiness = least_discomfort
        self.iteration += 1

    def is_valid_field(self, x, y):
        if not self.__is_field_inside_room(x, y):
            return False

        if self.__is_in_table(x, y, self.data.room.table):
            return False

        if self.__is_field_already_occupied(x, y):
            return False

        return True

    def __is_field_already_occupied(self, x, y):
        for guest in self.data.room.persons:
            if guest.position == (x, y):
                return True
        return False

    def __is_field_inside_room(self, x, y):
        return 0 <= x < self.data.room.size.x and 0 <= y < self.data.room.size.y

    @staticmethod
    def __is_in_table(x, y, table):
        collides_with_table_x = table.position.x <= x and x < table.position.x + table.size.x
        collides_with_table_y = table.position.y <= y and y < table.position.y + table.size.y
        return collides_with_table_x and collides_with_table_y

    def pause(self):
        self.is_paused = True 
        self.is_single_iteration_step = True 

    def play(self):
        self.is_paused = False
        self.is_single_iteration_step = False

    def stop(self):
        self.is_running = False

    def next_iteration(self):
        if not self.is_single_iteration_step:
            return
        self.is_paused = False

    def next_guest_iteration(self):
        self.do_single_guest_step = True
