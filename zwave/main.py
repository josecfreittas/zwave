import os
import pygame

import zwave.helper
from zwave.map import *
from zwave.player import *
from zwave.enemy import *

class Main:

    ## constructor ##
    def __init__(self, scale = 1, width = 1024, height = 512):

        ## game view ##
        self.view = {}
        self.view["scale"] = scale
        self.view["width"] = width
        self.view["height"] = height
        self.view["last"] = 0
        self.center = {}
        self.center["x"] = self.view["width"] / 2
        self.center["y"] = self.view["height"] / 2

        ## framerate ##
        self.tick = 60
        self.frame = 0

        ## game screen ##
        self.screen = pygame.display.set_mode((self.view["width"], self.view["height"]))

        ## TODO: Make a method to handle with the cursor ##
        ## cursor ##
        pygame.mouse.set_visible(False)
        self.cursor = {}
        self.cursor["x"] = 0
        self.cursor["y"] = 0
        self.cursor["size"] = 35
        self.cursor["image"] = os.path.join("assets", "img", "cursor.png")
        self.cursor["image"] = zwave.helper.pygame_image(self.cursor["image"], self.cursor["size"])

        ## game map ##
        self.map = Map(self)

        ## game view x and y ##
        self.view["x"] = (self.map.view["width"] / 2) - (width / 2)
        self.view["y"] = (self.map.view["height"] / 2) - (height / 2)

        ## player ##
        self.player = Player(self)

        ## TODO: Make a method to auto-make enemies dynamically ##
        ## make enemy ##
        self.enemies = {}
        self.enemies["sprites"] = []
        self.enemies["sprites"].append(Enemy(self))
        self.enemies["sprites"].append(Enemy(self))
        self.enemies["sprites"].append(Enemy(self))
        self.enemies["group"] = pygame.sprite.Group()
        self.enemies["colliders"] = pygame.sprite.Group()
        self.enemies["group"].add(self.enemies["sprites"][0].surface["sprite"])
        self.enemies["colliders"].add(self.enemies["sprites"][0].collider["sprite1"])
        self.enemies["group"].add(self.enemies["sprites"][1].surface["sprite"])
        self.enemies["colliders"].add(self.enemies["sprites"][1].collider["sprite1"])
        self.enemies["group"].add(self.enemies["sprites"][2].surface["sprite"])
        self.enemies["colliders"].add(self.enemies["sprites"][2].collider["sprite1"])

        ## game sound ##
        self.sound = {}
        self.sound["volume"] = {}
        self.sound["volume"]["geral"] = 1
        self.sound["volume"]["music"] = 0.5
        self.sound["volume"]["effects"] = 0.8

        ## init game loop ##
        self.sounds()
        self.loop()

    ## theme song ##
    def sounds(self):

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

    ## method to update enemies ##
    def update_enemies(self):
        for enemy in self.enemies["sprites"]:
            enemy.update()

    ## method to player/screen movimentation ##
    def move(self):

        ## check if had collision, if had, set last position of view ##
        if self.player.collision("walls") or self.player.collision("enemies"):
            self.view["x"] = self.view["last_x"]
            self.view["y"] = self.view["last_y"]

        ## save current positon of view for future use ##
        self.view["last_x"] = self.view["x"]
        self.view["last_y"] = self.view["y"]

        ## make 'keys' variable with pressed keys
        keys = pygame.key.get_pressed()

        ## footsteps sound if the player is walking ##
        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
            if not self.sound["channels"]["steps"].get_busy():
                self.sound["channels"]["steps"].play(self.sound["steps"], -1)
        else:
            self.sound["channels"]["steps"].stop()
        
        ## picks speed for each axis ##
        velocity = zwave.helper.velocity_by_keys(2 * self.view["scale"], keys)

        ## movement according to keys down ##
        if keys[pygame.K_w]:
            self.view["y"] -= velocity
        if keys[pygame.K_s]:
            self.view["y"] += velocity
        if keys[pygame.K_a]:
            self.view["x"] -= velocity
        if keys[pygame.K_d]:
            self.view["x"] += velocity

    ## method from game loop ##
    def loop(self):

        ## set pygame clock ##
        clock = pygame.time.Clock()

        running = True
        while running:

            pygame.display.set_caption("FPS: %.0f" % clock.get_fps())

            ## call method responsible for move view to new destiny, if one exists ##
            self.move()

            ## update map ##
            self.map.update()

            ## update player ##
            self.player.update()

            ## enemy update ##
            self.update_enemies()

            ## draw map ground ##
            self.screen.blit(self.map.surface["ground"], (self.map.view["x"], self.map.view["y"]))

            ## draw enemies ##
            self.enemies["group"].draw(self.screen)

	        ## draw player ##
            self.screen.blit(self.player.surface["sprite"], (self.player.view['x'], self.player.view['y']))

            ## draw map walls and shadows ##
            self.screen.blit(self.map.surface["walls"], (self.map.view["x"], self.map.view["y"]))

            ## draw cursor ##
            self.screen.blit(self.cursor["image"], (self.cursor["x"] - (self.cursor["size"] / 2), self.cursor["y"] - (self.cursor["size"] / 2)))

            ## cursor x position ##
            self.cursor["x"] = pygame.mouse.get_pos()[0]

            ## cursor y position ##
            self.cursor["y"] = pygame.mouse.get_pos()[1]

            ## events hunter ##
            for event in pygame.event.get():

                ## qui event ##
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
