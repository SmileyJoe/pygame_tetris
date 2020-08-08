import pygame
import random
from tetromino import Tetromino
from constants import BLOCK_WIDTH
from color import WHITE
import copy
from pprint import pprint


class Board:
    DIRECTION_DOWN = 1
    DIRECTION_LEFT = 2
    DIRECTION_RIGHT = 3
    ROTATE = 4
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20

    __height = BLOCK_WIDTH * BOARD_HEIGHT
    __width = BLOCK_WIDTH * BOARD_WIDTH
    __start_x = 0
    __screen = None
    __tetromino = None
    __tetromino_hold = None
    __tetrominos_upcoming = []
    __tetromino_next = None
    __wall_left = None
    __wall_right = None
    __wall_bottom = None
    __rows = {}
    __changed_rects = []
    __game_over = False
    __starting_position = [10, 0]
    __can_hold = True
    __hold_position = [2, 1]
    __next_position = [17, 1]

    def __init__(self, screen, start_x):
        self.__start_x = start_x
        self.__screen = screen
        self.speed = 1
        self.draw_frame()

    @property
    def tetromino(self):
        return self.__tetromino

    @tetromino.setter
    def tetromino(self, tetromino):
        if tetromino is not None:
            self.changed_rects.extend(tetromino.rects)

        if self.__tetromino is not None:
            self.changed_rects.extend(self.__tetromino.rects)

        self.__tetromino = tetromino

    @property
    def tetromino_next(self):
        return self.__tetromino_next

    @tetromino_next.setter
    def tetromino_next(self, tetromino_next):
        if tetromino_next is not None:
            self.changed_rects.extend(tetromino_next.rects)

        if self.__tetromino_next is not None:
            self.changed_rects.extend(self.__tetromino_next.rects)

        self.__tetromino_next = tetromino_next

    @property
    def tetromino_hold(self):
        return self.__tetromino_hold

    @tetromino_hold.setter
    def tetromino_hold(self, tetromino_hold):
        self.__tetromino_hold = tetromino_hold

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        self.__speed = speed

    @property
    def changed_rects(self):
        return self.__changed_rects

    @changed_rects.setter
    def changed_rects(self, changed_rects):
        self.__changed_rects = changed_rects

    @property
    def game_over(self):
        return self.__game_over

    @game_over.setter
    def game_over(self, game_over):
        self.__game_over = game_over

    def draw_frame(self):
        self.__wall_bottom = pygame.draw.line(self.__screen, WHITE, (self.__start_x, self.__height),
                                              (self.__start_x + self.__width, self.__height))

        self.__wall_left = pygame.draw.line(self.__screen, WHITE, (self.__start_x - 1, 0),
                                            (self.__start_x - 1, self.__height))

        self.__wall_right = pygame.draw.line(self.__screen, WHITE, (self.__start_x + self.__width, 0),
                                             (self.__start_x + self.__width, self.__height))

    def move_tetromino(self, direction):
        temp_tetromino = copy.copy(self.tetromino)

        if direction == self.DIRECTION_DOWN:
            temp_tetromino.move_down()

            if self.check_collision(temp_tetromino):
                self.end_turn()
            else:
                self.tetromino = temp_tetromino

        elif direction == self.DIRECTION_LEFT:
            temp_tetromino.move_left()

            if not self.check_collision(temp_tetromino):
                self.tetromino = temp_tetromino

        elif direction == self.DIRECTION_RIGHT:
            temp_tetromino.move_right()

            if not self.check_collision(temp_tetromino):
                self.tetromino = temp_tetromino

        elif direction == self.ROTATE:
            temp_tetromino.rotate_clockwise()

            if not self.check_collision(temp_tetromino):
                self.tetromino = temp_tetromino

    def hold(self):
        if self.__can_hold:
            self.__can_hold = False
            temp_tetromino = self.tetromino
            if self.tetromino_hold:
                self.tetromino = self.tetromino_hold
                self.tetromino.move_to(self.__starting_position)
                self.tetromino_hold = temp_tetromino
            else:
                self.tetromino_hold = temp_tetromino
                self.new_block()

            self.tetromino_hold.move_to(self.__hold_position)
            self.changed_rects.extend(self.tetromino_hold.rects)
            self.tetromino_hold.draw(self.__screen)

    def check_collision(self, tetromino):
        if tetromino.colliderect(self.__wall_bottom):
            return True
        elif tetromino.colliderect(self.__wall_right):
            return True
        elif tetromino.colliderect(self.__wall_left):
            return True
        else:
            for row, rects in self.__rows.items():
                for rect in rects:
                    if tetromino.colliderect(rect):
                        return True

    def new_block(self):
        if not self.__tetrominos_upcoming:
            pprint("no blocks")
            self.__tetrominos_upcoming = list(range(Tetromino.block_count()))
            random.shuffle(self.__tetrominos_upcoming)
            self.tetromino = Tetromino.get(self.__tetrominos_upcoming.pop(0), self.__starting_position)
            self.tetromino_next = Tetromino.get(self.__tetrominos_upcoming.pop(0), self.__next_position)
        else:
            pprint("have blocks")
            self.tetromino = self.__tetromino_next
            self.tetromino.move_to(self.__starting_position)
            self.tetromino_next = Tetromino.get(self.__tetrominos_upcoming.pop(0), self.__next_position)

        pprint(self.tetromino_next.name)
        self.tetromino_next.draw(self.__screen)

    def draw(self):
        self.draw_frame()

        self.tetromino.draw(self.__screen)

        for row, rects in self.__rows.items():
            for rect in rects:
                pygame.draw.rect(self.__screen, WHITE, rect)

        self.__remove_duplicate_changed()

    def __remove_duplicate_changed(self):
        filtered_changed_rects = []
        for rect in self.changed_rects:
            found = False
            for filtered in filtered_changed_rects:
                if filtered.x == rect.x and filtered.y == rect.y:
                    found = True
                    break

            if not found:
                filtered_changed_rects.append(rect)

        self.changed_rects = filtered_changed_rects

    def end_turn(self):
        self.__can_hold = True
        deleted_rows = []
        for rect in self.tetromino.rects:
            row = int(rect.y / BLOCK_WIDTH)
            rects = self.__rows.get(row)

            if not rects:
                rects = []

            rects.append(rect)

            if len(rects) == self.BOARD_WIDTH:
                del self.__rows[row]
                deleted_rows.append(row)
                self.changed_rects.extend(rects)
            else:
                self.__rows[row] = rects

        if len(deleted_rows) > 0:
            deleted_rows.sort(reverse=True)
            for index, deleted_row in enumerate(deleted_rows):
                deleted_row = deleted_row + index
                new_rows = {}
                for row, rects in self.__rows.items():
                    if row < deleted_row:
                        new_rows[row + 1] = copy.copy(rects)
                        for rect in rects:
                            self.changed_rects.append(copy.copy(rect))
                            rect.y = rect.y + BLOCK_WIDTH
                            self.changed_rects.append(copy.copy(rect))
                    else:
                        new_rows[row] = copy.copy(rects)
                self.__rows = copy.copy(new_rows)

        for rect in self.tetromino.rects:
            if rect.y <= 0:
                self.game_over = True

        if not self.game_over:
            self.new_block()
