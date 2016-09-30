import os
import random

import pygame
import zwave.helper


class Player(pygame.sprite.Sprite):

    def __init__(self, game, model = "01"):

        super(Player, self).__init__()

        self.weapon = {}
        self.weapon["type"] = "gun"
        self.weapon["delay"] = 20
        self.weapon["timer"] = 0
        self.weapon["damage"] = [35, 65]
        self.weapon["bullets"] = []

        self.life = 100
        self.total_life = 100
        self.speed = 2
        self.score = 0
        self.kills = {}
        self.kills["zombies"] = 0
        self.kills["headcrabs"] = 0

        ## init values ##
        self.game = game
        self.model = model
        self.size = 65 * game.scale
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
        self.x = self.game.center["x"] - (self.size / 2)
        self.y = self.game.center["y"] - (self.size / 2)

        ## saves the actual position of the enemy, relative to game screen ##
        self.center["x"] = self.game.center["x"]
        self.center["y"] = self.game.center["y"]

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
            collider1 = self.game.map.collider["walls"]
        elif collider1 == "enemies":
            collider1 = self.game.enemies["colliders"]

        return pygame.sprite.groupcollide(collider2, collider1, False, False)

    def update_angle(self):

        ## update enemy angle based in player location ##
        self.angle = zwave.helper.angle_by_two_points(self.center, self.game.mouse)
        self.image = zwave.helper.pygame_rotate(self.image_base, self.angle)

    def update_position(self):

        ## check if had collision, if had, set last position of view ##
        if self.collision("walls", self.collider2) or self.collision("enemies", self.collider2):
            self.game.x = self.game.last["x"]
            self.game.y = self.game.last["y"]

        ## save current positon of view for future use ##
        self.game.last["x"] = self.game.x
        self.game.last["y"] = self.game.y

        ## make 'keys' variable with pressed keys
        keys = pygame.key.get_pressed()

        ## footsteps sound if the player is walking ##
        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
            if not self.game.sound["channels"]["steps"].get_busy():
                self.game.sound["channels"]["steps"].play(self.game.sound["steps"], -1)
        else:
            self.game.sound["channels"]["steps"].stop()
        
        ## picks speed for each axis ##
        velocity = zwave.helper.velocity_by_keys(self.speed * self.game.scale, keys)

        ## movement according to keys down ##
        if keys[pygame.K_w]:
            self.game.y -= velocity
        if keys[pygame.K_s]:
            self.game.y += velocity
        if keys[pygame.K_a]:
            self.game.x -= velocity
        if keys[pygame.K_d]:
            self.game.x += velocity
  
    def shot(self):

        ## checks if timer for the shot is zero ##
        if self.weapon["timer"] == 0:

            ## check if the type of weapon is gun ##
            if self.weapon["type"] == "gun":

                angle = zwave.helper.angle_by_two_points(self.center, self.game.mouse)

                bullet = Bullet(angle, self.game)

                self.weapon["bullets"].append(bullet)

                ## gunshot sound ##
                self.game.sound["channels"]["attacks"].play(self.game.sound["gunshot"], 0)

                ## add timer for next gunshot ##
                self.weapon["timer"] = self.weapon["delay"]

    def update_bullets(self):

        ## random damage by weapon damage range ##
        damage = random.randint(self.weapon["damage"][0], self.weapon["damage"][1])

        ## get all bullets instances ##
        for bullet in self.weapon["bullets"]:
            collider = bullet.collider()

            ## check collision with walls ##
            if self.collision("walls", collider):
                bullet.kill()
            
            ## check collision with enemies ##
            elif self.collision("enemies", collider):
                enemy = self.collision("enemies", collider)[bullet][0].up
                enemy.life -= damage
                bullet.kill()

            ## if had no collision ##
            else:
                bullet.update()

    def draw(self):
        for bullet in self.weapon["bullets"]:
            group = bullet.collider()
            group.draw(self.game.screen)

        self.collider1.draw(self.game.screen)
        self.collider2.draw(self.game.screen)

    def wave_update(self):

        if self.weapon["damage"][0] < 100:
            self.weapon["damage"][0] += 10
            self.weapon["damage"][1] += 20

        if self.weapon["delay"] > 20:
            self.weapon["delay"] -= 3

        if self.total_life < 300:
            self.total_life += 10

        if self.life < self.total_life:
            if (self.total_life - self.life) >= 25:
                self.life += 25
            else:
                self.life += self.total_life - self.life

        if self.speed < 4: 
            self.speed += 0.1

    def update(self):

        if self.life <= 0:
            self.touch.kill()
            self.kill()

        ## update gunshot timer ##
        if self.weapon["timer"] > 0:
            self.weapon["timer"] -= 1

        self.update_bullets()
        self.update_angle()
        self.update_position()
        self.update_colliders()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, angle, game):
        pygame.sprite.Sprite.__init__(self)

        ## init values ##
        self.angle = angle - 180
        self.size = 10 * game.scale

        path = os.path.join("assets", "img", "bullet.png")
        self.image = zwave.helper.pygame_image(path, self.size)
        self.image = zwave.helper.pygame_rotate(self.image, angle)

        self.rect = self.image.get_rect()
        self.rect.x = game.player.center["x"] - (self.size / 2)
        self.rect.y = game.player.center["y"] - (self.size / 2)

        self.velocity = zwave.helper.velocity_by_angle(35 * game.scale, self.angle)
        self.sgroup = pygame.sprite.GroupSingle(self)

    def update(self):
        self.rect.x -= self.velocity["x"]
        self.rect.y -= self.velocity["y"]

    def collider(self):
        return self.sgroup
