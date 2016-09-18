import math
import os

import pygame

import zwave.helper
import zwave.lobby
from zwave.enemy import *
from zwave.map import *
from zwave.player import *


class Main:
    def __init__(self, text, scale, width, height, fullscreen):

        ## init values ##
        self.fullscreen = fullscreen
        self.text = text
        self.last = {}
        self.scale = scale
        self.width = width
        self.height = height
        self.wave = 1
        self.center = {}
        self.center["x"] = self.width / 2
        self.center["y"] = self.height / 2

        ## framerate ##
        self.tick = 40
        self.frame = 0
        self.timer = 241

        ## game screen ##

        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))

        ## game sounds ##
        self.sound = {}
        self.set_sounds()

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

        self.hub = Hub(self)
        self.loop()

    def set_sounds(self):

        self.sound["volume"] = {}
        self.sound["volume"]["geral"] = 1
        self.sound["volume"]["music"] = 0.2
        self.sound["volume"]["effects"] = 0.8

        ## init pygame mixer and configure ##
        pygame.mixer.init(22050, -16, 1, 512)
        pygame.mixer.set_num_channels(34)

        ## set channels ##
        self.sound["channels"] = {}
        self.sound["channels"]["steps"] = pygame.mixer.Channel(31)
        self.sound["channels"]["attacks"] = pygame.mixer.Channel(32)
        self.sound["channels"]["enemies_attacks"] = pygame.mixer.Channel(33)

        ## load, set volume and init music background ##
        pygame.mixer.music.load(os.path.join("assets", "sounds", "music", "2.ogg"))
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

        ## zombies sounds ##
        self.sound["enemy1"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "enemies", "zombies", "1.ogg"))
        self.sound["enemy2"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "enemies", "zombies", "2.ogg"))
        self.sound["enemy3"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "enemies", "zombies", "3.ogg"))
        self.sound["enemy4"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "enemies", "zombies", "4.ogg"))

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

        amount = int(math.ceil(self.wave * (self.wave / 2.0)))
        if amount > 30:
            amount = 30
        for i in range(amount):
            enemy = Enemy(self, i)
            self.enemies["sprites"].add(enemy)
            self.enemies["colliders"].add(enemy.collider2)

    def update_enemies(self):
        for enemy in self.enemies["sprites"].sprites():
            enemy.update()
        if not self.enemies["sprites"].sprites():
            if self.timer > 0:
                self.timer -= 1
            else:
                self.wave += 1
                self.set_enemies()
                self.player.wave_update()
                self.timer = 241

    def back_to_lobby(self):
        self.running = False
        pygame.mixer.stop()
        pygame.display.quit()
        zwave.lobby.Lobby()

    def loop(self):

        ## set pygame clock ##
        clock = pygame.time.Clock()

        self.running = True
        while self.running:

            pygame.display.set_caption("FPS: %.0f" % clock.get_fps())
            self.screen.fill((100, 125, 130))

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

            ## game quit ##
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] and self.fullscreen:
                self.back_to_lobby()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.back_to_lobby()

class Hub:
    def __init__(self, main):

        pygame.font.init()

        self.font = {}
        path = os.path.join("assets", "fonts", "Renogare.ttf")
        self.font["default"] = pygame.font.Font(path, 14)
        self.font["big"] = pygame.font.Font(path, 50)

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
        self.wave["x"] = self.main.width - 15
        self.wave["y"] = 50

        self.enemies = {}
        self.enemies["height"] = 30
        self.enemies["x"] = self.main.width - 15
        self.enemies["y"] = 15

        self.attributes = {}
        self.attributes["height"] = 30
        self.attributes["x"] = self.main.width - 15
        self.attributes["y"] = self.main.height - 15

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
            value = (float(part) / total) * 100.0
            if value < 0:
                value = 0
            return value

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
        text = "%s: %i / %i" % (self.main.text["life"].upper(), self.main.player.life, self.main.player.total_life)
        text = self.font["default"].render(text, 1, (255,255,255))

        ## lifebar text background ##
        surface = pygame.Surface((self.lifebar["width"] - 6, self.lifebar["height"] - 12))
        surface.fill((0, 0, 0))
        surface.blit(text, pygame.Rect(60, 6, text.get_rect().width, text.get_rect().height))
        surface.set_alpha(150)

        ## draw text and text background ##
        self.main.screen.blit(surface, (self.lifebar["x"], self.lifebar["y"] + 6))

    def draw_score(self):

        ## score text ##
        text = "%s: %i" % (self.main.text["score"].upper(), self.main.player.score)
        text = self.font["default"].render(text, 1, (255,255,255))

        ## score background ##
        surface = pygame.Surface((text.get_rect().width + 60, self.score["height"]))
        surface.fill((0, 0, 0))
        surface.blit(text, pygame.Rect(43, 9, text.get_rect().width, text.get_rect().height))
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
        surface.blit(text, pygame.Rect(8, 9, text.get_rect().width, text.get_rect().height))
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
        surface.blit(text, pygame.Rect(8, 9, text.get_rect().width, text.get_rect().height))
        surface.set_alpha(150)

        ## draw enemies ##
        self.main.screen.blit(surface, (self.enemies["x"] - surface.get_rect().width, self.enemies["y"]))

    def draw_wave_timer(self):

        ## checks if the timer is being modified ##
        if self.main.timer < 241:

            ## get seconds ##
            timer = int(self.main.timer / self.main.tick)

            ## timer text ##
            text = "%i" % (timer)
            text = self.font["big"].render(text, 1, (255,255,255))

            ## timer background ##
            surface = pygame.Surface((100, text.get_rect().height + 6))
            surface.fill((0, 0, 0))
            surface.blit(text, pygame.Rect(50 - (text.get_rect().width / 2), 9, text.get_rect().width, text.get_rect().height))
            surface.set_alpha(150)

            ## draw timer ##
            x = self.main.center["x"] - (surface.get_rect().width / 2)
            y = self.main.center["y"] - (surface.get_rect().height * 3)
            self.main.screen.blit(surface, (x, y))

    def draw_attributes(self):

        ## timer text ##
        speed = "%s: %.1f" % (self.main.text["speed"], self.main.player.speed)
        attackspeed = 1 + (1 - (self.main.player.weapon["delay"] / float(self.main.tick)))
        attackspeed = "%s: %.1f" % (self.main.text["attack_speed"], attackspeed)
        damage = "%i - %i" % (self.main.player.weapon["damage"][0], self.main.player.weapon["damage"][1])
        damage = "%s: [%s]" % (self.main.text["damage"], damage)
        text = "%s  |  %s  |  %s" % (speed, attackspeed, damage)
        text = self.font["default"].render(text.upper(), 1, (255,255,255))

        ## timer background ##
        surface = pygame.Surface((text.get_rect().width + 16, text.get_rect().height + 12))
        surface.fill((0, 0, 0))
        surface.blit(text, pygame.Rect(8, 7, text.get_rect().width, text.get_rect().height))
        surface.set_alpha(150)

        ## draw timer ##
        x = self.attributes["x"] - surface.get_rect().width
        y = self.attributes["y"] - surface.get_rect().height
        self.main.screen.blit(surface, (x, y))

    def draw(self):
        self.draw_lifebar()
        self.draw_score()
        self.draw_avatar()
        self.draw_wave()
        self.draw_enemies()
        self.draw_attributes()
        self.draw_wave_timer()

    def update(self):
        self.life_percentage = self.converter(self.main.player.life, self.main.player.total_life)
        self.draw()
