import math
import pygame

def velocity_by_keys(speed, keys):
    ## speed to axes in diagonal movement ##
    if (keys[pygame.K_a] or keys[pygame.K_d]) and (keys[pygame.K_w] or keys[pygame.K_s]):
        return (speed * 0.7)

    ## speed to axes in horizontal and vertical movements ##
    else:
        return speed

def velocity_by_angle(speed, angle):
    velocity = {}

    ## algorithm to set velocity for 'x' and 'y' based on the angle of sprite ##
    velocity["x"] = math.cos(math.radians(angle))
    velocity["y"] = (math.sin(math.radians(angle)) * -1)

    return velocity

def angle_by_two_points(point1, point2):

        dx =  point2["x"] - point1["x"]
        dy =  point2["y"] - point1["y"]

        rads = math.atan2(-dy,dx)
        rads %= 2 * math.pi

        return math.degrees(rads)

def pygame_image(image, width, height = False):
    if not height:
        height = width
    image = pygame.image.load(image).convert_alpha()
    image = pygame.transform.scale(image, (width, height))
    return image

def pygame_rotate(sprite, angle):

    area = sprite.get_rect()
    new = pygame.transform.rotozoom(sprite, angle, 1)
    area.center = new.get_rect().center
    return new.subsurface(area).copy()
