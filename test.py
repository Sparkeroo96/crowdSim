"""
The main GUI that creates the display and runs the code for the system

Created by Chris Clark cc604
Modified by Sam Parker swp5
"""
import pygame
import math
from Data import map_data
from time import sleep

print("in maps_saves.py")


class RunningMain:

    data = None

    # RGB Colours defined
    white = (255,255,255)
    black = (0,0,0)
    green = (51, 204, 51)
    red = (255, 0, 0)

    exit = False

    # Menu flags
    display = None
    pause = None
    menu = [None,"home"]
    load_name = False
    load_name_result = ''
    running_map_data_loc = ""
    text_done = False
    text_running = False
    error = False
    # Size of the screen
    screen_width = 800
    screen_height = 600

    #Error message
    error_message = ""

    def __init__(self):
        """This is the constructor that starts the main loop of the simulation"""
        #Starts the pygame
        pygame.init()
        #Gets the location for the map data
        self.set_map_data(map_data.map_data(self))
        # Creates a display to the size of the screen
        self.display = pygame.display.set_mode((self.get_screen_width(),self.get_screen_height()))
        # Adds name for the application
        pygame.display.set_caption("Crowd Simulation ")
        # Starts a clock that manages the ticks
        clock = pygame.time.Clock()
        # Flag for checking if the map loaded correclty
        success = False
        # Main loop for the applicaion
        while not self.get_exit():
            # This gets all the key presses and mouse movements and passes them as events
            for event in pygame.event.get():
                # Quit Function
                if event.type == pygame.QUIT:
                    self.set_exit()
                    # Pause function
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                #This is the code manages the user text imput
                if self.get_text_running() and event.type == pygame.KEYDOWN:
                    #Removes the last charater in the string
                    if event.key == pygame.K_BACKSPACE:
                        if self.get_load_name():
                            text = self.get_load_name_result()
                            text = text[:-1]
                            self.set_load_name_result(text)
                    # Sets the text done flag to true so the simultion can then load it
                    elif event.key == pygame.K_RETURN:
                        self.set_text_done(True)
                        self.set_text_running(False)

                        if self.get_load_name():
                            self.set_load_name(False)
                    # This is any other charactor and adds it to the running string for the user imput so it can be displayed
                    else:
                        if self.get_load_name():
                            running = self.get_load_name_result()
                            new_running = running + event.unicode
                            self.set_load_name_result(new_running)
            # Resets the display to white each tick so a new information can be displayed
            self.get_display().fill(self.white)
            # Function that runs the main program
            self.key_buttons()
            menu = self.get_menu()
            # Shows the first menu screen
            if menu[1] == "home":
                self.home_menu()
            # Displays the simulation option menu
            elif menu[1] == "Run Simulation":
                self.sim_menu()

                #Checks to see if the text is completed if so then it loads that building floor plan
                if self.get_text_done():
                    search = self.get_load_name_result()
                    success = self.load_map('maps_saves', search)
                    self.set_text_done(False)
            # This checks to see if it is on the simulation menu options
            elif menu[0] == "Run Simulation":
                # Running the simulation that is chosen or the default one
                if menu[1] == "Start":
                    # Gets the map from map data
                    objectArray = self.data.get_map()
                    # if it is empty then it loads the default
                    if objectArray == []:
                        self.data.export("maps_saves","default")
                    elif success:
                        # If there was a succesful load then it uses the user chosen one
                        self.draw_display()
                    else:
                        # Error management to see if it loads correct
                        print("loading defult")
                        self.draw_display()
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
                # loads a map that the user can edit
                if menu[1] == "Load":
                    print("load")
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

            pygame.display.update()
            clock.tick(30)
        pygame.quit()
        quit()


    def add_button(self,button_info, text, colour):
        """Adds a button to the screen with a given dimention and text inside and adds it to the display
        :param button_info, is the coordiate and size info
        :param text, is the text that is going inside the box
        :param colour, is the colour of the box
        """
        pygame.draw.rect(self.get_display(),colour,button_info,2)
        button_text = self.text(text)
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

    def text(self,text):
        """ This function creates a text object in pygame and returns the size of the text
        :param text: the string that is to be displayed
        :return: The text object and the height and width for further calucaltions
        """
        pygame.font.init()
        my_font = pygame.font.SysFont("Comic Sans MS", 50)
        text_surface = my_font.render(text, False, self.black)
        return [text_surface,my_font.size(text)[0],my_font.size(text)[1]]

    def key_buttons(self):
        """
        This function handeles the button presses in pygame, save, pause and creation of walls
        """
        while self.get_pause():
            for event in pygame.event.get():
                # print(event)
                #Pauses sim
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    #Allows wall adding
                    if event.key == pygame.K_w:
                        print("making wall")
                        wall = True
                    if event.key == pygame.K_s:
                        self.data.export("maps_saves","test_s_Button")
                 # Gets the starting cordinates for the walls
                if event.type == pygame.MOUSEBUTTONDOWN and wall:
                    x1, y1 = event.pos
                    drag = True
                # gets the width and height for the walls and creates the obj
                if event.type == pygame.MOUSEBUTTONUP and wall:
                    x2, y2 = event.pos
                    width = x1 - x2
                    width = width * -1
                    height = y1 - y2
                    height = height * -1
                    self.data.add_wall_to_map([x1,y1],width,height)
                    pygame.draw.rect(self.display,self.black,[x1,y1,width,height])
                    pygame.display.update()
                    drag = not drag
                # quits if x button is pressed
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def draw_display(self):
        """
        Draws the display
        :param display: The pygame display
        :param objectArray: The objects that you wish to draw
        :return:
        """
        # self.display.fill(self.white)
        # Goes though the map array obj
        objectArray = self.data.get_map()
        for obj in objectArray:
            obj.action()
            coordinates = obj.get_coordinates()
            angle = obj.get_angle()
            width = obj.get_width()
            colour = obj.get_colour()
            # print(obj.get_coordinates())
            shape = obj.get_shape()
            # print("shape = " + shape)
            # the process of adding a person and the funcitons that get called
            if shape == "circle":
                # Creating the cicle with the variables provided
                pygame.draw.circle(self.display, colour, coordinates, round(width / 2))
                # Maths to add the pixcels to represent the eyes
                eyes = obj.person_eyes(obj.coordinates, obj.angle, round(obj.width / 2))
                self.display.set_at((eyes[0][0], eyes[0][1]), self.white)
                self.display.set_at((eyes[1][0], eyes[1][1]), self.white)
                # print(vision)
                # print(objectArray)

            elif shape == "rectangle":
                # objects
                height = obj.get_height()
                coordinates = obj.get_coordinates()
                width = obj.get_width()
                pygame.draw.rect(self.display, self.black, [coordinates[0], coordinates[1], width, height])

        for obj in objectArray:
            if obj.get_shape() == "circle":
                # Calls the person vision function that returns an array of all the cordinates on the vision lines it makes
                vision = obj.personVision(obj.coordinates[0], obj.coordinates[1], obj.angle)
                # clears the person vision from the previous ittoration
                obj.clear_vision()
                # goes though every coordinates and works out what colour is in that pixcel
                for cord in vision:
                    # display.set_at((cord[0],cord[1]), black)
                    # try and catch to prevent out of array exceptions
                    try:
                        # gets the colour at the cordiate
                        colour = self.display.get_at((cord[0], cord[1]))
                        # if it is red then it must be a person
                        if colour == (255, 0, 0, 255):  # Red person
                            # calls a function that returns the id of the person they can see
                            whichPerson = self.data.whichPerson(cord)
                            # adds to the persons vision array in their obj
                            obj.add_to_vision(whichPerson)
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
                    pygame.display.update()
            self.add_button(info, button, colour)
            i = i + 1
        return True

    def builder_menu(self):
        """
        This fucntion creates the build menu
        """
        i = 0
        # sleep(0.1)
        button_text = ["New", "Load", "Back", "Exit"]
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
                    pygame.display.update()
            self.add_button(info, button, colour)
            i = i + 1

    def sim_menu(self):
        """
        This function creates the simulation menu
        """
        i = 0
        # sleep(0.1)
        button_text = ["Start","Floor Plan Load", "Options", "Back", "Exit"]
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
                    pygame.display.update()
            if self.get_load_name() and button == 'Floor Plan Load' and not self.get_text_done():
                self.user_text_input(info, colour)
            elif self.get_text_done() and button == 'Floor Plan Load':
                self.add_button(info,self.get_load_name_result(),self.green)
            else:
                self.add_button(info, button, colour)
            i = i + 1

    def user_text_input(self,button_info, colour):
        """
        This function initilizes the user input of text and creates the box for it
        :param button_info: Coordinates, height and width
        :param colour: colour of the box
        """
        self.set_text_running(True)
        pygame.draw.rect(self.get_display(), colour, button_info, 2)
        button_text = self.text(self.get_load_name_result())
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
        text = self.text(message)
        loaction = self.centre([0, 0, self.get_screen_width(), self.get_screen_height()], [text[1], text[2]])
        self.get_display().blit(text[0], loaction)
        text = self.text("Back To Main Menu")
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
        self.add_button(info, 'Back To Main Menu', colour)

    def get_map_data(self):
        return self.data

    def set_map_data(self,value):
        self.data = value

    def get_menu_select(self):
        return self.show_menu

    def get_pause(self):
        return self.pause

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

    def get_load_name_result(self):
        return self.load_name_result

    def set_load_name_result(self, value):
        self.load_name_result = value

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

    def get_exit(self):
        return self.exit

    def set_exit(self):
        self.exit = not self.exit

    def set_error_message(self, value):
        self.error_message = value

    def get_error_message(self):
        return self.error_message