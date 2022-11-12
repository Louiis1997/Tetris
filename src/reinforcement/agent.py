import os
import random
from random import *

from src.game.tetrominos.piece import Piece

LEFT = 'L'
RIGHT = 'R'
ROTATE = 'U'
NONE = 'N'
ACTIONS = [
    LEFT,
    RIGHT,
    ROTATE,
    NONE
]


def clear_console():
    """Clear console"""
    os.system('cls' if os.name == 'nt' else 'clear')


class Agent:
    def __init__(self, environment, alpha=1E-2, gamma=1, exploration=0, cooling_rate=0.99):
        self.__environment = environment
        self.reset(False)
        self.__qtable = {}
        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate

        self.__history = []
        self.__state = None
        self.__score = 0

        self.is_over = False

    def best_action(self):
        if random() < self.__exploration:
            self.__exploration *= self.__cooling_rate
            return choice(ACTIONS)
        else:
            q0 = self.__qtable.get(self.__state, {})  # Get the qtable for the current state
            max_q = max(q0, key=q0.get) if len(q0) > 0 else 0  # Get the max q value for the current state
            return max_q

    def reset(self, append_score=True):
        if append_score:
            self.__history.append(self.__score)
        self.__state = None
        self.__score = 0
        self.is_over = False
        self.__environment.reset(self.__environment.height, self.__environment.width)

    def heat(self):
        self.__exploration = 1

    @property
    def environment(self):
        return self.__environment

    @property
    def state(self):
        return self.__state

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

    def get_exploration(self):
        return self.__exploration

    def get_state(self):
        # The current state is the hash of :
        #   - The current piece (piece and rotation)
        #   - The radar under the current piece
        #   - The y position of the current piece on the board
        current_piece = self.__environment.get_current_piece()
        radar = self.__environment.states
        ys = [block.y for block in current_piece.blocks]

        return hash((current_piece, tuple(radar), tuple(ys)))

    def update_qtable(self, action, rewards):
        # 𝑄(𝑠t,𝑎t) ⟵ 𝑄(𝑠t,𝑎t) + 𝛼[𝑟+1 + 𝛾𝑄(𝑠t+1, 𝑎t+1) − 𝑄(𝑠t,𝑎t)]
        if self.__qtable.get(self.__state, 0) == 0:
            self.__qtable[self.__state] = {}
            for a in ACTIONS:
                self.__qtable[self.__state][a] = 0.0
            self.__qtable[self.__state][action] = 0.0

        maxQ = max(self.__qtable[self.__state].values())
        delta = self.__alpha * (rewards + self.__gamma * maxQ - self.__qtable[self.__state][action])
        self.__qtable[self.__state][action] += delta

    def step(self):
        """Do a step"""
        # TODO -> Implement reinforcement learning
        # TODO      -> Implement Q-learning
        # OR
        # TODO      -> Implement Neural Network
        # TODO      -> BEST OPTION -> BOTH
        self.__state = self.get_state()

        action = self.best_action()
        current_piece, rewards = self.__environment.do(action)
        self.__environment.__current_piece = current_piece
        self.update_qtable(action, rewards)

        if self.safe_move_down(current_piece) is False:
            self.__environment.clear_lines()

            current_piece = self.__environment.next_piece()
            self.__environment.place_piece_at_base_position(current_piece)
            if self.__environment.entering_in_collision(current_piece, True, False, False) is True:
                self.is_over = True
            return
