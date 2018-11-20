from tkinter import *
from GUI.GridGui import GridGui
from GUI.PersonGui import *
from Map.map_main import MapMain
from simulation import *
import time


class GuiController:
    grid_gui_obj = None
    grid_gui_obj_location = None
    size = None
    master = None
    canvas_info = None
    start = 0
    welcome_frame = None
    sim = None
    sim_frame = None
    grid_gui_obj = None
    frame_controller = None
    previous_frame = None

    # Defines the size of the squares on the grid
    offset = 10
    standard_size = 50

    def __int__(self):
        print("Gui Running")

        self.init_grid()

    def set_frame_controller(self, value):
        global frame_controller
        frame_controller = value

    def get_frame_controller(self):
        global frame_controller
        return frame_controller

    def set_grid_gui_obj(self, value):
        global grid_gui_obj
        grid_gui_obj = value

    def get_grid_gui_obj(self):
        global grid_gui_obj
        return grid_gui_obj

    def set_sim_frame(self, value):
        global sim_frame
        sim_frame = value

    def get_sim_frame(self):
        global sim_frame
        return sim_frame

    def get_standard_size(self):
        global standard_size
        return standard_size

    def set_master(self, newMaster):
        global master
        master = newMaster

    def get_master(self):
        global master
        return master

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
        return canvas_info

    def set_welcome_frame(self, value):
        global welcome_frame
        welcome_frame = value

    def get_welcome_frame(self):
        global welcome_frame
        return welcome_frame

    def set_sim(self,value):
        global sim
        sim = value

    def get_sim(self):
        global sim
        return sim

    def set_previous_frame(self, value):
        global previous_frame
        previous_frame = value

    def get_previous_frame(self):
        global previous_frame
        return previous_frame

    def init_master(self,simulation):
        """Creates the application and then calls the welcome page"""
        master = Tk()
        self.set_sim(simulation)
        print(simulation)
        # # Gets the requested values of the height and widht, then puts the screen in the centre of the page.
        # windowWidth = master.winfo_reqwidth()
        # windowHeight = master.winfo_reqheight()
        #
        # # Gets both half the screen width/height and window width/height
        # positionRight = int(master.winfo_screenwidth() / 2 - windowWidth / 2)
        # positionDown = int(master.winfo_screenheight() / 2 - windowHeight / 2)
        #
        # # Positions the window in the center of the page.
        # master.geometry("+{}+{}".format(positionRight, positionDown))

        # Sets the master as a global variable for other methods to be able to call
        self.set_master(master)

        # create a toplevel menu
        menubar = Menu(master)

        # display the menu
        master.config(menu=menubar)

        # Adding th file names
        file = Menu(menubar)
        # Adding Exit function and File and mounting the to the main menu bar
        file.add_command(label='Exit', command=self.client_exit)
        menubar.add_cascade(label='File', menu=file)
        #Opens the welcome page frame and incerts it into the main application
        self.init_welcome_page()

        # Calls the main loop function on the application so it runs
        master.mainloop()

    def manage_frames(self):
        pre_frame = self.get_previous_frame()
        if pre_frame is not None:
            next_frame = self.redraw()
            next_frame.pack()
            pre_frame.destroy()
            print(next_frame)
            print(pre_frame)
            print()
            # pre_frame.destroy()
            pre_frame = next_frame
            self.set_previous_frame(pre_frame)
            frame_controller = self.get_frame_controller()
            frame_controller.pack()
            self.get_master().update()

        time.sleep(0.1)



    def init_welcome_page(self):
        """This is the first page that is opened in the form of a fram that is mounted to master"""
        # Gets the master variable
        master = self.get_master()

        #Creates frame
        welcome_frame = Frame(master, bg="blue")

        # Makes it a global variable
        self.set_welcome_frame(welcome_frame)
        # Adds buttons to the page that call other methods
        # Adds a start button that will run a defult simulation
        startButton = Button(welcome_frame, text='Start Simulation', command=self.start_sim)
        # Quit button that closed the application
        quitButton = Button(welcome_frame, text="Exit", command=self.client_exit)
        # Places the button in the first coridanate on the frame
        startButton.place(x=0,y=0)
        # Adds the buttons to the frame and then the frame too the master
        startButton.pack()
        quitButton.pack()
        welcome_frame.pack()

    def start_sim(self):
        """This is the button function that start the defult application and closes the welcome frame"""
        welcome_frame = self.get_welcome_frame()
        welcome_frame.destroy()
        sim = self.get_sim()
        sim.start_simulation()

    def init_simulation_frame(self, map_array_obj):
        global grid_gui_obj
        global grid_gui_obj_location
        global canvas_info
        master = self.get_master()
        frame_controller = Frame(master)
        self.set_frame_controller(frame_controller)
        # Creates a frame to go into the master that will run the simulation canuvas
        offset = 10
        standard_size = 50


        # Corddinates for the first square in the grid
        X1 = offset
        Y1 = offset
        X2 = offset + standard_size
        Y2 = offset + standard_size
        grid_gui_obj = GridGui()
        print(map_array_obj.get_map())
        size = grid_gui_obj.get_size(standard_size,offset,map_array_obj)
        self.set_size(size)
        first_frame = grid_gui_obj.generate_grid(size[0], size[1], X1, Y1, X2, Y2, standard_size, offset,frame_controller)
        self.set_canvus_info(first_frame)
        grid_gui_obj_location = canvas_info
        self.set_grid_gui_obj(grid_gui_obj)
        print(frame_controller)
        self.set_previous_frame(first_frame)
        return first_frame

    def redraw(self):
        global grid_gui_obj
        global grid_gui_obj_location
        frame_controller = self.get_frame_controller()
        X1 = 10  #self.get_offset()
        Y1 = X1
        X2 = X1 + 50 #self.get_standard_size()
        Y2 = X1 + 50 # self.get_standard_size()
        size = self.get_size()
        master = self.get_master()
        next_grid = grid_gui_obj.generate_grid(size[0], size[1], 10, 10, 60, 60, 50, 10, frame_controller)
        return next_grid

    def client_exit(self):
        local_master = self.get_master()
        local_master.destroy()

