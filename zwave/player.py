import os
import math
import random
import pygame
import zwave.main

class Player:

    ## constructor ##
    def __init__(self, main = None, model = '01', width = 65, height = 65):    
        
        ## main game object ##
        self.main = main
        
        ## visual model of player ##
        self.model = model
        
        ## player surface ##
        self.surface = {}
        self.surface["original"] = None
        self.surface["sprite"] = None

        ## player collider ##
        self.collider = {}
        self.collider["sprite"] = None
        self.collider["touch"] = pygame.sprite.Group()

        ## player view ##
        self.view = {}
        self.view["angle"] = 0
        self.view["width"] = width * self.main.view["scale"]
        self.view["height"] = height * self.main.view["scale"]
        self.view["x"] = (self.main.view["width"] / 2) - (self.view["width"] / 2)
        self.view["y"] = (self.main.view["height"] / 2) - (self.view["height"] / 2)

        ## player status ##
        self.status = {}
        self.status["attack"] = {}
        self.status["attack"]["type"] = "gun"
        self.status["attack"]["delay"] = 0

        self.set_surface()
        self.set_collider()

    ## methods to allow external access to object values ##
    def __getitem__(self, name):
        if name == "view":
	        return self.view

    ## method to set player surface ##
    def set_surface(self):

        ## load and scale player model image ##
        self.surface["original"] = pygame.image.load(os.path.join("assets", "img", "players", "%s.png" % self.model)).convert_alpha()
        self.surface["original"] = pygame.transform.scale(self.surface["original"], (self.view["width"], self.view["height"]))

    ## method to draw player collider ##
    def set_collider(self):

        ## calculate size of collider based on player size ##
        size = int(((self.view["width"] / 1.7) + (self.view["height"] / 1.7)) / 2)

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
        self.collider["sprite"] = sprite
        self.collider["touch"].add(self.collider["sprite"])

    ## method to check if exist collision ##
    def collision(self, collider):
        if collider == "walls":
            collider = self.main.map.collider["walls"]
        if collider == "grass":
            collider = self.main.map.collider["grass"]
        if collider == "marble":
            collider = self.main.map.collider["marble"]
        if collider == "sand":
            collider = self.main.map.collider["sand"]
        if collider == "enemies":
            collider = self.main.enemies["colliders"]

        if pygame.sprite.groupcollide(self.collider["touch"], collider, False, False):
            return True
        else:
            return False

    ## method to rotate player ##
    def rotate(self):

        ## set angle of rotation based on current frame ##
        angle = self.view["angle"]

        ## get area of original light ##
        area = self.surface["original"].get_rect()

        ## make a copy of light with a new angle ##
        new = pygame.transform.rotozoom(self.surface["original"], angle, 1)

        ## define center of new copy ##
        area.center = new.get_rect().center

        self.surface["sprite"] = new.subsurface(area).copy()

    ## method to define angle for player rotation acording to the cursor position ##
    def set_angle(self):

        if (self.main.cursor['x'] > 0) or (self.main.cursor['y'] > 0):

            ## calculate angle by two points, cursor position and player position ##
            dx = self.main.cursor["x"] - (self.view["x"] + (self.view["width"] / 2))
            dy = self.main.cursor["y"] - (self.view["y"] + (self.view["height"] / 2))
            rads = math.atan2(-dy,dx)
            rads %= 2 * math.pi
            self.view["angle"] = math.degrees(rads)

    ## method to player shots ##    
    def shot(self):

        ## checks if delay for the shot is zero ##
        if self.status["attack"]["delay"] == 0:

            ## check if the type of weapon is gun ##
            if self.status["attack"]["type"] == "gun":

                ## gunshot sound ##
                self.main.sound["channels"]["attacks"].play(self.main.sound["gunshot"], 0)

                ## add delay for next gunshot ##
                self.status["attack"]["delay"] = 60

    ## method to update player ##
    def update(self):

        ## update gunshot timer ##
        if self.status["attack"]["delay"] > 0:
            self.status["attack"]["delay"] -= 1

        self.set_angle()
        self.rotate()
