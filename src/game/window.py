import time

import arcade

from src.reinforcement.environment import EMPTY_BLOCK

SPRITE_SIZE = 40


class TetrisWindow(arcade.Window):
    def __init__(self, agent):
        super().__init__(agent.environment.width * (SPRITE_SIZE * 1.25), agent.environment.height * (SPRITE_SIZE * 1.1),
                         'Tetris')

        self.__agent = agent
        self.__iteration = 1

        self.__board = None

        self.set_update_rate(1 / 10)

    def setup(self):
        # Set background color
        arcade.set_background_color(arcade.color.BLACK)

        self.__board = arcade.SpriteList()

        for rows in range(len(self.__agent.environment.board)):
            for columns in range(len(self.__agent.environment.board[rows])):
                # Create block sprite using its color
                # Create rounded border blocks
                sprite_border = arcade.SpriteSolidColor(SPRITE_SIZE, SPRITE_SIZE, arcade.color.BLACK)
                sprite = arcade.SpriteSolidColor(SPRITE_SIZE - 1, SPRITE_SIZE - 1, arcade.color.COBALT)
                sprite_border.center_x, sprite_border.center_y = self.state_to_xy((rows, columns))
                sprite.center_x, sprite.center_y = self.state_to_xy((rows, columns))
                self.__board.append(sprite_border)
                self.__board.append(sprite)

        self.__agent.reset()

    def block_to_xy(self, block):
        return (block.y + 0.5 * 3.5) * SPRITE_SIZE, \
               (self.__agent.environment.height - block.x - 0.5 * -2) * SPRITE_SIZE

    def state_to_xy(self, state):
        return (state[1] + 0.5 * 3.5) * SPRITE_SIZE, \
               (self.__agent.environment.height - state[0] - 0.5 * -2) * SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()

        self.__board.draw()
        self.draw_grid(self.__agent.environment.board)

        arcade.draw_text(
            f"#{self.__iteration:04d} Score : {self.__agent.score:.2f} T°C : {self.__agent.exploration:.2f}",
            10, 10, arcade.csscolor.WHITE, 20)

    def on_update(self, delta_time):
        if not self.__agent.is_over:
            self.__agent.step()
            # Make program sleep for 1 second
            time.sleep(0.1)
        else:
            self.__agent.reset()
            self.__iteration += 1

    def get_color_from_grid_representation(self, grid_representation):
        """ Get the color of a grid representation. """
        if grid_representation == EMPTY_BLOCK:
            return arcade.color.COBALT
        return self.__agent.environment.pieces[grid_representation][0].blocks[0].color

    def draw_grid(self, grid):
        """ Draw the grid. Used to draw the falling stones. The board is drawn by the sprite list. """
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                # Figure out what color to draw the box
                color = self.get_color_from_grid_representation(grid[row][column])

                sprite_border = arcade.SpriteSolidColor(SPRITE_SIZE, SPRITE_SIZE, arcade.color.BLACK)
                sprite = arcade.SpriteSolidColor(SPRITE_SIZE - 1, SPRITE_SIZE - 1, color)
                sprite_border.center_x, sprite_border.center_y = self.state_to_xy((row, column))
                sprite.center_x, sprite.center_y = self.state_to_xy((row, column))
                self.__board.append(sprite_border)
                self.__board.append(sprite)
