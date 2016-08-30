import os
import pygame

class Heart:

    ## main game object ##
    main = None
    
    ## base heart color/type ##
    color = None

    ## heart view ##
    view = {
        "scale": None,
        "width": None,
        "height": None,
        "x": None,
        "y": None,
    }

    ## heart estructure ##
    structure = {
        "base": None,
        "light": None,
        "star": None,
        "point": None,
    }
        
    ## constructor ##
    def __init__(self, main, color = 'blue', scale = 1, width = 128, height = 128):
        
        ## set init values ##
        self.view["scale"] = scale
        self.view["width"] = width
        self.view["height"] = height
        self.view["x"] = 0
        self.view["y"] = 0
        self.main = main

        ## set heart color/type ##
        self.color = color
        
        self.set_structure()

    ## method to set surfaces / structures of base heart ##
    def set_structure(self):

        ## load heart base image ##
        base = pygame.image.load(os.path.join("assets", "img", "hearts", "base.png")).convert_alpha()

        ## scale heart base ##
        self.structure["base"] = pygame.transform.scale(
            base,
            (int((self.view["width"] * 1.5) * self.view["scale"]), int((self.view["height"] * 1.5) * self.view["scale"]))
        )


        ## load heart light image ##
        light = pygame.image.load(os.path.join("assets", "img", "hearts", "%s_light.png" % self.color)).convert_alpha()

        ## scale heart light ##
        self.structure["light"] = pygame.transform.scale(
            light,
            (int(self.view["width"] * self.view["scale"]), int(self.view["height"] * self.view["scale"]))
        )


        ## load heart star image ##
        star = pygame.image.load(os.path.join("assets", "img", "hearts", "%s_star.png" % self.color)).convert_alpha()

        ## scale heart light ##
        self.structure["star"] = pygame.transform.scale(
            star,
            (int(self.view["width"] * self.view["scale"]), int(self.view["height"] * self.view["scale"]))
        )


        ## load heart point image ##
        point = pygame.image.load(os.path.join("assets", "img", "hearts", "point.png")).convert_alpha()

        ## scale heart point ##
        self.structure["point"] = pygame.transform.scale(
            point,
            (int(self.view["width"] * self.view["scale"]), int(self.view["height"] * self.view["scale"]))
        )
    
    ## method to animate star of heart ##
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
        new = new.subsurface(area).copy()
        
        return new

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
        new = new.subsurface(area).copy()
        
        return new

    ## method to update heart view position ##
    def update_position(self):

        ## if is blue heart ##
        if self.color == 'blue':
            self.view["x"] = (0 - self.main.view["x"]) + 320
            self.view["y"] = (1024 - self.main.view["y"]) + 576

        ## if is orange heart ##
        else:
            self.view["x"] = (1024 - self.main.view["x"]) + 576
            self.view["y"] = (0 - self.main.view["y"]) + 320

    def update(self):

        ## call method to update heart position acording to the actual game view ##
        self.update_position()

        ## draw heart base in the screen ##
        self.main.screen.blit(self.structure["base"], (self.view["x"], self.view["y"]))

        ## draw animated heart light in the screen ##
        self.main.screen.blit(self.animate_light(), (self.view["x"], self.view["y"]))

        ## draw animated heart star in the screen ##
        self.main.screen.blit(self.animate_star(), (self.view["x"], self.view["y"]))

        ## draw heart point in the screen ##
        self.main.screen.blit(self.structure["point"], (self.view["x"], self.view["y"]))