import os
import random

from src.game.tetrominos.piece import Piece

ACTION_LEFT = 'L'
ACTION_RIGHT = 'R'
ACTION_ROTATE = 'U'
ACTION_NONE = 'N'
ACTIONS = [ACTION_LEFT, ACTION_RIGHT, ACTION_ROTATE, ACTION_NONE]


def clear_console():
    """Clear console"""
    os.system('cls' if os.name == 'nt' else 'clear')


class Agent:
    def __init__(self, environment, alpha=1E-2, gamma=1, exploration=0, cooling_rate=0.99):
        self.__environment = environment
        self.reset(False)
        self.__qtable = {}
        for state in environment.states:
            self.__qtable[state] = {}
            for action in ACTIONS:
                self.__qtable[state][action] = 0.0
        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate

        self.__history = []
        self.__state = None
        self.__state0 = None
        self.__state1 = None
        self.__state2 = None
        self.__state3 = None
        self.__score = 0

        self.is_over = False

    def best_action(self):
        q0 = self.__qtable[self.__state0]
        q1 = self.__qtable[self.__state1]
        q2 = self.__qtable[self.__state2]
        q3 = self.__qtable[self.__state3]
        max_q0 = max(q0, key=q0.get)
        max_q1 = max(q1, key=q1.get)
        max_q2 = max(q2, key=q2.get)
        max_q3 = max(q3, key=q3.get)
        return max(max_q0, max_q1, max_q2, max_q3)

    def reset(self, append_score=True):
        if append_score:
            self.__history.append(self.__score)
        self.__state = None
        self.__state0 = None
        self.__state1 = None
        self.__state2 = None
        self.__state3 = None
        self.__score = 0
        self.is_over = False
        self.__environment.reset(self.__environment.height, self.__environment.width)

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

    def step(self):
        """Do a step"""
        # TODO -> Implement reinforcement learning
        # TODO      -> Implement Q-learning
        # OR
        # TODO      -> Implement Neural Network
        # TODO      -> BEST OPTION -> BOTH
        self.__state0 = (self.__environment.get_current_piece().blocks[0].x,
                         self.__environment.get_current_piece().blocks[0].y)
        self.__state1 = (self.__environment.get_current_piece().blocks[1].x,
                         self.__environment.get_current_piece().blocks[1].y)
        self.__state2 = (self.__environment.get_current_piece().blocks[2].x,
                         self.__environment.get_current_piece().blocks[2].y)
        self.__state3 = (self.__environment.get_current_piece().blocks[3].x,
                         self.__environment.get_current_piece().blocks[3].y)
        '''self.__state = (self.__state0, self.__state1, self.__state2, self.__state3)

        if random.random() < self.__exploration:
            action = random.choice(ACTIONS)
        else:
            action = self.best_action()

        if action == ACTION_LEFT:
            self.__environment.move_left(self.__environment.get_current_piece())
        elif action == ACTION_RIGHT:
            self.__environment.move_right(self.__environment.get_current_piece())
        elif action == ACTION_ROTATE:
            self.__environment.rotate(self.__environment.get_current_piece())
        elif action == ACTION_NONE:
            pass
        else:
            raise ValueError(f"Unknown action {action}")

        reward = 0
        if self.safe_move_down(self.__environment.get_current_piece()) is False:
            reward = -1
            self.is_over = True
            self.__environment.add_piece(self.__environment.get_current_piece())
            self.__environment.remove_full_lines()
            self.__environment.generate_new_piece()
            self.__environment.print_board()
            self.__exploration *= self.__cooling_rate
            self.reset()

        maxQ = max(self.__qtable[self.__state].values())
        delta = self.__alpha * (reward + self.__gamma * maxQ - self.__qtable[self.__state][action])
        self.__qtable[self.__state][action] += delta

        self.__score += reward

        return action, reward'''
        action = self.best_action()
        current_piece, reward = self.__environment.do(action)

        if self.safe_move_down(current_piece) is False:
            self.__environment.add_piece_to_wall()
            self.__environment.clear_lines()
            current_piece = self.__environment.next_piece()
            self.__environment.place_piece_at_base_position(current_piece)
            if self.__environment.entering_in_collision(current_piece, True, False, False) is True:
                self.is_over = True
            return
