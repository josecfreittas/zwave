import math
import os

import pygame

import zwave.helper
import zwave.lobby
from zwave.enemy import *
from zwave.map import *
from zwave.player import *


class Game:
    def __init__(self, text, settings):

        ## init values ##
        self.settings = settings
        self.paused = False
        self.scale = self.settings["scale"]
        self.width = self.settings["width"]
        self.height = self.settings["height"]
        self.wave = 1
        self.text = text
        self.last = {}
        self.center = {}
        self.center["x"] = self.width / 2
        self.center["y"] = self.height / 2

        ## framerate ##
        self.tick = 50
        self.frame = 0
        self.timer = 241

        ## game screen ##

        if self.settings["fullscreen"]:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))

        ## game sounds ##
        self.sound = {}
        self.set_sounds()

        ## game cursor ##
        self.mouse = {}
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
        pygame.mixer.music.set_volume(self.settings["volume"]["music"] * self.settings["volume"]["geral"])
        pygame.mixer.music.play(-1)

        ## footsteps sound ##
        self.sound["channels"]["steps"].set_volume(self.settings["volume"]["effects"] * self.settings["volume"]["geral"])
        self.sound["steps"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "footsteps.ogg"))

        ## gun shot sound ##
        self.sound["channels"]["attacks"].set_volume(self.settings["volume"]["effects"] * self.settings["volume"]["geral"])
        self.sound["gunshot"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "attacks", "gunshot.ogg"))

        ## enemy attack sound ##
        self.sound["channels"]["enemies_attacks"].set_volume(self.settings["volume"]["effects"] * self.settings["volume"]["geral"])
        self.sound["bite"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "attacks", "bite.ogg"))

        ## zombies sounds ##
        self.sound["enemy1"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "enemies", "zombies", "1.ogg"))
        self.sound["enemy2"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "enemies", "zombies", "2.ogg"))
        self.sound["enemy3"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "enemies", "zombies", "3.ogg"))
        self.sound["enemy4"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "enemies", "zombies", "4.ogg"))

    def set_cursor(self):
        self.mouse["x"] = 0
        self.mouse["y"] = 0
        pygame.mouse.set_visible(False)
        size = 35
        image = os.path.join("assets", "img", "cursor.png")
        image = zwave.helper.pygame_image(image, size)
        sprite = zwave.helper.pygame_sprite_by_image(image)
        self.cursor = pygame.sprite.GroupSingle(sprite)

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

        ## update all enemies ##
        for enemy in self.enemies["sprites"].sprites():
            enemy.update()

        ## check if all enemies are dead ##
        if not self.enemies["sprites"].sprites():

            ## update timer for new wave ##
            if self.timer > 0:
                self.timer -= 1
            else:

                ## init new wave ##
                self.wave += 1
                self.set_enemies()
                self.player.wave_update()
                self.timer = 241

    def back_to_lobby(self):

        ## stop game, stop sounds and quit pygame display ##
        self.running = False
        pygame.mixer.stop()
        pygame.display.quit()

        ## init game lobby ##
        zwave.lobby.Lobby()

    def loop(self):

        ## set pygame clock ##
        clock = pygame.time.Clock()

        self.running = True
        while self.running:

            pygame.display.set_caption("FPS: %.0f" % clock.get_fps())

            if (not self.paused) and (self.player.life > 0):
                self.screen.fill((100, 125, 130))

                ## update map, player, enemies ##
                self.map.update()
                self.player.update()
                self.update_enemies()

                ## draw map ground, enemies, player, map walls and cursor ##
                self.screen.blit(self.map.surface["ground"], (self.map.x, self.map.y))

                ## draw enemies ##
                self.enemies["sprites"].draw(self.screen)
                self.enemies["colliders"].draw(self.screen)

                ## draw player ##
                self.player.draw()

                ## draw walls and shadows ##
                self.screen.blit(self.map.surface["walls"], (self.map.x, self.map.y))

            self.hub.update()

            ## cursor new position and draw  ##
            self.mouse["x"] = pygame.mouse.get_pos()[0]
            self.mouse["y"] = pygame.mouse.get_pos()[1]
            self.cursor.sprites()[0].rect.x = pygame.mouse.get_pos()[0] - (35.0 / 2)
            self.cursor.sprites()[0].rect.y = pygame.mouse.get_pos()[1] - (35.0 / 2)
            self.cursor.draw(self.screen)

            ## increment or reset atual frame ##
            self.frame = (self.frame + 1) if self.frame < self.tick else 0

            ## pygame clock tick ##
            clock.tick(self.tick)

            ## update pygame screen ##
            pygame.display.update()

            for event in pygame.event.get():

                ## game exit ##
                if event.type == pygame.QUIT:
                    self.running = False

                ## game pause ##
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused

                ## mouse left click for buttons interaction ##
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.hub.click()

                ## player shot if game is not paused ##
                if event.type == pygame.MOUSEBUTTONDOWN and not self.paused:
                    self.player.shot()

class Hub:
    def __init__(self, game):

        pygame.font.init()

        self.font = {}
        path = os.path.join("assets", "fonts", "Renogare.ttf")
        self.font["default"] = pygame.font.Font(path, 14)
        self.font["button"] = pygame.font.Font(path, 30)
        self.font["big"] = pygame.font.Font(path, 50)

        ## init values ##
        self.game = game
        self.life = 100

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
        self.wave["x"] = self.game.width - 15
        self.wave["y"] = 50

        self.enemies = {}
        self.enemies["height"] = 30
        self.enemies["x"] = self.game.width - 15
        self.enemies["y"] = 15

        self.attributes = {}
        self.attributes["height"] = 30
        self.attributes["x"] = self.game.width - 15
        self.attributes["y"] = self.game.height - 15

        self.set_surfaces()

    def set_surfaces(self):

        ## loads the avatar with different expressions ##
        path = os.path.join("assets", "img", "players", self.game.player.model, "avatar_01.png")
        self.avatar["image"].append(zwave.helper.pygame_image(path, self.avatar["width"], self.avatar["height"]))
        path = os.path.join("assets", "img", "players", self.game.player.model, "avatar_02.png")
        self.avatar["image"].append(zwave.helper.pygame_image(path, self.avatar["width"], self.avatar["height"]))
        path = os.path.join("assets", "img", "players", self.game.player.model, "avatar_03.png")
        self.avatar["image"].append(zwave.helper.pygame_image(path, self.avatar["width"], self.avatar["height"]))

        ## lifebar background ##
        self.lifebar["background"] = pygame.surface.Surface((self.lifebar["width"], self.lifebar["height"]))
        self.lifebar["background"].set_alpha(127)
        self.lifebar["background"].fill(( 0, 0, 0))

        ## resume game button ##
        x = 10
        y = (self.game.height / 2) - 65
        self.bt_resume = {}
        self.bt_resume["normal"] = zwave.helper.pygame_button(self.game.text["resume"].upper(), self.font["button"], x, y, (50, 50, 50), "right")
        self.bt_resume["hover"] = zwave.helper.pygame_button(self.game.text["resume"].upper(), self.font["button"], x, y, (0, 140, 90), "right")
        self.bt_resume["draw"] =  self.bt_resume["normal"]

        ## main manu button ##
        x = 10
        y = self.game.height / 2
        self.bt_main = {}
        self.bt_main["normal"] = zwave.helper.pygame_button(self.game.text["main"].upper(), self.font["button"], x, y, (50, 50, 50), "right")
        self.bt_main["hover"] = zwave.helper.pygame_button(self.game.text["main"].upper(), self.font["button"], x, y, (0, 140, 90), "right")
        self.bt_main["draw"] =  self.bt_main["normal"]

    def converter(self, part, total, ctype = "percentage"):
        if ctype == "percentage":
            value = (float(part) / total) * 100.0
            if value < 0:
                value = 0
            return value

    def mouse_hover(self, button):

        ## checks if has a collision with cursor and button ##
        if pygame.sprite.groupcollide(self.game.cursor, button, False, False):
            return True
        else:
            return False

    def update_button(self, button, selected = False):

        ## checks if the mouse is over the button and change your appearance if yes or not ## 
        if self.mouse_hover(button["draw"]):
            button["draw"] = button["hover"]
        else:
            button["draw"] = button["normal"]

        if selected:
            button["selected"].draw(self.game.screen)
        else:
            button["draw"].draw(self.game.screen)

    def draw_lifebar(self):

        ## set color acording to the life percentage ##
        if self.life < 35:
            color = (195, 100, 70)
        elif self.life < 65:
            color = (195, 175, 70)
        else:
            color = (45, 200, 100)

        ## lifebar ##
        self.game.screen.blit(self.lifebar["background"], (self.lifebar["x"], self.lifebar["y"]))
        pygame.draw.rect(self.game.screen, color, (self.lifebar["x"], self.lifebar["y"] + 3, self.life * 2, 30))

        ## lifebar text ##
        text = "%s: %i / %i" % (self.game.text["life"].upper(), self.game.player.life, self.game.player.total_life)
        text = self.font["default"].render(text, 1, (255,255,255))

        ## lifebar text background ##
        surface = pygame.Surface((self.lifebar["width"] - 6, self.lifebar["height"] - 12))
        surface.fill((0, 0, 0))
        surface.blit(text, pygame.Rect(60, 6, text.get_rect().width, text.get_rect().height))
        surface.set_alpha(150)

        ## draw text and text background ##
        self.game.screen.blit(surface, (self.lifebar["x"], self.lifebar["y"] + 6))

    def draw_score(self):

        ## score text ##
        text = "%s: %i" % (self.game.text["score"].upper(), self.game.player.score)
        text = self.font["default"].render(text, 1, (255,255,255))

        ## score background ##
        surface = pygame.Surface((text.get_rect().width + 60, self.score["height"]))
        surface.fill((0, 0, 0))
        surface.blit(text, pygame.Rect(43, 9, text.get_rect().width, text.get_rect().height))
        surface.set_alpha(150)

        ## draw score ##
        self.game.screen.blit(surface, (self.score["x"], self.score["y"] + 6))
    
    def draw_avatar(self):

        ## set avatar acording to the life percentage ##
        if self.life < 35:
            avatar = self.avatar["image"][2]
        elif self.life < 65:
            avatar = self.avatar["image"][1]
        else:
            avatar = self.avatar["image"][0]

        ## draw avatar ##
        self.game.screen.blit(avatar, (self.avatar["x"], self.avatar["y"]))

    def draw_wave(self):

        ## wave text ##
        text = "%s: %i" % (self.game.text["wave"].upper(), self.game.wave)
        text = self.font["default"].render(text, 1, (255,255,255))

        ## wave background ##
        surface = pygame.Surface((text.get_rect().width + 16, self.wave["height"]))
        surface.fill((0, 0, 0))
        surface.blit(text, pygame.Rect(8, 9, text.get_rect().width, text.get_rect().height))
        surface.set_alpha(150)

        ## draw wave ##
        self.game.screen.blit(surface, (self.wave["x"] - surface.get_rect().width, self.wave["y"]))

    def draw_enemies(self):

        ## enemies text ##
        text = "%s: %i" % (self.game.text["enemies"].upper(), len(self.game.enemies["sprites"].sprites()))
        text = self.font["default"].render(text, 1, (255,255,255))

        ## enemies background ##
        surface = pygame.Surface((text.get_rect().width + 16, self.enemies["height"]))
        surface.fill((0, 0, 0))
        surface.blit(text, pygame.Rect(8, 9, text.get_rect().width, text.get_rect().height))
        surface.set_alpha(150)

        ## draw enemies ##
        self.game.screen.blit(surface, (self.enemies["x"] - surface.get_rect().width, self.enemies["y"]))

    def draw_wave_timer(self):

        ## checks if the timer is being modified ##
        if self.game.timer < 241:

            ## get seconds ##
            timer = int(self.game.timer / self.game.tick)

            ## timer text ##
            text = "%s %i" % (self.game.text["next_wave"].upper() ,timer)
            text = self.font["big"].render(text, 1, (255,255,255))

            ## timer background ##
            surface = pygame.Surface((600, text.get_rect().height + 6))
            surface.fill((0, 0, 0))
            surface.blit(text, pygame.Rect(300 - (text.get_rect().width / 2), 9, text.get_rect().width, text.get_rect().height))
            surface.set_alpha(150)

            ## draw timer ##
            x = self.game.center["x"] - (surface.get_rect().width / 2)
            y = self.game.center["y"] - (surface.get_rect().height * 2)
            self.game.screen.blit(surface, (x, y))

    def draw_attributes(self):

        ## timer text ##
        speed = "%s: %.1f" % (self.game.text["speed"], self.game.player.speed)
        attackspeed = 1 + (1 - (self.game.player.weapon["delay"] / float(self.game.tick)))
        attackspeed = "%s: %.1f" % (self.game.text["attack_speed"], attackspeed)
        damage = "%i - %i" % (self.game.player.weapon["damage"][0], self.game.player.weapon["damage"][1])
        damage = "%s: [%s]" % (self.game.text["damage"], damage)
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
        self.game.screen.blit(surface, (x, y))

    def draw_pause(self):
        self.game.screen.fill((40, 80, 60))
        self.update_button(self.bt_resume)
        self.update_button(self.bt_main)

    def draw_endgame(self):
        self.game.screen.fill((40, 80, 60))

    def draw(self):
        if self.game.paused:
            self.draw_pause()
        elif self.game.player.life < 0:
            self.draw_endgame()
        else:   
            self.draw_lifebar()
            self.draw_score()
            self.draw_avatar()
            self.draw_wave()
            self.draw_enemies()
            self.draw_attributes()
            self.draw_wave_timer()

    def click(self):
        if self.mouse_hover(self.bt_main["draw"]):
            self.game.back_to_lobby()
        if self.mouse_hover(self.bt_resume["draw"]):
            self.game.paused = False

    def update(self):
        self.life = self.converter(self.game.player.life, self.game.player.total_life)
        self.draw()
