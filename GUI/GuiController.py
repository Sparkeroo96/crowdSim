import tkinter
from GUI.GridGui import *
from GUI.PersonGui import *

#Difines the size of the squares on the grid
offset = 10
standard_size = 100

#Corddinates for the first square in the grid
X1 = offset
Y1 = offset
X2 = offset + standard_size
Y2 = offset + standard_size

#Creates the grid
main_grid = GridGui()
size = main_grid.get_size(standard_size,offset)
canvas_info = main_grid.generate_grid(size[0], size[1], X1, Y1, X2, Y2, standard_size, offset)
master = canvas_info[0]
mainGrid = canvas_info[1]
#Creates one person and puts them on the map
test_person_Gui = PersonGui()
canvas_info = test_person_Gui.on_to_map(mainGrid, standard_size, offset)


mainGrid.pack()
master.mainloop()
