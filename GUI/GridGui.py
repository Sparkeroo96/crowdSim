# #!/usr/bin/python
import tkinter
from Map.map_main import MapMain
from People.person import Person


mapInfo = MapMain()
mapArray = mapInfo.get_map()


class GridGui:

    def __init__(self):
        print("GUI for map")

    def get_size(self, standard_size, offset):
        num_rows_cols = mapInfo.grid_size(mapInfo.get_map())
        num_rows = num_rows_cols[0]
        num_cols = num_rows_cols[1]
        canvas_width = standard_size * num_rows + (2 * offset)
        canvas_height = standard_size * num_cols + (2 * offset)
        return [canvas_width, canvas_height]

    def generate_grid(self, canvas_width, canvus_height, x1, y1, x2, y2, standard_size, offset):
        master = tkinter.Tk()
        mainGrid = tkinter.Canvas(master, width=canvas_width, height=canvus_height, bg="Green")

        # Takes the martix and converts it into a grid patten baced on the size of the arrays
        # Creates the rows
        colour = ""
        for i in range(len(mapArray)):
            #Creates the Columns
            for j in range(len(mapArray[i])):
                colour = "gray"
                if mapArray[i][j] != 0:
                    colour = "white"
                mainGrid.create_rectangle(x1, y1, x2, y2, fill = colour)
                x1 = x2
                x2 = x2 + standard_size
            x1 = offset
            x2 = standard_size + offset
            y1 = y2
            y2 = y2 + standard_size

        return [master, mainGrid]
