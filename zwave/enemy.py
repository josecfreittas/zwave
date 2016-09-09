import os
import math
import random
import pygame

class Enemy:

    ## constructor ##
    def __init__(self, main, model = '01', width = 65, height = 65):
        
        ## game main ##
        self.main = main

        ## enemy model ##
        self.model = model

        ## enemy surface ##
        self.surface = None

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
        self.set_colliders()


    ## methods to allow external access to object values ##
    def __getattr__(self, name):
        if name == "view":
            return self.view
        if name == "collider":
            return self.collider
    def __getitem__(self, name):
        if name == 'view':
	        return self.view
        if name == "collider":
            return self.collider

    ## method to set player surface ##
    def set_surface(self):

        ## load and scale player model image ##
        model = pygame.image.load(os.path.join("assets", "img", "enemies", "%s.png" % self.model)).convert_alpha()
        self.surface = pygame.transform.scale(model, (self.view["width"], self.view["height"]))

    ## set object position relative to map ##
    def set_position(self):
        self.view["relative"]["x"] = 900 * self.main.view["scale"]
        self.view["relative"]["y"] = 900 * self.main.view["scale"]

    ## method to draw player collider ##
    def set_colliders(self):

        ## calculate sizes of colliders based on enemy size ##
        size1 = int(((self.view["width"] / 1.7) + (self.view["height"] / 1.7)) / 2)
        size2 = int((self.view["width"] + self.view["height"]) / 2)

        ## make a generic sprite  ##
        sprite1 = pygame.sprite.Sprite()
        sprite1.image = pygame.Surface((size1, size1))
        sprite2 = pygame.sprite.Sprite()
        sprite2.image = pygame.Surface((size2, size2))

        ## fill the sprite with red and after that make colorkey with red, making the sprite transparent ##
        sprite1.image.fill((100, 0, 0))
        sprite1.image.set_colorkey((100, 0, 0))
        sprite2.image.fill((255, 0, 0))
        sprite2.image.set_colorkey((255, 0, 0))

        ## make sprite rect ##
        sprite1.rect = sprite1.image.get_rect()
        sprite2.rect = sprite2.image.get_rect()

        ## set new position ##
        sprite1.rect.x = 0
        sprite1.rect.y = 0
        sprite2.rect.x = 0
        sprite2.rect.y = 0


        ## add new collider to colliders group ##
        self.collider["sprite1"] = sprite1
        self.collider["sprite2"] = sprite2
        self.collider["damage"].add(self.collider["sprite2"])
        self.collider["touch"].add(self.collider["sprite1"])
    
    def update_collider(self):
        x1 = (self.view["x"] + (self.view["width"] / 2)) - (self.collider["sprite1"].rect.width / 2)
        y1 = (self.view["y"] + (self.view["height"] / 2)) - (self.collider["sprite1"].rect.height / 2)
        x2 = (self.view["x"] + (self.view["width"] / 2)) - (self.collider["sprite2"].rect.width / 2)
        y2 = (self.view["y"] + (self.view["height"] / 2)) - (self.collider["sprite2"].rect.height / 2)

        pygame.draw.rect(self.main.screen, (255, 0, 0), (x2, y2, self.collider["sprite2"].rect.width, self.collider["sprite2"].rect.height))
        pygame.draw.rect(self.main.screen, (100, 0, 0), (x1, y1, self.collider["sprite1"].rect.width, self.collider["sprite1"].rect.height))

        self.collider["sprite1"].rect.x = x1
        self.collider["sprite1"].rect.y = y1
        self.collider["sprite2"].rect.x = x2
        self.collider["sprite2"].rect.y = y2

    ## method to check if exist collision ##
    def check_collision(self, collider1, collider2 = 'touch'):

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
        area = self.surface.get_rect()

        ## make a copy of light with a new angle ##
        new = pygame.transform.rotozoom(self.surface, angle, 1)

        ## define center of new copy ##
        area.center = new.get_rect().center

        return new.subsurface(area).copy()

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
        self.view["x"] = self.view["relative"]["x"] - self.main.view["x"]
        self.view["y"] = self.view["relative"]["y"] - self.main.view["y"]

    ## method to update enemy ##
    def update(self):
        self.set_angle()
        self.update_collider()
        if self.check_collision("player"):
            pass
        self.update_position()
        self.main.screen.blit(self.rotate(), (self.view['x'], self.view['y']))
