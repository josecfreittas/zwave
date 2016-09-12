import math
import pygame

def get_speed(speed, var, angle = False):

    if not angle:
        ## speed to axes in diagonal movement ##
        if (var[pygame.K_a] or var[pygame.K_d]) and (var[pygame.K_w] or var[pygame.K_s]):
            velocity = speed * 0.7

        ## speed to axes in horizontal and vertical movements ##
        else:
            velocity = speed
    else:
        velocity = {}

        ## algorithm to set velocity for 'x' and 'y' based on the angle of sprite ##
        velocity["x"] = math.cos(math.radians(var))
        velocity["y"] = (math.sin(math.radians(var)) * -1)

    return velocity
