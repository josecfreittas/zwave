import os
import math
import random
import pygame

class Player:

    ## main game object ##
    main = None
    
    ## visual model of player ##
    model = None
    
    ## player surface ##
    surface = None

    ## player collider ##
    collider = None

    ## player view ##
    view = {
        "width": None,
        "height": None,
        "x": None,
        "y": None,
        "angle": None,
    }

    ## constructor ##
    def __init__(self, main, model = 'random', width = 65, height = 65):
        
        ## set init values ##
        self.main = main
        self.view["width"] = width
        self.view["height"] = height
        self.view["angle"] = 0
        self.collider = pygame.sprite.Group()

        ## set position in center of game screen ##
        self.view["x"] = (self.main.view["width"] / 2) - ((self.view["width"] * self.main.view["scale"]) / 2)
        self.view["y"] = (self.main.view["height"] / 2) - ((self.view["height"] * self.main.view["scale"]) / 2)

        ## set defined or ramdom player model ##
        self.model = '0' + str(random.randint(1,9)) if model == 'random' else model

        
        self.set_surface()
        self.set_collider()

    ## method to set player surface ##
    def set_surface(self):

        ## load player model image ##
        model = pygame.image.load(os.path.join("assets", "img", "players", "%s.png" % self.model)).convert_alpha()

        ## scale player ##
        self.surface = pygame.transform.scale(
            model,
            (self.view["width"] * self.main.view["scale"], self.view["height"] * self.main.view["scale"])
        )

    ## method to draw player collider ##
    def set_collider(self):

        ## calculate size of collider based on player size ##
        size = int(
                (
                    ((self.view["width"] * self.main.view["scale"]) / 1.5) + 
                    ((self.view["height"] * self.main.view["scale"]) / 1.5)
                ) / 2
            )

        x = (self.main.view["width"] / 2) - (size / 2)
        y = (self.main.view["height"] / 2) - (size / 2)

        ## make a generic sprite  ##
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.Surface((size, size))

        ## fill the sprite with red and after that make colorkey with red, making the sprite transparent ##
        sprite.image.fill((255, 0, 0))
        sprite.image.set_colorkey((255, 0, 0))

        ## make sprite rect ##
        sprite.rect = sprite.image.get_rect()

	    ## set new position ##
        sprite.rect.x = x
        sprite.rect.y = y

        ## add new collider to colliders group ##
        self.collider.add(sprite)

    ## method to check if exist collision ##
    def check_collision(self, collider):
        if collider == 'wall':
            collider = self.main.map.colliders["group"]

        if pygame.sprite.groupcollide(self.collider, collider, False, False):
            return True
        else:
            return False

    ## method to rotate player ##
    def rotate(self):

        ## set angle of rotation based on current frame ##
        angle = self.view["angle"]

        ## get area of original light ##
        area = self.surface.get_rect()

        ## make a copy of light with a new angle ##
        new = pygame.transform.rotozoom(self.surface, angle, 1)

        ## define center of new copy ##
        area.center = new.get_rect().center

        return new.subsurface(area).copy()

    ## method to define angle for player rotation acording to the mouse position ##
    def set_angle(self):

        if (self.main.mouse['x'] > 0) or (self.main.mouse['y'] > 0):

            ## calculate angle by two points, mouse position and player position ##
            dx = self.main.mouse["x"] - (self.view["x"] + ((self.view["width"] * self.main.view["scale"]) / 2))
            dy = self.main.mouse["y"] - (self.view["y"] + ((self.view["height"] * self.main.view["scale"]) / 2))
            rads = math.atan2(-dy,dx)
            rads %= 2 * math.pi
            self.view["angle"] = math.degrees(rads)
    
    ## method to update player ##
    def update(self):
        self.set_angle()
        self.main.screen.blit(self.rotate(), (self.view['x'], self.view['y']))
