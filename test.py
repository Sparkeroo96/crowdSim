"""
The main GUI that creates the display and runs the code for the system

Created by Chris Clark cc604
Modified by Sam Parker swp5
"""
import pygame
import math
import sys
import os
from Data import map_data
from time import sleep
from People.person import Person
from Objects.wall import Wall
from Objects.danceFloor import DanceFloor


class RunningMain:

    data = None

    # RGB Colours defined
    white = (255,255,255)
    black = (0,0,0)
    green = (51, 204, 51)
    red = (255, 0, 0)
    blue = (0, 0, 153)
    orange = (255, 128, 0)
    yellow = (250,250,0)
    purple = (128,0,128)

    exit = False

    # Menu flags
    display = None
    pause = None
    menu = [None,"home"]
    load_name = False
    user_input_result = ''
    running_map_data_loc = ""
    text_done = False
    text_running = False
    error = False
    show_heatmap_toggle = False

    # Size of the screen
    screen_width = 1000
    # screen_height = 800
    screen_height = 700

    sim_screen_width = math.floor(screen_width - (screen_width / 3))
    sim_screen_height = math.floor(screen_height - (screen_height/ 4))

    offset = 0

    #Error message
    error_message = ""

    #Builder Functionality
    builder_active = False
    xCrod1 = None
    yCord1 = None
    width = 0
    height = 0
    drag = False
    current_tool = "wall"
    new_tool = False
    size_of_menu_buttons = 0

    #Debug flags
    add_person_on_click = False

    #Save flags
    save_active = None
    save_name = False

    tick_rate = 20

    heat_map = []

    selected_person = None
    size_info_pannel = None

    #Info for changing their needs
    x1_first_click = None
    startAmount_of_need = None
    new_value_for_need = None
    dragging_bar = False
    selected_button = None
    temp_width = None
    nodes_generated = 0
    current_route = []

    menu_bar_info = None
    menu_bar_clicked = None
    pause_toggle = False

    show_nodes = False
    dance_floor_info = None

    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(0) + "," + str(0)

        self.set_offset(self.centre([0, 0, self.get_screen_width(), self.get_screen_height()],[self.get_sim_screen_width(), self.get_sim_screen_height()]))
        """This is the constructor that starts the main loop of the simulation"""
        #Starts the pygame
        pygame.init()
        self.create_heatmap()
        #Gets the location for the map data
        self.set_map_data(map_data.map_data(self,self.get_tick_rate()))
        # Creates a display to the size of the screen
        self.display = pygame.display.set_mode((self.get_screen_width(),self.get_screen_height()))
        # Adds name for the application
        pygame.display.set_caption("Crowd Simulation ")
        # Starts a clock that manages the ticks
        clock = pygame.time.Clock()
        # Flag for checking if the map loaded correclty
        success = False
        self.get_map_data().set_size_screen(self.sim_screen_width, self.sim_screen_height)
        # Main loop for the applicaion
        while not self.get_exit():

            self.get_display().fill(self.white)
            # This gets all the key presses and mouse movements and passes them as events
            for event in pygame.event.get():
                # Quit Function
                if event.type == pygame.QUIT:
                    self.set_exit()
                # This allows an agent to be selected to see what they are thinking
                main_sim_screen = [self.get_offset()[0],self.get_offset()[1],self.get_sim_screen_width(), self.get_sim_screen_height()]
                if event.type == pygame.MOUSEBUTTONDOWN and self.get_menu()[1] == 'Start' and self.in_area(pygame.mouse.get_pos(), main_sim_screen):
                    selected = self.get_map_data().what_object(self.gui_to_map_data_coords_offset(pygame.mouse.get_pos()), True)
                    if isinstance(selected, Person):
                        self.set_selected_person(selected)
                    else:
                        self.set_selected_person(None)
                    sleep(0.1)
                # This is gets the button in the info pannel they seleced
                if self.get_selected_person() is not None:
                    if event.type == pygame.MOUSEBUTTONDOWN and self.get_size_info_pannel() is not None:
                        x, y = pygame.mouse.get_pos()
                        info_size = self.get_size_info_pannel()
                        box_x1 = info_size[0]
                        box_y1 = info_size[1]
                        box_x2 = info_size[0] + info_size[2]
                        size_one_box = info_size[3] / info_size[4]
                        if x >= box_x1 and x <= box_x2:
                            for i in range(0, info_size[4]):
                                if(self.in_area(pygame.mouse.get_pos(),[box_x1,box_y1 + (size_one_box * i),info_size[2], size_one_box])):
                                    self.set_selected_button(i)

                if self.get_selected_button() is not None and self.in_area(pygame.mouse.get_pos(),self.get_size_info_pannel()):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.set_x1_first_click(pygame.mouse.get_pos()[0])
                        array = self.get_selected_person().get_person_needs()
                        self.set_startAmount_of_need(array[self.get_selected_button()][1])
                        self.set_dragging_bar()

                if event.type == pygame.MOUSEBUTTONUP and self.get_dragging_bar() and self.get_selected_person() is not None:
                    info = self.get_size_info_pannel()
                    starting_value = self.get_startAmount_of_need() / (info[2]/100)
                    new_value = pygame.mouse.get_pos()[0] / (info[2]/100)
                    new_value = starting_value + (new_value - starting_value)
                    new_value = round(new_value)
                    if new_value < 0:
                        new_value = 0
                    if new_value > 100:
                        new_value = 100
                    self.get_selected_person().set_needs_values(self.get_selected_button(),new_value)
                    self.set_x1_first_click(None)
                    self.set_startAmount_of_need(None)
                    self.set_dragging_bar()

                # Pause function
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F10:
                        self.set_pause()
                    #Saves the current map
                    if event.key == pygame.K_F1 and self.get_build_active():
                        self.set_save_active(True)
                        self.set_save_name(True)
                    if event.key == pygame.K_F2:
                        self.set_home_menu()
                    if event.key == pygame.K_F9:
                        self.set_add_person_on_click()
                    if event.key == pygame.K_F8:
                        self.set_show_heatmap_toggle()
                        self.pause = True

                # Adding objects if the load menu is active
                if pygame.mouse.get_pressed()[0] and self.get_build_active() and self.get_drag() == False and ((pygame.mouse.get_pos()[1] < self.get_screen_height() * 0.90) and pygame.mouse.get_pos()[0] > self.get_size_of_menu_buttons()) and self.get_current_tool() != "Remove" and not self.get_new_tool():
                    self.set_xCord1(pygame.mouse.get_pos()[0])
                    self.set_yCord1(pygame.mouse.get_pos()[1])
                    self.set_drag(True)

                # gets the width and height for the object and creates the obj
                if event.type == pygame.MOUSEBUTTONUP and self.get_build_active() and self.get_drag() and self.get_current_tool() is not "Remove":
                    x2, y2 = pygame.mouse.get_pos()
                    width = self.get_xCord1() - x2
                    self.set_width(width * -1)
                    height = self.get_yCord1() - y2
                    self.set_height(height * -1)
                    coord = (self.get_xCord1(), self.get_yCord1())
                    coord = self.gui_to_map_data_coords_offset(coord)
                    xCord1, yCord1 = coord
                    self.data.add_to_map(self.get_current_tool(),xCord1, yCord1, self.get_width(), self.get_height())
                    pygame.display.update()
                    self.set_drag(False)

                # Adds a person to the map if clicked
                if self.get_add_person_on_click() and event.type == pygame.MOUSEBUTTONUP and not self.get_build_active() and self.in_area(pygame.mouse.get_pos(),[self.get_offset()[0],self.get_offset()[1],self.get_sim_screen_width(),self.get_sim_screen_height()]):
                    #Need to have a check to say if you can create a person at these coordinates
                    personCoordinates = self.gui_to_map_data_coords_offset(pygame.mouse.get_pos())
                    size = 20
                    self.get_map_data().add_people_to_map(personCoordinates, size, 0)

                #The remove object function
                if self.get_current_tool() == "Remove" and event.type == pygame.MOUSEBUTTONUP:
                    self.get_map_data().delete_object(self.gui_to_map_data_coords_offset(pygame.mouse.get_pos()))

                #This is the code manages the user text imput
                if self.get_text_running() and event.type == pygame.KEYDOWN:
                    #Removes the last charater in the string
                    if event.key == pygame.K_BACKSPACE:
                        if self.get_load_name():
                            text = self.get_user_input_result()
                            text = text[:-1]
                            self.set_user_input_result(text)
                    # Sets the text done flag to true so the simultion can then load it
                    elif event.key == pygame.K_RETURN:
                        self.set_text_done(True)
                        self.set_text_running(False)
                        self.set_save_name(False)
                        self.set_load_name(False)
                    # This is any other charactor and adds it to the running string for the user imput so it can be displayed
                    else:
                        if self.get_load_name() or self.get_save_name():
                            running = self.get_user_input_result()
                            new_running = running + event.unicode
                            self.set_user_input_result(new_running)

                if event.type == pygame.MOUSEBUTTONDOWN and not self.menu_bar_info == None and self.in_area(pygame.mouse.get_pos(), self.menu_bar_info):
                    x, y = pygame.mouse.get_pos()
                    menu_size = self.menu_bar_info
                    button_size = menu_size[2] / menu_size[4]
                    current_x = 0
                    first_x = menu_size[0]

                    while current_x < menu_size[4]:
                        if x > (first_x + (button_size * current_x)) and x < first_x + button_size + (button_size * current_x):
                            self.menu_bar_clicked = current_x


                        current_x = current_x + 1



            # this tracks the mouse movement when holding down the left button and puts a rectangle there each time
            if self.get_drag() and self.get_current_tool() != "Remove":
                width, height = pygame.mouse.get_pos()
                width = width - self.get_xCord1()
                height = height - self.get_yCord1()
                self.set_width(width)
                self.set_height(height)
                pygame.draw.rect(self.get_display(), self.object_colour(self.get_current_tool()),
                                 [self.get_xCord1(), self.get_yCord1(), self.get_width(), self.get_height()])
                pygame.display.update()

            # Resets the display to white each tick so a new information can be displayed
            menu = self.get_menu()
            # Shows the first menu screen

            if menu[1] == "home":
                self.home_menu()

            # Displays the simulation option menu
            elif menu[1] == "Run Simulation":
                self.sim_menu()

                #Checks to see if the text is completed if so then it loads that building floor plan
                if self.get_text_done():
                    search = self.get_user_input_result()
                    success = self.load_map('maps_saves', search)
                    self.set_text_done(False)

            # This checks to see if it is on the simulation menu options
            elif menu[0] == "Run Simulation":
                # Running the simulation that is chosen or the default one
                if menu[1] == "Start":
                    # Gets the map from map data
                    objectArray = self.data.get_map()
                    # if it is empty then it loads the default
                    if len(self.get_map_data().get_map()) == 0:
                        print("Load Default")
                        self.get_map_data().import_from_file("maps_saves","default")

                    self.draw_display()
                    # self.draw_display()
                # Starts the user input function
                if menu[1] == "Floor Plan Load":
                    self.data.clear_map()
                    self.set_load_name(True)
                    self.set_menu("Run Simulation")
                # Creates the config page for the simulation
                if menu[1] == "Options":
                    print("options")
                # Goes back to the previous page
                if menu[1] == "Back":
                    self.set_home_menu()
                # Closes the applicaion
                if menu[1] == "Exit":
                    self.set_exit()
            # Loads the builder menu
            elif menu[1] == "Builder":
                self.builder_menu()
            # Checks to see if it is within the builder menu
            elif menu[0] == "Builder":
                # Creates a new empty map for the user to add objects
                if menu[1] == "New":
                    self.new_build()
                    if self.get_save_active():
                        self.save()
                # loads a map that the user can edit
                if menu[1] == "Load":
                    self.get_map_data().clear_map()
                    self.set_load_name(True)
                    self.set_menu("Builder")
                # Goes back to the previous menu
                if menu[1] == "Back":
                    self.set_home_menu()
                # Quits the appliction
                if menu[1] == "Exit":
                    self.set_exit()
            # Quits the appliction
            elif menu[1] == "Exit":
                self.set_exit()
            elif menu[1] == "error":
                self.error_page(self.get_error_message())
            # Prints an error that no selection was found with that name
            else:
                self.error_page("Menu Option has failed")

            if self.get_dragging_bar():
                info_size = self.get_size_info_pannel()

                width = pygame.mouse.get_pos()[0]
                starting_coord = (info_size[2] / 100) * self.get_startAmount_of_need()
                width = ((width - self.get_x1_first_click()) / info_size[2]) * 100
                width = starting_coord + width

                if width > info_size[2]:
                    width = info_size[2]
                if width < 0:
                    width = 0

                self.set_temp_width(width)
                button_num = self.get_selected_button()
                info_size = [info_size[0] / info_size[4],info_size[1] / info_size[4], info_size[2], info_size[3] / info_size[4]]
                info = [0, info_size[1] + info_size[3] + (info_size[3] * button_num) - (info_size[3] / 5), info_size[2], info_size[3] / 5]
                pygame.draw.rect(self.get_display(),self.red,info)

                info = [0, info_size[1] + info_size[3] + (info_size[3] * button_num) - (info_size[3] / 5), self.get_temp_width(), info_size[3] / 5]
                pygame.draw.rect(self.get_display(),self.green,info)
            pygame.display.update()
            clock.tick(self.tick_rate)

            while self.get_pause():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F10:
                            self.set_pause()

                    if event.type == pygame.MOUSEBUTTONDOWN and not self.menu_bar_info == None and self.in_area(pygame.mouse.get_pos(), self.menu_bar_info):
                        x, y = pygame.mouse.get_pos()
                        menu_size = self.menu_bar_info
                        button_size = menu_size[2] / menu_size[4]
                        current_x = 0
                        first_x = menu_size[0]

                        while current_x < menu_size[4]:
                            if x > (first_x + (button_size * current_x)) and x < first_x + button_size + (
                                    button_size * current_x):
                                if x == 1:
                                    self.pause_toggle = not self.pause_toggle
                                self.menu_bar_clicked = current_x

                            current_x = current_x + 1
                            self.menu_bar()
                            self.menu_option(self.menu_bar_clicked)

        pygame.quit()
        quit()

    def add_button(self,button_info, text, colour, text_size):
        """Adds a button to the screen with a given dimention and text inside and adds it to the display
        :param button_info, is the coordiate and size info
        :param text, is the text that is going inside the box
        :param colour, is the colour of the box
        """
        pygame.draw.rect(self.get_display(),colour,button_info,2)
        button_text = self.text(text,text_size)
        loaction = self.centre(button_info,[button_text[1],button_text[2]])
        self.get_display().blit(button_text[0], loaction)


    def centre(self,box,text):
        """This is a function that provides the cordinates for a box so that it is centered in the middle of the sceen
        :param box, takes the x and y coordinates and the width and height of the outside box
        :param text, takes the height and width of the box or text that is going inside the other box
        :return, the x and y coordinate for the internal box to be centred
        """
        # Values for the outside box (screen)
        box_x = box[0]
        box_y = box[1]
        box_width = box[2]
        box_height = box[3]

        # Size of the text or box that wants to be centred in the larger box
        text_width = text[0]
        text_height = text[1]

        #Maths that works out the cordinate for the X coordinate
        half_box_width = math.floor(box_width/2)
        half_text_width = math.floor(text_width/2)
        chaneg_in_x = half_box_width - half_text_width
        x_coord = box_x + chaneg_in_x

        #Maths that works out the coordinate for the Y
        half_box_height = math.floor(box_height / 2)
        half_text_height = math.floor(text_height / 2)
        chaneg_in_y = half_box_height - half_text_height

        y_coord = box_y + chaneg_in_y

        # Puts both in a tuple format
        text_location = (x_coord,y_coord)

        # Returns x and y coordinate for the ceneter
        return text_location

    def text(self,text, size):
        """ This function creates a text object in pygame and returns the size of the text
        :param text: the string that is to be displayed
        :return: The text object and the height and width for further calucaltions
        """
        # if text is None:
        #     text = "ERROR"
        pygame.font.init()
        my_font = pygame.font.SysFont("Arial", size)
        text_surface = my_font.render(text, False, self.black)
        return [text_surface,my_font.size(text)[0],my_font.size(text)[1]]

    def key_buttons(self):
        """
        This function handeles the button presses in pygame, save, pause and creation of walls
        """
        for event in pygame.event.get():
            # Gets the starting cordinates for the walls
            # quits if x button is pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def draw_display(self):
        """
        Draws the display for the actul simulation by going though the map array and drawing the shape that is required in the correct loactions
        """
        if not self.builder_active:
            self.menu_bar()
            self.menu_option(self.menu_bar_clicked)
        x_offset, y_offset = self.get_offset()
        if self.show_nodes:
            list_nodes = self.get_map_data().open_nodes
            if not list_nodes == []:
                for node in list_nodes:
                    x1, y1  = node
                    x1 = x1 * 20
                    y1 = y1 * 20
                    x1 = x1 + x_offset
                    y1 = y1 + y_offset
                    self.node_icon((x1,y1))
        # Draws the border around the simulation
        pygame.draw.rect(self.get_display(),self.black,[x_offset,y_offset,self.get_sim_screen_width(), self.get_sim_screen_height()],2)
        # Goes though the map array obj
        objectArray = self.data.get_map()

        for obj in objectArray:
            obj.action()
            coordinates = obj.get_coordinates()
            coordinates = self.map_data_to_gui_coords_offset(coordinates)
            angle = obj.get_angle()
            width = obj.get_width()
            obj_colour = obj.get_colour()
            shape = obj.get_shape()
            # the process of adding a person and the funcitons that get called
            if isinstance(obj, Person) and not self.get_show_heatmap_toggle():
                try:
                    # Adds the coordinates to the heat map in a try to avoid an error where and object is created outside of the area
                    self.add_heatmap(coordinates)
                except:
                    nothing = 1
                # if obj.get_state_action() == "dance":
                if obj.currentState == "dance":
                    red, blue, green = obj.colour
                    red = (red + 10) % 225
                    blue = (blue + 20) % 225
                    green = (green + 30) % 225
                    obj.colour = (red, blue, green)
                else:
                    obj.colour = self.red

                # This is a check to make sure that the people are inside of the area
                # if not self.dance_floor_info == None:
                #     dance_floor_x, dance_floor_y = self.dance_floor_info.get_coordinates()
                #     dance_floor_width = self.dance_floor_info.get_width()
                #     dance_floor_height = self.dance_floor_info.get_height()
                #     dance_floor_x, dance_floor_y = self.map_data_to_gui_coords_offset((dance_floor_x, dance_floor_y))
                #     info = [dance_floor_x, dance_floor_y, dance_floor_width, dance_floor_height]
                #     self.get_map_data().get_coordinates_range()
                #     if self.in_area(coordinates, info):
                #         obj.colour = self.black

                if(obj == self.get_selected_person()):
                    text_info = self.get_selected_person().get_person_needs()
                    size_info = [0,0,150,50]
                    saved_size_info = size_info
                    obj_colour = self.green
                    running_size = size_info
                    path = self.get_selected_person().astarCoords
                    if not path == [] and path is not None:
                        self.draw_path(path)
                    for item in text_info:
                        text = str(item[0] + ": " + str(math.floor(item[1])))
                        self.add_button(size_info,text, self.black, 20)
                        self.need_bar(item[0],item[1],size_info)
                        size_info = [size_info[0],size_info[1] + size_info[3],size_info[2],size_info[3]]
                        running_size =[size_info[0],size_info[1],size_info[2], size_info[3]+ running_size[3]]
                    current_state = self.get_selected_person().currentState
                    if current_state is None:
                        current_state = ""
                    size_info = [0,150,150,50]
                    self.add_button(size_info,current_state,self.black,20)
                    # size_info = [0, 200, 150, 50]
                    # self.add_button(size_info, str(obj.coordinates), self.black, 20)
                    running_size =[saved_size_info[0],saved_size_info[1],saved_size_info[2], running_size[3] - size_info[3], len(text_info)]
                    self.set_size_info_pannel(running_size)

                pygame.draw.circle(self.display, obj_colour, coordinates, round(width / 2))
                # Maths to add the pixcels to represent the eyes
                eyes = obj.person_eyes(coordinates, angle, round(width / 2))
                self.display.set_at((eyes[0][0], eyes[0][1]), self.white)
                self.display.set_at((eyes[1][0], eyes[1][1]), self.white)

            elif self.get_show_heatmap_toggle():
                self.show_heatmap()

            if shape == "rectangle" or shape == "wall":
                # objects
                height = obj.get_height()
                pygame.draw.rect(self.display, obj_colour, [coordinates[0], coordinates[1], width, height])
                # testing
                # if isinstance(obj, DanceFloor):
                #     self.dance_floor_info = obj

        for obj in objectArray:
            if isinstance(obj, Person):
                objCoordinates = obj.get_coordinates()
                angle = obj.get_angle()
                sight = obj.get_sight()
                # Calls the person vision function that returns an array of all the cordinates on the vision lines it makes
                vision = obj.personVision(objCoordinates[0], objCoordinates[1], angle, sight)
                # clears the person vision from the previous ittoration
                obj.clear_vision()
                # goes though every coordinates and works out what colour is in that pixcel
                for cordArray in vision:
                    # try and catch to prevent out of array exceptions
                    for cord in cordArray:
                        try:
                            seenObj = 0
                            cords_new = self.map_data_to_gui_coords_offset((cord[0],cord[1]))
                            # cords_new = self.map_data_to_gui_coords_offset(cords_new)
                            if(self.selected_person == obj):
                                self.display.set_at(cords_new, self.red)
                            colour = self.display.get_at(cords_new)
                            # if it is red then it must be a person
                            newCoords = self.map_data_to_gui_coords_offset(cord)
                            colour = self.display.get_at(newCoords)

                            # if it is coloured then it must be an object
                            if colour != (255, 255, 255, 255):
                                # Its an object of some kind
                                seenObj = self.data.what_object(cord, False)

                                obj.add_to_vision(seenObj)
                                obj.add_to_memory(seenObj)

                            if isinstance(seenObj, Wall):
                                break


                        except IndexError:
                            nothing = 0

    def home_menu(self):
        """Functtion that makes the menu screen with buttons all centred automaticly"""
        i = 0
        button_text = ["Run Simulation", "Builder", "Exit"]
        num_buttons = len(button_text)
        height_of_buttons = 50
        width_of_buttons = 300
        space_between = 10
        height_of_all_buttons = ((height_of_buttons + space_between)* num_buttons)
        position = self.centre([0,0,self.get_screen_width(),self.get_screen_height()],[width_of_buttons,height_of_all_buttons])
        option_1_x_coord = position[0]
        option_1_y_coord = position[1]
        for button in button_text:
            info = [option_1_x_coord, (option_1_y_coord + ((height_of_buttons + 10) * i)), width_of_buttons,height_of_buttons]
            colour = self.black
            # If statement that checks to see if the mouse is over the button
            if pygame.mouse.get_pos()[0] >= info[0] and pygame.mouse.get_pos()[0] <= info[0] + width_of_buttons and \
                    pygame.mouse.get_pos()[1] >= info[1] and pygame.mouse.get_pos()[1] <= info[1] + height_of_buttons:
                colour = self.red
                if pygame.mouse.get_pressed()[0]:
                    self.set_menu(button)
                    sleep(0.1)
                    # pygame.display.update()
            self.add_button(info, button, colour,50)
            i = i + 1
        return True

    def builder_menu(self):
        """
        This fucntion creates the build menu
        """
        i = 0
        # sleep(0.1)
        button_text = ["New", "Back", "Exit"]
        num_buttons = len(button_text)
        height_of_buttons = 50
        width_of_buttons = 300
        space_between = 10
        height_of_all_buttons = ((height_of_buttons + space_between) * num_buttons)
        position = self.centre([0, 0, self.get_screen_width(), self.get_screen_height()], [width_of_buttons, height_of_all_buttons])
        option_1_x_coord = position[0]
        option_1_y_coord = position[1]
        for button in button_text:
            info = [option_1_x_coord, (option_1_y_coord + ((height_of_buttons + 10) * i)), width_of_buttons,
                    height_of_buttons]
            colour = self.black
            if pygame.mouse.get_pos()[0] >= info[0] and pygame.mouse.get_pos()[0] <= info[0] + width_of_buttons and pygame.mouse.get_pos()[1] >= info[1] and pygame.mouse.get_pos()[1] <= info[1] + height_of_buttons:
                colour = self.red
                if pygame.mouse.get_pressed()[0]:
                    self.set_menu(button)
                    sleep(0.1)
                    # pygame.display.update()
            if button == "New" and pygame.mouse.get_pressed()[0]:
                self.get_map_data().clear_map()
            if self.get_load_name() and button == 'Load' and not self.get_text_done():
                self.user_text_input(info, colour)
            elif self.get_text_done() and button == 'Load':
                self.add_button(info,self.get_user_input_result(),self.green,50)
            else:
                self.add_button(info, button, colour, 50)
            i = i + 1

    def sim_menu(self):
        """
        This function creates the simulation menu
        """
        i = 0
        # sleep(0.1)
        button_text = ["Start","Floor Plan Load", "Back", "Exit"]
        num_buttons = len(button_text)
        height_of_buttons = 50
        width_of_buttons = 300
        space_between = 10
        height_of_all_buttons = ((height_of_buttons + space_between) * num_buttons)
        position = self.centre([0, 0, self.get_screen_width(), self.get_screen_height()], [width_of_buttons, height_of_all_buttons])
        option_1_x_coord = position[0]
        option_1_y_coord = position[1]
        for button in button_text:
            info = [option_1_x_coord, (option_1_y_coord + ((height_of_buttons + 10) * i)), width_of_buttons,
                    height_of_buttons]
            colour = self.black
            # If statement that checks to see if the mouse is over the button
            if pygame.mouse.get_pos()[0] >= info[0] and pygame.mouse.get_pos()[0] <= info[0] + width_of_buttons and pygame.mouse.get_pos()[1] >= info[1] and pygame.mouse.get_pos()[1] <= info[1] + height_of_buttons:
                colour = self.red
                if pygame.mouse.get_pressed()[0]:
                    self.set_menu(button)
                    sleep(0.1)
                    # pygame.display.update()
            if self.get_load_name() and button == 'Floor Plan Load' and not self.get_text_done():
                self.user_text_input(info, colour)
            elif self.get_text_done() and button == 'Floor Plan Load':
                self.add_button(info,self.get_user_input_result(),self.green,50)
                # self.load_map("map_saves",self.get_user_input_result())
            else:
                self.add_button(info, button, colour,50)
            i = i + 1

    def user_text_input(self,button_info, colour):
        """
        This function initilizes the user input of text and creates the box for it
        :param button_info: Coordinates, height and width
        :param colour: colour of the box
        """
        self.set_text_running(True)
        pygame.draw.rect(self.get_display(), colour, button_info, 2)
        button_text = self.text(self.get_user_input_result(),50)
        loaction = self.centre(button_info, [button_text[1], button_text[2]])
        self.get_display().blit(button_text[0], loaction)

    def save_map(self,file,save_name):
        """
        Saves the map t the map_saves.txt
        :param file: map_saves.txt
        :param save_name: the name that the current simulation watns to be saved as
        """
        map = self.get_map_data()
        map.export(file,save_name)

    def load_map(self,file,search):
        """
        Loads the map it is looking for
        :param file: maps_saves.txt
        :param search: the name of the file you are looking for
        :return: True if the file is found, False if it isn't
        """
        map = self.get_map_data()

        if self.nodes_generated == 0:
            self.nodes_generated = 1
            self.data.generate_nodes()

        result = map.import_from_file(file, search)
        if result:
            return True
        else:
            return False

    def error_page(self, message):
        """
        Creates an error page with a message on it
        :param message: The string message you want displayed, creates a button to go back to main menu
        """
        self.set_menu("error")
        text = self.text(message,50)
        loaction = self.centre([0, 0, self.get_screen_width(), self.get_screen_height()], [text[1], text[2]])
        self.get_display().blit(text[0], loaction)
        text = self.text("Back To Main Menu",50)
        position = self.centre([0, text[2]+10, self.get_screen_width(), self.get_screen_height()],[text[1],text[2]])
        info = [position[0], position[1], text[1]+5, text[2]+5]
        colour = self.black
        # Checks the mouse possition and changes it to red if the mouse is hovered over it and if clciked it runs the second if statement
        if pygame.mouse.get_pos()[0] >= info[0] and pygame.mouse.get_pos()[0] <= info[0]+ info[2] and pygame.mouse.get_pos()[1] >= info[1] and pygame.mouse.get_pos()[1] <= info[1] + info[3]:
            colour = self.red
            if pygame.mouse.get_pressed()[0]:
                #Sends the user back to the home menu
                self.set_home_menu()
                sleep(0.1)
        # Adds the button with the back or
        self.add_button(info, 'Back To Main Menu', colour,50)

    def new_build(self):
        """
        This creates a new builder map, the user can then select the buttons to add new ojects to the map
        :return: Null
        """
        self.set_build_active(True)
        self.draw_display()
        items = ['Wall','Bar','Toilet','D Floor','Remove']
        size = len(items)
        self.set_size_of_menu_buttons(size)
        button_width = (self.get_screen_width() / size)
        button_height = self.get_screen_height() * 0.1
        i = 1;
        current = self.get_current_tool()
        info = [0, self.get_screen_height() * 0.90, button_width,button_height]
        colour = self.black
        colour1 = self.black
        if self.in_area(pygame.mouse.get_pos(), info):
            colour = self.green

        self.add_button(info,current,colour,50)

        if pygame.mouse.get_pos()[0] >= info[0] and pygame.mouse.get_pos()[0] <= info[0] + info[2] and pygame.mouse.get_pos()[1] >= info[1] and pygame.mouse.get_pos()[1] <= info[1] + info[3] and pygame.mouse.get_pressed()[0]:
            self.set_new_tool()
            sleep(0.1)
        if self.get_new_tool():
            pygame.draw.rect(self.display, self.white, [0, (self.get_screen_height() * 0.90) - ((len(info) + 1) * button_height), button_width, button_height * (len(info) + 1)])
            for objectName in items:
                colour = self.red
                info = [0,(self.get_screen_height() * 0.90) - (i * button_height),button_width,button_height]
                if pygame.mouse.get_pos()[0] >= info[0] and pygame.mouse.get_pos()[0] <= info[0] + info[2] and pygame.mouse.get_pos()[1] >= info[1] and pygame.mouse.get_pos()[1] <= info[1] + info[3] and pygame.mouse.get_pressed()[0]:
                    colour = self.green
                    sleep(0.1)
                    self.set_current_tool(objectName)
                    self.set_new_tool()
                if self.get_current_tool() == objectName:
                    colour = self.green
                self.add_button(info,objectName,colour,50)
                i= i + 1

        info = [button_width, self.get_screen_height() - button_height, button_width, button_height]
        if self.in_area(pygame.mouse.get_pos(), info):
            colour1 = self.green
            if(pygame.mouse.get_pressed()[0]):
                self.set_save_active(True)
                self.set_save_name(True)
        self.add_button(info, "save", colour1, 50)

        # pygame.draw.rect(self.get_display(), self.green, info)

    def save(self):
        """Function that pulls up the save icon, it checks to see if the name is alread in use and then asks for a different name
        if not then it allows the save to be made"""
        cords = self.centre([0,0,self.get_screen_width(),self.get_screen_height()],[200,100])
        info = [cords[0],cords[1], 250,50]
        self.user_text_input(info,self.red)
        if not self.get_save_name():
            test_name = self.get_user_input_result()
            result = self.get_map_data().check_save_name("maps_saves",test_name)
            if result == True:
                print("Name is free")
                self.data.export("maps_saves",test_name)
                self.set_home_menu()
                self.set_save_active(False)

            else:
                self.clear_user_text()
                self.set_save_name(True)
                print("Name is taken")

    def object_colour(self, object):
        """
        This function returns what colour that object is, this is needed for the drag function beucase at that state it can't talk to the
        objects to find out their colours
        :param object: The object name
        :return: The colour of that object
        """
        object = object.lower()
        if object == "wall":
            return self.black
        if object == "bar":
            return self.blue
        if object == "toilet":
            return self.orange
        if object == "d floor":
            return self.red

    def create_heatmap(self):
        heatmap = self.get_heatmap()
        x_running, y_running = self.get_offset()
        y_running_save = y_running
        num_x = self.get_sim_screen_width()
        num_y = self.get_sim_screen_height()
        for x in range(num_x):
            y = 0
            y_list = []
            for y in range(num_y):
                y_list.append(0)
            heatmap.append(y_list)


    def add_heatmap(self,coord):
        """Ittorates the number of times that a person has been on that pixel on the screen"""
        x_index, y_index = self.gui_to_map_data_coords_offset(coord)
        heatmap = self.heat_map
        heatmap[x_index][y_index] = heatmap[x_index][y_index] + 1

    def show_heatmap(self):
        max_heat_value = 0
        min_heat_value = 100000
        heat_map = self.get_heatmap()
        average_heat = []
        size_of_square = 10
        screen_width = self.get_sim_screen_width()
        screen_height = self.get_sim_screen_height()

        for x in range(math.floor(len(heat_map)/size_of_square)):
            y_list = []
            for y in range(math.floor(len(heat_map[x])/size_of_square)):
                sum_total = 0
                for x1 in range(size_of_square):
                    y1 = 0
                    current_x = (x * size_of_square) + x1
                    for y1 in range(size_of_square):
                        current_y = (y * size_of_square) + y1
                        if not heat_map[current_x][current_y] == 0:
                            sum_total = sum_total + heat_map[current_x][current_y]
                average = sum_total / (size_of_square * size_of_square)
                if average < min_heat_value:
                    min_heat_value = average
                if average > max_heat_value:
                    max_heat_value = average
                y_list.append(average)
            average_heat.append(y_list)

        x_offset, y_offset = self.get_offset()
        for x_show in range(len(average_heat)):
            for y_show in range(len(average_heat[x_show])):
                value = average_heat[x_show][y_show]
                if not value == 0.0:
                    show_x_coord = x_offset + (x_show * size_of_square)
                    show_y_coord = y_offset + (y_show * size_of_square)
                    info = [show_x_coord, show_y_coord, size_of_square, size_of_square]
                    colour = self.colour_picker(min_heat_value,max_heat_value,value)
                    pygame.draw.rect(self.get_display(), colour, info)


    def colour_picker(self,min_value,max_value,value):
        EPSILON = sys.float_info.epsilon
        colours = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]
        i_f = float(value - min_value) / float(max_value - min_value) * (len(colours) - 1)
        i, f = int(i_f // 1), i_f % 1
        if f < EPSILON:
            return colours[i]
        else:
            (r1, g1, b1), (r2, g2, b2) = colours[i], colours[i + 1]
            return (int(r1 + f * (r2 - r1)), int(g1 + f * (g2 - g1)), int(b1 + f * (b2 - b1)))

    def gui_to_map_data_coords_offset(self,coords):
        oldx, oldy = coords
        offset_x, offset_y = self.get_offset()
        new_cords = (oldx - offset_x, oldy - offset_y)
        return new_cords

    def map_data_to_gui_coords_offset(self,coords):
        oldx, oldy = coords
        offset_x, offset_y = self.get_offset()
        new_cords = (oldx + offset_x, oldy + offset_y)
        return new_cords

    def need_bar(self, needName, value, box_info):
        pygame.draw.rect(self.get_display(),self.red,[box_info[0],(box_info[1] + box_info[3]) - (box_info[3] / 5),box_info[2],box_info[3]/5])
        x_coord = (box_info[2]/100) * value
        pygame.draw.rect(self.get_display(),self.green,[0, (box_info[1] + box_info[3]) - (box_info[3] / 5), x_coord,box_info[3]/5])

    def in_area(self, coords, box_info):
        if coords[0] >= box_info[0] and coords[0] <= box_info[0]+ box_info[2]:
            if coords[1] >= box_info[1] and coords[1] <= box_info[1]+ box_info[3]:
                return True
            else:
                return False
        else:
            return False

    def menu_bar(self):
        button_names = ["Home", "Pause", "Add Person", "Show Nodes","Heat Map"]
        height_of_button = self.get_screen_height() / 10
        width_of_button = self.get_screen_width() / 8
        start_coords = [1,self.get_screen_height() - height_of_button - 1]
        x = 0
        colour = self.black
        self.menu_bar_info = [start_coords[0],start_coords[1], len(button_names) * width_of_button, height_of_button, len(button_names)]
        for button in button_names:
            if self.pause_toggle == True and x == 1:
                colour == self.green
            info = [start_coords[0] + (x * width_of_button), start_coords[1], width_of_button, height_of_button]
            self.add_button(info, button, colour, 30)
            x = x + 1

    def menu_option(self, option):
        if option == 0:
            self.set_home_menu()
            self.menu_bar_clicked = None
        elif option == 1:
            self.set_pause()
            self.menu_bar_clicked = None
        elif option == 2:
            self.set_add_person_on_click()
            self.menu_bar_clicked = None
        elif option == 3:
            self.show_nodes = not self.show_nodes
            self.menu_bar_clicked = None
        elif option == 4:
            self.set_selected_person(None)
            self.set_pause()
            self.set_show_heatmap_toggle()
            self.menu_bar_clicked = None


    def node_icon(self, coord):
        x, y = coord
        top_coord = (x , y - 5)
        bottom_coord = (x, y + 5)
        left_coord = (x - 5, y)
        right_coord = (x + 5, y)
        pygame.draw.line(self.get_display(),self.purple,top_coord,left_coord)
        pygame.draw.line(self.get_display(),self.purple,left_coord,bottom_coord)
        pygame.draw.line(self.get_display(),self.purple,bottom_coord,right_coord)
        pygame.draw.line(self.get_display(),self.purple,right_coord,top_coord)
        pygame.draw.line(self.get_display(),self.purple,top_coord,bottom_coord)
        pygame.draw.line(self.get_display(),self.purple,left_coord,right_coord)

    def draw_path(self, coords):
        end_of_line = len(coords)
        index = 0
        x_offset, y_offset = self.get_offset()
        if self.current_route == []:
            self.current_route = coords
        while index < end_of_line:
            x, y  = coords[index]
            start_line = (x + x_offset, y + y_offset)
            if not index + 1 == end_of_line:
                x1, y1 = coords[index + 1]
                finish_line = (x1 + x_offset, y1 + y_offset)
                pygame.draw.line(self.get_display(), self.purple, start_line, finish_line,2)
            index = index + 1



    def get_map_data(self):
        return self.data

    def set_map_data(self,value):
        self.data = value

    def get_menu_select(self):
        return self.show_menu

    def get_pause(self):
        return self.pause

    def set_pause(self):
        self.pause = not self.pause

    def set_pause_must(self, value):
        self.pause = value

    def get_screen_width(self):
        return self.screen_width

    def get_screen_height(self):
        return self.screen_height

    def get_display(self):
        return self.display

    def get_running_map_data_loc(self):
        return self.running_map_data_loc

    def set_running_map_data_loc(self, value):
        self.running_map_data_loc = value

    def set_load_name(self,value):
        self.load_name = value

    def get_load_name(self):
        return self.load_name

    def get_user_input_result(self):
        return self.user_input_result

    def set_user_input_result(self, value):
        self.user_input_result = value

    def set_text_done(self,value):
        self.text_done = value

    def get_text_done(self):
        return self.text_done

    def set_text_running(self,value):
        self.text_running = value

    def get_text_running(self):
        return self.text_running

    def get_error(self):
        return self.error

    def set_error(self):
        self.error = not self.error

    def get_menu(self):
        return self.menu

    def set_menu(self, value):
        menu = self.get_menu()
        new_menu = [menu[1],value]
        self.menu = new_menu

    def set_home_menu(self):
        new_menu = [None, "home"]
        self.menu = new_menu
        self.user_input_result = ""
        self.save_name = False
        self.load_name = False
        self.text_running = False
        self.text_done = False
        self.builder_active = False
        self.clear_heat_map()
        self.show_nodes = False

    def get_exit(self):
        return self.exit

    def set_exit(self):
        self.exit = not self.exit

    def set_error_message(self, value):
        self.error_message = value

    def get_error_message(self):
        return self.error_message

    def get_build_active(self):
        return self.builder_active

    def set_build_active(self, value):
        self.builder_active = value

    def get_xCord1(self):
        return self.xCrod1

    def get_yCord1(self):
        return self.yCord1

    def set_xCord1(self, value):
        self.xCrod1 = value

    def set_yCord1(self, value):
        self.yCord1 = value

    def get_drag(self):
        return self.drag

    def set_drag(self,value):
        self.drag = value

    def get_width(self):
        return self.width

    def set_width(self,value):
        self.width = value

    def get_height(self):
        return self.height

    def set_height(self,value):
        self.height = value

    def get_save_active(self):
        return self.save_active

    def set_save_active(self, value):
        self.save_active = value

    def clear_user_text(self):
        self.user_input_result = ""

    def get_save_name(self):
        return self.save_name

    def set_save_name(self, value):
        self.save_name = value

    def get_current_tool(self):
        return self.current_tool

    def set_current_tool(self, value):
        self.current_tool= value

    def get_add_person_on_click(self):
        return self.add_person_on_click

    def set_add_person_on_click(self):
        self.add_person_on_click= not self.add_person_on_click

    def get_tick_rate(self):
        """
        Function gets the tick rate
        :return: tick_rate
        """
        return self.tick_rate

    def get_heatmap(self):
        return self.heat_map

    def clear_heat_map(self):
        self.heat_map = []

    def get_show_heatmap_toggle(self):
        return  self.show_heatmap_toggle

    def set_show_heatmap_toggle(self):
        self.show_heatmap_toggle = not self.show_heatmap_toggle

    def get_new_tool(self):
        return self.new_tool

    def set_new_tool(self):
        self.new_tool = not self.new_tool

    def set_size_of_menu_buttons(self, value):
        self.size_of_menu_buttons = value

    def get_size_of_menu_buttons(self):
        return self.size_of_menu_buttons

    def set_offset(self, value):
        self.offset = value

    def get_offset(self):
        return self.offset

    def get_sim_screen_height(self):
        return self.sim_screen_height

    def get_sim_screen_width(self):
        return self.sim_screen_width

    def set_selected_person(self,value):
        self.selected_person = value

    def get_selected_person(self):
        return self.selected_person

    def set_size_info_pannel(self, value):
        self.size_info_pannel = value

    def get_size_info_pannel(self):
        return self.size_info_pannel

    def get_x1_first_click(self):
        return self.x1_first_click

    def set_x1_first_click(self, value):
        self.x1_first_click = value

    def get_startAmount_of_need(self):
        return self.startAmount_of_need

    def set_startAmount_of_need(self, value):
        self.startAmount_of_need = value

    def get_new_value_for_need(self):
        return self.new_value_for_need

    def set_new_value_for_need(self, value):
        self.new_value_for_need = value

    def get_dragging_bar(self):
        return self.dragging_bar

    def set_dragging_bar(self):
        self.dragging_bar = not self.dragging_bar

    def get_selected_button(self):
        return self.selected_button

    def set_selected_button(self, value):
        self.selected_button = value

    def get_temp_width(self):
        return self.temp_width

    def set_temp_width(self, value):
        self.temp_width = value