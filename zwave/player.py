import os

import pygame

import zwave.main


class Player:

    ## constructor ##
    def __init__(self, main = None, model = '01', width = 65, height = 65):    
        
        ## main game object ##
        self.main = main
        
        ## visual model of player ##
        self.model = model
        
        ## player surface ##
        self.surface = {}
        self.surface["original"] = None
        self.surface["sprite"] = None

        ## player collider ##
        self.collider = {}
        self.collider["sprite"] = None
        self.collider["touch"] = pygame.sprite.Group()

        ## player view ##
        self.angle = 0
        self.width = width * self.main.scale
        self.height = height * self.main.scale
        self.x = (self.main.width / 2) - (self.width / 2)
        self.y = (self.main.height / 2) - (self.height / 2)
        self.center = self.main.center

        ## player status ##
        self.status = {}
        self.status["attack"] = {}
        self.status["attack"]["type"] = "gun"
        self.status["attack"]["delay"] = 0
        self.status["attack"]["bullets"] = []

        self.set_surface()
        self.set_collider()

    ## methods to allow external access to object values ##
    def __getitem__(self, name):
        if name == "center":
            return self.center

    ## method to set player surface ##
    def set_surface(self):

        ## load and scale player model image ##
        image = os.path.join("assets", "img", "players", "%s.png" % self.model)
        self.surface["original"] = zwave.helper.pygame_image(image, self.width, self.height)

    ## method to draw player collider ##
    def set_collider(self):

        ## calculate size of collider based on player size ##
        size = int(((self.width / 1.7) + (self.height / 1.7)) / 2)

        x = (self.main.width / 2) - (size / 2)
        y = (self.main.height / 2) - (size / 2)

        ## make a generic sprite  ##
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.Surface((size, size))

        ## fill the sprite with red and after that make colorkey with red, making the sprite transparent ##
        sprite.image.fill((255, 0, 0))
        sprite.image.set_colorkey((255, 0, 0))

        ## make sprite rect ##
        sprite.rect = sprite.image.get_rect()

        ## set new position ##
        sprite.rect.x = x
        sprite.rect.y = y

        ## add new collider to colliders group ##
        self.collider["sprite"] = sprite
        self.collider["touch"].add(self.collider["sprite"])

    ## method to check if exist collision ##
    def collision(self, collider1, collider2 = "touch"):
        if collider1 == "walls":
            collider1 = self.main.map.collider["walls"]
        elif collider1 == "grass":
            collider1 = self.main.map.collider["grass"]
        elif collider1 == "marble":
            collider1 = self.main.map.collider["marble"]
        elif collider1 == "sand":
            collider1 = self.main.map.collider["sand"]
        elif collider1 == "enemies":
            collider1 = self.main.enemies["colliders"]
        elif collider1 == "enemies2":
            collider1 = self.main.enemies["sprites"]

        if collider2 == "touch":
            collider2 = self.collider["touch"]

        return pygame.sprite.groupcollide(collider2, collider1, False, False)

    def rotate(self):
        angle = zwave.helper.angle_by_two_points(self.center, self.main.cursor)
        self.surface["sprite"] = zwave.helper.pygame_rotate(self.surface["original"], angle)

    ## method to player/screen movimentation ##
    def move(self):

        ## check if had collision, if had, set last position of view ##
        if self.collision("walls") or self.collision("enemies"):
            self.main.x = self.main.last["x"]
            self.main.y = self.main.last["y"]

        ## save current positon of view for future use ##
        self.main.last["x"] = self.main.x
        self.main.last["y"] = self.main.y

        ## make 'keys' variable with pressed keys
        keys = pygame.key.get_pressed()

        ## footsteps sound if the player is walking ##
        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
            if not self.main.sound["channels"]["steps"].get_busy():
                self.main.sound["channels"]["steps"].play(self.main.sound["steps"], -1)
        else:
            self.main.sound["channels"]["steps"].stop()
        
        ## picks speed for each axis ##
        velocity = zwave.helper.velocity_by_keys(2 * self.main.scale, keys)

        ## movement according to keys down ##
        if keys[pygame.K_w]:
            self.main.y -= velocity
        if keys[pygame.K_s]:
            self.main.y += velocity
        if keys[pygame.K_a]:
            self.main.x -= velocity
        if keys[pygame.K_d]:
            self.main.x += velocity

    ## method to player shots ##    
    def shot(self):

        ## checks if delay for the shot is zero ##
        if self.status["attack"]["delay"] == 0:

            ## check if the type of weapon is gun ##
            if self.status["attack"]["type"] == "gun":

                angle = zwave.helper.angle_by_two_points(self.center, self.main.cursor)

                bullet = Bullet(angle, self.main)

                self.status["attack"]["bullets"].append(bullet)

                ## gunshot sound ##
                self.main.sound["channels"]["attacks"].play(self.main.sound["gunshot"], 0)

                ## add delay for next gunshot ##
                self.status["attack"]["delay"] = 50

    def update_bullets(self):
        for sprite in self.status["attack"]["bullets"]:

            group = sprite.collider()

            ## check collisions ##
            if self.collision("walls", group):
                self.status["attack"]["bullets"].remove(sprite)
            elif self.collision("enemies", group):
                co = self.collision("enemies", group)
                print(co[sprite][0].up)
                self.status["attack"]["bullets"].remove(sprite)
            else:

                ## move bullet and draw on screen ##
                sprite.update()
                group.draw(self.main.screen)

    ## method to update player ##
    def update(self):

        ## update gunshot timer ##
        if self.status["attack"]["delay"] > 0:
            self.status["attack"]["delay"] -= 1

        self.rotate()
        self.move()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, main):
        super().__init__()

        self.angle = angle - 180

        self.size = 10 * main.scale

        path = os.path.join("assets", "img", "bullet.png")
        self.image = zwave.helper.pygame_image(path, self.size)
        self.image = zwave.helper.pygame_rotate(self.image, angle)

        self.rect = self.image.get_rect()
        self.rect.x = main.player.center["x"] - (self.size / 2)
        self.rect.y = main.player.center["y"] - (self.size / 2)

        self.velocity = zwave.helper.velocity_by_angle(30, self.angle)
        self.sgroup = pygame.sprite.GroupSingle(self)

    def update(self):
        self.rect.x -= self.velocity["x"]
        self.rect.y -= self.velocity["y"]

    def collider(self):
        return self.sgroup
