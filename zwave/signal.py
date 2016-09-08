import os
import pygame

class Signal:

    ## main game object ##
    main = None
    
    ## signal point/position ##
    point = None

    ## signal view ##
    view = {
        "width": None,
        "height": None,
        "x": None,
        "y": None,
    }

    ## signal estructure ##
    structure = {
        "base": None,
        "light": None,
        "star": None,
        "point": None,
    }
        
    ## constructor ##
    def __init__(self, main, point = 'north', width = 128, height = 128):
        
        ## set init values ##
        self.main = main
        self.view["width"] = width
        self.view["height"] = height
        self.view["x"] = 0
        self.view["y"] = 0

        ## set signal point/type ##
        self.point = point
        
        self.set_structure()

    ## method to set surfaces / structures of base signal ##
    def set_structure(self):

        ## load signal base image ##
        base = pygame.image.load(os.path.join("assets", "img", "signals", "base.png")).convert_alpha()

        ## scale signal base ##
        self.structure["base"] = pygame.transform.scale(
            base,
            (int(self.view["width"] * self.main.view["scale"]), int(self.view["height"] * self.main.view["scale"]))
        )


        ## load signal light image ##
        light = pygame.image.load(os.path.join("assets", "img", "signals", "light.png")).convert_alpha()

        ## scale signal light ##
        self.structure["light"] = pygame.transform.scale(
            light,
            (int(self.view["width"] * self.main.view["scale"]), int(self.view["height"] * self.main.view["scale"]))
        )


        ## load signal star image ##
        star = pygame.image.load(os.path.join("assets", "img", "signals", "star.png")).convert_alpha()

        ## scale signal light ##
        self.structure["star"] = pygame.transform.scale(
            star,
            (int(self.view["width"] * self.main.view["scale"]), int(self.view["height"] * self.main.view["scale"]))
        )


        ## load signal point image ##
        point = pygame.image.load(os.path.join("assets", "img", "signals", "point.png")).convert_alpha()

        ## scale signal point ##
        self.structure["point"] = pygame.transform.scale(
            point,
            (int(self.view["width"] * self.main.view["scale"]), int(self.view["height"] * self.main.view["scale"]))
        )
    
    ## method to animate star of signal ##
    def animate_star(self):

        ## set angle of rotation based on current frame ##
        angle = self.main.frame * 1.5

        ## get area of original star ##
        area = self.structure["star"].get_rect()

        ## make a copy of star with a new angle ##
        new = pygame.transform.rotozoom(self.structure["star"], angle, 1)

        ## define center of new copy ##
        area.center = new.get_rect().center
        
        ## ##
        return new.subsurface(area).copy()

    def animate_light(self):

        ## set angle of rotation based on current frame ##
        angle = (self.main.frame * -1) * 3

        ## get area of original light ##
        area = self.structure["light"].get_rect()

        ## make a copy of light with a new angle ##
        new = pygame.transform.rotozoom(self.structure["light"], angle, 1)

        ## define center of new copy ##
        area.center = new.get_rect().center
        
        ## ##
        return new.subsurface(area).copy()

    ## method to update signal view position ##
    def update_position(self):

        ## if is north signal ##
        if self.point == 'north':
            self.view["x"] = (320 * self.main.view["scale"]) - self.main.view["x"]
            self.view["y"] = (1600 * self.main.view["scale"]) - self.main.view["y"]

        ## if is orange signal ##
        else:
            self.view["x"] = (1600 * self.main.view["scale"]) - self.main.view["x"]
            self.view["y"] = (320 * self.main.view["scale"]) - self.main.view["y"]

    def update(self):

        ## call method to update signal position acording to the actual game view ##
        self.update_position()

        ## draw signal base in the screen ##
        self.main.screen.blit(self.structure["base"], (self.view["x"], self.view["y"]))

        ## draw animated signal light in the screen ##
        self.main.screen.blit(self.animate_light(), (self.view["x"], self.view["y"]))

        ## draw animated signal star in the screen ##
        self.main.screen.blit(self.animate_star(), (self.view["x"], self.view["y"]))

        ## draw signal point in the screen ##
        self.main.screen.blit(self.structure["point"], (self.view["x"], self.view["y"]))