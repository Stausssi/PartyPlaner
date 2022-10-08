from tkinter import *
from PIL import Image, ImageTk
from datenhaltung.data_classes import Position
fieldWidth = 25
fieldHeight = 25


class Darstellung(Frame):
    def __init__(self, data, window):
        super().__init__(window)
        self.data = data 
        self.window = window
        # self.window.geometry(str(self.room_dimension[0]) + "x" + str(self.room_dimension[1]))
        
        
        # Open the image and resize it
        img = Image.open("Darstellung/table.png")
        img.thumbnail((fieldWidth, fieldHeight))
        tableImage = ImageTk.PhotoImage(img, master=self.master)
         # Open the image and resize it
        img = Image.open("Darstellung/person.png")
        img.thumbnail((fieldWidth, fieldHeight))
        personImage = ImageTk.PhotoImage(img, master=self.master)

        self.images = {
            "table": tableImage,
            "person": personImage,
        }
        self.labels = {
            "table": [],
            "person": {}
        }
        self.createRoom()

    def createRoom(self):
        # Room is a rectangle, since it only has a width and height
        for x in range(self.data.room.size.x):
            self.rowconfigure(x)
        for y in range(self.data.room.size.y):
            self.columnconfigure(y)

        # Create the grid
        for x in range(self.data.room.size.x):
            for y in range(self.data.room.size.y):
                frame = Frame(
                    self,
                    width=fieldWidth, height=fieldHeight,
                    highlightbackground="black", highlightthickness=1)
                frame.grid(row=y, column=x)
        self.draw_table()
        self.pack()
        self.window.update()

    def draw(self):
        drawn_count = 0

        # Prüfen, ob alle Gäste gezeichnet wurden -> Fertig
        persons = self.data.room.persons
        while drawn_count < len(persons):
            # Position des Gastes überprüfen -> Fehlermeldung
            if not self.detect_collision(persons[drawn_count]):
                # Gast neu zeichnen
                self.draw_person(persons[drawn_count])
            else:
                print("Gast " + persons[drawn_count].name + " befindet sich an einer illegalen Position!")
            drawn_count += 1
        self.pack()
        self.window.update()

    def draw_table(self):
        # Table is a rectangle since it can only be constructed by a coord followed by width and height
        table = self.data.room.table
        position = table.position
        position_end = Position(table.size.x + position.x, table.size.y + position.y) 


        for label in self.labels["table"]:
            label.destroy()
        # print table elements
        for x in range(position.x, position_end.x):
            for y in range(position.y, position_end.y):
                label = self.draw_image(x, y, self.images["table"])
                self.labels["table"].append(label)

    def draw_person(self, person):
        x, y = person.position
        if label := self.labels["person"].get(person.id, None):
            self.update_image(x,y, label)
        else:
            label = self.draw_image(x, y, self.images["person"])
            self.labels["person"][person.id] = label

    def draw_image(self, x, y, img) -> Label:
        # - 4 in width and height because of the border
        label = Label(self, width=fieldWidth - 4, height=fieldHeight - 4, image=img)
        label.image = img
        label.grid(row=y, column=x)
        return label

    def update_image(self, x, y, label):
        label.grid(row=y, column=x)

    def detect_collision(self, person) -> bool:
        table = self.data.room.table
        collides_with_table_x = table.position.x <= person.position.x and person.position.x < table.position.x + table.size.x
        collides_with_table_y = table.position.y <= person.position.y and person.position.y < table.position.y + table.size.y
        return collides_with_table_x and collides_with_table_y


if __name__ == "__main__":
    Darstellung()
