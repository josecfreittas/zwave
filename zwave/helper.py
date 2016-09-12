import pygame

def get_speed(speed, vars, Mode = 1):

    if Mode == 1:
        ## speed to axes in diagonal movement ##
        if (vars[pygame.K_a] or vars[pygame.K_d]) and (vars[pygame.K_w] or vars[pygame.K_s]):
            velocity = speed * 0.7

        ## speed to axes in horizontal and vertical movements ##
        else:
            velocity = speed
    elif Mode == 2:
        velocity = {}
        velocity["x"] = 0
        velocity["y"] = 0
        if vars["x"] > vars["y"]:
            diference = float(vars["x"]) / float(vars["y"])
            velocity["x"] = 2 - (2 / diference)
            velocity["y"] = 2 / diference
        elif vars["x"] < vars["y"]:
            diference = float(vars["y"]) / float(vars["x"])
            velocity["x"] = 2 / diference
            velocity["y"] = 2 - (2 / diference)

    return velocity
