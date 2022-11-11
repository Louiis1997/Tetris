import copy
import os
import random
import time

from src.game.tetrominos.piece import Piece


def clear_console():
    """Clear console"""
    os.system('cls' if os.name == 'nt' else 'clear')


class Agent:

    def __init__(self, environment, alpha=1E-2, gamma=1, exploration=0, cooling_rate=0.99):
        self.__environment = environment
        self.reset(False)

        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate

        self.__history = []
        self.__state = None
        self.__score = 0

        self.is_over = False

    def reset(self, append_score=True):
        if append_score:
            self.__history.append(self.__score)
        self.__state = None
        self.__score = 0
        self.is_over = False
        self.__environment.reset(self.__environment.height, self.__environment.width)

    @property
    def environment(self):
        return self.__environment

    @property
    def score(self):
        return self.__score

    @property
    def exploration(self):
        return self.__exploration

    def safe_move_down(self, current_piece: Piece) -> bool:
        """Move down if possible"""
        if self.__environment.entering_in_collision(current_piece, True, False, False) is False:
            self.__environment.move_down(current_piece)
            self.__score += 1
            return True
        # print(f"Has entered in collision at score {self.__score}")
        return False

    def safe_move_left(self, current_piece: Piece) -> bool:
        """Move left if possible"""
        if self.__environment.entering_in_collision(current_piece, False, True, False) is False:
            self.__environment.move_left(current_piece)
            return True
        return False

    def safe_move_right(self, current_piece: Piece) -> bool:
        """Move right if possible"""
        if self.__environment.entering_in_collision(current_piece, False, False, True) is False:
            self.__environment.move_right(current_piece)
            return True
        return False

    def safe_rotate(self, current_piece: Piece) -> Piece:
        """Rotate if possible"""
        next_rotated_piece = current_piece.get_next_rotated_piece(self.environment.current_rotation,
                                                                  self.environment.pieces,
                                                                  self.environment.current_piece_index)
        if self.__environment.entering_in_collision(next_rotated_piece, False, False, False, current_piece) is False:
            return self.__environment.rotate(current_piece, next_rotated_piece)
        return current_piece

    def print_board_if_needed(self, should_display_board):
        if should_display_board:
            self.__environment.print_board()

    def step(self):
        """Do a step"""
        current_piece = self.__environment.get_current_piece()

        current_piece = self.safe_rotate(current_piece)  # TODO -> FIX

        if self.safe_move_down(current_piece) is False:
            self.__environment.clear_lines()

            current_piece = self.__environment.next_piece()
            self.__environment.place_piece_at_base_position(current_piece)
            if self.__environment.entering_in_collision(current_piece, True, False, False) is True:
                self.is_over = True
            return

        # Make a random move for now
        # TODO -> Implement reinforcement learning
        # TODO      -> Implement Q-learning
        # OR
        # TODO      -> Implement Neural Network
        # TODO      -> BEST OPTION -> BOTH
        left_or_right = random.randint(0, 1)
        number_of_times = random.randint(1, 6)
        for _ in range(number_of_times):
            if left_or_right == 0:
                self.safe_move_left(current_piece)
            else:
                for _ in range(number_of_times):
                    self.safe_move_right(current_piece)
