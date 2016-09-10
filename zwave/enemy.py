import os
import math
import random
import pygame

class Enemy:

    spaws = [
        "2x2", "5x2", "8x2", "11x2", "14x2", "17x2", "20x2", "23x2", "26x2", "29x2",
        "2x5", "5x5", "8x5", "11x5", "14x5", "17x5", "20x5", "23x5", "26x5", "29x5",
        "2x8", "5x8", "8x8", "11x8", "14x8", "17x8", "20x8", "23x8", "26x8", "29x8",
        "2x11", "5x11", "8x11", "11x11", "14x11", "17x11", "23x11", "26x11", "29x11",
        "2x14", "5x14", "8x14", "11x14", "14x14", "20x14", "23x14", "26x14", "29x14",
        "2x17", "5x17", "8x17", "11x17", "17x17", "20x17", "23x17", "26x17", "29x17",
        "2x20", "5x20", "8x20", "14x20", "17x20", "20x20", "23x20", "26x20", "29x20",
        "2x23", "5x23", "8x23", "11x23", "14x23", "17x23", "20x23", "23x23", "26x23", "29x23",
        "2x26", "5x26", "8x26", "11x26", "14x26", "17x26", "20x26", "23x26", "26x26", "29x26",
        "2x29", "5x29", "8x29", "11x29", "14x29", "17x29", "20x29", "23x29", "26x29", "29x29",
    ]

    ## constructor ##
    def __init__(self, main, model = '01', width = 65, height = 65):

        ## game main ##
        self.main = main

        ## enemy model ##
        self.model = model

        ## enemy surface ##
        self.surface = {}
        self.surface["original"] = None
        self.surface["sprite"] = pygame.sprite.Sprite()

        ## enemy collider ##
        self.collider = {}
        self.collider["sprite1"] = None
        self.collider["sprite2"] = None
        self.collider["touch"] = pygame.sprite.Group()
        self.collider["damage"] = pygame.sprite.Group()

        ## enemy view ##
        self.view = {}
        self.view["width"] = width * self.main.view["scale"]
        self.view["height"] = height * self.main.view["scale"]
        self.view["x"] = 0
        self.view["y"] = 0
        self.view["relative"] = {"x": 0, "y": 0} ## relative position to map
        self.view["angle"] = 0
        
        self.set_position()
        self.set_surface()
        self.rotate()
        self.set_colliders()


    ## methods to allow external access to object values ##
    def __getitem__(self, name):
        if name == 'view':
	        return self.view
        if name == "collider":
            return self.collider
        if name == "surface":
            return self.surface

    ## method to set player surface ##
    def set_surface(self):

        ## load and scale player model image ##
        self.surface["original"] = pygame.image.load(os.path.join("assets", "img", "enemies", "%s.png" % self.model)).convert_alpha()
        self.surface["original"] = pygame.transform.scale(self.surface["original"], (self.view["width"], self.view["height"]))

        self.surface["sprite"].image = self.surface["original"]
        self.surface["sprite"].rect = self.surface["original"].get_rect()

    ## set object position relative to map ##
    def set_position(self):

        tile = random.choice(self.spaws).split("x")

        x = int(tile[0]) * self.main.map.collider["size"]
        y = int(tile[1]) * self.main.map.collider["size"]
        self.view["relative"]["x"] = x
        self.view["relative"]["y"] = y

    ## method to draw player collider ##
    def set_colliders(self):

        ## calculate sizes of colliders based on enemy size ##
        size1 = int(((self.view["width"] / 2) + (self.view["height"] / 2)) / 2)
        size2 = int((self.view["width"] + self.view["height"]) / 2)

        ## make a generic sprite  ##
        touch = pygame.sprite.Sprite()
        touch.image = pygame.Surface((size1, size1))
        damage = pygame.sprite.Sprite()
        damage.image = pygame.Surface((size2, size2))

        ## fill the sprite with red and after that make colorkey with red, making the sprite transparent ##
        touch.image.fill((100, 0, 0))
        touch.image.set_colorkey((100, 0, 0))
        damage.image.fill((255, 0, 0))
        damage.image.set_colorkey((255, 0, 0))

        ## make sprite rect ##
        touch.rect = touch.image.get_rect()
        damage.rect = damage.image.get_rect()

        ## set new position ##
        touch.rect.x = 0
        touch.rect.y = 0
        damage.rect.x = 0
        damage.rect.y = 0


        ## add new collider to colliders group ##
        self.collider["sprite1"] = touch
        self.collider["sprite2"] = damage
        self.collider["damage"].add(self.collider["sprite2"])
        self.collider["touch"].add(self.collider["sprite1"])
    
    def update_collider(self):
        x1 = (self.view["x"] + (self.view["width"] / 2)) - (self.collider["sprite1"].rect.width / 2)
        y1 = (self.view["y"] + (self.view["height"] / 2)) - (self.collider["sprite1"].rect.height / 2)
        x2 = (self.view["x"] + (self.view["width"] / 2)) - (self.collider["sprite2"].rect.width / 2)
        y2 = (self.view["y"] + (self.view["height"] / 2)) - (self.collider["sprite2"].rect.height / 2)

        self.collider["sprite1"].rect.x = x1
        self.collider["sprite1"].rect.y = y1
        self.collider["sprite2"].rect.x = x2
        self.collider["sprite2"].rect.y = y2

    ## method to check if exist collision ##
    def collision(self, collider1, collider2 = 'touch'):

        ## check collider 1 ##
        if collider1 == 'walls':
            collider1 = self.main.map.collider["walls"]
        elif collider1 == 'player':
            collider1 = self.main.player.collider["touch"]

        ## check collider 2 ##
        collider2 = self.collider[collider2]

        if pygame.sprite.groupcollide(collider2, collider1, False, False):
            return True
        else:
            return False

    ## method to rotate enemy ##
    def rotate(self):

        ## set angle of rotation based on current frame ##
        angle = self.view["angle"]

        ## get area of original light ##
        area = self.surface["original"].get_rect()

        ## make a copy of light with a new angle ##
        new = pygame.transform.rotozoom(self.surface["original"], angle, 1)

        ## define center of new copy ##
        area.center = new.get_rect().center

        self.surface["sprite"].image = new.subsurface(area).copy()

    ## method to define angle for enemy rotation acording to enemy destination ##
    def set_angle(self):

        ## calculate angle by two points, player position and enemy position ##
        player = {
            "x": (self.main.player["view"]["x"] + (self.main.player["view"]["width"] / 2)),
            "y": (self.main.player["view"]["y"] + (self.main.player["view"]["height"] / 2)),
        }
        dx =  player["x"] - (self.view["x"] + (self.view["width"] / 2))
        dy =  player["y"] - (self.view["y"] + (self.view["height"] / 2))
        rads = math.atan2(-dy,dx)
        rads %= 2 * math.pi
        self.view["angle"] = math.degrees(rads)

    ## method to update enemy view position relative to the map ##
    def update_position(self):
        x = self.view["relative"]["x"] - self.main.view["x"]
        y = self.view["relative"]["y"] - self.main.view["y"]

        self.view["x"] = x
        self.view["y"] = y

        self.surface["sprite"].rect.x = self.view["x"]
        self.surface["sprite"].rect.y = self.view["y"]

    ## method to update enemy ##
    def update(self):
        self.set_angle()
        self.rotate()
        self.update_collider()
        self.update_position()
