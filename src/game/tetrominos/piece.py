import copy
import math


class Piece:
    def __init__(self, blocks, rotation, grid_representation):
        self.blocks = blocks
        self.rotation = rotation
        self.grid_representation = grid_representation
        self.current_matrix_position_in_board = [0, 0]

    def move_down(self):
        self.move(1, 0)
        self.current_matrix_position_in_board[0] += 1

    def move_right(self):
        self.move(0, 1)
        self.current_matrix_position_in_board[1] += 1

    def move_left(self):
        self.move(0, -1)
        self.current_matrix_position_in_board[1] -= 1

    def move(self, x, y):
        for block in self.blocks:
            block.move(x, y)

    def init_matrix_position(self, board_size):
        matrix_width = 4
        self.current_matrix_position_in_board = [0, math.floor(board_size / 2) - math.floor(matrix_width / 2)]

    def get_next_rotated_piece(self, current_rotation, pieces, current_piece_index):
        next_rotation = (current_rotation + 90) % 360
        next_rotated_piece = copy.deepcopy(pieces[current_piece_index][next_rotation])
        next_rotated_piece.current_matrix_position_in_board = self.current_matrix_position_in_board

        # Place next piece at the same position as the current piece
        for block in next_rotated_piece.blocks:
            block.x = block.x + next_rotated_piece.current_matrix_position_in_board[0]
            block.y = block.y + next_rotated_piece.current_matrix_position_in_board[1]
        return next_rotated_piece
