from People.person import *
import tkinter

# Person Placement

# testPerson = Person()


class PersonGui:

    def __int__(self):
        print("I was also called")
        
    def createPerson(self):
        testPerson = Person()
        return testPerson

    def on_to_map(self,person, main_grid, standard_size, offset):
        print("on to the map was called")
        coordiantes = person.startingLoc()
        personX1 = (coordiantes[0] * standard_size) + offset - standard_size
        personY1 = (coordiantes[1] * standard_size) + offset - standard_size
        personX2 = personX1 + standard_size
        personY2 = personY1 + standard_size
        print(personX1)
        print(personY1)
        main_grid.create_oval(personX1, personY1, personX2, personY2, fill="red")
