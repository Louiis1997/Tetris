import os
import random

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

    def print_board_if_needed(self, should_display_board):
        if should_display_board:
            self.__environment.print_board()

    def step(self):
        """Do a step"""
        # TODO -> Implement reinforcement learning
        # TODO      -> Implement Q-learning
        # OR
        # TODO      -> Implement Neural Network
        # TODO      -> BEST OPTION -> BOTH

        current_piece = self.__environment.do()

        if self.safe_move_down(current_piece) is False:
            self.__environment.add_piece_to_wall()
            self.__environment.clear_lines()
            current_piece = self.__environment.next_piece()
            self.__environment.place_piece_at_base_position(current_piece)
            if self.__environment.entering_in_collision(current_piece, True, False, False) is True:
                self.is_over = True
            return
