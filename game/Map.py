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

    ## size in pixels of map tiles tiles ##
    tile_size = None

    ## map colliders ##
    colliders = {
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
    def __init__(self, main, scale = 1, width = 2048, height = 2048):

        ## set init values ##
        self.view["scale"] = scale
        self.view["width"] = width
        self.view["height"] = height
        self.view["x"] = 0
        self.view["y"] = 0
        self.tile_size = 64
        self.colliders["list"] = []
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
    
    def draw_collider(self, row, column):
        x = ((column - 1) * self.tile_size) - self.main.view["x"]
        y = ((row - 1) * self.tile_size)  - self.main.view["y"]
        return pygame.draw.rect(self.main.screen, (0,0,0), (x, y, self.tile_size, self.tile_size), 0)

    def update_colliders(self):

        ## map number of rows ##
        rows = self.view["width"] / self.tile_size

        ## map number of columns ##
        columns = self.view["height"] / self.tile_size

        ## current row ##
        row = 1

        ## current column ##
        column = 0

        ## current tile ##
        tile = 0

        ## loop for all the tiles ##
        while tile < (rows * columns):

            ## increment current tile ##
            tile += 1

            if column < columns:
                column += 1
            else:
                column = 1
                row += 1
            if self.colliders["raw"][str(row)][column] == '@':
                self.draw_collider(row, column)

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