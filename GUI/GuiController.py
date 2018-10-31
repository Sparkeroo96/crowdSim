import tkinter
from GUI.GridGui import GridGui
from GUI.PersonGui import *
import time



class GuiController:

    canvas_grid = None
    canvas_grid_location = None
    size = None
    master = None
    canvas_info = None
    # Defines the size of the squares on the grid
    offset = 10
    standard_size = 50

    def __int__(self):
        print("Gui Running")

        self.init_grid()

    def get_standard_size(self):
        global standard_size
        return standard_size


    def get_size(self):
        global size
        return size

    def set_size(self, sizeNew):
        global size
        size = sizeNew

    def get_offset(self):
        global offset
        return offset

    def set_canvus_info(self, canvas_info1):
        global canvas_info
        canvas_info = canvas_info1

    def get_cannvas_info(self):
        global canvas_info
        return  canvas_info

    # Creates the grid
    def init_grid(self, map_info):
        global canvas_grid
        global canvas_grid_location
        global master
        offset = 10
        standard_size = 50

        # Corddinates for the first square in the grid
        X1 = offset
        Y1 = offset
        X2 = offset + standard_size
        Y2 = offset + standard_size
        canvas_grid = GridGui()
        size = canvas_grid.get_size(standard_size,offset,map_info)
        self.set_size(size)
        canvas_info = canvas_grid.generate_canvus(size[0], size[1], X1, Y1, X2, Y2, standard_size, offset)
        self.set_canvus_info(canvas_info)
        # canvas_grid.generate_grid(size[0], size[1], X1, Y1, X2, Y2, standard_size, offset)
        master = canvas_info[0]
        canvas_grid_location = canvas_info[1]
        canvas_grid_location.pack()

    def redraw(self):
        global canvas_grid
        global canvas_grid_location
        size = self.get_size()
        canvas_info_local = self.get_cannvas_info()
        # Corddinates for the first square in the grid
        X1 = 10  #self.get_offset()
        Y1 = X1
        X2 = X1 + 50 #self.get_standard_size()
        Y2 = X1 + 50 # self.get_standard_size()
        canvas_grid.generate_grid(canvas_info_local[0], canvas_info_local[1], 10, 10, 60, 60, 50, 10)

        # canvas_grid.generate_grid([0], size[1], X1, Y1, X2, Y2, self.get_standard_size(), self.get_offset())
        # while True:
        master.update_idletasks()
        master.update()
        canvas_grid_location.delete('all')
        time.sleep(0.5)




