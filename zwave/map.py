import os
import sys
import math
import pygame

class Map:

    ## constructor ##
    def __init__(self, main, width = 2048, height = 2048):

        ## game main ##
        self.main = main

        ## map view ##
        self.view = {}
        self.view["width"] = width * self.main.view["scale"]
        self.view["height"] = height * self.main.view["scale"]
        self.view["x"] = 0
        self.view["y"] = 0

        ## map suface ##
        self.surface = {}
        self.surface["ground"] = None
        self.surface["walls"] = None

        ## map colliders ##
        self.collider = {}
        self.collider["size"] = 64 * self.main.view["scale"]
        self.collider["sprites"] = {}
        self.collider["walls"] = pygame.sprite.Group()
        self.collider["grass"] = pygame.sprite.Group()
        self.collider["marble"] = pygame.sprite.Group()
        self.collider["sand"] = pygame.sprite.Group()
        self.collider["raw"] = [
            "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "W", "W", "W", "W", "W", "W", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "M", "W", "M", "M", "M", "M", "W", "W", "W", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "M", "M", "M", "M", "M", "M", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "M", "M", "M", "M", "M", "M", "M", "M", "W", "W", "W", "G", "G", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "M", "M", "M", "M", "M", "M", "M", "M", "W", "W", "W", "G", "G", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "M", "M", "M", "M", "M", "M", "M", "W", "W", "W", "W", "G", "G", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "M", "M", "M", "M", "M", "M", "M", "M", "W", "W", "W", "G", "G", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "M", "M", "M", "M", "M", "M", "M", "M", "M", "W", "W", "G", "G", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "M", "M", "M", "M", "M", "M", "M", "M", "W", "W", "G", "G", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "W", "W", "W", "W", "M", "M", "M", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "M", "M", "M", "W", "W", "W", "W", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "G", "G", "W", "W", "M", "M", "M", "M", "M", "M", "M", "M", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "G", "G", "W", "W", "M", "M", "M", "M", "M", "M", "M", "M", "M", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "G", "G", "W", "W", "W", "M", "M", "M", "M", "M", "M", "M", "M", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "G", "G", "W", "W", "W", "W", "M", "M", "M", "M", "M", "M", "M", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "G", "G", "W", "W", "W", "M", "M", "M", "M", "M", "M", "M", "M", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "G", "G", "W", "W", "W", "M", "M", "M", "M", "M", "M", "M", "M", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "M", "M", "M", "M", "M", "M", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "G", "G", "G", "G", "W", "W", "W", "M", "M", "M", "M", "W", "M", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "W", "W", "W", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"
        ]

        self.set_surface()
        self.set_colliders()

    ## method to set/load and scale map surfaces ##
    def set_surface(self):

        self.surface["ground"] = pygame.image.load(os.path.join("assets", "img", "map", "ground.png")).convert_alpha()
        self.surface["ground"] = pygame.transform.scale(self.surface["ground"], (self.view["width"], self.view["height"]))

        self.surface["walls"] = pygame.image.load(os.path.join("assets", "img", "map", "walls.png")).convert_alpha()
        self.surface["walls"] = pygame.transform.scale(self.surface["walls"], (self.view["width"], self.view["height"]))
    
    def set_colliders(self):

        ## loop for all the tiles ##
        for key, tile in enumerate(self.collider["raw"]):

            ## make a generic sprite with size of map tiles  ##
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.Surface((self.collider["size"], self.collider["size"]))

            ## fill the sprite with red and after that make colorkey with red, making the sprite transparent ##
            sprite.image.fill((255, 0, 0))
            sprite.image.set_colorkey((255, 0, 0))

            ## make sprite rect ##
            sprite.rect = sprite.image.get_rect()

            ## add sprit to map colliders list (dict) ##
            self.collider["sprites"][key] = sprite

            ## if current tile is a wall, add in wall group ##
            if tile == 'W':
                self.collider["walls"].add(self.collider["sprites"][key])

            ## if current tile is grass, add in grass group ##
            elif tile == 'G':
                self.collider["grass"].add(self.collider["sprites"][key])

            ## if current tile is stone/marble, add in marble group ##
            elif tile == 'M':
                self.collider["marble"].add(self.collider["sprites"][key])

            ## if current tile is sand, add in sand group ##
            elif tile == 'S':
                self.collider["sand"].add(self.collider["sprites"][key])

    ## method to update all colliders position acording to screen position ##
    def update_colliders(self):

        ## check version of python 2 or 3, and set var 'items' with the appropriate syntax for each version ##
        if sys.version_info.major == 2:
            items = self.collider["sprites"].iteritems()
        else:
            items = self.collider["sprites"].items()

        rows = self.view["width"] / self.collider["size"]

        ## loop for update all sprites ##
        for key, sprite in items:

            ## get row and column by dict key ##
            column = key % rows;
            row = int(key / float(rows))

            ## calcule new position of collider ##
            x = (column * self.collider["size"]) - self.main.view["x"]
            y = (row * self.collider["size"])  - self.main.view["y"]

            ## set new position ##
            self.collider["sprites"][key].rect.x = x
            self.collider["sprites"][key].rect.y = y

    ## method to update map view position ##
    def update_position(self):
        self.view["x"] = self.main.view["x"] * -1
        self.view["y"] = self.main.view["y"] * -1

    ## method to update map ##
    def update(self):

        ## call method to update position ##
        self.update_position()

        ## call method to update colliders ##
        self.update_colliders()

        ## draw invisible colliders ##
        self.collider["walls"].draw(self.main.screen)
