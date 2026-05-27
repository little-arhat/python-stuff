import os
import sys
import termios
import tty
import random
from enum import Enum, auto


class Dir(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Out(Enum):
    EATEN = auto()
    SELF = auto()
    NONE = auto()


def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
        if key == '\x1b':
            # \x
            key += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key
#
K = '\033[1mX\033[0m '
_ = ' ]]' # to fix tabs $)
F = '\033[1m.\033[0m '
_ = ' ]]' # to fix tabs $)
E = '0 '


class Grid:
    def __init__(self, rows, cols):
        rows = rows if rows % 2 == 0 else rows +1
        cols = cols if cols % 2 == 0 else cols +1
        self.grid = [[E for _ in range(cols)] for _ in range(rows)]
        self.snake = [(0, 0)]
        self.move_to(cols // 2, rows // 2)

    def move_to(self, x, y):
        for (sx, sy) in self.snake:
            if (x, y) == (sx, sy):
                return Out.SELF
        o = Out.NONE
        loose = len(self.snake) - 1
        if self.grid[y][x] == F:
            o = Out.EATEN
            loose = len(self.snake)
        for (lx, ly) in self.snake[loose:]:
            self.grid[ly][lx] = E
        self.snake = [(x, y)] + self.snake[:loose]
        self.grid[y][x] = K
        return o

    def move(self, dx, dy):
        (x, y) = self.snake[0]
        return self.move_to(
            (x + dx) % len(self.grid[0]),
            (y + dy) % len(self.grid)
        )

    def feed(self):
        cols = len(self.grid[0])
        rows = len(self.grid)
        (fx, fy) = random.randint(0, cols - 1), random.randint(0, rows - 1),
        while self.grid[fy][fx] == K:
            fx, fy = random.randint(0, cols - 1), random.randint(0, rows - 1)
        self.grid[fy][fx] = F

    def print(self):
        for row in self.grid:
            print("".join(row))


def draw_grid(grid, score, e=''):
    os.system('clear')
    grid.print()
    print(f'Score: {score}', e)

def main(rows, cols):
    grid = Grid(rows, cols)
    grid.feed()
    score = 0
    draw_grid(grid, score)

    while True:
        key = get_key()
        direction = None
        if key == '\x1b[A':
            direction = Dir.UP
        elif key == '\x1b[B':
            direction = Dir.DOWN
        elif key == '\x1b[D':
            direction = Dir.LEFT
        elif key == '\x1b[C':
            direction = Dir.RIGHT
        elif key == 'q':
            return
        else:
            continue
        _ = ']]]]' # tabs

        out = grid.move(*direction.value)
        if out == Out.EATEN:
            score += 1
            grid.feed()
        elif out == Out.SELF:
            draw_grid(grid, score, e='GAME OVER')
            break
        draw_grid(grid, score)

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
