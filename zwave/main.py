import os
import pygame

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
        self.view["last_x"] = 0
        self.view["last_y"] = 0


        ## framerate ##
        self.tick = 60
        self.frame = 0

        ## game screen ##
        self.screen = pygame.display.set_mode((self.view["width"], self.view["height"]))

        ## cursor ##
        pygame.mouse.set_visible(False)
        self.cursor = {}
        self.cursor["x"] = 0
        self.cursor["y"] = 0
        self.cursor["size"] = 35
        self.cursor["image"] = pygame.image.load(os.path.join("assets", "img", "cursor.png")).convert_alpha()
        self.cursor["image"] = pygame.transform.scale(self.cursor["image"], (self.cursor["size"], self.cursor["size"]))

        ## game map ##
        self.map = Map(self)

        ## game view x and y ##
        self.view["x"] = (self.map.view["width"] / 2) - (width / 2)
        self.view["y"] = (self.map.view["height"] / 2) - (height / 2)

        ## player ##
        self.player = Player(self)

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

        pygame.mixer.init(44100, -16, 2, 512)
        pygame.mixer.set_num_channels(8)

        self.sounds = {}
        self.sounds["volume"] = {}
        self.sounds["channels"] = {}
        self.sounds["musics"] = {}
        self.sounds["steps"] = {}

        self.sounds["volume"]["geral"] = 0.8
        self.sounds["volume"]["music"] = 0.5
        self.sounds["volume"]["effects"] = 0.2

        self.sounds["steps"]["last"] = None
        self.sounds["steps"]["marble"] = None
        self.sounds["channels"]["steps"] = pygame.mixer.Channel(2)

        self.load_sounds()

        ## init music ##
        self.sounds["channels"]["steps"].set_volume(self.sounds["volume"]["effects"] * self.sounds["volume"]["geral"])
        pygame.mixer.music.set_volume(self.sounds["volume"]["music"] * self.sounds["volume"]["geral"])
        pygame.mixer.music.play()

        ## init game loop ##
        self.loop()

    ## theme song ##
    def load_sounds(self):
        pygame.mixer.music.load(os.path.join("assets", "sounds", "music", "02.ogg"))
        self.sounds["steps"]["marble"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "steps", "marble.ogg"))
        self.sounds["steps"]["sand"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "steps", "sand.ogg"))
        self.sounds["steps"]["grass"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "steps", "grass.ogg"))

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

        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
            if self.player.collision("grass"):
                if (not self.sounds["steps"]["last"] == "grass") and self.sounds["channels"]["steps"].get_busy():
                    self.sounds["channels"]["steps"].stop()
                elif not self.sounds["channels"]["steps"].get_busy():
                    self.sounds["channels"]["steps"].play(self.sounds["steps"]["grass"])
                    self.sounds["steps"]["last"] = "grass"

            elif self.player.collision("marble"):
                if (not self.sounds["steps"]["last"] == "marble") and self.sounds["channels"]["steps"].get_busy():
                    self.sounds["channels"]["steps"].stop()
                elif not self.sounds["channels"]["steps"].get_busy():
                    self.sounds["channels"]["steps"].play(self.sounds["steps"]["marble"], True)
                    self.sounds["steps"]["last"] = "marble"

            elif self.player.collision("sand"):
                if (not self.sounds["steps"]["last"] == "sand") and self.sounds["channels"]["steps"].get_busy():
                    self.sounds["channels"]["steps"].stop()
                elif not self.sounds["channels"]["steps"].get_busy():
                    self.sounds["channels"]["steps"].play(self.sounds["steps"]["sand"], True)
                    self.sounds["steps"]["last"] = "sand"
        else:
            self.sounds["channels"]["steps"].stop()

        ## speed to axes in diagonal movement ##
        if (keys[pygame.K_w] or keys[pygame.K_s]) and (keys[pygame.K_a] or keys[pygame.K_d]):
            velocity = 1.5 * self.view["scale"]

        ## speed to axes in horizontal and vertical movements ##
        else:
            velocity = 2 * self.view["scale"]

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

            ## update pygame screen ##
            pygame.display.update()

            ## cursor x position ##
            self.cursor["x"] = pygame.mouse.get_pos()[0]

            ## cursor y position ##
            self.cursor["y"] = pygame.mouse.get_pos()[1]

            ## events hunter ##
            for event in pygame.event.get():

                ## qui event ##
                if event.type == pygame.QUIT:
                    running = False

            ## increment or reset atual frame ##
            self.frame = (self.frame + 1) if self.frame < self.tick else 0

            ## pygame clock tick ##
            clock.tick(self.tick)
