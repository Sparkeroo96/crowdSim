import tkinter
from GUI.GridGui import GridGui
from GUI.PersonGui import *



class GuiController:

    def __int__(self):
        print("Gui Running")

        self.init_grid()


    # Creates the grid
    @staticmethod
    def init_grid(map_info):
        # Defines the size of the squares on the grid
        offset = 10
        standard_size = 50

        # Corddinates for the first square in the grid
        X1 = offset
        Y1 = offset
        X2 = offset + standard_size
        Y2 = offset + standard_size

        main_grid = GridGui()
        size = main_grid.get_size(standard_size,offset,map_info)
        canvas_info = main_grid.generate_grid(size[0], size[1], X1, Y1, X2, Y2, standard_size, offset)
        master = canvas_info[0]
        main_grid_location = canvas_info[1]
        # Creates one person and puts them on the map
        # test_person_gui = PersonGui()
        # canvas_info = test_pGerson_gui.on_to_map(main_grid_location, standard_size, offset)
        print("GUI making grid")
        main_grid_location.pack()
        master.mainloop()


