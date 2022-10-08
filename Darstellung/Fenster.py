from tkinter import *

from Darstellung.Darstellung import Darstellung


class Fenster:
    def __init__(self, data, management, height, width, bg_color, title):
        self.title = title
        self.management = management
        self.height = height
        self.width = width
        self.bg_color = bg_color
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.on_quit)
        # self.window.geometry(str(width) + "x" + str(height))
        self.buttons = ["Stopp", "Play", "Pause", "Iteration", "Gast"]
        self.darstellung = Darstellung(data, window=self.window)

        self.is_running = True
        # buttons
        self.button_stop = Button(self.window, text="Stopp", command=self.on_stop)
        self.button_stop.pack()
        self.button_play = Button(self.window, text="Play", command=self.on_play)
        self.button_play.pack()
        self.button_pause = Button(self.window, text="Pause", command=self.on_pause)
        self.button_pause.pack()
        self.button_iteration = Button(self.window, text="Iteration", command=self.on_next_iteration)
        self.button_iteration.pack()
        self.button_guest = Button(self.window, text="Gast", command=self.on_next_guest)
        self.button_guest.pack()
        

    def draw(self):
        self.darstellung.draw()
        self.window.update()

    def on_stop(self):
        self.management.stop()

    def on_pause(self):
        self.management.pause()

    def on_play(self):
        self.management.play()

    def on_next_iteration(self):
        self.management.next_iteration()

    #TODO
    def on_next_guest(self):
        pass

    def on_quit(self):
        self.is_running = False
        


