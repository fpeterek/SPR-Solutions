
class Dir:
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

    def __init__(self, direction):
        self.dir = direction

    def negate(self):
        if self.dir == Dir.LEFT:
            return Dir.right
        if self.dir == Dir.RIGHT:
            return Dir.left
        if self.dir == Dir.UP:
            return Dir.down
        return Dir.up

    def move(self, direction):
        if self.dir == Dir.RIGHT:
            if direction == Dir.RIGHT:
                return Dir.down
            return Dir.up

        if self.dir == Dir.LEFT:
            if direction == Dir.RIGHT:
                return Dir.up
            return Dir.down

        if self.dir == Dir.UP:
            return Dir(direction)

        return Dir(direction.negate())

    def tilt90(self):
        if self.dir == Dir.RIGHT:
            return Dir.up
        if self.dir == Dir.UP:
            return Dir.left
        if self.dir == Dir.LEFT:
            return Dir.down
        return Dir.right

    def __str__(self):
        if self.dir == Dir.UP:
            return 'up'
        if self.dir == Dir.DOWN:
            return 'down'
        if self.dir == Dir.RIGHT:
            return 'right'
        return 'left'

    def __repr__(self):
        return str(self)

    def to_path(self):
        if self.dir in (Dir.UP, Dir.DOWN):
            return '|'
        return '_'


class Map:
    def __init__(self):
        self.row = 0
        self.col = -1

        self.map = [[' ']]

    def __str__(self):
        return '\n'.join([''.join(line).rstrip() for line in self.map]) + '\n^'

    def __repr__(self):
        return str(self)

    def add_move(self, move):
        
        if move.dir == Dir.RIGHT:
            self.col += 1
            self.check_bounds()
            self.map[self.row][self.col] = move.to_path()
            self.col += 1
        elif move.dir == Dir.LEFT:
            self.col -= 1
            self.check_bounds()
            self.map[self.row][self.col] = move.to_path()
            self.col -= 1
        elif move.dir == Dir.UP:
            self.map[self.row][self.col] = move.to_path()
            self.row -= 1
        elif move.dir == Dir.DOWN:
            self.row += 1
            self.check_bounds()
            self.map[self.row][self.col] = move.to_path()

        self.check_bounds()


    def check_bounds(self):
        change = False
        if self.col == len(self.map[0]):
            self.append_right()
            change = True
        if self.col == -1:
            self.col = 0
            self.prepend_left()
            chage = True
        if self.row == len(self.map):
            self.append_bottom()
            change = True
        if self.row == -1:
            self.row = 0
            self.prepend_top()
            change = True

        if change:
            self.check_bounds()

    def append_right(self):
        for l in self.map:
            l.append(' ')

    def prepend_left(self):
        for l in self.map:
            l.insert(0, ' ')

    def append_bottom(self):
        self.map.append(list(' ' * len(self.map[0])))

    def prepend_top(self):
        self.map.insert(0, list(' ' * len(self.map[0])))

    @staticmethod
    def empty(lst):
        return all(map(lambda x: (not x) or x.isspace(), lst))

    def trim(self):
        while self.map and Map.empty(self.map[0]):
            self.map.pop(0)

        while self.map and Map.empty(self.map[-1]):
            self.map.pop()


Dir.left = Dir(Dir.LEFT)
Dir.right = Dir(Dir.RIGHT)
Dir.up = Dir(Dir.UP)
Dir.down = Dir(Dir.DOWN)


def fold(path):
    copy = path[::-1]
    for move in copy:
        path.append(move.tilt90())


def calc(folds):
    path = [Dir.right]

    for _ in range(folds):
        fold(path)

    return path


def print_path(path):
    m = Map()

    for p in path:
        m.add_move(p)

    m.trim()

    print(m)


if __name__ == '__main__':
    folds = int(input())
    while folds:
        print_path(calc(folds))
        folds = int(input())

