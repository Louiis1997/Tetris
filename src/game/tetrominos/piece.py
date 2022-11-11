class Piece:
    def __init__(self, blocks, rotation, grid_representation):
        self.blocks = blocks
        self.rotation = rotation
        self.grid_representation = grid_representation

    def move_down(self):
        self.move(1, 0)

    def move_right(self):
        self.move(0, 1)

    def move_left(self):
        self.move(0, -1)

    def move(self, x, y):
        for block in self.blocks:
            block.move(x, y)
