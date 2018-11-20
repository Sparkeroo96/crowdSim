# #!/usr/bin/python
from tkinter import *
from Map.map_main import *



class GridGui:
    map_obj = None
    map = None
    frame = None

    def __init__(self):
        print("GUI for map")
    def set_map_obj(self, value):
        global map_obj
        map_obj = value

    def get_map_obj(self):
        return map_obj

    def set_map(self, value):
        global map
        map = value

    def get_map(self):
        global map
        return map

    def set_frame(self, value):
        global frame
        frame = value

    def get_frame(self):
        global frame
        return frame

    def get_size(self, standard_size, offset, map_obj):
        """Returns the size of the map so that the screen can be created to the correct size"""
        self.set_map(map_obj.get_map())
        num_rows = map_obj.get_map_height()
        num_cols = map_obj.get_map_length()
        self.set_map_obj(map_obj)
        canvas_width = standard_size * num_rows + (2 * offset)
        canvas_height = standard_size * num_cols + (2 * offset)
        return [canvas_width, canvas_height]


    def generate_grid(self,canvas_width, canvas_height, x1, y1, x2, y2, standard_size, offset, frame):
        """THis is the method that creates the grid. X axis runs along the top and Y axis is down the left side"""
        self.set_frame(frame)
        canvas_grid = Canvas(frame, width=canvas_width, height=canvas_height, bg="Green")
        # Takes the martix and converts it into a grid patten baced on the size of the arrays
        # Creates the rows
        mapArray = map_obj.get_map()
        colour = ""
        for i in range(len(mapArray)):
            #Creates the Columns
            for j in range(len(mapArray[i])):
                colour = "gray"
                if mapArray[i][j] == 0:
                    colour = "white"
                if mapArray[i][j] != 0:
                    person = mapArray[i][j]
                    # print(person.get_coordinates())

                canvas_grid.create_rectangle(x1, y1, x2, y2, fill = colour)
                x1 = x2
                x2 = x2 + standard_size
            x1 = offset
            x2 = standard_size + offset
            y1 = y2
            y2 = y2 + standard_size

        return canvas_grid

    def remove_canvas(self,frame):
        frame.destroy()
