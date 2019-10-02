import pygame
import color
import random
import math
import copy
from constants import BLOCK_WIDTH
from pygame import Rect


class Tetromino:

    BLOCK = (BLOCK_WIDTH, BLOCK_WIDTH)

    BLOCK_I = [
        Rect((0, 0), BLOCK),
        Rect((0, BLOCK_WIDTH), BLOCK),
        Rect((0, BLOCK_WIDTH*2), BLOCK),
        Rect((0, BLOCK_WIDTH*3), BLOCK)
    ]
    BLOCK_J = [
        Rect((0, BLOCK_WIDTH*2), BLOCK),
        Rect((BLOCK_WIDTH, 0), BLOCK),
        Rect((BLOCK_WIDTH, BLOCK_WIDTH), BLOCK),
        Rect((BLOCK_WIDTH, BLOCK_WIDTH*2), BLOCK)
    ]
    BLOCK_L = [
        Rect((0, 0), BLOCK),
        Rect((0, BLOCK_WIDTH), BLOCK),
        Rect((0, BLOCK_WIDTH*2), BLOCK),
        Rect((BLOCK_WIDTH, BLOCK_WIDTH*2), BLOCK)
    ]
    BLOCK_O = [
        Rect((0, 0), BLOCK),
        Rect((0, BLOCK_WIDTH), BLOCK),
        Rect((BLOCK_WIDTH, 0), BLOCK),
        Rect((BLOCK_WIDTH, BLOCK_WIDTH), BLOCK)
    ]
    BLOCK_Z = [
        Rect((0, 0), BLOCK),
        Rect((BLOCK_WIDTH, 0), BLOCK),
        Rect((BLOCK_WIDTH, BLOCK_WIDTH), BLOCK),
        Rect((BLOCK_WIDTH*2, BLOCK_WIDTH), BLOCK)
    ]
    BLOCK_S = [
        Rect((0, BLOCK_WIDTH), BLOCK),
        Rect((BLOCK_WIDTH, BLOCK_WIDTH), BLOCK),
        Rect((BLOCK_WIDTH, 0), BLOCK),
        Rect((BLOCK_WIDTH*2, 0), BLOCK)
    ]
    BLOCK_T = [
        Rect((0, 0), BLOCK),
        Rect((BLOCK_WIDTH, 0), BLOCK),
        Rect((BLOCK_WIDTH*2, 0), BLOCK),
        Rect((BLOCK_WIDTH, BLOCK_WIDTH), BLOCK)
    ]

    __blocks = [
        ('I', color.CYAN, BLOCK_I),
        ('J', color.BLUE, BLOCK_J),
        ('O', color.YELLOW, BLOCK_O),
        ('L', color.ORANGE, BLOCK_L),
        ('Z', color.RED, BLOCK_Z),
        ('S', color.GREEN, BLOCK_S),
        ('T', color.PURPLE, BLOCK_T)
    ]

    __color = None
    __rects = None
    __start_position = None
    __name = None

    def random():
        return Tetromino(random.choice(list(Tetromino.__blocks)))

    def get(id, position=[0, 0]):
        return Tetromino(Tetromino.__blocks[id], position)

    @property
    def rects(self):
        return self.__rects

    @rects.setter
    def rects(self, rects):
        self.__rects = rects

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    def get_rects(self):
        return self.__rects

    def __init__(self, block, position=[0, 0]):
        self.name = block[0]
        self.__color = block[1]
        self.__start_position = block[2]
        self.move_to(position)

    def move_to(self, position):
        x = position[0]
        y = position[1]
        rects = []

        for rect in self.__start_position:
            new_rect = rect.copy()

            if x > 0:
                new_rect.x = rect.x + (x*BLOCK_WIDTH)

            if y > 0:
                new_rect.y = rect.y + (y*BLOCK_WIDTH)

            rects.append(new_rect)

        self.rects = rects

    def block_count():
        return len(Tetromino.__blocks)

    def move_left(self):
        self.__move(-BLOCK_WIDTH, 0)

    def move_right(self):
        self.__move(BLOCK_WIDTH, 0)

    def move_down(self):
        self.__move(0, BLOCK_WIDTH)

    def move_up(self):
        self.__move(0, -BLOCK_WIDTH)

    def rotate_clockwise(self):
        self.__rotate(90)

    def rotate_anticlockwise(self):
        self.__rotate(-90)

    def __rotate(self, angle):
        new_rects = []
        min_max_x = [-1, 0]
        min_max_y = [-1, 0]

        for rect in self.__rects:
            min_max_x = self.__get_min_max(rect.x, min_max_x)
            min_max_y = self.__get_min_max(rect.y, min_max_y)

        center_x = self.__get_center(min_max_x)
        center_y = self.__get_center(min_max_y)

        for rect in self.__rects:
            rads = math.radians(angle)
            x = math.cos(rads) * (rect.x - center_x) - math.sin(rads) * (rect.y - center_y) + center_x

            x = x - (x % BLOCK_WIDTH)

            y = math.sin(rads) * (rect.x - center_x) + math.cos(rads) * (rect.y - center_y) + center_y

            y = y - (y % BLOCK_WIDTH)

            new_rects.append(Rect((x, y), self.BLOCK))
        self.__rects = new_rects

    def __get_center(self, min_max):
        return min_max[0] + (min_max[1] - min_max[0])/2

    def __get_min_max(self, value, min_max):
        min = min_max[0]
        max = min_max[0]

        if min == -1 or value < min:
            min = value

        if value + BLOCK_WIDTH > max:
            max = value + BLOCK_WIDTH

        return [min, max]

    def __move(self, x_change, y_change):
        new_rects = []

        for rect in self.__rects:
            new_rects.append(rect.move(x_change, y_change))

        self.__rects = new_rects

    def draw(self, screen):
        for rect in self.__rects:
            pygame.draw.rect(screen, self.__color, rect)

    def collidetetromino(self, tetromino):
        for rect in self.__rects:
            if tetromino.colliderect(rect):
                return True
        return False

    def colliderect(self, external_rect):
        for rect in self.__rects:
            if rect.colliderect(external_rect):
                return True
        return False
