import random

class Tetris:
    def __init__(self, height=20, width=10):
        self.height = height
        self.width = width
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.tetrominoes = {
            'I': [[1, 1, 1, 1]],
            'O': [[1, 1], [1, 1]],
            'T': [[0, 1, 0], [1, 1, 1]],
            'S': [[0, 1, 1], [1, 1, 0]],
            'Z': [[1, 1, 0], [0, 1, 1]],
            'J': [[1, 0, 0], [1, 1, 1]],
            'L': [[0, 0, 1], [1, 1, 1]],
        }
        self.current_tetromino = None
        self.current_pos = [0, 0]
        self.game_over = False

    def new_tetromino(self):
        self.current_tetromino = random.choice(list(self.tetrominoes.values()))
        self.current_pos = [0, (self.width - len(self.current_tetromino[0])) // 2]
        if not self.valid_position():
            self.game_over = True

    def valid_position(self, dx=0, dy=0):
        for y, row in enumerate(self.current_tetromino):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = x + self.current_pos[1] + dx, y + self.current_pos[0] + dy
                    if (new_x < 0 or new_x >= self.width or new_y >= self.height or self.board[new_y][new_x]):
                        return False
        return True

    def merge_tetromino(self):
        for y, row in enumerate(self.current_tetromino):
            for x, cell in enumerate(row):
                if cell:
                    self.board[y + self.current_pos[0]][x + self.current_pos[1]] = 1

    def clear_lines(self):
        self.board = [row for row in self.board if any(cell == 0 for cell in row)]
        while len(self.board) < self.height:
            self.board.insert(0, [0 for _ in range(self.width)])

    def move(self, direction):
        dx, dy = 0, 0
        if direction == "left":
            dx = -1
        elif direction == "right":
            dx = 1
        elif direction == "down":
            dy = 1
        if self.valid_position(dx, dy):
            self.current_pos[0] += dy
            self.current_pos[1] += dx
        elif direction == "down":
            self.merge_tetromino()
            self.clear_lines()
            self.new_tetromino()

    def rotate(self):
        rotated = [list(row) for row in zip(*self.current_tetromino[::-1])]
        old_tetromino = self.current_tetromino
        self.current_tetromino = rotated
        if not self.valid_position():
            self.current_tetromino = old_tetromino

    def print_board(self):
        display = [row[:] for row in self.board]
        for y, row in enumerate(self.current_tetromino):
            for x, cell in enumerate(row):
                if cell:
                    display[y + self.current_pos[0]][x + self.current_pos[1]] = 1
        print("\n".join("".join("#" if cell else "." for cell in row) for row in display))
        print("\n" + "=" * self.width)

    def step(self):
        if not self.game_over:
            self.move("down")
        self.print_board()

tetris = Tetris()
tetris.new_tetromino()
while not tetris.game_over:
    tetris.step()
    command = input("Enter command (left, right, down, rotate, quit): ").strip().lower()
    if command == "quit":
        break
    elif command in ["left", "right", "down"]:
        tetris.move(command)
    elif command == "rotate":
        tetris.rotate()
