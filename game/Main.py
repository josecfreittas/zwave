import pygame
from Map import *
from Heart import *
from Player import *

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

    ## hearts of bases ##
    heart = {
        "blue": None,
        "orange": None,
    }


    ## constructor ##
    def __init__(self, scale = 1, width = 1024, height = 512):

        ## set init values ##
        self.view["scale"] = scale
        self.view["width"] = width
        self.view["height"] = height
        self.view["x"] = 0
        self.view["y"] = 1450
        self.tick = 60
        self.frame = 0

        ## set pygame screen ##
        self.screen = pygame.display.set_mode((self.view["width"], self.view["height"]))
        
        ## make map ##
        self.map = Map(self)

        ## make base hearts ##
        self.heart["blue"] = Heart(self, 'blue')
        self.heart["orange"] = Heart(self, 'orange')

        ## make player ##
        self.player = Player(self, '02')

        ## init game loop ##
        self.loop()

    def move(self):

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

            ## call method responsible for move view to new destiny, if one exists ##
            self.move()

            ## update game map ##
            self.map.update()

            ## update base hearts ##
            self.heart["blue"].update()
            self.heart["orange"].update()

            ## update player ##
            self.player.update()

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
