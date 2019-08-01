import pygame
from pygame import *

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target, window_width, window_height):
        self.state = self.camera_func(self.state, target.rect, window_width, window_height)

def complex_camera(camera, target_rect, window_width, window_height):
    # we want to center target_rect
    x = -target_rect.center[0] + window_width/2 
    y = -target_rect.center[1] + window_height/2
    # move the camera. Let's use some vectors so we can easily substract/multiply
    camera.topleft += (pygame.Vector2((x, y)) - pygame.Vector2(camera.topleft)) * 0.06 # add some smoothness coolnes
    # set max/min x/y so we don't see stuff outside the world
    camera.x = max(-(camera.width-window_width), min(0, camera.x))
    camera.y = max(-(camera.height-window_height), min(0, camera.y))

    return camera