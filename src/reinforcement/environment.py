import copy
import math

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
        self.__radar_states_1 = {}

        self.__current_bag_piece_index = list()
        self.__current_piece_index = None
        self.__current_piece = None
        self.__current_rotation = None
        self.__clear_line_reward_weight = 200
        self.__avg_column_heights_reward_weight = -5
        self.__reward_piece_height = 1
        self.__bumpiness_reward_weight = -1
        self.__quadratic_bumpiness_reward_weight = 2
        self.__holes_reward_weight = -16
        self.__reward_new_holes = -30

    def get_lowest_x_for_states_by_current_piece(self):
        x = 0
        for block in self.get_current_piece().blocks:
            if x > block.x:
                x = block.x
        return x

    def fill_radar_states_with_board(self, radar_states, current_x, radar_y_start, radar_y_end):
        """Fill the radar states with the current board"""
        """Update the radar with the current board"""
        for y in range(radar_y_start, radar_y_end):
            if y < 0 or y >= len(self.__board[current_x]):
                radar_states[current_x, y] = WALL
            else:
                radar_states[current_x, y] = WALL if self.__board[current_x][y] != EMPTY_BLOCK else EMPTY_BLOCK

    def update_states_for_current_board(self, current_piece=None):
        """Update the radar for the current board"""
        if current_piece is None:
            return

        radar_width = 3
        radar_height = 3

        left_overflow = radar_width

        states_first_line_x_coordinate = self.get_lowest_x_for_states_by_current_piece()
        for x in range(states_first_line_x_coordinate, states_first_line_x_coordinate + radar_height):
            # 10 * 28 * 2^(3*3) * 3
            if x > len(self.__board):
                self.__radar_states_1[x] = [WALL for _ in range(radar_width)]
                continue

            radar_1_y_start = current_piece.current_matrix_position_in_board[1] - left_overflow
            radar_1_y_end = radar_1_y_start + (radar_width - 1)

            self.fill_radar_states_with_board(self.__radar_states_1, x, radar_1_y_start, radar_1_y_end)

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

        self.__radar_states_1 = {}
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
    def states_1(self):
        return self.__radar_states_1

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
        self.update_states_for_current_board(piece)

    def place_piece_at_base_position(self, piece: Piece):
        """Place a piece on the board"""
        piece.init_matrix_position(self.width)
        for block in piece.blocks:
            block.x = block.x
            block.y = block.y + piece.current_matrix_position_in_board[1]

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
                              previous_rotated_piece: Piece = None, without_current_piece: bool = True) -> bool:
        """Checks if the piece collides with pieces in current board"""
        for block in next_piece_position.blocks:  # y => row, x => column
            x = block.x + 1 if down else block.x
            y = block.y + 1 if right else (block.y - 1 if left else block.y)

            if x >= self.__height:
                # print("Collision detected -> down -> touched the bottom")
                return True

            if y >= self.__width:
                # print("Collision detected -> right -> touched the right wall")
                return True

            if y < 0:
                # print("Collision detected -> left -> touched the left wall")
                return True

            if without_current_piece:
                board = self.get_board_without_current_piece(
                    previous_rotated_piece if previous_rotated_piece else next_piece_position)
            else:
                board = self.__board
            simulated_next_position_value = board[x][y]
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

    def compute_line_cleared_reward(self):
        line_cleared = 0
        # The more lines cleared, the more reward
        for index, row in enumerate(self.__board):
            if all(block != EMPTY_BLOCK for block in row):
                line_cleared += 1 * (index + 1)  # To round index 19 to 20 for example
        # The height of the current piece reward
        return line_cleared * self.__clear_line_reward_weight

    def compute_avg_column_heights_reward(self):
        column_heights = 0
        for column in range(self.width):
            for row in range(self.height):
                if self.__board[row][column] != EMPTY_BLOCK:
                    column_heights += self.height - row
                    break
        avg_column_heights = column_heights / self.width
        return avg_column_heights * self.__avg_column_heights_reward_weight

    def get_column_height(self, col, board):
        """Returns the height of the given column"""
        height = 0
        for row in range(self.__height):
            if board[row][col] != EMPTY_BLOCK:
                height = self.__height - row
                break
        return height

    def get_current_bumpiness(self):
        """Sum of the absolute differences between the heights of adjacent columns"""
        total_bumpiness = 0

        for col in range(self.__width - 1):
            bumpiness = abs(self.get_column_height(col, self.__board) - self.get_column_height(col + 1, self.__board))
            total_bumpiness += (bumpiness ** self.__quadratic_bumpiness_reward_weight)

        return total_bumpiness

    def compute_bumpiness_reward(self):
        bumpiness = self.get_current_bumpiness()
        return bumpiness * self.__bumpiness_reward_weight

    def compute_piece_height_reward(self):
        return math.floor(
            sum([(block.x - self.height) for block in
                 self.get_current_piece().blocks]) * self.__reward_piece_height)

    def get_old_holes_count(self):
        old_board = self.get_board_without_current_piece(self.get_current_piece())
        return self.get_holes_count(old_board)

    def get_holes_count(self, board):
        """Returns the number of holes in the board (meaning empty spaces that are underneath at least one block)"""
        holes = 0

        # Iterate on each cell of the board by column, from top to bottom and left to right
        for col in range(self.__width):
            found_block = False
            for row in range(self.__height):
                # If a block is found, then the next empty spaces are holes
                if board[row][col] != EMPTY_BLOCK:
                    found_block = True
                elif found_block and board[row][col] == EMPTY_BLOCK:
                    holes += 1

        return holes

    def get_new_holes_count(self):
        old_holes_count = self.get_old_holes_count()
        current_holes_count = self.get_holes_count(self.__board)
        return current_holes_count - old_holes_count

    def compute_holes_reward(self):
        return self.__reward_new_holes * self.get_new_holes_count()

    def get_number_of_blocks_on_the_board(self):
        """Returns the number of blocks in the board"""
        blocks = 0
        for row in range(self.__height):
            for col in range(self.__width):
                if self.board[row][col] != EMPTY_BLOCK:
                    blocks += 1
        return blocks

    def compute_rewards(self):
        rewards = 0

        line_cleared_reward = self.compute_line_cleared_reward()
        # print("line_cleared_reward: ", line_cleared_reward)
        rewards += line_cleared_reward

        piece_height_reward = self.compute_piece_height_reward()
        # print("piece_height_reward: ", piece_height_reward)
        rewards += piece_height_reward

        # avg_column_heights_reward = self.compute_avg_column_heights_reward()
        # print("avg_column_heights_reward: ", avg_column_heights_reward)
        # rewards += avg_column_heights_reward

        holes_reward = self.compute_holes_reward()
        # print("holes_reward: ", holes_reward)
        rewards += holes_reward

        bumpiness_reward = self.compute_bumpiness_reward()
        # print("bumpiness_reward: ", bumpiness_reward)
        rewards += bumpiness_reward

        return rewards / (self.get_number_of_blocks_on_the_board() / 4)

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
            rewards += self.compute_rewards()

        return current_piece, rewards
