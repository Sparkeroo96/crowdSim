from tkinter import *
from GUI.GridGui import GridGui
from Map.map_main import *

class mapEditGui:
    gui_controller = None
    working_map = None
    size = None
    square_size = None

    def __int__(self, parent):
        self.set_gui_controller(parent)

    def set_size(self,value):
        global size
        size = value

    def get_size(self):
        global size
        return size

    def set_square_size(self,value):
        global square_size
        square_size = value

    def get_square_size(self):
        global square_size
        return square_size

    def set_working_map(self, value):
        global working_map
        working_map = value

    def get_working_map(self):
        global working_map
        return working_map

    def set_gui_controller(self,value):
        global gui_controller
        gui_controller = value

    def get_gui_controller(self):
        global gui_controller
        return gui_controller

    def options_page(self,frame,master):
        Label(frame, text="Height: ").grid(row=0)
        Label(frame, text="Width: ").grid(row=1)
        Label(frame, text="Size of Boxs: ").grid(row=2)
        value1 = Entry(frame)
        value2 = Entry(frame)
        value3 = Entry(frame)
        value1.grid(row=0, column=1)
        value2.grid(row=1, column=1)
        value3.grid(row=2, column=1)
        Button(frame, text='Enter', command=lambda master1 = master, frame1 = frame, x = value1, y = value2, z = value3 : self.make_blank_map(x, y,z,frame1,master1)).grid(row=3, column=1, sticky=W, pady=4)
        frame.pack()
        return frame

    def make_blank_map(self, x, y,z,frame,master):
        map_obj = MapMain()
        int_x = int(x.get())
        int_y = int(y.get())
        int_z = int(z.get())
        frame.destroy()
        map_obj.map_generate(int_x,int_y)
        map_array = map_obj.get_map()
        self.set_working_map(map_obj)
        self.generate_map(map_obj,master,int_z)

    def generate_map(self,map, master, int_z):
        map_gui = GridGui()
        map_edit_frame = Frame(master)
        size = map_gui.get_size(int_z,5,map)
        self.set_size(size)
        self.set_square_size(int_z)
        gui_controller = self.get_gui_controller()
        first = gui_controller.first_square(map,5,int_z)
        print(first)
        map_canvas = map_gui.generate_grid(size[0],size[1],first[0],first[1],first[2],first[3],int_z,5,map_edit_frame)
        map_canvas.bind("<Button-1>", self.onClick)
        map_canvas.pack()
        map_edit_frame.pack()
        map_edit_frame.update()

    def onClick(self,other):
        x = other.x
        y = other.y
        array_cords = self.cordinate_converstion(x, y)
        print(array_cords)

    def cordinate_converstion(self, x, y):
        """Does the maths to work out what cordanate has been selected so it can edit the map data"""
        # cordinate 0,0 on a board of 10,10 size 50 is top left: 5,455 bottom right: 55,505
        size = self.get_size()
        square_size = self.get_square_size()
        offset = 5
        cord1_x = [offset,offset + square_size]
        cord1_y = [size[1] - square_size, size[1]]
        result_x = None
        result_y = None
        print(x,y)
        # print(cord1_x)
        # print(cord1_y)
        cord1 = [[cord1_x[0],cord1_y[0]],[cord1_x[1],cord1_y[1]]]
        map_obj = self.get_working_map()
        map_grid = map_obj.grid_size(map_obj.get_map())
        max_x = map_grid[0]
        max_y = map_grid[1]
        for i in range(0, max_x):
            X1 = offset + (i * square_size)
            X2 = X1 + square_size
            # print("%s < %s AND %s > %s" % (X1,x,x,X2))
            if X1 <= x and x <= X2:
                result_x = i
                break

        for i in range(0, max_y):
            Y1 = size[1] - (square_size * i)
            Y2 = Y1 - square_size
            # print("%s < %s AND %s > %s" % (Y1,y,y,Y2))
            if Y1 >= y and y >= Y2:
                result_y = i
                break

        result = [result_x,result_y]

        return result

