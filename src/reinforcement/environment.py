import copy

from src.game.tetrominos.piece import Piece
from src.reinforcement.agent import clear_console, ACTIONS, LEFT, RIGHT, ROTATE, NONE

EMPTY_BLOCK = 0
CURRENT_PIECE_BLOCK = 1
WALL = 2


class TetrisEnvironment:
    def __init__(self, height, width, pieces):
        self.__height = height
        self.__width = width
        self.__pieces = pieces
        self.__board = [[EMPTY_BLOCK for _ in range(width)] for _ in range(height)]
        self.__states = {}

        self.__current_bag_piece_index = list()
        self.__current_piece_index = None
        self.__current_piece = None
        self.__current_rotation = None
        self.__reward_clear_line = 100

    def get_lowest_x_for_states_by_current_piece(self):
        x = 0
        for block in self.get_current_piece().blocks:
            if x > block.x:
                x = block.x
        return x

    def update_states_for_current_board(self):
        # Add next 3 lines (without edges) to the states
        states_first_line_x_coordinate = self.get_lowest_x_for_states_by_current_piece()
        for x in range(states_first_line_x_coordinate, states_first_line_x_coordinate + 3):
            if x < len(self.__board):
                for y in range(1, len(self.__board[x])):
                    board_value = self.__board[x][y]
                    if board_value == EMPTY_BLOCK:
                        self.__states[x, y] = EMPTY_BLOCK
                    else:
                        self.__states[x, y] = WALL

        # Add current pieces to the states
        for block in self.get_current_piece().blocks:
            self.__states[block.x, block.y] = CURRENT_PIECE_BLOCK

    def reset(self, height, width):
        """Resets the game and returns the current state"""
        self.__height = height
        self.__width = width
        self.__board = [[EMPTY_BLOCK for _ in range(width)] for _ in range(height)]
        # Fill the board with pieces
        # for i in range(5, self.__height):
        #     for j in range(0, self.__width):
        #         rand = random.randint(0, 3)
        #         if rand == 1 or rand == 2:
        #             self.__board[i][j] = random.randint(0, 7)
        #         else:
        #             self.__board[i][j] = 0

        self.__current_bag_piece_index = list()
        self.__current_piece_index = None
        self.__current_piece = None
        self.__current_rotation = 0

        self.new_round()

        self.__states = {}  # Use as a radar for 3 lines under the current piece
        self.update_states_for_current_board()

    def new_round(self):
        """Starts a new round with a new piece and renew the bag of pieces if needed"""
        self.create_shuffled_bag()
        self.next_piece()
        self.place_piece_at_base_position(self.__current_piece)
        self.place_piece_in_board(self.__current_piece)

    def print_board(self):
        clear_console()
        print("Board state is : ")
        for row in self.__board:
            print(row)

    @property
    def board(self):
        return self.__board

    @property
    def states(self):
        return self.__states

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
        return self.__current_piece_index

    @property
    def current_rotation(self):
        return self.__current_rotation

    def get_current_piece(self) -> Piece:
        return self.__current_piece

    def set_current_piece(self, piece):
        self.__current_piece = piece

    def next_piece(self):
        """Get the next piece"""
        if len(self.__current_bag_piece_index) == 0:
            self.create_shuffled_bag()
        self.__current_piece_index = self.__current_bag_piece_index.pop()
        current_piece = copy.deepcopy(self.__pieces[self.current_piece_index][0])
        self.set_current_piece(current_piece)
        return self.get_current_piece()

    def create_shuffled_bag(self):
        """Create a queue of shuffled pieces"""
        piece_indexes_bag = list(range(1, len(self.__pieces) + 1))
        # self.__current_bag_piece_index = random.sample(piece_indexes_bag, len(piece_indexes_bag))
        self.__current_bag_piece_index = piece_indexes_bag

    def place_piece_in_board(self, piece: Piece):
        """Place the piece in the board"""
        for block in piece.blocks:
            self.__board[block.x][block.y] = piece.grid_representation
        self.update_states_for_current_board()

    def place_piece_at_base_position(self, piece: Piece):
        """Place a piece on the board"""
        piece.init_matrix_position(self.width)
        for block in piece.blocks:
            block.x = block.x
            block.y = block.y + piece.current_matrix_position_in_board[1]
            self.__board[block.x][block.y] = piece.grid_representation
        self.update_states_for_current_board()

    @staticmethod
    def is_touching_itself(piece, x, y) -> bool:
        """Checks if the piece collides with itself"""
        next_piece_position = (x, y)
        piece_block_positions = map(lambda block: (block.x, block.y), piece.blocks)
        if next_piece_position in piece_block_positions:
            return True

        return False

    def get_board_without_current_piece(self, current_piece):
        """Returns a copy of the board without the current piece"""
        board_without_current_piece = copy.deepcopy(self.__board)
        for block in current_piece.blocks:
            if 0 <= block.x < len(board_without_current_piece):
                if 0 <= block.y < len(board_without_current_piece[block.x]):
                    board_without_current_piece[block.x][block.y] = EMPTY_BLOCK
        return board_without_current_piece

    def entering_in_collision(self, next_piece_position, down, left, right,
                              previous_rotated_piece: Piece = None) -> bool:
        """Checks if the piece collides with pieces in current board"""
        for block in next_piece_position.blocks:  # y => row, x => column
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

            simulated_board_without_current_pieces = self.get_board_without_current_piece(
                previous_rotated_piece if previous_rotated_piece else next_piece_position)
            simulated_next_position_value = simulated_board_without_current_pieces[x][y]
            if simulated_next_position_value != EMPTY_BLOCK:
                return True

        return False

    def move_down(self, piece: Piece):
        """Move the piece down"""
        for block in piece.blocks:
            self.__board[block.x][block.y] = EMPTY_BLOCK
        piece.move_down()
        self.set_current_piece(piece)
        self.place_piece_in_board(self.get_current_piece())

    def move_left(self, piece: Piece):
        """Move the piece left"""
        for block in piece.blocks:
            self.__board[block.x][block.y] = EMPTY_BLOCK
        piece.move_left()
        self.set_current_piece(piece)
        self.place_piece_in_board(self.get_current_piece())

    def move_right(self, piece: Piece):
        """Move the piece right"""
        for block in piece.blocks:
            self.__board[block.x][block.y] = EMPTY_BLOCK
        piece.move_right()
        self.set_current_piece(piece)
        self.place_piece_in_board(self.get_current_piece())

    def rotate(self, previous_piece, next_rotated_piece: Piece) -> Piece:
        """Rotate the piece"""
        self.__current_rotation = next_rotated_piece.rotation
        for block in previous_piece.blocks:
            self.__board[block.x][block.y] = EMPTY_BLOCK

        for block in next_rotated_piece.blocks:
            self.__board[block.x][block.y] = next_rotated_piece.grid_representation

        self.set_current_piece(next_rotated_piece)
        return self.get_current_piece()

    def clear_lines(self) -> int:
        """Clears the lines"""
        line_clear_count = 0
        for row in self.__board:
            if all(block != EMPTY_BLOCK for block in row):
                self.__board.remove(row)
                self.__board.insert(0, [EMPTY_BLOCK] * self.__width)
                line_clear_count += 1
        return line_clear_count

    def safe_move_left(self, current_piece: Piece) -> bool:
        """Move left if possible"""
        if self.entering_in_collision(current_piece, False, True, False) is False:
            self.move_left(current_piece)
            return True
        return False

    def safe_move_right(self, current_piece: Piece) -> bool:
        """Move right if possible"""
        if self.entering_in_collision(current_piece, False, False, True) is False:
            self.move_right(current_piece)
            return True
        return False

    def safe_rotate(self, current_piece: Piece) -> Piece:
        """Rotate if possible"""
        next_rotated_piece = current_piece.get_next_rotated_piece(self.current_rotation,
                                                                  self.pieces,
                                                                  self.current_piece_index)
        if self.entering_in_collision(next_rotated_piece, False, False, False, current_piece) is False:
            return self.rotate(current_piece, next_rotated_piece)
        return current_piece

    def compute_line_cleared_reward(self, cleared_lines_count):
        if cleared_lines_count == 1:
                return 100
        elif cleared_lines_count == 2:
            return 300
        elif cleared_lines_count == 3:
            return 500
        elif cleared_lines_count == 4:
            return 800
        elif cleared_lines_count > 4:
            return 1500
        return 0

    def compute_rewards(self, cleared_lines_count):
        rewards = 0
        rewards += self.compute_line_cleared_reward(cleared_lines_count)
        return rewards

    def do(self, action: ACTIONS):
        current_piece = self.get_current_piece()
        if action == LEFT:
            self.safe_move_left(current_piece)
        elif action == RIGHT:
            self.safe_move_right(current_piece)
        elif action == ROTATE:
            current_piece = self.safe_rotate(current_piece)
        elif action == NONE:
            pass

        rewards = 0
        if self.entering_in_collision(current_piece, True, False, False) is True:
            # The more lines cleared, the more reward
            for row in self.__board:
                if all(block != EMPTY_BLOCK for block in row):
                    rewards += self.__reward_clear_line
            # The height of the current piece reward
            rewards = sum([block.x for block in current_piece.blocks]) - ((self.__height - 1) * 2)

        return current_piece, rewards
