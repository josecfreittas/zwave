import os
import random

import pygame

import zwave.main


class Player(pygame.sprite.Sprite):

    def __init__(self, main, model = "01"):
        pygame.sprite.Sprite.__init__(self)

        
        self.status = {}

        self.status["weapon"] = {}
        self.status["weapon"]["type"] = "gun"
        self.status["weapon"]["delay"] = 40
        self.status["weapon"]["timer"] = 0
        self.status["weapon"]["damage"] = [35, 65]
        self.status["weapon"]["bullets"] = []

        self.status["life"] = 100
        self.status["total_life"] = 100
        self.status["speed"] = 2.5
        self.status["score"] = 0

        ## init values ##
        self.main = main
        self.model = model
        self.size = 65 * main.scale
        self.angle = 0
        self.center = {}
        self.last = {}

        self.generate_position()

        path = os.path.join("assets", "img", "players", self.model, "sprite.png")
        self.image_base = zwave.helper.pygame_image(path, self.size)
        self.image = self.image_base

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.set_colliders()

    def generate_position(self):

        ## set position ##
        self.x = self.main.center["x"] - (self.size / 2)
        self.y = self.main.center["y"] - (self.size / 2)

        ## saves the actual position of the enemy, relative to game screen ##
        self.center["x"] = self.main.center["x"]
        self.center["y"] = self.main.center["y"]

    def set_colliders(self):

        ## default collider, with same size of sprite image ##
        self.collider1 = pygame.sprite.GroupSingle(self)

        ## touch/collider2 is a small collider for player, that simulates a better "touch" for the player, ##
        ## without the large original image edges ##
        self.touch = pygame.sprite.Sprite()
        self.touch.up = self
        self.touch.size = int(self.size / 2)

        self.touch.image = pygame.surface.Surface((self.touch.size, self.touch.size))
        self.touch.image.fill((255, 0, 0))
        self.touch.image.set_colorkey((255, 0, 0))

        self.touch.rect = self.touch.image.get_rect()
        self.touch.rect.x = self.center["x"] - (self.touch.size / 2)
        self.touch.rect.y = self.center["y"] - (self.touch.size / 2)

        self.collider2 = pygame.sprite.GroupSingle(self.touch)

    def update_colliders(self):

        ## update position of the second collider of enemy ##
        self.touch.rect.x = self.center["x"] - (self.touch.size / 2)
        self.touch.rect.y = self.center["y"] - (self.touch.size / 2)

    def collision(self, collider1, collider2):

        ## check collider 1 ##
        if collider1 == "walls":
            collider1 = self.main.map.collider["walls"]
        elif collider1 == "enemies":
            collider1 = self.main.enemies["colliders"]

        return pygame.sprite.groupcollide(collider2, collider1, False, False)

    def update_angle(self):

        ## update enemy angle based in player location ##
        self.angle = zwave.helper.angle_by_two_points(self.center, self.main.cursor)
        self.image = zwave.helper.pygame_rotate(self.image_base, self.angle)

    def update_position(self):

        ## check if had collision, if had, set last position of view ##
        if self.collision("walls", self.collider2) or self.collision("enemies", self.collider2):
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
        velocity = zwave.helper.velocity_by_keys(self.status["speed"] * self.main.scale, keys)

        ## movement according to keys down ##
        if keys[pygame.K_w]:
            self.main.y -= velocity
        if keys[pygame.K_s]:
            self.main.y += velocity
        if keys[pygame.K_a]:
            self.main.x -= velocity
        if keys[pygame.K_d]:
            self.main.x += velocity
  
    def shot(self):

        ## checks if timer for the shot is zero ##
        if self.status["weapon"]["timer"] == 0:

            ## check if the type of weapon is gun ##
            if self.status["weapon"]["type"] == "gun":

                angle = zwave.helper.angle_by_two_points(self.center, self.main.cursor)

                bullet = Bullet(angle, self.main)

                self.status["weapon"]["bullets"].append(bullet)

                ## gunshot sound ##
                self.main.sound["channels"]["attacks"].play(self.main.sound["gunshot"], 0)

                ## add timer for next gunshot ##
                self.status["weapon"]["timer"] = self.status["weapon"]["delay"]

    def update_bullets(self):

        ## random damage by weapon damage range ##
        damage = random.randint(self.status["weapon"]["damage"][0], self.status["weapon"]["damage"][1])

        ## get all bullets instances ##
        for bullet in self.status["weapon"]["bullets"]:
            collider = bullet.collider()

            ## check collision with walls ##
            if self.collision("walls", collider):
                bullet.kill()
            
            ## check collision with enemies ##
            elif self.collision("enemies", collider):
                enemy = self.collision("enemies", collider)[bullet][0].up
                enemy.status["life"] -= damage
                bullet.kill()

            ## if had no collision ##
            else:
                bullet.update()

    def draw(self):
        for bullet in self.status["weapon"]["bullets"]:
            group = bullet.collider()
            group.draw(self.main.screen)

        self.collider1.draw(self.main.screen)
        self.collider2.draw(self.main.screen)

    def wave_update(self):

        if self.status["weapon"]["damage"][0] < 100:
            self.status["weapon"]["damage"][0] += 10
            self.status["weapon"]["damage"][1] += 20

        if self.status["weapon"]["delay"] > 10:
            self.status["weapon"]["delay"] -= 2

        if self.status["total_life"] < 300:
            self.status["total_life"] += 10

        if self.status["life"] < self.status["total_life"]:
            if (self.status["total_life"] - self.status["life"]) >= 10:
                self.status["life"] += 10
            else:
                self.status["life"] += self.status["total_life"] - self.status["life"]

        if self.status["speed"] < 4: 
            self.status["speed"] += 0.1

    def update(self):

        if self.status["life"] <= 0:
            self.touch.kill()
            self.kill()

        ## update gunshot timer ##
        if self.status["weapon"]["timer"] > 0:
            self.status["weapon"]["timer"] -= 1

        self.update_bullets()
        self.update_angle()
        self.update_position()
        self.update_colliders()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, main):
        pygame.sprite.Sprite.__init__(self)

        ## init values ##
        self.angle = angle - 180
        self.size = 10 * main.scale

        path = os.path.join("assets", "img", "bullet.png")
        self.image = zwave.helper.pygame_image(path, self.size)
        self.image = zwave.helper.pygame_rotate(self.image, angle)

        self.rect = self.image.get_rect()
        self.rect.x = main.player.center["x"] - (self.size / 2)
        self.rect.y = main.player.center["y"] - (self.size / 2)

        self.velocity = zwave.helper.velocity_by_angle(35, self.angle)
        self.sgroup = pygame.sprite.GroupSingle(self)

    def update(self):
        self.rect.x -= self.velocity["x"]
        self.rect.y -= self.velocity["y"]

    def collider(self):
        return self.sgroup
