import random
from time import sleep
from typing import List, Any

# Rendering game
import cv2
import numpy as np
from PIL import Image

ACTIONS = []

# class TetrisGame:

# Tetris Board variables
MAP_EMPTY = 0
MAP_BLOCK = 1
MAP_PLAYER = 2
BOARD_HEIGHT = 20
BOARD_WIDTH = 10

# Tetris Colors
COLORS = {
    0: (255, 255, 255),
    1: (247, 64, 99),
    2: (0, 167, 247),
}

# Each piece is represented by a 4x4 matrix
# Each piece has 4 rotations
# Each element of the matrix is a 2-tuple (x, y)
# where x and y are the coordinates of the piece's block
PIECES = {
    0: {  # I
        0: [(0, 0), (1, 0), (2, 0), (3, 0)],
        90: [(1, 0), (1, 1), (1, 2), (1, 3)],
        180: [(3, 0), (2, 0), (1, 0), (0, 0)],
        270: [(1, 3), (1, 2), (1, 1), (1, 0)],
    },
    1: {  # T
        0: [(1, 0), (0, 1), (1, 1), (2, 1)],
        90: [(0, 1), (1, 2), (1, 1), (1, 0)],
        180: [(1, 2), (2, 1), (1, 1), (0, 1)],
        270: [(2, 1), (1, 0), (1, 1), (1, 2)],
    },
    2: {  # L
        0: [(1, 0), (1, 1), (1, 2), (2, 2)],
        90: [(0, 1), (1, 1), (2, 1), (2, 0)],
        180: [(1, 2), (1, 1), (1, 0), (0, 0)],
        270: [(2, 1), (1, 1), (0, 1), (0, 2)],
    },
    3: {  # J
        0: [(1, 0), (1, 1), (1, 2), (0, 2)],
        90: [(0, 1), (1, 1), (2, 1), (2, 2)],
        180: [(1, 2), (1, 1), (1, 0), (2, 0)],
        270: [(2, 1), (1, 1), (0, 1), (0, 0)],
    },
    4: {  # Z
        0: [(0, 0), (1, 0), (1, 1), (2, 1)],
        90: [(0, 2), (0, 1), (1, 1), (1, 0)],
        180: [(2, 1), (1, 1), (1, 0), (0, 0)],
        270: [(1, 0), (1, 1), (0, 1), (0, 2)],
    },
    5: {  # S
        0: [(2, 0), (1, 0), (1, 1), (0, 1)],
        90: [(0, 0), (0, 1), (1, 1), (1, 2)],
        180: [(0, 1), (1, 1), (1, 0), (2, 0)],
        270: [(1, 2), (1, 1), (0, 1), (0, 0)],
    },
    6: {  # O
        0: [(1, 0), (2, 0), (1, 1), (2, 1)],
        90: [(1, 0), (2, 0), (1, 1), (2, 1)],
        180: [(1, 0), (2, 0), (1, 1), (2, 1)],
        270: [(1, 0), (2, 0), (1, 1), (2, 1)],
    }
}

BASIC_REWARD = 1
GAME_OVER_REWARD = -2


class TetrisEnvironment:
    __height: int
    __width: int
    __board: List[Any]
    __game_over: bool
    __bag_pieces: list[Any]
    __next_piece: int
    __score: int

    __current_piece: int
    __current_rotation: int
    __current_position: tuple[int, int]

    def __init__(self, rows=10, cols=20):
        self.reset(rows, cols)

    @property
    def score(self):
        """Returns the score of the game"""
        return self.__score

    def get_state_size(self):
        """Size of the state"""
        return 4

    def reset(self, rows, cols):
        """Resets the game and returns the current state"""
        self.__height = rows
        self.__width = cols
        self.__board = [[MAP_EMPTY for _ in range(self.__width)] for y in range(self.__height)]
        self.__game_over = False

        self.__bag_pieces = list(range(len(PIECES)))
        random.shuffle(self.__bag_pieces)
        self.__next_piece = self.__bag_pieces.pop()

        self._new_round()

        self.__score = 0

        return self.get_board_props(self.__board)

    def _get_rotated_piece(self):
        """Returns the piece rotated by the given rotation (e.g. piece 1 (T), rotation 90°"""
        return PIECES[self.__current_piece][self.__current_rotation]

    def _get_complete_board(self):
        """Returns the board with the current piece in it"""
        piece = self._get_rotated_piece()
        piece = [(x + self.__current_position[0], y + self.__current_position[1]) for x, y in piece]

        board = [row[:] for row in self.__board]
        for x, y in piece:
            if y >= 0:
                board[y][x] = MAP_PLAYER
        return board

    def _new_round(self):
        """Starts a new round with a new piece and renew the bag of pieces if needed"""
        if len(self.__bag_pieces) == 0:
            self.__bag_pieces = list(range(len(PIECES)))
            random.shuffle(self.__bag_pieces)

        self.__current_piece = self.__next_piece
        self.__next_piece = self.__bag_pieces.pop()
        self.__current_rotation = 0
        self.__current_position = [3, 0]  # Set the current position of the piece at the top of the board

        # Check if the game is over
        if self.check_collision(self._get_rotated_piece(), self.__current_position):
            self.__game_over = True

    def check_collision(self, piece, position):
        """Checks if the piece collides with the board"""
        for x, y in piece:  # y => row, x => column
            x += position[0]
            y += position[1]
            if x < 0 or x >= self.__width or y >= self.__height:
                return True
            elif y >= 0 and self.__board[y][x] == MAP_BLOCK:
                return True
        return False

    def get_board_props(self, board):
        """Returns the board properties"""
        lines, board = self.clear_lines(board)
        holes = self.get_number_of_holes(board)
        total_bumpiness, max_bumpiness = self.bumpiness(board)
        sum_height, max_height, min_height = self.get_heights(board)
        return [lines, holes, total_bumpiness, sum_height]

    def rotate(self, angle):
        """Rotates the piece by the given angle"""
        rotation = self.__current_rotation + angle
        self.__current_rotation = rotation % 360  # TODO: Check if correct (e.g. -90° => 270°)

    def add_piece_to_the_board(self, piece, position):
        """Adds the piece to the board"""
        board = [row[:] for row in self.__board]
        for x, y in piece:
            # board[y + position[1]][x + position[0]] = MAP_BLOCK
            x += position[0]
            y += position[1]
            if y >= 0:
                print("Board size: ", len(board), len(board[0]))
                print("Adding piece to the board : ", x, y)
                if y >= len(board) or x >= len(board[0]):
                    print("Out of bounds")
                else:
                    board[y][x] = MAP_BLOCK
        return board

    def clear_lines(self, board):
        """Clears the lines and returns the number of cleared lines"""
        lines_to_clear = [index for index, row in enumerate(board) if MAP_EMPTY not in row]  # TODO: Check if correct
        if len(lines_to_clear) > 0:
            # Removing cleared lines and adding new empty lines
            for index in lines_to_clear:
                board.pop(index)
                board.insert(0, [MAP_EMPTY for _ in range(self.__width)])

        return len(lines_to_clear), board

    def get_number_of_holes(self, board):
        """Returns the number of holes in the board (meaning empty spaces that are underneath at least one block)"""
        holes = 0

        # Iterate on each cell of the board by column, from top to bottom and left to right
        for col in range(self.__width):
            found_block = False
            for row in range(self.__height):
                # If a block is found, then the next empty spaces are holes
                if board[row][col] == MAP_BLOCK:
                    found_block = True
                elif found_block and board[row][col] == MAP_EMPTY:
                    holes += 1

        return holes

    def bumpiness(self, board):
        """Sum of the absolute differences between the heights of adjacent columns"""
        total_bumpiness = 0
        max_bumpiness = 0

        for col in range(self.__width - 1):
            bumpiness = abs(self.__get_column_height(board, col) - self.__get_column_height(board, col + 1))
            total_bumpiness += bumpiness
            max_bumpiness = max(max_bumpiness, bumpiness)

        return total_bumpiness, max_bumpiness

    def __get_column_height(self, board, col):
        """Returns the height of the given column"""
        height = 0
        for row in range(self.__height):
            if board[row][col] == MAP_BLOCK:
                height = self.__height - row
                break
        return height

    def get_heights(self, board):
        """Returns the sum of the heights of the columns, the maximum height and the minimum height"""
        sum_height = 0
        max_height = 0
        min_height = self.__height

        for col in range(self.__width):
            height = self.__get_column_height(board, col)
            sum_height += height
            max_height = max(max_height, height)
            min_height = min(min_height, height)

        return sum_height, max_height, min_height

    def get_next_states(self):
        """Get the list of all possible next states"""
        states = {}
        piece_id = self.__current_piece

        if piece_id == 6:  # The piece is the squared 'o' no need to rotate it 4 times only 1
            rotations = [0]
        elif piece_id == 0:  # The piece is the 'i' no need to rotate it 4 times only 2
            rotations = [0, 90]
        else:
            rotations = [0, 90, 180, 270]

        # Get all possible rotations
        for rotation in rotations:
            piece = PIECES[piece_id][rotation]
            min_x = min([x for x, y in piece])
            max_x = max([x for x, y in piece])

            # Get all possible positions
            for placement in range(self.__width - (max_x - min_x)):
                position = [placement - min_x, 0]

                # Get the lowest position
                while not self.check_collision(piece, position):
                    position[1] += 1
                position[1] -= 1

                # Add the state to the list
                if position[1] >= 0:
                    board = self.add_piece_to_the_board(piece, position)
                    states[(placement, rotation)] = self.get_board_props(board)

        return states

    def do(self, x, rotation, render=False, render_delay=None):
        """Play a round given a position, a rotation and returning the reward if the game is over"""
        self.__current_position = [x, 0]
        self.__current_rotation = rotation

        # Make the piece drop
        while not self.check_collision(self._get_rotated_piece(), self.__current_position):
            # Handle rendering
            if render:
                self.render()
                if render_delay:
                    sleep(render_delay)
            self.__current_position[1] += 1
        self.__current_position[1] -= 1

        # Update game board
        piece = self._get_rotated_piece()
        self.__board = self.add_piece_to_the_board(piece, self.__current_position)
        cleared_lines, self.__board = self.clear_lines(self.__board)

        # Compute score
        score = BASIC_REWARD + (cleared_lines ** 2) * self.__width
        self.__score += score

        # Start a new round and Check if game over
        self._new_round()
        if self.__game_over:
            score += GAME_OVER_REWARD

        return score, self.__game_over

    def render(self):
        """Renders the current board"""
        img = [COLORS[p] for row in self._get_complete_board() for p in row]
        img = np.array(img).reshape(BOARD_HEIGHT, BOARD_WIDTH, 3).astype(np.uint8)
        img = img[..., ::-1]  # Convert RRG to BGR (used by cv2)
        img = Image.fromarray(img, 'RGB')
        img = img.resize((BOARD_WIDTH * 25, BOARD_HEIGHT * 25))
        img = np.array(img)
        cv2.putText(img, str(self.score), (22, 22), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        cv2.imshow('image', np.array(img))
        cv2.waitKey(1)

    def print(self):
        for row in self.__board:
            print(row)

# class Agent:
#     def __init__(self, env, alpha=1, gamma=0.3):
#         self.__qtable = {}
#         for state in env.states:
#             self.__qtable[state] = {}
#             for action in ACTIONS:
#                 self.__qtable[state][action] = 0.0
#
#         self.__env = env
#         self.__alpha = alpha
#         self.__gamma = gamma
#         self.__history = []
#         self.__state = None
#         self.__score = 0
#         self.reset(False)
#
#     def reset(self, store_history=True):
#         if store_history:
#             self.__history.append(self.__score)
#         self.__state = self.__env.start
#         self.__score = 0
