#--*-- conding: utf-8 --*--
import json
import os

import pygame

import zwave
import zwave.helper

## TODO: Cleanup lobby, improve recursion ##
class Lobby:

    def __init__(self, settings, text):

        pygame.font.init()

        self.font = {}
        path = os.path.join("assets", "fonts", "Renogare.ttf")
        self.font["default"] = pygame.font.Font(path, 14)
        self.font["big"] = pygame.font.Font(path, 30)

        ## init values ##
        self.running = True
        self.settings = settings
        self.text = text
        self.screen = pygame.display.set_mode((1024, 512))

        self.cursor = None
        self.bt_exit = {}
        self.bt_settings = {}
        self.bt_start = {}

        self.buttons()
        self.set_cursor()
        self.loop()

    def set_cursor(self):
        pygame.mouse.set_visible(False)
        size = 35
        image = os.path.join("assets", "img", "cursor.png")
        image = zwave.helper.pygame_image(image, size)
        sprite = zwave.helper.pygame_sprite_by_image(image)
        self.cursor = pygame.sprite.GroupSingle(sprite)

    def buttons(self):
        ## start game button ##
        x = 1024 / 2
        y = (512 / 2) - 65
        self.bt_start["normal"] = zwave.helper.pygame_button(self.text["start"].upper(), self.font["big"], x, y, (0, 0, 0), True)
        self.bt_start["hover"] = zwave.helper.pygame_button(self.text["start"].upper(), self.font["big"], x, y, (0, 140, 90), True)
        self.bt_start["draw"] =  self.bt_start["normal"]

        ## exit button #
        x = 1024 / 2
        y = (512 / 2)
        self.bt_settings["normal"] = zwave.helper.pygame_button(self.text["settings"].upper(), self.font["big"], x, y, (0, 0, 0), True)
        self.bt_settings["hover"] = zwave.helper.pygame_button(self.text["settings"].upper(), self.font["big"], x, y, (0, 140, 90), True)
        self.bt_settings["draw"] =  self.bt_settings["normal"]

        ## exit button #
        x = 1024 / 2
        y = (512 / 2) + 65
        self.bt_exit["normal"] = zwave.helper.pygame_button(self.text["exit"].upper(), self.font["big"], x, y, (0, 0, 0), True)
        self.bt_exit["hover"] = zwave.helper.pygame_button(self.text["exit"].upper(), self.font["big"], x, y, (0, 140, 90), True)
        self.bt_exit["draw"] =  self.bt_exit["normal"]

    def draw(self):

        self.bt_start["draw"].draw(self.screen)
        self.bt_settings["draw"].draw(self.screen)
        self.bt_exit["draw"].draw(self.screen)

    def mouse_hover(self, button):
        if pygame.sprite.groupcollide(self.cursor, button, False, False):
            return True
        else:
            return False

    def start_game(self):
        self.running = False
        settings = self.settings
        zwave.init(texts, settings["scale"], settings["width"], settings["height"], settings["fullscreen"])

    def loop(self):

        ## set pygame clock ##
        clock = pygame.time.Clock()

        while self.running:

            pygame.display.set_caption("FPS: %.0f" % clock.get_fps())

            ## fill screen ##
            self.screen.fill((100, 125, 130))
            
            ## cursor x position ##
            self.cursor.sprites()[0].rect.x = pygame.mouse.get_pos()[0]
            self.cursor.sprites()[0].rect.y = pygame.mouse.get_pos()[1]

            ## draw menu ##
            self.draw()

            ## draw cursor ##
            self.cursor.draw(self.screen)

            if self.mouse_hover(self.bt_exit["draw"]):
                self.bt_exit["draw"] = self.bt_exit["hover"]
            else:
                self.bt_exit["draw"] = self.bt_exit["normal"]

            if self.mouse_hover(self.bt_settings["draw"]):
                self.bt_settings["draw"] = self.bt_settings["hover"]
            else:
                self.bt_settings["draw"] = self.bt_settings["normal"]

            if self.mouse_hover(self.bt_start["draw"]):
                self.bt_start["draw"] = self.bt_start["hover"]
            else:
                self.bt_start["draw"] = self.bt_start["normal"]

            ## game events ##
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.mouse_hover(self.bt_exit["draw"]):
                        self.running = False
                    if self.mouse_hover(self.bt_settings["draw"]):
                        pass
                    if self.mouse_hover(self.bt_start["draw"]):
                        self.start_game()

                ## quit ##
                if event.type == pygame.QUIT:
                    self.running = False

            ## pygame clock tick ##
            clock.tick(60)

            ## update pygame screen ##
            pygame.display.update()

settings = json.loads(open("data/settings.json").read())
texts = json.loads(open("data/languages/%s.json" % settings["language"]).read())

lobby = Lobby(settings, texts)
