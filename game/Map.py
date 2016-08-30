import os
import pygame

class Map:
    
    ## main game object ##
    main = None

    ## map view ##
    view = {
        "scale": None,
        "width": None,
        "height": None,
        "x": None,
        "y": None,
    }

    ## map surface ##
    surface = None

    ## constructor ##
    def __init__(self, main, scale = 1, width = 2048, height = 2048):

        ## set init values ##
        self.view["scale"] = scale
        self.view["width"] = width
        self.view["height"] = height
        self.view["x"] = 0
        self.view["y"] = 0
        self.main = main

        self.set_surface()
    
    ## method to set map surface ##
    def set_surface(self):

        ## load map image ##
        surface = pygame.image.load(os.path.join("assets", "img", "map.png")).convert_alpha()

        ## scale map ##
        self.surface = pygame.transform.scale(
            surface,
            ((self.view["width"] * self.view["scale"]), (self.view["height"] * self.view["scale"]))
        )
    
    ## method to update map view position ##
    def update_position(self):
        self.view["x"] = self.main.view["x"] * -1
        self.view["y"] = self.main.view["y"] * -1

    ## method to update map ##
    def update(self):

        ## call method to update position ##
        self.update_position()

        ## draw map on the screen ##
        self.main.screen.blit(
            self.surface,
            (self.view["x"], self.view["y"])
        )
