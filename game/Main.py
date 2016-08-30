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
    destiny = {
        "x": None,
        "y": None,
        "x-way": None,
        "y-way": None,
        "x_velocity": None,
        "y_velocity": None,
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

    def move_to_destiny(self):
        if (self.destiny['x'] > 0) and (self.destiny['y'] > 0):
            if self.destiny['x'] > self.destiny['y']:
                diference = float(self.destiny['x']) / float(self.destiny['y'])
                self.destiny['x_velocity'] = 2 - (2 / diference)
                self.destiny['y_velocity'] = 2 / diference
            else:
                diference = float(self.destiny['y']) / float(self.destiny['x'])
                self.destiny['x_velocity'] = 2 / diference
                self.destiny['y_velocity'] = 2 - (2 / diference)

        else:
            self.destiny['x_velocity'] = 2
            self.destiny['y_velocity'] = 2

        if self.destiny['x'] > 0:
            self.destiny['x'] = self.destiny['x'] - self.destiny['x_velocity']
            if self.destiny['x-way'] == 'left':
                self.view["x"] = self.view["x"] - self.destiny['x_velocity']
            else:
                self.view["x"] = self.view["x"] + self.destiny['x_velocity']

        if self.destiny['y'] > 0:
            self.destiny['y'] = self.destiny['y'] - self.destiny['y_velocity']
            if self.destiny['y-way'] == 'top':
                self.view["y"] = self.view["y"] - self.destiny['y_velocity']
            else:
                self.view["y"] = self.view["y"] + self.destiny['y_velocity']

    ## method from game loop ##
    def loop(self):

        ## set pygame clock ##
        clock = pygame.time.Clock()

        running = True
        while running:

            ## call method responsible for move view to new destiny, if one exists ##
            self.move_to_destiny()

            ## update game map ##
            self.map.update()

            ## update base hearts ##
            self.heart["blue"].update()
            self.heart["orange"].update()

            ## update player ##
            self.player.update()

            ## update pygame screen ##
            pygame.display.update()

            ## events hunter ##
            for event in pygame.event.get():

                ## qui event ##
                if event.type == pygame.QUIT:
                    running = False

                ## click event ##
                if event.type == pygame.MOUSEBUTTONDOWN:

                    ## check which side of the x-axis was the click ##
                    ## if left ##
                    if pygame.mouse.get_pos()[0] < (self.view["width"] / 2):

                        ## sets the direction that the screen must move ##
                        self.destiny['x-way'] = 'left'

                        ## defines how much should move ##
                        self.destiny['x'] = (self.view["width"] / 2) - pygame.mouse.get_pos()[0]

                    ## if right ##
                    else:

                        ## sets the direction that the screen must move ##
                        self.destiny['x-way'] = 'right'
                        
                        ## defines how much should move ##
                        self.destiny['x'] = pygame.mouse.get_pos()[0] - (self.view["width"] / 2)


                    ## check which side of the y-axis was the click ##
                    ## if top ##
                    if pygame.mouse.get_pos()[1] < (self.view["height"] / 2):

                        ## sets the direction that the screen must move ##
                        self.destiny['y-way'] = 'top'

                        ## defines how much should move ##
                        self.destiny['y'] = (self.view["height"] / 2) - pygame.mouse.get_pos()[1]

                    ## if down ##
                    else:

                        ## sets the direction that the screen must move ##
                        self.destiny['y-way'] = 'bottom'

                        ## defines how much should move ##
                        self.destiny['y'] = pygame.mouse.get_pos()[1] - (self.view["height"] / 2)

            ## increment or reset atual frame ##
            self.frame = (self.frame + 1) if self.frame < self.tick else 0
            
            ## pygame clock tick ##
            clock.tick(self.tick)
