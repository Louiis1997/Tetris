import arcade

from src.game.tetrominos.block import Block
from src.game.tetrominos.piece import Piece


class TetrominosFactory:

    @staticmethod
    def create_tetrominos():
        return {
            1: TetrominosFactory.create_I_tetrominos(1),
            2: TetrominosFactory.create_T_tetrominos(2),
            3: TetrominosFactory.create_L_tetrominos(3),
            4: TetrominosFactory.create_J_tetrominos(4),
            5: TetrominosFactory.create_Z_tetrominos(5),
            6: TetrominosFactory.create_S_tetrominos(6),
            7: TetrominosFactory.create_O_tetrominos(7),
        }

    @staticmethod
    def create_I_tetrominos(grid_representation):
        return {
            0: Piece(
                [
                    Block(0, 0, arcade.color.ELECTRIC_CYAN),
                    Block(1, 0, arcade.color.ELECTRIC_CYAN),
                    Block(2, 0, arcade.color.ELECTRIC_CYAN),
                    Block(3, 0, arcade.color.ELECTRIC_CYAN),
                ],
                0,
                grid_representation
            ),
            90: Piece(
                [
                    Block(1, 0, arcade.color.ELECTRIC_CYAN),
                    Block(1, 1, arcade.color.ELECTRIC_CYAN),
                    Block(1, 2, arcade.color.ELECTRIC_CYAN),
                    Block(1, 3, arcade.color.ELECTRIC_CYAN),
                ],
                90,
                grid_representation
            ),
            180: Piece(
                [
                    Block(3, 0, arcade.color.ELECTRIC_CYAN),
                    Block(2, 0, arcade.color.ELECTRIC_CYAN),
                    Block(1, 0, arcade.color.ELECTRIC_CYAN),
                    Block(0, 0, arcade.color.ELECTRIC_CYAN),
                ],
                180,
                grid_representation
            ),
            270: Piece(
                [
                    Block(1, 3, arcade.color.ELECTRIC_CYAN),
                    Block(1, 2, arcade.color.ELECTRIC_CYAN),
                    Block(1, 1, arcade.color.ELECTRIC_CYAN),
                    Block(1, 0, arcade.color.ELECTRIC_CYAN),
                ],
                270,
                grid_representation
            ),
        }

    @staticmethod
    def create_T_tetrominos(grid_representation):
        return {
            0: Piece(
                [
                    Block(1, 0, arcade.color.ELECTRIC_VIOLET),
                    Block(0, 1, arcade.color.ELECTRIC_VIOLET),
                    Block(1, 1, arcade.color.ELECTRIC_VIOLET),
                    Block(2, 1, arcade.color.ELECTRIC_VIOLET),
                ],
                0,
                grid_representation
            ),
            90: Piece(
                [
                    Block(1, 0, arcade.color.ELECTRIC_VIOLET),
                    Block(1, 1, arcade.color.ELECTRIC_VIOLET),
                    Block(2, 1, arcade.color.ELECTRIC_VIOLET),
                    Block(1, 2, arcade.color.ELECTRIC_VIOLET),
                ],
                90,
                grid_representation
            ),
            180: Piece(
                [
                    Block(0, 1, arcade.color.ELECTRIC_VIOLET),
                    Block(1, 1, arcade.color.ELECTRIC_VIOLET),
                    Block(2, 1, arcade.color.ELECTRIC_VIOLET),
                    Block(1, 2, arcade.color.ELECTRIC_VIOLET),
                ],
                180,
                grid_representation
            ),
            270: Piece(
                [
                    Block(1, 0, arcade.color.ELECTRIC_VIOLET),
                    Block(0, 1, arcade.color.ELECTRIC_VIOLET),
                    Block(1, 1, arcade.color.ELECTRIC_VIOLET),
                    Block(1, 2, arcade.color.ELECTRIC_VIOLET),
                ],
                270,
                grid_representation
            ),
        }

    @staticmethod
    def create_L_tetrominos(grid_representation):
        return {
            0: Piece(
                [
                    Block(0, 0, arcade.color.FLAME),
                    Block(0, 1, arcade.color.FLAME),
                    Block(1, 1, arcade.color.FLAME),
                    Block(2, 1, arcade.color.FLAME),
                ],
                0,
                grid_representation
            ),
            90: Piece(
                [
                    Block(1, 0, arcade.color.FLAME),
                    Block(2, 0, arcade.color.FLAME),
                    Block(1, 1, arcade.color.FLAME),
                    Block(1, 2, arcade.color.FLAME),
                ],
                90,
                grid_representation
            ),
            180: Piece(
                [
                    Block(0, 1, arcade.color.FLAME),
                    Block(1, 1, arcade.color.FLAME),
                    Block(2, 1, arcade.color.FLAME),
                    Block(2, 2, arcade.color.FLAME),
                ],
                180,
                grid_representation
            ),
            270: Piece(
                [
                    Block(1, 0, arcade.color.FLAME),
                    Block(1, 1, arcade.color.FLAME),
                    Block(1, 2, arcade.color.FLAME),
                    Block(0, 2, arcade.color.FLAME),
                ],
                270,
                grid_representation
            ),
        }

    @staticmethod
    def create_J_tetrominos(grid_representation):
        return {
            0: Piece(
                [
                    Block(2, 0, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                    Block(0, 1, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                    Block(1, 1, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                    Block(2, 1, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                ],
                0,
                grid_representation
            ),
            90: Piece(
                [
                    Block(1, 0, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                    Block(1, 1, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                    Block(1, 2, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                    Block(2, 2, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                ],
                90,
                grid_representation
            ),
            180: Piece(
                [
                    Block(0, 1, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                    Block(1, 1, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                    Block(2, 1, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                    Block(0, 2, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                ],
                180,
                grid_representation
            ),
            270: Piece(
                [

                    Block(1, 1, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                    Block(2, 1, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                    Block(2, 2, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                    Block(2, 3, arcade.color.INTERNATIONAL_KLEIN_BLUE),
                ],
                270,
                grid_representation
            ),
        }

    @staticmethod
    def create_Z_tetrominos(grid_representation):
        return {
            0: Piece(
                [
                    Block(0, 0, arcade.color.MEDIUM_CANDY_APPLE_RED),
                    Block(1, 0, arcade.color.MEDIUM_CANDY_APPLE_RED),
                    Block(1, 1, arcade.color.MEDIUM_CANDY_APPLE_RED),
                    Block(2, 1, arcade.color.MEDIUM_CANDY_APPLE_RED),
                ],
                0,
                grid_representation
            ),
            90: Piece(
                [
                    Block(1, 0, arcade.color.MEDIUM_CANDY_APPLE_RED),
                    Block(1, 1, arcade.color.MEDIUM_CANDY_APPLE_RED),
                    Block(0, 1, arcade.color.MEDIUM_CANDY_APPLE_RED),
                    Block(0, 2, arcade.color.MEDIUM_CANDY_APPLE_RED),
                ],
                90,
                grid_representation
            ),
            180: Piece(
                [
                    Block(0, 0, arcade.color.MEDIUM_CANDY_APPLE_RED),
                    Block(1, 0, arcade.color.MEDIUM_CANDY_APPLE_RED),
                    Block(1, 1, arcade.color.MEDIUM_CANDY_APPLE_RED),
                    Block(2, 1, arcade.color.MEDIUM_CANDY_APPLE_RED),
                ],
                180,
                grid_representation
            ),
            270: Piece(
                [
                    Block(1, 0, arcade.color.MEDIUM_CANDY_APPLE_RED),
                    Block(1, 1, arcade.color.MEDIUM_CANDY_APPLE_RED),
                    Block(0, 1, arcade.color.MEDIUM_CANDY_APPLE_RED),
                    Block(0, 2, arcade.color.MEDIUM_CANDY_APPLE_RED),
                ],
                270,
                grid_representation
            ),
        }

    @staticmethod
    def create_S_tetrominos(grid_representation):
        return {
            0: Piece(
                [
                    Block(1, 0, arcade.color.MALACHITE),
                    Block(2, 0, arcade.color.MALACHITE),
                    Block(0, 1, arcade.color.MALACHITE),
                    Block(1, 1, arcade.color.MALACHITE),
                ],
                0,
                grid_representation
            ),
            90: Piece(
                [
                    Block(0, 0, arcade.color.MALACHITE),
                    Block(0, 1, arcade.color.MALACHITE),
                    Block(1, 1, arcade.color.MALACHITE),
                    Block(1, 2, arcade.color.MALACHITE),
                ],
                90,
                grid_representation
            ),
            180: Piece(
                [
                    Block(1, 0, arcade.color.MALACHITE),
                    Block(2, 0, arcade.color.MALACHITE),
                    Block(0, 1, arcade.color.MALACHITE),
                    Block(1, 1, arcade.color.MALACHITE),
                ],
                180,
                grid_representation
            ),
            270: Piece(
                [
                    Block(0, 0, arcade.color.MALACHITE),
                    Block(0, 1, arcade.color.MALACHITE),
                    Block(1, 1, arcade.color.MALACHITE),
                    Block(1, 2, arcade.color.MALACHITE),
                ],
                270,
                grid_representation
            ),
        }

    @staticmethod
    def create_O_tetrominos(grid_representation):
        return {
            0: Piece(
                [
                    Block(0, 0, arcade.color.MELLOW_YELLOW),
                    Block(1, 0, arcade.color.MELLOW_YELLOW),
                    Block(0, 1, arcade.color.MELLOW_YELLOW),
                    Block(1, 1, arcade.color.MELLOW_YELLOW),
                ],
                0,
                grid_representation
            ),
            90: Piece(
                [
                    Block(0, 0, arcade.color.MELLOW_YELLOW),
                    Block(1, 0, arcade.color.MELLOW_YELLOW),
                    Block(0, 1, arcade.color.MELLOW_YELLOW),
                    Block(1, 1, arcade.color.MELLOW_YELLOW),
                ],
                90,
                grid_representation
            ),
            180: Piece(
                [
                    Block(0, 0, arcade.color.MELLOW_YELLOW),
                    Block(1, 0, arcade.color.MELLOW_YELLOW),
                    Block(0, 1, arcade.color.MELLOW_YELLOW),
                    Block(1, 1, arcade.color.MELLOW_YELLOW),
                ],
                180,
                grid_representation
            ),
            270: Piece(
                [
                    Block(0, 0, arcade.color.MELLOW_YELLOW),
                    Block(1, 0, arcade.color.MELLOW_YELLOW),
                    Block(0, 1, arcade.color.MELLOW_YELLOW),
                    Block(1, 1, arcade.color.MELLOW_YELLOW),
                ],
                270,
                grid_representation
            ),
        }
