import os
import pygame
import random

class Player:

    ## main game object ##
    main = None
    
    ## visual model of player ##
    model = None
    
    ## player surface ##
    surface = None

    ## player view ##
    view = {
        "scale": None,
        "width": None,
        "height": None,
        "x": None,
        "y": None,
        "angle": None,
    }

    ## constructor ##
    def __init__(self, main, model = 'random', scale = 1, width = 49, height = 49):
        
        ## set init values ##
        self.main = main
        self.view["scale"] = scale
        self.view["width"] = width
        self.view["height"] = height
        self.view["angle"] = 0

        ## set position in center of game screen ##
        self.view["x"] = (self.main.view["width"] / 2) - ((self.view["width"] * self.view["scale"]) / 2)
        self.view["y"] = (self.main.view["height"] / 2) - ((self.view["height"] * self.view["scale"]) / 2)

        ## set defined or ramdom player model ##
        self.model = '0' + str(random.randint(1,9)) if model == 'random' else model

        self.set_surface()

    ## method to set player surface ##
    def set_surface(self):

        ## load player model image ##
        model = pygame.image.load(os.path.join("assets", "img", "players", "%s.png" % self.model)).convert_alpha()

        ## scale player ##
        self.surface = pygame.transform.scale(
            model,
            (int(self.view["width"] * self.view["scale"]), int(self.view["height"] * self.view["scale"]))
        )

    def rotate(self):

        ## set angle of rotation based on current frame ##
        angle = self.view["angle"]

        ## get area of original light ##
        area = self.surface.get_rect()

        ## make a copy of light with a new angle ##
        new = pygame.transform.rotozoom(self.surface, angle, 1)

        ## define center of new copy ##
        area.center = new.get_rect().center
        
        ## ##
        new = new.subsurface(area).copy()
        
        return new

    def set_angle(self):
        if (self.main.destiny['x'] > 0) or (self.main.destiny['y'] > 0):
            if (self.main.destiny['x-way'] == 'right') and (self.main.destiny['y-way'] == 'bottom'):
                self.view["angle"] = - (self.main.destiny['y_velocity'] * 45)
            elif (self.main.destiny['x-way'] == 'right') and (self.main.destiny['y-way'] == 'top'):
                self.view["angle"] = self.main.destiny['y_velocity'] * 45
            elif (self.main.destiny['x-way'] == 'left') and (self.main.destiny['y-way'] == 'bottom'):
                self.view["angle"] = ((self.main.destiny['y_velocity'] * 45) - 180)
            elif (self.main.destiny['x-way'] == 'left') and (self.main.destiny['y-way'] == 'top'):
                self.view["angle"] = - ((self.main.destiny['y_velocity'] * 45) - 180)
            else:
                self.view["angle"] = 0
    
    def update(self):

        self.set_angle()

        self.main.screen.blit(self.rotate(), (self.view['x'], self.view['y']))