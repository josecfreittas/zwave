import os

import pygame

import zwave.helper


class Map:
    def __init__(self, main, width = 2048, height = 2048):

        ## init values ##
        self.main = main
        self.width = width * self.main.scale
        self.height = height * self.main.scale
        self.x = 0
        self.y = 0
        self.center = {}
        self.center["x"] = self.width / 2
        self.center["y"] = self.height / 2

        ## map suface ##
        self.surface = {}
        self.surface["ground"] = None
        self.surface["walls"] = None

        ## map colliders ##
        self.collider = {}
        self.collider["sprites"] = {}
        self.collider["raw"] = [
            "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "W", "W", "W", "W", "W", "W", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "M", "W", "M", "M", "M", "W", "W", "W", "W", "G", "G", "G", "G", "G", "W", "W", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "M", "M", "M", "M", "M", "M", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "M", "M", "M", "M", "M", "M", "M", "M", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "M", "M", "M", "M", "M", "M", "M", "M", "W", "W", "W", "G", "G", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "M", "M", "M", "M", "M", "M", "M", "W", "W", "W", "W", "G", "G", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "M", "M", "M", "M", "M", "M", "M", "M", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "M", "M", "M", "M", "M", "M", "M", "M", "M", "W", "W", "G", "G", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "M", "M", "M", "M", "M", "M", "M", "M", "W", "W", "G", "G", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "W", "W", "W", "W", "M", "M", "M", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "M", "M", "M", "W", "W", "W", "W", "S", "S", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "G", "G", "W", "W", "M", "M", "M", "M", "M", "M", "M", "M", "S", "S", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "G", "G", "W", "W", "M", "M", "M", "M", "M", "M", "M", "M", "M", "S", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "M", "M", "M", "M", "M", "M", "M", "M", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "G", "G", "W", "W", "W", "W", "M", "M", "M", "M", "M", "M", "M", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "G", "G", "W", "W", "W", "M", "M", "M", "M", "M", "M", "M", "M", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "M", "M", "M", "M", "M", "M", "M", "M", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "M", "M", "M", "M", "M", "M", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "G", "W", "W", "G", "G", "G", "G", "G", "W", "W", "W", "W", "M", "M", "M", "W", "M", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "W", "W", "W", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"
        ]

        self.set_surface()
        self.set_colliders()

    def set_surface(self):

        ## load and scale map ground ##
        ground = os.path.join("assets", "img", "map", "ground.png")
        self.surface["ground"] = zwave.helper.pygame_image(ground, self.width, self.height, False)

        ## load and scale map walls ##
        walls = os.path.join("assets", "img", "map", "walls.png")
        self.surface["walls"] = zwave.helper.pygame_image(walls, self.width, self.height)

    def set_colliders(self):
        
        #self.collider["grass"] = pygame.sprite.Group()
        #self.collider["marble"] = pygame.sprite.Group()
        #self.collider["sand"] = pygame.sprite.Group()
        self.collider["walls"] = pygame.sprite.Group()

        ## loop for all the tiles ##
        for key, tile in enumerate(self.collider["raw"]):

            ## if current tile is a wall, add in wall group ##
            if tile == 'W':

                ## make a generic sprite with size of map tiles  ##
                sprite = Tile(self.main, key, 32)
                self.collider["sprites"][key] = sprite
                self.collider["walls"].add(self.collider["sprites"][key])

            '''
            FOR FUTURE USE:

            ## if current tile is grass, add in grass group ##
            elif tile == 'G':
                self.collider["grass"].add(self.collider["sprites"][key])

            ## if current tile is stone/marble, add in marble group ##
            elif tile == 'M':
                self.collider["marble"].add(self.collider["sprites"][key])

            ## if current tile is sand, add in sand group ##
            elif tile == 'S':
                self.collider["sand"].add(self.collider["sprites"][key])
            '''

    def update_colliders(self):

        ## loop for update all sprites ##
        for key in self.collider["sprites"].keys():
            self.collider["sprites"][key].update()

    def update_position(self):
        self.x = self.main.x * -1
        self.y = self.main.y * -1

    def update(self):
        self.update_position()
        self.update_colliders()
        self.collider["walls"].draw(self.main.screen)

class Tile(pygame.sprite.Sprite):
    def __init__(self, main, position, columns):
        pygame.sprite.Sprite.__init__(self)

        self.main =  main
        self.size =  64 * self.main.scale

        self.image = pygame.surface.Surface((self.size, self.size))
        self.image.fill((255, 0, 0))
        self.image.set_colorkey((255, 0, 0))

        self.rect = self.image.get_rect()
        self.generate_position(position, columns)

    def generate_position(self, position, columns):

        column = position % columns
        row = int(position / float(columns))

        ## set new position ##
        self.x = column * self.size
        self.y = row * self.size

    def update_position(self):
        self.rect.x = self.x - self.main.x
        self.rect.y = self.y - self.main.y

    def update(self):
        self.update_position()
