#!/usr/bin/env python3

import pygame
import sys
import os
import enum
import pickle

GRID_X, GRID_Y = (200, 200)
BLOCK_SIZE = 5
REFRESH_SIZE = 50

FILENAME = 'grid.p'

class PixelType(enum.Enum):
    EMPTY = 0
    PROBE = 1
    HIT = 2
    ANCHOR = 3


#COLOR_MAP = {
#    PixelType.EMPTY: (0, 0, 255),
#    PixelType.PROBE: (255, 255, 0),
#    PixelType.HIT: (0, 0, 0),
#    PixelType.ANCHOR: (255, 0, 0)
#}
COLOR_MAP = {
    PixelType.EMPTY: (255, 255, 255),
    PixelType.PROBE: (0, 0, 0),
    PixelType.HIT: (0, 255, 0),
    PixelType.ANCHOR: (255, 0, 0)
}


def main():
    pygame.init()
    screen = pygame.display.set_mode([GRID_X * BLOCK_SIZE, GRID_Y * BLOCK_SIZE])
    clock = pygame.time.Clock()

    def clear():
        nonlocal grid

        grid = []
        for i in range(GRID_X):
            grid.append([PixelType.EMPTY] * GRID_Y)

        grid[150][50] = PixelType.ANCHOR

    if os.path.exists(FILENAME):
        print("Loading", FILENAME)
        with open(FILENAME, 'rb') as f:
            grid = pickle.load(f)
    else:
        print("Generating empty grid")
        clear()

    screen.fill(COLOR_MAP[PixelType.EMPTY])

    blink_state = False
    check_state = False

    position = [10, 10]

    def draw_block(screen, pixel_type, x, y):
        nonlocal blink_state

        #if blink_state:
        #   COLOR_MAP[PixelType.EMPTY] = (0, 0, 0) 
        #else:
        #   COLOR_MAP[PixelType.EMPTY] = (255, 255, 255)

        if pixel_type == PixelType.PROBE:
            if blink_state:
                pixel_type = PixelType.EMPTY

            blink_state = not blink_state

        if check_state:
            if pixel_type == PixelType.HIT:
                if blink_state:
                    pixel_type = PixelType.PROBE
                else:
                    pixel_type = PixelType.HIT

        color = COLOR_MAP[pixel_type]

        screen.fill(color, (
            x * BLOCK_SIZE, y * BLOCK_SIZE,
            BLOCK_SIZE, BLOCK_SIZE))

        #pygame.display.flip()

    def redraw(full=False):
        for x, row in enumerate(grid):
            if not full and abs(position[0] - x) > REFRESH_SIZE:
                p = PixelType.HIT
                continue

            for y, p in enumerate(row):
                if not full and abs(position[1] - y) > REFRESH_SIZE:
                    p = PixelType.HIT
                    continue

                if position == [x, y]:
                    p = PixelType.PROBE

                draw_block(screen, p, x, y)

    def full_redraw():
        for x, row in enumerate(grid):
            for y, p in enumerate(row):
                draw_block(screen, p, x, y)

    full_redraw()

    while True:
        #print(position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open(FILENAME, 'wb') as f:
                    pickle.dump(grid, f)
                print("Stored to", FILENAME)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    position[0] -= 1
                elif event.key == pygame.K_RIGHT:
                    position[0] += 1
                elif event.key == pygame.K_UP:
                    position[1] -= 1
                elif event.key == pygame.K_DOWN:
                    position[1] += 1
                elif event.key == pygame.K_r:
                    full_redraw()
                elif event.key == pygame.K_RSHIFT:
                    check_state = not check_state
                elif event.key == pygame.K_c:
                    clear()
                    full_redraw()
                elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    grid[position[0]][position[1]] = PixelType.HIT
                elif event.key == pygame.K_BACKSPACE:
                    grid[position[0]][position[1]] = PixelType.EMPTY
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = map(int, event.pos)
                position = [x//BLOCK_SIZE, y//BLOCK_SIZE]

        redraw()
        pygame.time.delay(100)
        pygame.display.flip()
        clock.tick()


if __name__ == '__main__':
    main()
