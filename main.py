import pygame
import time
from color import BLACK
from board import Board
from constants import BLOCK_WIDTH

pygame.init()
BORDER = 2
board_start = BLOCK_WIDTH * BORDER + (BLOCK_WIDTH * 4)
width = (Board.BOARD_WIDTH * BLOCK_WIDTH) + (BLOCK_WIDTH * BORDER) + (BLOCK_WIDTH * 4) + board_start
height = (Board.BOARD_HEIGHT * BLOCK_WIDTH) + (BLOCK_WIDTH * BORDER * 2)

refresh_board = True

screen = pygame.display.set_mode((width, height))

board = Board(screen, board_start)
board.new_block()
board.speed = 1

while True:
    screen.fill(BLACK)

    if not board.game_over:
        for event in pygame.event.get():
            if event.type == pygame.K_o:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    board.move_tetromino(Board.DIRECTION_LEFT)
                if event.key == pygame.K_RIGHT:
                    board.move_tetromino(Board.DIRECTION_RIGHT)
                if event.key == pygame.K_q:
                    board.move_tetromino(Board.ROTATE)
                if event.key == pygame.K_w:
                    board.hold()
                if event.key == pygame.K_1:
                    board.speed = 1
                if event.key == pygame.K_2:
                    board.speed = 2
                if event.key == pygame.K_3:
                    board.speed = 3
                if event.key == pygame.K_4:
                    board.speed = 4
                if event.key == pygame.K_5:
                    board.speed = 5

        board.move_tetromino(Board.DIRECTION_DOWN)
        board.draw()

        if refresh_board:
            pygame.display.flip()
            refresh_board = False
        else:
            pygame.display.update(board.changed_rects)

        board.changed_rects = []

    # else:
    # todo: show scores, retry/quit
    time.sleep((1000 / board.speed) / 1000)
