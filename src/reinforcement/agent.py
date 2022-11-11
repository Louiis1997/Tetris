import copy
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
        print(f"Has entered in collision at score {self.__score}")
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


    def step(self):
        """Do a step"""
        current_piece = self.__environment.get_current_piece()[0]
        clear_console()
        self.__environment.print_board()

        if self.safe_move_down(current_piece) is False:
            self.__environment.add_piece_to_wall()
            current_piece = self.__environment.next_piece()[0]
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
