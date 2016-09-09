import pygame

from zwave.map import *
from zwave.signal import *
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

        ## mouse ##
        self.mouse = {}
        self.mouse["x"] = 0
        self.mouse["y"] = 0

        ## framerate ##
        self.tick = 60
        self.frame = 0

        ## game screen ##
        self.screen = pygame.display.set_mode((self.view["width"], self.view["height"]))

        ## game map ##
        self.map = Map(self)

        ## game view x and y ##
        self.view["x"] = (self.map.view["width"] / 2) - (width / 2)
        self.view["y"] = (self.map.view["height"] / 2) - (height / 2)

        ## make base signals ##
        self.signal = {}
        self.signal["south"] = Signal(self, "south")
        self.signal["north"] = Signal(self, "north")

        ## player ##
        self.player = Player(self)

        ## make enemy ##
        self.enemies = pygame.sprite.Group()
        self.enemy1 = Enemy(self)
        self.enemies.add(self.enemy1.collider["sprite1"])

        ## init game loop ##
        self.loop()

    ## method to allow external access to object values ##
    def __getattr__(self, name):
        if name == "view":
            return self.view
        elif name == "screen":
            return self.screen
        elif name == "map":
            return self.map
        elif name == "player":
            return self.player

    ## method to player/screen movimentation ##
    def move(self):

        ## check if had collision, if had, set last position of view ##
        if self.player.check_collision("wall") or self.player.check_collision("enemies"):
            self.view["x"] = self.view["last_x"]
            self.view["y"] = self.view["last_y"]

        ## save current positon of view for future use ##
        self.view["last_x"] = self.view["x"]
        self.view["last_y"] = self.view["y"]

        ## make 'keys' variable with pressed keys
        keys = pygame.key.get_pressed()

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

            ## update game map ##
            self.map.update()

            ## update base signals ##
            self.signal["north"].update()
            self.signal["south"].update()

            ## enemy update ##
            self.enemy1.update()

            ## update player ##
            self.player.update()

            ## call method responsible for move view to new destiny, if one exists ##
            self.move()

            ## update pygame screen ##
            pygame.display.update()

            ## mouse x position ##
            self.mouse["x"] = pygame.mouse.get_pos()[0]

            ## mouse y position ##
            self.mouse["y"] = pygame.mouse.get_pos()[1]

            ## events hunter ##
            for event in pygame.event.get():

                ## qui event ##
                if event.type == pygame.QUIT:
                    running = False

            ## increment or reset atual frame ##
            self.frame = (self.frame + 1) if self.frame < self.tick else 0

            ## pygame clock tick ##
            clock.tick(self.tick)
