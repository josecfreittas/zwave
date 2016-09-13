import os
import math
import pygame
import zwave.helper
from zwave.map import *
from zwave.player import *
from zwave.enemy import *

class Main:

    ## constructor ##
    def __init__(self, scale = 1, width = 1024, height = 512):

        ## game status ##
        self.wave = 1

        ## game view ##
        self.last = {}
        self.scale = scale
        self.width = width
        self.height = height
        self.center = {}
        self.center["x"] = self.width / 2
        self.center["y"] = self.height / 2

        ## framerate ##
        self.tick = 50
        self.frame = 0

        ## game screen ##
        self.screen = pygame.display.set_mode((self.width, self.height))

        ## game cursor ##
        self.cursor = {}
        self.set_cursor()

        ## game map ##
        self.map = Map(self)

        ## game view x and y ##
        self.x = self.map.center["x"] - self.center["x"]
        self.y = self.map.center["y"] - self.center["y"]

        ## player ##
        self.player = Player(self)

        ## game enemies ##
        self.enemies = {}
        self.set_enemies()

        ## game sounds ##
        self.sound = {}
        self.set_sounds()

        self.loop()

    def set_sounds(self):

        self.sound["volume"] = {}
        self.sound["volume"]["geral"] = 1
        self.sound["volume"]["music"] = 0.5
        self.sound["volume"]["effects"] = 0.8

        ## init pygame mixer and configure ##
        pygame.mixer.init(44100, -16, 2, 512)
        pygame.mixer.set_num_channels(8)

        ## set channels ##
        self.sound["channels"] = {}
        self.sound["channels"]["steps"] = pygame.mixer.Channel(2)
        self.sound["channels"]["attacks"] = pygame.mixer.Channel(3)

        ## load, set volume and init music background ##
        pygame.mixer.music.load(os.path.join("assets", "sounds", "music", "02.ogg"))
        pygame.mixer.music.set_volume(self.sound["volume"]["music"] * self.sound["volume"]["geral"])
        pygame.mixer.music.play(-1)

        ## footsteps sound ##
        self.sound["channels"]["steps"].set_volume(self.sound["volume"]["effects"] * self.sound["volume"]["geral"])
        self.sound["steps"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "footsteps.ogg"))

        ## gun shot sound ##
        self.sound["channels"]["attacks"].set_volume(self.sound["volume"]["effects"] * self.sound["volume"]["geral"])
        self.sound["gunshot"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "attacks", "gunshot.ogg"))
    

    def set_cursor(self):
        pygame.mouse.set_visible(False)
        self.cursor["x"] = 0
        self.cursor["y"] = 0
        self.cursor["size"] = 35
        self.cursor["image"] = os.path.join("assets", "img", "cursor.png")
        self.cursor["image"] = zwave.helper.pygame_image(self.cursor["image"], self.cursor["size"])

    def set_enemies(self):

        self.enemies["sprites"] = []
        self.enemies["group"] = pygame.sprite.Group()
        self.enemies["colliders"] = pygame.sprite.Group()

        amount = math.ceil(self.wave * (self.wave / 2))

        for enemy in range(amount):
            self.enemies["sprites"].append(Enemy(self))
            self.enemies["group"].add(self.enemies["sprites"][enemy].surface["sprite"])
            self.enemies["colliders"].add(self.enemies["sprites"][enemy].collider["sprite1"])

    ## method to update enemies ##
    def update_enemies(self):
        for enemy in self.enemies["sprites"]:
            enemy.update()

    ## method from game loop ##
    def loop(self):

        ## set pygame clock ##
        clock = pygame.time.Clock()

        running = True
        while running:

            pygame.display.set_caption("FPS: %.0f" % clock.get_fps())

            ## update map, player, enemies ##
            self.map.update()
            self.player.update()
            self.update_enemies()

            ## draw map ground, enemies, player, map walls and cursor ##
            self.screen.blit(self.map.surface["ground"], (self.map.x, self.map.y))
            self.enemies["group"].draw(self.screen)
            self.player.update_bullets()
            self.screen.blit(self.player.surface["sprite"], (self.player.x, self.player.y))
            self.screen.blit(self.map.surface["walls"], (self.map.x, self.map.y))
            self.screen.blit(self.cursor["image"], (self.cursor["x"] - (self.cursor["size"] / 2), self.cursor["y"] - (self.cursor["size"] / 2)))

            ## cursor x position ##
            self.cursor["x"] = pygame.mouse.get_pos()[0]
            self.cursor["y"] = pygame.mouse.get_pos()[1]

            ## events hunter ##
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            ## check if the left mouse button is pressed ##
            if pygame.mouse.get_pressed()[0]:
                self.player.shot()

            ## increment or reset atual frame ##
            self.frame = (self.frame + 1) if self.frame < self.tick else 0

            ## pygame clock tick ##
            clock.tick(self.tick)

            ## update pygame screen ##
            pygame.display.update()
