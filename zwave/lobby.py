# -*- conding: utf-8 -*-

import json
import os
import sys

import pygame

import zwave.game
import zwave.helper

class Lobby:

    def __init__(self):

        ## load data ##
        self.load_settings()
        self.load_language()

        ## fonts ##
        pygame.font.init()
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "Renogare.ttf"), 30)

        ## init values ##
        self.running = True
        self.screen = pygame.display.set_mode((1024, 512))
        self.background = zwave.helper.pygame_image(os.path.join("assets", "img", "background.png"), 1024, 512)
        self.page = "main"

        self.cursor = None

        self.bt_exit = {}
        self.bt_settings = {}
        self.bt_start = {}

        self.bt_ptbr = {}
        self.bt_enus = {}
        self.bt_1024x512 = {}
        self.bt_1366x768 = {}
        self.bt_fullscreen = {}
        self.bt_back = {}

        self.set_sounds()
        self.buttons()
        self.set_cursor()
        self.loop()

    def load_settings(self):
        self.settings = json.loads(open("data/settings.json").read())

    def load_language(self):
        if sys.version_info.major > 2:
            self.text = json.loads(open("data/languages/%s.json" % self.settings["language"], encoding="utf-8").read())
        else:
            self.text = json.loads(open("data/languages/%s.json" % self.settings["language"]).read())

    def save_settings(self):
        with open("data/settings.json", "w") as outfile:
            json.dump(self.settings, outfile, indent=4)

    def reload(self):
        self.save_settings()
        self.load_language()
        self.buttons()

    def set_sounds(self):

        self.sound = {}

        ## init pygame mixer and configure ##
        pygame.mixer.init(22050, -16, 1, 512)

        ## load, set volume and init music background ##
        pygame.mixer.music.load(os.path.join("assets", "sounds", "music", "1.ogg"))
        pygame.mixer.music.set_volume(self.settings["volume"]["music"] * self.settings["volume"]["geral"])
        pygame.mixer.music.play(-1)

        self.sound["channel"] = pygame.mixer.Channel(1)

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
        self.bt_start["normal"] = zwave.helper.pygame_button(self.text["start"].upper(), self.font, x, y, (50, 50, 50), "center")
        self.bt_start["hover"] = zwave.helper.pygame_button(self.text["start"].upper(), self.font, x, y, (0, 140, 90), "center")
        self.bt_start["draw"] =  self.bt_start["normal"]

        ## settings button #
        x = 1024 / 2
        y = (512 / 2)
        self.bt_settings["normal"] = zwave.helper.pygame_button(self.text["settings"].upper(), self.font, x, y, (50, 50, 50), "center")
        self.bt_settings["hover"] = zwave.helper.pygame_button(self.text["settings"].upper(), self.font, x, y, (0, 140, 90), "center")
        self.bt_settings["draw"] =  self.bt_settings["normal"]

        ## exit button #
        x = 1024 / 2
        y = (512 / 2) + 65
        self.bt_exit["normal"] = zwave.helper.pygame_button(self.text["exit"].upper(), self.font, x, y, (50, 50, 50), "center")
        self.bt_exit["hover"] = zwave.helper.pygame_button(self.text["exit"].upper(), self.font, x, y, (0, 140, 90), "center")
        self.bt_exit["draw"] =  self.bt_exit["normal"]

        ## pt-br button #
        x = (1024 / 2) - 5
        y = (512 / 2) - 65
        self.bt_ptbr["normal"] = zwave.helper.pygame_button("PT-BR", self.font, x, y, (50, 50, 50), "left")
        self.bt_ptbr["hover"] = zwave.helper.pygame_button("PT-BR", self.font, x, y, (0, 140, 90), "left")
        self.bt_ptbr["selected"] = zwave.helper.pygame_button("PT-BR", self.font, x, y, (0, 0, 0), "left")
        self.bt_ptbr["draw"] =  self.bt_ptbr["normal"]

        ## en-us button #
        x = (1024 / 2) + 5
        y = (512 / 2) - 65
        self.bt_enus["normal"] = zwave.helper.pygame_button("EN-US", self.font, x, y, (50, 50, 50), "right")
        self.bt_enus["hover"] = zwave.helper.pygame_button("EN-US", self.font, x, y, (0, 140, 90), "right")
        self.bt_enus["selected"] = zwave.helper.pygame_button("EN-US", self.font, x, y, (0, 0, 0), "right")
        self.bt_enus["draw"] =  self.bt_enus["normal"]

        ## 1024x512 button #
        x = (1024 / 2) - 5
        y = 512 / 2
        self.bt_1024x512["normal"] = zwave.helper.pygame_button("1024x512", self.font, x, y, (50, 50, 50), "left")
        self.bt_1024x512["hover"] = zwave.helper.pygame_button("1024x512", self.font, x, y, (0, 140, 90), "left")
        self.bt_1024x512["selected"] = zwave.helper.pygame_button("1024x512", self.font, x, y, (0, 0, 0), "left")
        self.bt_1024x512["draw"] =  self.bt_1024x512["normal"]

        ## 1366x768 button #
        x = (1024 / 2) + 5
        y = 512 / 2
        self.bt_1366x768["normal"] = zwave.helper.pygame_button("1366x768", self.font, x, y, (50, 50, 50), "right")
        self.bt_1366x768["hover"] = zwave.helper.pygame_button("1366x768", self.font, x, y, (0, 140, 90), "right")
        self.bt_1366x768["selected"] = zwave.helper.pygame_button("1366x768", self.font, x, y, (0, 0, 0), "right")
        self.bt_1366x768["draw"] =  self.bt_1366x768["normal"]

        ## fullscreen button #
        x = 1024 / 2
        y = (512 / 2) + 65
        self.bt_fullscreen["normal"] = zwave.helper.pygame_button(self.text["fullscreen"].upper(), self.font, x, y, (50, 50, 50), "center")
        self.bt_fullscreen["hover"] = zwave.helper.pygame_button(self.text["fullscreen"].upper(), self.font, x, y, (0, 140, 90), "center")
        self.bt_fullscreen["selected"] = zwave.helper.pygame_button(self.text["fullscreen"].upper(), self.font, x, y, (0, 0, 0), "center")
        self.bt_fullscreen["draw"] =  self.bt_fullscreen["normal"]

        ## back button #
        x = 1024 / 2
        y = (512 / 2) + 130
        self.bt_back["normal"] = zwave.helper.pygame_button(self.text["back"].upper(), self.font, x, y, (50, 50, 50), "center")
        self.bt_back["hover"] = zwave.helper.pygame_button(self.text["back"].upper(), self.font, x, y, (0, 140, 90), "center")
        self.bt_back["draw"] =  self.bt_back["normal"]

    def draw_main(self):

        ## start game button ##
        self.update_button(self.bt_start)

        ## game settings button ##
        self.update_button(self.bt_settings)

        ## game exit button ##
        self.update_button(self.bt_exit)

    def draw_settings(self):

        ## language pt-br button ##
        selected = self.settings["language"] == "pt-br"
        self.update_button(self.bt_ptbr, selected)

        ## language en-us button ##
        selected = self.settings["language"] == "en-us"
        self.update_button(self.bt_enus, selected)

        ## resolution 1024x512 button ##
        selected = (self.settings["width"] == 1024) and (self.settings["height"] == 512)
        self.update_button(self.bt_1024x512, selected)

        ## resolution 1366x768 button ##
        selected = (self.settings["width"] == 1366) and (self.settings["height"] == 768)
        self.update_button(self.bt_1366x768, selected)

        ## fullscreen on or off button ##
        selected = self.settings["fullscreen"]
        self.update_button(self.bt_fullscreen, selected)

        ## back to loby main page button ##
        self.update_button(self.bt_back)

    def draw(self):

        ## draw current page ##
        if self.page == "main":
            self.draw_main()
        elif self.page == "settings":
            self.draw_settings()

    def mouse_hover(self, button):

        ## checks if has a collision with cursor and button ##
        if pygame.sprite.groupcollide(self.cursor, button, False, False):
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
            button["selected"].draw(self.screen)
        else:
            button["draw"].draw(self.screen)

    def start_game(self):

        ## end lobby loop, sound and pygame display ##
        self.running = False
        pygame.mixer.stop()
        pygame.display.quit()

        ## start the game ##
        zwave.game.Game(self.text, self.settings)

    def loop(self):

        ## set pygame clock ##
        clock = pygame.time.Clock()

        while self.running:

            pygame.display.set_caption("FPS: %.0f" % clock.get_fps())

            ## fill screen ##
            self.screen.blit(self.background, (0, 0))
            
            ## cursor x position ##
            self.cursor.sprites()[0].rect.x = pygame.mouse.get_pos()[0]
            self.cursor.sprites()[0].rect.y = pygame.mouse.get_pos()[1]

            ## draw current page ##
            self.draw()

            ## draw cursor ##
            self.cursor.draw(self.screen)

            ## game events ##
            for event in pygame.event.get():

                ## check button clicks ##
                if event.type == pygame.MOUSEBUTTONUP:

                    ## lobby main page ##
                    if self.page == "main":

                        ## game start ##
                        if self.mouse_hover(self.bt_start["draw"]):
                            self.start_game()

                        ## game settings ##
                        if self.mouse_hover(self.bt_settings["draw"]):
                            self.page = "settings"

                        ## game quit ##
                        if self.mouse_hover(self.bt_exit["draw"]):
                            self.running = False

                    ## lobby settings page ##
                    elif self.page == "settings":

                        ## language pt-br ##
                        if self.mouse_hover(self.bt_ptbr["draw"]):
                            self.settings["language"] = "pt-br"
                            self.reload()

                        ## language en-us ##
                        if self.mouse_hover(self.bt_enus["draw"]):
                            self.settings["language"] = "en-us"
                            self.reload()

                        ## resolution 1024x512 ##
                        if self.mouse_hover(self.bt_1024x512["draw"]):
                            self.settings["width"] = 1024
                            self.settings["height"] = 512
                            self.settings["scale"] = 1
                            self.reload()

                        ## resolution 1366x768 ##
                        if self.mouse_hover(self.bt_1366x768["draw"]):
                            self.settings["width"] = 1366
                            self.settings["height"] = 768
                            self.settings["scale"] = 2
                            self.reload()

                        ## fullscreen ##
                        if self.mouse_hover(self.bt_fullscreen["draw"]):
                            if self.settings["fullscreen"]:
                                self.settings["fullscreen"] = False
                            else:
                                self.settings["fullscreen"] = True
                            self.reload()

                        ## back to lobby main page ##
                        if self.mouse_hover(self.bt_back["draw"]):
                            self.page = "main"

                ## quit ##
                if event.type == pygame.QUIT:
                    self.running = False

            ## pygame clock tick ##
            clock.tick(60)

            ## update pygame screen ##
            pygame.display.update()
