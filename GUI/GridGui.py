# #!/usr/bin/python
import tkinter
from Map.map_main import MapMain

#map_info = MapMain()
#mapArray = map_info.get_map()


class GridGui:
    map_info = None


    def __init__(self):
        print("GUI for map")

    def get_size(self, standard_size, offset, map_info1):
        num_rows_cols = map_info1.grid_size(map_info1.get_map())
        num_rows = num_rows_cols[0]
        num_cols = num_rows_cols[1]
        global map_info
        map_info = map_info1
        canvas_width = standard_size * num_rows + (2 * offset)
        canvas_height = standard_size * num_cols + (2 * offset)
        return [canvas_width, canvas_height]

    def generate_canvus(self, canvas_width, canvus_height, x1, y1, x2, y2, standard_size, offset):
        master = tkinter.Tk()
        canvas_grid = tkinter.Canvas(master, width=canvas_width, height=canvus_height, bg="Green")
        return [master,canvas_grid]

    def generate_grid(self,master, canvas_grid, x1, y1, x2, y2, standard_size, offset):
        # Takes the martix and converts it into a grid patten baced on the size of the arrays
        # Creates the rows
        global map_info
        mapArray = map_info.get_map()
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

        return [master, canvas_grid]
