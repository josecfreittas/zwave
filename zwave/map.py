import os
import sys
import pygame

class Map:
    
    ## main game object ##
    main = None

    ## map view ##
    view = {
        "width": None,
        "height": None,
        "x": None,
        "y": None,
    }

    ## map surface ##
    surface = None

    ## map colliders ##
    colliders = {
        "size": None,
        "sprites": None,
        "group": None,
        "raw": {
            "1":  ' @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',
            "2":  ' @                       @@@@@@@@',
            "3":  ' @                        @   @@@',
            "4":  ' @                             @@',
            "5":  ' @       @@@@   @@@   @        @@',
            "6":  ' @                @   @        @@',
            "7":  ' @                @   @       @@@',
            "8":  ' @         @          @        @@',
            "9":  ' @   @      @                   @',
            "10": ' @   @       @     @            @',
            "11": ' @   @  @          @     @@@@   @',
            "12": ' @   @   @        @             @',
            "13": ' @        @     @@              @',
            "14": ' @                    @@        @',
            "15": ' @      @@           @    @@@   @',
            "16": ' @   @  @@   @      @       @   @',
            "17": ' @   @       @      @       @   @',
            "18": ' @   @@@    @                   @',
            "19": ' @        @@                    @',
            "20": ' @              @@     @        @',
            "21": ' @             @        @   @   @',
            "22": ' @   @@@@     @          @  @   @',
            "23": ' @            @     @       @   @',
            "24": ' @               @@  @      @   @',
            "25": ' @@        @     @@   @         @',
            "26": ' @@@       @   @                @',
            "27": ' @@        @   @                @',
            "28": ' @@        @   @@@   @@@@       @',
            "29": ' @@                             @',
            "30": ' @@@   @                        @',
            "31": ' @@@@@@@@                       @',
            "32": ' @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
        },
    }


    ## constructor ##
    def __init__(self, main, width = 2048, height = 2048):

        ## set init values ##
        self.main = main
        self.view["width"] = width
        self.view["height"] = height
        self.view["x"] = 0
        self.view["y"] = 0
        self.colliders["size"] = 64
        self.colliders["sprites"] = {}
        self.colliders["group"] = pygame.sprite.Group()
        
        self.set_surface()
        self.set_colliders()
    
    ## method to set map surface ##
    def set_surface(self):

        ## calculate scaled map width and height ##
        width = int(self.view["width"] * self.main.view["scale"])
        height = int(self.view["height"] * self.main.view["scale"])

        ## load and scale map image ##
        surface = pygame.image.load(os.path.join("assets", "img", "map.png")).convert_alpha()
        self.surface = pygame.transform.scale(surface, (width, height))
    
    def set_colliders(self):

        ## scaled tile/collider size ##
        tile_size = (self.colliders["size"] * self.main.view["scale"])

        ## map number of rows ##
        rows = (self.view["width"] * self.main.view["scale"]) / tile_size

        ## map number of columns ##
        columns = (self.view["height"] * self.main.view["scale"]) / tile_size

        ## current row, column and tile ##
        row = 1
        column = 0
        tile = 0

        ## loop for all the tiles ##
        while tile < (rows * columns):

            ## increment current tile ##
            tile += 1

            ## increment current column or current row ##
            if column < columns:
                column += 1
            else:
                column = 1
                row += 1
            
            ## check if in raw, current tile is a wall ##
            if self.colliders["raw"][str(row)][column] == '@':

                ## make a generic sprite with size of map tiles  ##
                sprite = pygame.sprite.Sprite()
                sprite.image = pygame.Surface((tile_size, tile_size))

                ## fill the sprite with red and after that make colorkey with red, making the sprite transparent ##
                sprite.image.fill((255, 0, 0))
                sprite.image.set_colorkey((255, 0, 0))

                ## make sprite rect ##
                sprite.rect = sprite.image.get_rect()

                ## add sprit to map colliders list (dict) ##
                name = str(row) + "," + str(column)
                self.colliders["sprites"][name] = sprite

                ## add new collider to colliders group ##
                self.colliders["group"].add(self.colliders["sprites"][name])


    ## method to update all colliders position acording to screen position ##
    def update_colliders(self):

        ## check version of python 2 or 3, and set var 'items' with the appropriate syntax for each version ##
        if sys.version_info.major == 2:
            items = self.colliders["sprites"].iteritems()
        else:
            items = self.colliders["sprites"].items()

        ## loop for update all sprites ##
        for key, sprite in items:

            ## get row and column by dict key ##
            point = key.split(",")
            row = int(point[0])
            column = int(point[1])

            ## calcule new position of collider ##
            x = ((column - 1) * (self.colliders["size"] * self.main.view["scale"])) - self.main.view["x"]
            y = ((row - 1) * (self.colliders["size"] * self.main.view["scale"]))  - self.main.view["y"]

            ## set new position ##
            self.colliders["sprites"][key].rect.x = x
            self.colliders["sprites"][key].rect.y = y

    ## method to update map view position ##
    def update_position(self):
        self.view["x"] = self.main.view["x"] * -1
        self.view["y"] = self.main.view["y"] * -1

    ## method to update map ##
    def update(self):

        ## call method to update position ##
        self.update_position()

        ## draw map on the screen ##
        self.main.screen.blit(self.surface,(self.view["x"], self.view["y"]))

        ## call method to update colliders ##
        self.update_colliders()

        ## draw invisible colliders ##
        self.colliders["group"].draw(self.main.screen)
