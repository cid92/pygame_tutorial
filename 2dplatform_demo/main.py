import sys
import random
import math

import pygame
import pygame.gfxdraw
from pygame.locals import *

# Initialise the pygame library
pygame.init()
clock = pygame.time.Clock()
fps = 60

# Define the colors we will use in RGB format
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)


pygame.font.init()
FONT = pygame.font.Font(None, 15)

W = 800
H = 600
HW = W/2
HH = H/2
PH = 1.5*HH
DISPLAY_AREA = W * H
PEAK_SPEED = 15

# create the primary display surface  based on the chosen resolution
screen = pygame.display.set_mode((W, H))
collision_map = pygame.Surface((W, H))
pygame.display.set_caption("2D Platform Game")
# OBJECT CLASSES


class Platform:
    def __init__(self, x, y, width):
        self.x1 = x
        self.y = y
        self.x2 = x+width


class Platforms:
        def __init__(self):
            self.container = list([])

        def add(self, p):
            self.container.append(p)

        def draw(self):
            global WHITE
            global collision_map
            display = pygame.display.get_surface()
            for p in self.container:
                pygame.draw.line(display, WHITE, (p.x1, p.y), (p.x2, p.y), 1)
                pygame.draw.line(collision_map, WHITE, (p.x1, p.y), (p.x2, p.y), 1)

        def do(self):
            self.draw()


class Player:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.falling = True
        self.jumping = False
        self.size = size
        self.collision = False
        self.i = PEAK_SPEED

    def do_action(self):
        global collision_map
        global velocity
        # Perform side movement
        self.x += self.velocity_x
        #Check falling
        read_color = collision_map.get_at((int(self.x), int(self.y+self.size)))
        if read_color == BLACK and self.jumping is False:
            self.falling = True
            self.jumping = False
            self.collision = False
        # Perform jumping
        if self.jumping is True and self.falling is False:
            self.velocity_y = int(velocity[self.i])
            self.y += self.velocity_y
            self.collision = False
            if self.i < PEAK_SPEED:
                self.i = self.i + 1
            else:
                self.jumping = False
                self.falling = True
                self.i = PEAK_SPEED
        # Perform falling
        if self.falling is True and self.jumping is False:
            bottom_y = self.y + self.size
            for collision_y in range(bottom_y, bottom_y + self.velocity_y):
                read_color = collision_map.get_at((int(self.x), int(collision_y)))
                if read_color == WHITE:
                    self.collision = True
                    self.y = collision_y - self.size
                    self.falling = False
                    self.velocity_y = 0
                    self.i = PEAK_SPEED
                    break
            if not self.collision:
                self.y += self.velocity_y
                self.velocity_y = int(self.velocity_y + 1)


# this function read the control keys

    def keys(self):
        key_press = pygame.key.get_pressed()
        if key_press[K_UP] and (self.jumping is False and self.falling is False):
            self.jumping = True
            p.i = 0
        if key_press[K_LEFT]:
            self.velocity_x = -5
        elif key_press[K_RIGHT]:
            self.velocity_x = 5
        else:
            self.velocity_x = 0

    def draw(self):
        global screen
        global RED
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.size)

    def do(self):
        self.do_action()
        self.keys()
        self.draw()


# FUNCTIONS -------------------------------------------------------------------------------------------------- FUNCTIONS


# this function handles window controls [x] and key presses [esc]


def event_handler():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

# Plot platforms


def draw_platform():
    pygame.draw.line(screen, WHITE, [0, PH], [W, PH], 1)
    pygame.draw.line(collision_map, WHITE, (0, PH), (W, PH), 1)


# MAIN -------------------------------------------------------------------------------------------------------- MAIN


player_size = 20
platform_width = 50
p = Player(HW, 0, player_size)
velocity = [(i / 2.0) - 7.5 for i in range(0, 31)]
platforms = Platforms()
platforms.add(Platform(0, HW, W))

for i in range(0,25):
    platforms.add(Platform(random.randint(0, W-50), random.randint(0, HW-20), platform_width))

while True:
    event_handler()  # check for [esc] and [x] pressed
    p.do()
    platforms.do()
    # update screen
    pygame.display.update()
    clock.tick(fps)
    screen.fill(BLACK)








