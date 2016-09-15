import math
import os

import pygame

import zwave.helper
from zwave.enemy import *
from zwave.map import *
from zwave.player import *


class Main:
    def __init__(self, text, scale = 1, width = 1024, height = 512):

        self.text = text
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
        self.tick = 40
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

        self.hub = Hub(self)
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
        self.sound["channels"]["enemies_attacks"] = pygame.mixer.Channel(4)

        ## load, set volume and init music background ##
        pygame.mixer.music.load(os.path.join("assets", "sounds", "music", "1.ogg"))
        pygame.mixer.music.set_volume(self.sound["volume"]["music"] * self.sound["volume"]["geral"])
        pygame.mixer.music.play(-1)

        ## footsteps sound ##
        self.sound["channels"]["steps"].set_volume(self.sound["volume"]["effects"] * self.sound["volume"]["geral"])
        self.sound["steps"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "footsteps.ogg"))

        ## gun shot sound ##
        self.sound["channels"]["attacks"].set_volume(self.sound["volume"]["effects"] * self.sound["volume"]["geral"])
        self.sound["gunshot"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "attacks", "gunshot.ogg"))

        ## enemy attack sound ##
        self.sound["channels"]["enemies_attacks"].set_volume(self.sound["volume"]["effects"] * self.sound["volume"]["geral"])
        self.sound["bite"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "attacks", "bite.ogg"))

    def set_cursor(self):
        pygame.mouse.set_visible(False)
        self.cursor["x"] = 0
        self.cursor["y"] = 0
        self.cursor["size"] = 35
        self.cursor["image"] = os.path.join("assets", "img", "cursor.png")
        self.cursor["image"] = zwave.helper.pygame_image(self.cursor["image"], self.cursor["size"])

    def set_enemies(self):
        self.enemies["sprites"] = pygame.sprite.Group()
        self.enemies["colliders"] = pygame.sprite.Group()

        amount = int(math.ceil(self.wave * (self.wave / 2)))
        for i in range(amount):
            enemy = Enemy(self)
            self.enemies["sprites"].add(enemy)
            self.enemies["colliders"].add(enemy.collider2)

    def update_enemies(self):
        for enemy in self.enemies["sprites"].sprites():
            enemy.update()
        if not self.enemies["sprites"].sprites():
            self.wave += 1
            self.set_enemies()
            self.player.wave_update()

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

            self.enemies["sprites"].draw(self.screen)
            self.enemies["colliders"].draw(self.screen)

            self.player.draw()

            self.screen.blit(self.map.surface["walls"], (self.map.x, self.map.y))

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
            
            ## draw hub ##
            self.hub.update()

            ## draw cursor ##
            self.screen.blit(self.cursor["image"], (self.cursor["x"] - (self.cursor["size"] / 2), self.cursor["y"] - (self.cursor["size"] / 2)))

            ## increment or reset atual frame ##
            self.frame = (self.frame + 1) if self.frame < self.tick else 0

            ## pygame clock tick ##
            clock.tick(self.tick)

            ## update pygame screen ##
            pygame.display.update()

class Hub:
    def __init__(self, main):

        pygame.font.init()
        self.font = {}
        self.font["default"] = pygame.font.Font(pygame.font.get_default_font(), 14)

        ## init values ##
        self.main = main
        self.life_percentage = 100

        self.avatar = {}
        self.avatar["width"] = 107
        self.avatar["height"] = 107
        self.avatar["x"] = 10
        self.avatar["y"] = 10
        self.avatar["image"] = []

        self.lifebar = {}
        self.lifebar["width"] = 203
        self.lifebar["height"] = 36
        self.lifebar["x"] = 63
        self.lifebar["y"] = 15
        self.lifebar["background"] = None

        self.score = {}
        self.score["height"] = 30
        self.score["x"] = 80
        self.score["y"] = 50

        self.wave = {}
        self.wave["height"] = 30
        self.wave["x"] = self.main.width - 10
        self.wave["y"] = 10

        self.enemies = {}
        self.enemies["height"] = 30
        self.enemies["x"] = self.main.width - 10
        self.enemies["y"] = 45

        self.set_surfaces()

    def set_surfaces(self):

        ## loads the avatar with different expressions ##
        path = os.path.join("assets", "img", "players", self.main.player.model, "avatar_01.png")
        self.avatar["image"].append(zwave.helper.pygame_image(path, self.avatar["width"], self.avatar["height"]))
        path = os.path.join("assets", "img", "players", self.main.player.model, "avatar_02.png")
        self.avatar["image"].append(zwave.helper.pygame_image(path, self.avatar["width"], self.avatar["height"]))
        path = os.path.join("assets", "img", "players", self.main.player.model, "avatar_03.png")
        self.avatar["image"].append(zwave.helper.pygame_image(path, self.avatar["width"], self.avatar["height"]))

        ## lifebar background ##
        self.lifebar["background"] = pygame.surface.Surface((self.lifebar["width"], self.lifebar["height"]))
        self.lifebar["background"].set_alpha(127)
        self.lifebar["background"].fill(( 0, 0, 0))

    def converter(self, part, total, ctype = "percentage"):
        if ctype == "percentage":
            return (part / total) * 100

    def draw_lifebar(self):

        ## set color acording to the life percentage ##
        if self.life_percentage < 35:
            color = (195, 100, 70)
        elif self.life_percentage < 65:
            color = (195, 175, 70)
        else:
            color = (45, 200, 100)

        ## lifebar getal background ##
        self.main.screen.blit(self.lifebar["background"], (self.lifebar["x"], self.lifebar["y"]))

        ## lifebar ##
        pygame.draw.rect(self.main.screen, color, (self.lifebar["x"], self.lifebar["y"] + 3, self.life_percentage * 2, 30))

        ## lifebar text ##
        text = "%s: %i / %i" % (self.main.text["life"].upper(), self.main.player.status["life"], self.main.player.status["total_life"])
        text = self.font["default"].render(text, 1, (255,255,255))

        ## lifebar text background ##
        surface = pygame.Surface((self.lifebar["width"] - 6, self.lifebar["height"] - 12))
        surface.fill((0, 0, 0))
        surface.blit(text, pygame.Rect(60, 5, text.get_rect().width, text.get_rect().height))
        surface.set_alpha(150)

        ## draw text and text background ##
        self.main.screen.blit(surface, (self.lifebar["x"], self.lifebar["y"] + 6))

    def draw_score(self):

        ## score text ##
        text = "%s: %i" % (self.main.text["score"].upper(), self.main.player.status["score"])
        text = self.font["default"].render(text, 1, (255,255,255))

        ## score background ##
        surface = pygame.Surface((text.get_rect().width + 60, self.score["height"]))
        surface.fill((0, 0, 0))
        surface.blit(text, pygame.Rect(43, 8, text.get_rect().width, text.get_rect().height))
        surface.set_alpha(150)

        ## draw score ##
        self.main.screen.blit(surface, (self.score["x"], self.score["y"] + 6))
    
    def draw_avatar(self):

        ## set avatar acording to the life percentage ##
        if self.life_percentage < 35:
            avatar = self.avatar["image"][2]
        elif self.life_percentage < 65:
            avatar = self.avatar["image"][1]
        else:
            avatar = self.avatar["image"][0]

        ## draw avatar ##
        self.main.screen.blit(avatar, (self.avatar["x"], self.avatar["y"]))

    def draw_wave(self):

        ## wave text ##
        text = "%s: %i" % (self.main.text["wave"].upper(), self.main.wave)
        text = self.font["default"].render(text, 1, (255,255,255))

        ## wave background ##
        surface = pygame.Surface((text.get_rect().width + 16, self.wave["height"]))
        surface.fill((0, 0, 0))
        surface.blit(text, pygame.Rect(8, 8, text.get_rect().width, text.get_rect().height))
        surface.set_alpha(150)

        ## draw wave ##
        self.main.screen.blit(surface, (self.wave["x"] - surface.get_rect().width, self.wave["y"]))

    def draw_enemies(self):

        ## enemies text ##
        text = "%s: %i" % (self.main.text["enemies"].upper(), len(self.main.enemies["sprites"].sprites()))
        text = self.font["default"].render(text, 1, (255,255,255))

        ## enemies background ##
        surface = pygame.Surface((text.get_rect().width + 16, self.enemies["height"]))
        surface.fill((0, 0, 0))
        surface.blit(text, pygame.Rect(8, 8, text.get_rect().width, text.get_rect().height))
        surface.set_alpha(150)

        ## draw enemies ##
        self.main.screen.blit(surface, (self.enemies["x"] - surface.get_rect().width, self.enemies["y"]))

    def draw(self):
        self.draw_lifebar()
        self.draw_score()
        self.draw_avatar()
        self.draw_wave()
        self.draw_enemies()

    def update(self):
        self.life_percentage = self.converter(self.main.player.status["life"], self.main.player.status["total_life"])
        self.draw()
