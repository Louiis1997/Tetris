import copy
import random
from typing import List

from src.game.tetrominos.piece import Piece

EMPTY_BLOCK = 0


class TetrisEnvironment:
    def __init__(self, height, width, pieces):
        self.__height = height
        self.__width = width
        self.__pieces = pieces

        self.__current_bag_piece_index = list()
        self.__current_piece_index = None
        self.__current_piece = None

        self.__board = [[EMPTY_BLOCK for i in range(width)] for j in range(height)]

    def reset(self, height, width):
        """Resets the game and returns the current state"""
        self.__height = height
        self.__width = width
        self.__board = [[EMPTY_BLOCK for i in range(width)] for j in range(height)]

        self.__current_bag_piece_index = list()
        self.__current_piece_index = None
        self.__current_piece = None

        self.new_round()

    def new_round(self):
        """Starts a new round with a new piece and renew the bag of pieces if needed"""
        self.create_shuffled_bag()
        self.next_piece()
        self.place_piece_at_base_position(self.__current_piece[0])

    def print_board(self):
        print("Board state is : ")
        for row in self.__board:
            print(row)

    @property
    def board(self):
        return self.__board

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @property
    def pieces(self):
        return self.__pieces

    @property
    def current_piece_index(self):
        return self.__current_piece_index + 1;

    def get_current_piece(self) -> List[Piece]:
        return self.__current_piece

    def next_piece(self):
        """Get the next piece"""
        if len(self.__current_bag_piece_index) == 0:
            self.create_shuffled_bag()
        else:
            self.__current_piece_index = self.__current_bag_piece_index.pop()

        self.__current_piece = copy.deepcopy(self.__pieces[self.current_piece_index])
        return self.__current_piece

    def create_shuffled_bag(self):
        """Create a queue of shuffled pieces"""
        piece_indexes_bag = list(range(len(self.__pieces)))
        self.__current_bag_piece_index = random.sample(piece_indexes_bag, len(piece_indexes_bag))

    def place_piece_at_base_position(self, piece: Piece):
        """Place a piece on the board"""
        for block in piece.blocks:
            block.x = block.x
            block.y = block.y + 4
            self.__board[block.x][block.y] = piece.grid_representation

    @staticmethod
    def is_touching_itself(piece, x, y):
        """Checks if the piece collides with itself"""
        block_position_down = (x, y)
        piece_block_positions = map(lambda block: (block.x, block.y), piece.blocks)
        if block_position_down in piece_block_positions:
            return True

        return False

    def entering_in_collision(self, piece, down, left, right):
        """Checks if the piece collides with pieces in current board"""
        for block in piece.blocks:  # y => row, x => column
            # Ternary operator
            x = block.x + 1 if down else block.x
            y = block.y + 1 if right else block.y - 1 if left else block.y

            if x >= self.__height:
                # print("Collision detected -> down -> touched the bottom")
                return True

            if y >= self.__width:
                # print("Collision detected -> right -> touched the right wall")
                return True

            if y < 0:
                # print("Collision detected -> left -> touched the left wall")
                return True

            simulated_next_position_value = self.__board[x][y]
            if self.is_touching_itself(piece, x, y):
                pass
            elif simulated_next_position_value != EMPTY_BLOCK:
                return True

        return False

    def move_down(self, piece: Piece):
        """Move the piece down"""
        for block in piece.blocks:  # Clearing piece in board
            self.__board[block.x][block.y] = EMPTY_BLOCK
        piece.move_down()
        for block in piece.blocks:  # Placing piece in board
            self.__board[block.x][block.y] = piece.grid_representation

    def move_left(self, piece: Piece):
        """Move the piece left"""
        for block in piece.blocks:
            self.__board[block.x][block.y] = EMPTY_BLOCK
        piece.move_left()
        for block in piece.blocks:
            self.__board[block.x][block.y] = piece.grid_representation

    def move_right(self, piece: Piece):
        """Move the piece right"""
        for block in piece.blocks:
            self.__board[block.x][block.y] = EMPTY_BLOCK
        piece.move_right()
        for block in piece.blocks:
            self.__board[block.x][block.y] = piece.grid_representation
