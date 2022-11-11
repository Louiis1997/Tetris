class Block:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move_down(self):
        self.move(1, 0)

    def move_right(self):
        self.move(0, 1)

    def move_left(self):
        self.move(0, -1)

    def move(self, x, y):
        self.x += x
        self.y += y

    def get_pos(self):
        return self.x, self.y

    def get_color(self):
        return self.color

    def __str__(self):
        return "Block({0}, {1}, {2})".format(self.x, self.y, self.color)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.color == other.color

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y, self.color))

    def __copy__(self):
        return Block(self.x, self.y, self.color)

    def __deepcopy__(self, memo):
        return Block(self.x, self.y, self.color)

    def __getstate__(self):
        return self.x, self.y, self.color

    def __setstate__(self, state):
        self.x, self.y, self.color = state
