import pygame
from pygame import *

import constants
import spritesheet

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

def simple_camera(camera, target_rect):
        l, t, _, _ = target_rect # l = left,  t = top
        _, _, w, h = camera      # w = width, h = height
        return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    # we want to center target_rect
    x = -target_rect.center[0] + WIN_WIDTH/2 
    y = -target_rect.center[1] + WIN_HEIGHT/2
    # move the camera. Let's use some vectors so we can easily substract/multiply
    camera.topleft += (pygame.Vector2((x, y)) - pygame.Vector2(camera.topleft)) * 0.06 # add some smoothness coolnes
    # set max/min x/y so we don't see stuff outside the world
    camera.x = max(-(camera.width-WIN_WIDTH), min(0, camera.x))
    camera.y = max(-(camera.height-WIN_HEIGHT), min(0, camera.y))

    return camera

def main():
    global cameraX, cameraY
    #pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Use arrows to move!")
    timer = pygame.time.Clock()

    ss = spritesheet.spritesheet('PixelAtlas.png')
    groundImage = ss.load_image_at((0, 0, 32, 32))
    skyimage = ss.load_image_at((32, 96, 32, 32))

    up = down = left = right = running = False
    #bg = Surface((32,32))
    #bg.convert()
    #bg.fill(Color("#000000"))
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    platforms = []
    x = y = 0
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                P",
        "P                                P",
        "P                                P",
        "P                                P",
        "P                                P",
        "P                                P",
        "P                                P",
        "P       PPPPPPPPPPP              P",
        "P                                P",
        "P                                P",
        "P                                P",
        "P                                P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]

    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y, groundImage)
                platforms.append(p)
                entities.add(p)
            x += 32
        y += 32
        x = 0

    total_level_width  = len(level[0])*32 # calculate size of level in pixels
    total_level_height = len(level)*32    # maybe make 32 an constant
    camera = Camera(complex_camera, total_level_width, total_level_height)

    entities.add(player)
    while 1:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT: 
                raise SystemExit("QUIT")
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    raise SystemExit("ESCAPE")
                if e.key == K_UP:
                    up = True
                if e.key == K_DOWN:
                    down = True
                if e.key == K_LEFT:
                    left = True
                if e.key == K_RIGHT:
                    right = True
                if e.key == K_SPACE:
                    running = True

            if e.type == KEYUP:
                if e.key == K_UP:
                    up = False
                if e.key == K_DOWN:
                    down = False
                if e.key == K_RIGHT:
                    right = False
                if e.key == K_LEFT:
                    left = False
                if e.key == K_RIGHT:
                    right = False

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(skyimage, (x * 32, y * 32))

        camera.update(player) # camera follows player. Note that we could also follow any other sprite

        # update player, draw everything else
        player.update(up, down, left, right, running, platforms)

        for e in entities:
            # apply the offset to each entity.
            # call this for everything that should scroll,
            # which is basically everything other than GUI/HUD/UI
            screen.blit(e.image, camera.apply(e)) 

        pygame.display.update()

    

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Player(Entity):

    def __init__(self, x, y):
        Entity.__init__(self)
        self.jumpVelocity = 10
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32,32))
        self.image.fill(Color("#0000FF"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self, up, down, left, right, running, platforms):
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= self.jumpVelocity
        if down:
            pass
        if running:
            self.xvel = 12
        if left:
            self.xvel = -8
        if right:
            self.xvel = 8
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                    print("collide right")
                if xvel < 0:
                    self.rect.left = p.rect.right
                    print("collide left")
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

class Platform(Entity):
    def __init__(self, x, y, image):
        Entity.__init__(self)
        self.image = image
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

if __name__ == "__main__":
    main()