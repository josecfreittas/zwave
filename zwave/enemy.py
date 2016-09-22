import os
import random

import pygame

import zwave.helper

class Enemy(pygame.sprite.Sprite):

    ## spaw points ##
    spaws = [
        "2x2", "5x2", "8x2", "11x2", "14x2", "17x2", "20x2", "23x2", "26x2",
        "2x5", "5x5", "8x5", "11x5", "14x5", "17x5", "20x5", "23x5", "26x5", "29x5",
        "2x8", "5x8", "8x8", "11x8", "14x8", "17x8", "20x8", "23x8", "26x8", "29x8",
        "2x11", "5x11", "8x11", "11x11", "14x11", "17x11", "23x11", "26x11", "29x11",
        "2x14", "5x14", "8x14", "11x14", "14x14", "20x14", "23x14", "26x14", "29x14",
        "2x17", "5x17", "8x17", "11x17", "17x17", "20x17", "23x17", "26x17", "29x17",
        "2x20", "5x20", "8x20", "14x20", "17x20", "20x20", "23x20", "26x20", "29x20",
        "2x23", "5x23", "8x23", "11x23", "14x23", "17x23", "20x23", "23x23", "26x23", "29x23",
        "2x26", "5x26", "8x26", "11x26", "14x26", "17x26", "20x26", "23x26", "26x26", "29x26",
        "5x29", "8x29", "11x29", "14x29", "17x29", "20x29", "23x29", "26x29", "29x29",
    ]

    def __init__(self, game, channel, model = "random"):

        pygame.sprite.Sprite.__init__(self)

        if model == "random":
            models = ["zombie", "zombie", "zombie", "zombie", "zombie", "zombie", "headcrab"]
            model = random.choice(models)

        self.delay = 62 + (-2 * game.wave)
        self.timer = 0
        if self.delay < 10:
            self.delay = 10

        self.timer = 0
        self.damage = [23, 43]
        self.damage[0] += (2 * game.wave)
        self.damage[1] += (2 * game.wave)
        if self.damage[0] > 100:
            self.damage[0] = 100
            self.damage[1] = 120

        self.life = 80 + (15 * game.wave)
        if self.life > 500:
            self.life = 500
            self.total_life = 500

        self.speed = 1 + (0.15 * game.wave)
        if self.speed > 3.5:
            self.speed = 3.5

        if model == "headcrab":
            self.speed *= 3
            self.life = int(0.5 * self.life)
            self.damage[0] = int(0.5 * self.damage[0])
            self.damage[1] = int(0.5 * self.damage[1])

        self.total_life = self.life

        ## init values ##
        self.game = game
        self.model = model
        if self.model == "zombie":
            self.channel = pygame.mixer.Channel(channel + 1)

        self.player_distance = None
        self.size = 65 * game.scale
        self.angle = 0
        self.movement = "x"
        self.relative = {}
        self.center = {}
        self.last = {}

        self.generate_position()

        color = random.randint(1, 9)
        path = os.path.join("assets", "img", "enemies", self.model, "%i.png" % color)
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
        x = int(tile[0]) * (64 * self.game.scale)
        y = int(tile[1]) * (64 * self.game.scale)

        ## set relative position ##
        self.relative["x"] = x
        self.relative["y"] = y
        self.last["x"] = self.relative["x"]
        self.last["y"] = self.relative["y"]

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
            collider1 = self.game.map.collider["walls"]
        elif collider1 == "player":
            collider1 = self.game.player.collider2

        return pygame.sprite.groupcollide(collider2, collider1, False, False)

    def update_angle(self):

        ## update enemy angle based in player location ##
        self.angle = zwave.helper.angle_by_two_points(self.center, self.game.player.center)
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
        velocity = zwave.helper.velocity_by_angle((self.speed * self.game.scale) * 2, self.angle)

        ## move ##
        if self.movement == "x":
            self.relative["x"] += velocity["x"]
            self.movement = "y"
        elif self.movement == "y":
            self.relative["y"] += velocity["y"]
            self.movement = "x"

        ## update view ##
        self.rect.x = self.relative["x"] - self.game.x
        self.rect.y = self.relative["y"] - self.game.y

        ## update enemy center point ##
        self.center["x"] =  self.rect.x + (self.size / 2)
        self.center["y"] =  self.rect.y + (self.size / 2)

        self.player_distance = (((self.game.player.center["x"] - self.center["x"]) ** 2) + ((self.game.player.center["y"] - self.center["y"]) ** 2)) ** 0.5

    def attack(self):

        ## random damage by weapon damage range ##
        damage = random.randint(self.damage[0], self.damage[1])

        ## check if has collision with player ##
        if self.collision("player", self.collider1):

            ## decrease player life and set timer for next attack ##
            self.game.player.life -= damage
            self.timer = self.delay

            self.game.sound["channels"]["enemies_attacks"].play(self.game.sound["bite"], 0)

    def sound(self):
        if not self.channel.get_busy():
            sound = "enemy" + str(random.randint(1, 4))
            self.channel.play(self.game.sound[sound], 0)
        
        volume_distance = (100 - (self.player_distance / 5)) * 0.01
        volume_geral = self.game.settings["volume"]["effects"] * self.game.settings["volume"]["geral"]
        volume = (volume_geral * volume_distance) * 0.8

        if volume < 0:
            volume = 0

        self.channel.set_volume(volume)

    def update(self):

        ## update gunshot timer ##
        if self.timer > 0:
            self.timer -= 1
        else:
            self.attack()

        self.update_angle()
        self.update_position()
        self.update_colliders()

        if self.model == "zombie":
            self.sound()

        ## kill if enemy has no life ##
        if self.life <= 0:
            ## increse player score ##
            self.game.player.score += 100

            if self.model == "zombie":
                self.channel.stop()
                self.channel = None

            self.touch.kill()
            self.kill()
