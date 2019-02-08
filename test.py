"""
The main GUI that creates the display and runs the code for the system

Created by Chris Clark cc604
Modified by Sam Parker swp5
"""
import pygame
import math
from Data import map_data
from time import sleep
from People.person import Person


class RunningMain:

    data = None

    # RGB Colours defined
    white = (255,255,255)
    black = (0,0,0)
    green = (51, 204, 51)
    red = (255, 0, 0)

    # Menu flags
    display = None
    pause = None
    show_menu = True
    menu_option = None
    build_menu_option = None
    sim_menu_option = None
    show_sim_menu = True
    load_name = False
    load_name_result = ''
    running_map_data_loc = ""
    text_done = False
    text_running = False

    screen_width = 500
    screen_height = 500

    tick_rate = 120

    def __init__(self):
        pygame.init()
        # self.data = map_data.map_data(self)
        self.set_map_data(map_data.map_data(self, self.tick_rate))
        # Getting intial data to start the main loop for the simulation method
        self.display = pygame.display.set_mode((self.get_screen_width(),self.get_screen_height()))
        pygame.display.set_caption("Crowd Simulation ")
        self.set_sim_menu_option("")
        self.set_build_menu_option("")
        self.set_menu_option("")
        clock = pygame.time.Clock()
        exit = False

        # Main loop for the applicaion

        while not exit:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = not self.pause

                if self.get_text_running() and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if self.get_load_name():
                            text = self.get_load_name_result()
                            text = text[:-1]
                            self.set_load_name_result(text)

                    elif event.key == pygame.K_RETURN:
                        self.set_text_done(True)
                        self.set_text_running(False)

                        if self.get_load_name():
                            self.set_load_name(False)

                    else:
                        if self.get_load_name():
                            running = self.get_load_name_result()
                            new_running = running + event.unicode
                            self.set_load_name_result(new_running)


            self.get_display().fill(self.white)
            # Function that runs the main program
            self.key_buttons()
            # print(self.get_sim_menu_option())
            if self.get_menu_select():
                self.menu(event)

            elif self.get_menu_option() == "Run Simulation":
                if self.get_show_sim_menu() == True:
                    self.sim_menu(event)

                if self.get_sim_menu_option() == "Start":
                    objectArray = self.data.get_map()
                    if objectArray == []:
                        objectArray = self.data.map_default()
                        print(self.data.export("maps_saves","Test1"))
                    else:
                        self.draw_display()

                if self.get_sim_menu_option() == "Floor Plan Load":
                    self.data.clear_map()
                    self.set_load_name(True)
                    if self.get_text_done():
                        search = self.get_load_name_result()
                        self.load_map('maps_saves',search)
                        self.set_sim_menu_option("")

                if self.get_sim_menu_option() == "Options":
                    print("options")

                if self.get_sim_menu_option() == "Back":
                    self.set_menu_option("")
                    self.set_show_menu()
                    self.set_sim_menu_option("")

                elif self.get_sim_menu_option() == "Exit":
                    exit = True

            elif self.get_menu_option() == "Builder":
                self.builder_menu(event)
                if self.get_build_menu_option() == "New":
                    self.new_build()

                elif self.get_build_menu_option() == "Load":
                    print("load")

                elif self.get_build_menu_option() == "Back":
                    self.set_menu_option("")
                    self.set_show_menu()
                    self.set_build_menu_option("")

                elif self.get_build_menu_option() == "Exit":
                    exit = True

            elif self.get_menu_option() == "Exit":
                exit = True

            pygame.display.update()
            clock.tick(self.tick_rate)

        pygame.quit()
        quit()

    def clear_menu_flags(self):
        self.set_build_menu_option("")
        self.set_menu_option("")
        self.set_sim_menu_option("")

    def add_button(self,button_info, text, colour):
        pygame.draw.rect(self.get_display(),colour,button_info,2)
        button_text = self.text(text)
        loaction = self.centre(button_info,[button_text[1],button_text[2]])
        self.get_display().blit(button_text[0], loaction)

    def centre(self,box,text):
        box_x = box[0]
        box_y = box[1]
        box_width = box[2]
        box_height = box[3]
        text_width = text[0]
        text_height = text[1]

        half_box_width = math.floor(box_width/2)
        half_text_width = math.floor(text_width/2)
        chaneg_in_x = half_box_width - half_text_width
        x_coord = box_x + chaneg_in_x

        half_box_height = math.floor(box_height / 2)
        half_text_height = math.floor(text_height / 2)
        chaneg_in_y = half_box_height - half_text_height
        y_coord = box_y + chaneg_in_y

        text_location = (x_coord,y_coord)
        return text_location

    def text(self,text):
        pygame.font.init()
        my_font = pygame.font.SysFont("Comic Sans MS", 50)
        text_surface = my_font.render(text, False, self.black)
        return [text_surface,my_font.size(text)[0],my_font.size(text)[1]]

    def key_buttons(self):
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
            shape = obj.get_shape()
            # print("shape = " + shape)
            # the process of adding a person and the funcitons that get called
            if shape == "circle":
                # Creating the cicle with the variables provided
                pygame.draw.circle(self.display, colour, coordinates, round(width / 2))
                # Maths to add the pixcels to represent the eyes
                eyes = obj.person_eyes(coordinates, angle, round(width / 2))
                self.display.set_at((eyes[0][0], eyes[0][1]), self.white)
                self.display.set_at((eyes[1][0], eyes[1][1]), self.white)
                # print(vision)
                # print(objectArray)

            elif shape == "rectangle":
                # objects
                height = obj.get_height()
                pygame.draw.rect(self.display, colour, [coordinates[0], coordinates[1], width, height])
            elif shape == "wall":
                height = obj.get_height()
                # print(angle, width, height)
                pygame.draw.rect(self.display, colour, [coordinates[0], coordinates[1], width, height])
            elif shape == "dancefloor":
                height = obj.get_height()
                pygame.draw.rect(self.display, colour, [coordinates[0], coordinates[1], width, height], 1)

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

                for cord in vision:
                    # display.set_at((cord[0],cord[1]), black)
                    # try and catch to prevent out of array exceptions
                    try:
                        seenObj = 0
                        colour = self.display.get_at((cord[0], cord[1]))
                        # if it is red then it must be a person
                        if colour != (255, 255, 255, 255):
                            # Its an object of some kind
                            seenObj = self.data.what_object(cord)

                            obj.add_to_vision(seenObj)
                            obj.add_to_memory(seenObj)


                    except IndexError:
                        nothing = 0


    def get_tick_rate(self):
        """
        Function gets the tick rate
        :return: tick_rate
        """
        return self.tick_rate

    def menu(self,event):
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
            if pygame.mouse.get_pos()[0] >= info[0] and pygame.mouse.get_pos()[0] <= info[0] + width_of_buttons and pygame.mouse.get_pos()[1] >= info[1] and pygame.mouse.get_pos()[1] <= info[1] + height_of_buttons:
                colour = self.red
                clicked = False
                if pygame.mouse.get_pressed()[0] and self.get_menu_option() is not None:
                    clicked = True
                if clicked:
                    self.wait()
                    self.set_menu_option(button)
                    self.set_show_menu()
                    pygame.display.update()
            self.add_button(info,button,colour)
            i = i + 1

    def builder_menu(self,event):
        i = 0
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
                clicked = False
                if pygame.mouse.get_pressed()[0] and self.get_build_menu_option() is not None:
                    clicked = True
                if clicked:
                    self.wait()
                    self.set_build_menu_option(button)
                    pygame.display.update()
            self.add_button(info, button, colour)
            i = i + 1

    def sim_menu(self,event):
        i = 0
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
                clicked = False
                if pygame.mouse.get_pressed()[0] and self.get_sim_menu_option() is not None:
                    clicked = True
                if clicked:
                    self.wait()
                    self.set_sim_menu_option(button)
                    if button == "Start":
                        self.set_sim_show_menu()
                    pygame.display.update()
            # print(self.get_load_name())
            # print(self.get_text_done())
            if self.get_load_name() and button == 'Floor Plan Load' and not self.get_text_done():
                self.user_text_input(event, info, colour)
            elif self.get_text_done() and button == 'Floor Plan Load':
                self.add_button(info,self.get_load_name_result(),self.green)
            else:
                self.add_button(info, button, colour)
            i = i + 1

    def user_text_input(self,event,button_info, colour):
        self.set_text_running(True)
        pygame.draw.rect(self.get_display(), colour, button_info, 2)
        button_text = self.text(self.get_load_name_result())
        loaction = self.centre(button_info, [button_text[1], button_text[2]])
        self.get_display().blit(button_text[0], loaction)


    def wait(self):
        sleep(0.1)

    def new_build(self):
        print("building new")

    def start_sim(self):
        if self.get_running_map_data_loc() == "":
            print("No map selected, please load one")
        else:
            map = self.get_map_data()

    def save_map(self,file,save_name):
        map = self.get_map_data()
        map.export(file,save_name)

    def load_map(self,file,search):
        map = self.get_map_data()
        map.import_from_file(file, search)

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

    def set_sim_show_menu(self):
        self.show_sim_menu = not self.show_sim_menu

    def get_show_sim_menu(self):
        return self.show_sim_menu

    def set_show_menu(self):
        self.show_menu = not self.show_menu

    def set_menu_option(self, value):
        self.menu_option = value

    def get_menu_option(self):
        return self.menu_option

    def set_build_menu_option(self, value):
        self.build_menu_option = value

    def get_build_menu_option(self):
        return self.build_menu_option

    def set_sim_menu_option(self, value):
        self.sim_menu_option = value

    def get_sim_menu_option(self):
        return self.sim_menu_option

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
