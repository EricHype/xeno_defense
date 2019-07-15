from pygame import *

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
        l, t, _, _ = target_rect # l = left,  t = top
        _, _, w, h = camera      # w = width, h = height
        return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)