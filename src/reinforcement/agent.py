import os
import pickle
from random import choice, random

from src.game.tetrominos.piece import Piece

LEFT = 'L'
RIGHT = 'R'
ROTATE = 'U'
NONE = 'N'
ACTIONS = {
    LEFT: 'L',
    RIGHT: 'R',
    ROTATE: 'U',
    NONE: 'N',
}


def clear_console():
    """Clear console"""
    os.system('cls' if os.name == 'nt' else 'clear')

class Agent:
    def __init__(self, environment, alpha=1, gamma=1, exploration=0, cooling_rate=0.99):
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
        q0 = self.__qtable.get(self.__state, None)  # Get the qtable for the current state
        if q0 is None:
            self.__qtable[self.__state] = {}
            for action in ACTIONS.values():
                if self.__qtable[self.__state].get(action, None) is None:
                    self.__qtable[self.__state][action] = 0.0
            q0 = self.__qtable[self.__state]

        if random() < self.__exploration:
            self.__exploration *= self.__cooling_rate
            return choice(list(ACTIONS.values()))

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
    def score(self):
        return self.__score

    @property
    def exploration(self):
        return self.__exploration

    @property
    def history(self):
        return self.__history

    def load(self, filename):
        with open(filename, 'rb') as file:
            try:
                self.__qtable, self.__history = pickle.load(file)
            except EOFError:
                print("/!\\ The file is empty")
            except Exception as e:
                print(f"/!\\ Error while loading the file : {e}")

            file.close()

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.__qtable, self.__history), file)
            file.close()

    def safe_move_down(self, current_piece: Piece) -> bool:
        """Move down if possible"""
        if self.__environment.entering_in_collision(current_piece, True, False, False) is False:
            self.__environment.move_down(current_piece)
            return True
        # print(f"Has entered in collision at score {self.__score}")
        return False

    def print_board_if_needed(self, should_display_board):
        if should_display_board:
            self.__environment.print_board()

    def update_current_state(self):
        # The current state is the hash of :
        #   - The current piece (piece and rotation)
        #   - The radar under the current piece
        #   - The y position of the current piece on the board
        current_piece_blocks = [(block.x - self.__environment.get_current_piece().current_matrix_position_in_board[0],
                                 block.y - self.__environment.get_current_piece().current_matrix_position_in_board[1])
                                for block in self.__environment.get_current_piece().blocks]
        radar = [value for value in self.__environment.states.values()]
        ys = [block.y for block in self.__environment.get_current_piece().blocks]

        self.__state = hash((tuple(current_piece_blocks), tuple(radar), tuple(ys)))

    def update_qtable(self, action, rewards):
        # 𝑄(𝑠t,𝑎t) ⟵ 𝑄(𝑠t,𝑎t) + 𝛼[𝑟+1 + 𝛾𝑄(𝑠t+1, 𝑎t+1) − 𝑄(𝑠t,𝑎t)]

        maxQ = max(self.__qtable[self.__state].values())
        delta = self.__alpha * (rewards + self.__gamma * maxQ - self.__qtable[self.__state][action])
        self.__qtable[self.__state][action] += delta

    def set_current_piece(self, current_piece):
        self.__environment.set_current_piece(current_piece)

    def get_current_piece(self):
        return self.__environment.get_current_piece()

    def step(self):
        """Do a step"""
        # TODO -> Implement reinforcement learning
        # TODO      -> Implement Q-learning
        # OR
        # TODO      -> Implement Neural Network
        # TODO      -> BEST OPTION -> BOTH
        action = None
        rewards = 0

        for movement in range(10):
            self.update_current_state()
            action = self.best_action()
            current_piece, rewards = self.__environment.do(action)
            self.__score += rewards
            self.set_current_piece(current_piece)
            if self.__environment.entering_in_collision(current_piece, True, False, False) is True:
                break

        if self.safe_move_down(self.get_current_piece()) is False:
            # print("Q-table value : ", self.__qtable[self.__state])
            self.update_qtable(action, rewards)
            self.__environment.clear_lines()

            self.__environment.next_piece()
            self.__environment.place_piece_at_base_position(self.get_current_piece())

            if self.__environment.entering_in_collision(self.get_current_piece(), down=False, left=False, right=False,
                                                        without_current_piece=False) is True:
                self.is_over = True
                return
            self.__environment.place_piece_in_board(self.get_current_piece())
