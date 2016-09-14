import os
import random

import pygame

import zwave.helper

class Enemy(pygame.sprite.Sprite):

    ## spaw points ##
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

    def __init__(self, main, model = "01"):
        super().__init__()

        
        self.status = {}

        self.status["delay"] = 52 + (-2 * main.wave)
        self.status["timer"] = 0
        self.status["damage"] = [23, 43]
        self.status["damage"][0] += (2 * main.wave)
        self.status["damage"][1] += (2 * main.wave)

        self.status["life"] = 80 + (20 * main.wave)
        self.status["speed"] = 0.9 + (0.15 * main.wave)

        ## init values ##
        self.main = main
        self.model = model
        self.size = 65 * main.scale
        self.angle = 0
        self.relative = {}
        self.center = {}
        self.last = {}

        self.generate_position()

        path = os.path.join("assets", "img", "enemies", "%s.png" % self.model)
        self.image_base = zwave.helper.pygame_image(path, self.size)
        self.image = self.image_base

        self.rect = self.image.get_rect()
        self.rect.x = self.relative["x"]
        self.rect.y = self.relative["y"]

        self.set_colliders()

    def generate_position(self):

        ## get a random spaw of lis ##
        tile = random.choice(self.spaws).split("x")

        ## calculates the axes ##
        x = int(tile[0]) * (64 * self.main.scale)
        y = int(tile[1]) * (64 * self.main.scale)

        ## set relative position ##
        self.relative["x"] = x
        self.relative["y"] = y

        ## saves the actual position of the enemy, relative to game screen ##
        self.center["x"] = self.relative["x"] - (self.size / 2)
        self.center["y"] = self.relative["y"] - (self.size / 2)

    def set_colliders(self):

        ## default collider, with same size of sprite image ##
        self.collider1 = pygame.sprite.GroupSingle(self)

        ## touch/collider2 is a small collider for enemy, that simulates a better "touch" for the enemy, ##
        ## without the large original image edges ##
        self.touch = pygame.sprite.Sprite()
        self.touch.up = self
        self.touch.size = int(self.size / 2)

        self.touch.image = pygame.surface.Surface((self.touch.size, self.touch.size))
        self.touch.image.fill((255, 0, 0))
        self.touch.image.set_colorkey((255, 0, 0))
        self.touch.rect = self.touch.image.get_rect()
        self.touch.rect.x = self.center["x"] - (self.touch.size / 2)
        self.touch.rect.y = self.center["y"] - (self.touch.size / 2)

        self.collider2 = pygame.sprite.GroupSingle(self.touch)

    def update_colliders(self):

        ## update position of the second collider of enemy ##
        self.touch.rect.x = self.center["x"] - (self.touch.size / 2)
        self.touch.rect.y = self.center["y"] - (self.touch.size / 2)

    def collision(self, collider1, collider2):

        ## check collider 1 ##
        if collider1 == "walls":
            collider1 = self.main.map.collider["walls"]
        elif collider1 == "player":
            collider1 = self.main.player.collider2

        return pygame.sprite.groupcollide(collider2, collider1, False, False)

    def update_angle(self):

        ## update enemy angle based in player location ##
        self.angle = zwave.helper.angle_by_two_points(self.center, self.main.player.center)
        self.image = zwave.helper.pygame_rotate(self.image_base, self.angle)

    def update_position(self):

        ## check if had collision, if had, set last position of view ##
        if self.collision("walls", self.collider2) or self.collision("player", self.collider2):
            self.relative["x"] = self.last["x"]
            self.relative["y"] = self.last["y"]

        ## save last position ##
        self.last["x"] = self.relative["x"]
        self.last["y"] = self.relative["y"]
        
        ## get 'x' and 'y' velocity based on enemy angle ##
        velocity = zwave.helper.velocity_by_angle(1 * self.main.scale, self.angle)

        ## move ##
        self.relative["x"] += velocity["x"]
        self.relative["y"] += velocity["y"]

        ## update view ##
        self.rect.x = self.relative["x"] - self.main.x
        self.rect.y = self.relative["y"] - self.main.y

        ## update enemy center point ##
        self.center["x"] =  self.rect.x + (self.size / 2)
        self.center["y"] =  self.rect.y + (self.size / 2)

    def update(self):
        if self.status["life"] <= 0:
            self.touch.kill()
            self.kill()

        self.update_angle()
        self.update_position()
        self.update_colliders()
