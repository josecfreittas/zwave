import pygame

from zwave.map import *
from zwave.signal import *
from zwave.player import *

class Main:
    
    ## pygame screen ##
    screen = None

    ## pygame tick number ##
    tick = None

    ## game frame [0-tick] ##
    frame = None

    ## game view ##
    view = {
        "scale": None,
        "width": None,
        "height": None,
        "x": None,
        "y": None,
        "last_x": None,
        "last_y": None,
    }

    ## target to change game view change ##
    mouse = {
        "x": None,
        "y": None,
        "relative-x": None,
        "relative-x": None,
        "x-way": None,
        "y-way": None,
    }

    ## map of game ##
    map = None

    ## player ##
    player = None

    ## signals of bases ##
    signal = {
        "blue": None,
        "orange": None,
    }


    ## constructor ##
    def __init__(self, scale = 1, width = 1024, height = 512):

        ## set init values ##
        self.view["scale"] = scale
        self.view["width"] = width
        self.view["height"] = height
        self.tick = 60
        self.frame = 0
        self.mouse['x'] = 0
        self.mouse['y'] = 0

        ## set pygame screen ##
        self.screen = pygame.display.set_mode((self.view["width"], self.view["height"]))
        
        ## make map ##
        self.map = Map(self)

        ## make base signals ##
        self.signal["north"] = Signal(self, 'north')
        self.signal["south"] = Signal(self, 'south')

        ## make player ##
        self.player = Player(self, '02')

        ## screen center (player position in map) ##
        self.view["x"] = (self.map.view["width"] / 2) - (self.view["width"] / 2)
        self.view["y"] = (self.map.view["height"] / 2) - (self.view["height"] / 2)

        ## init game loop ##
        self.loop()

    ## method to player/screen movimentation ##
    def move(self):

        ## check if had collision, if had, set last position of view ##
        if self.player.check_collision("wall"):
            self.view["x"] = self.view["last_x"]
            self.view["y"] = self.view["last_y"]

        ## save current positon of view for future use ##
        self.view["last_x"] = self.view["x"]
        self.view["last_y"] = self.view["y"]

        ## make 'keys' variable with pressed keys
        keys = pygame.key.get_pressed()

        ## speed to axes in diagonal movement ##
        if (keys[pygame.K_w] or keys[pygame.K_s]) and (keys[pygame.K_a] or keys[pygame.K_d]):
            velocity = 1.5

        ## speed to axes in horizontal and vertical movements ##
        else:
            velocity = 2

        ## movement according to keys down ##
        if keys[pygame.K_w]:
            self.view["y"] -= velocity
        if keys[pygame.K_s]:
            self.view["y"] += velocity
        if keys[pygame.K_a]:
            self.view["x"] -= velocity
        if keys[pygame.K_d]:
            self.view["x"] += velocity


    ## method from game loop ##
    def loop(self):

        ## set pygame clock ##
        clock = pygame.time.Clock()

        running = True
        while running:

            ## update game map ##
            self.map.update()

            ## update base signals ##
            self.signal["north"].update()
            self.signal["south"].update()

            ## update player ##
            self.player.update()

            ## call method responsible for move view to new destiny, if one exists ##
            self.move()

            ## update pygame screen ##
            pygame.display.update()

            ## mouse x position ##
            self.mouse["x"] = pygame.mouse.get_pos()[0]

            ## mouse y position ##
            self.mouse["y"] = pygame.mouse.get_pos()[1]

            ## events hunter ##
            for event in pygame.event.get():

                ## qui event ##
                if event.type == pygame.QUIT:
                    running = False

            ## increment or reset atual frame ##
            self.frame = (self.frame + 1) if self.frame < self.tick else 0

            ## pygame clock tick ##
            clock.tick(self.tick)
