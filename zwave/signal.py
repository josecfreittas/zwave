import os
import pygame

class Signal:

    ## main game object ##
    main = None
    
    ## signal point/position ##
    point = None

    ## signal color number ##
    color = None

    ## signal view ##
    view = {
        "width": None,
        "height": None,
        "x": None,
        "y": None,
    }

    ## signal estructure ##
    structure = {
        "light": None,
        "star": None,
        "point": None,
    }
        
    ## constructor ##
    def __init__(self, main, point = 'north', color = '01', width = 128, height = 128):
        
        ## set init values ##
        self.main = main
        self.point = point
        self.color = color
        self.view["x"] = 0
        self.view["y"] = 0
        self.view["width"] = width * self.main.view["scale"]
        self.view["height"] = height * self.main.view["scale"]
        
        self.set_structure()

    ## method to set surfaces / structures of signal ##
    def set_structure(self):

        ## load and scale signal light image ##
        light = pygame.image.load(os.path.join("assets", "img", "signals", "light_%s.png" % self.color)).convert_alpha()
        self.structure["light"] = pygame.transform.scale(light, (self.view["width"], self.view["height"]))

        ## load and scale signal star image ##
        star = pygame.image.load(os.path.join("assets", "img", "signals", "star_%s.png" % self.color)).convert_alpha()
        self.structure["star"] = pygame.transform.scale(star, (self.view["width"], self.view["height"]))

        ## load and scale signal point image ##
        point = pygame.image.load(os.path.join("assets", "img", "signals", "point.png")).convert_alpha()
        self.structure["point"] = pygame.transform.scale(point, (self.view["width"], self.view["height"]))

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
        
        ## return new star ##
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
        
        ## return new light ##
        return new.subsurface(area).copy()

    ## method to update signal view position ##
    def update_position(self):

        ## if is north signal ##
        if self.point == 'north':
            self.view["x"] = (320 * self.main.view["scale"]) - self.main.view["x"]
            self.view["y"] = (1600 * self.main.view["scale"]) - self.main.view["y"]

        ## if is south signal ##
        else:
            self.view["x"] = (1600 * self.main.view["scale"]) - self.main.view["x"]
            self.view["y"] = (320 * self.main.view["scale"]) - self.main.view["y"]

    def update(self):

        ## call method to update signal position acording to the actual game view ##
        self.update_position()

        ## draw animated signal light in the screen ##
        self.main.screen.blit(self.animate_light(), (self.view["x"], self.view["y"]))

        ## draw animated signal star in the screen ##
        self.main.screen.blit(self.animate_star(), (self.view["x"], self.view["y"]))

        ## draw signal point in the screen ##
        self.main.screen.blit(self.structure["point"], (self.view["x"], self.view["y"]))
