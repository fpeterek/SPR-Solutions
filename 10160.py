
class Town:
    def __init__(self, number):
        self.town = number
        self.connection_list = []

    # List of towns a station in this town could cover (neighbours + self)
    @property
    def coverage_set(self):
        s = set(map(lambda town: town.town, self.connection_list))
        s.add(self.town)
        return s

    def add_connection(self, t2):
        self.connection_list.append(t2)


# Remove redundant coverage sets -> subsets of bigger sets
def remove_redundant(sets):
    for key, value in sets.items():
        for k2, v2 in sets.items():
            if key == k2:
                continue
            if not (value - v2):
                sets.pop(key)
                return remove_redundant(sets)


# First value in a set -> I can't use set[0]
def first(s):
    for val in s:
        return val


# Remove coverage sets which could only cover towns which already have coverage
# Also removes towns with coverage from existing sets so we don't perform calculations with already covered towns
def remove_unusable(sets, placed, unplaced):
    for k, v in sets.items():
        if not (v - placed):
            sets.pop(k)
            return remove_unusable(sets, placed, unplaced)
        else:
            sets[k] = v.intersection(unplaced)


# Union of all sets except one set
def union(sets, exclude):
    un = set()
    for k, v in sets.items():
        if k == exclude:
            continue
        un = un.union(v)
    return un


# Returns coverage sets which cover towns covered by only a single coverage set because we don't have a choice but to
# use these coverage sets
def find_unique(sets):
    unique = []
    unique_towns = []
    for town, coverage in sets.items():
        if coverage - union(sets, exclude=town):
            unique.append(coverage)
            unique_towns.append(town)

    for town in unique_towns:
        sets.pop(town)

    return unique


# Returns two sets which together form the biggest union
# If there are multiple such pairs of sets, we take the first pair with the smallest intersection
def biggest_union(sets):
    t1 = 0
    t2 = 0
    un_size = 0
    i_size = 0

    for k1, s1 in sets.items():
        for k2, s2 in sets.items():
            if k1 == k2:
                continue
            l_un = len(s1.union(s2))
            l_i = len(s1.intersection(s2))
            if l_un > un_size or (l_un == un_size and l_i < i_size):
                un_size = l_un
                i_size = l_i
                t1, t2 = k1, k2

    return t1, t2


def solve(towns):
    sets = {town.town: town.coverage_set for town in towns}
    towns = {town.town for town in towns}
    remove_redundant(sets)
    placed = set()
    stations_created = 0

    # Remove sets I have no use for
    remove_unusable(sets, placed, towns - placed)
    # Remove subsets of bigger sets, filter out unneeded connections
    remove_redundant(sets)

    # Find unique connections
    while True:
        unique = find_unique(sets)
        if not unique:
            break
        stations_created += len(unique)
        for un in unique:
            placed = placed.union(un)
        remove_unusable(sets, placed, towns - placed)
        remove_redundant(sets)

    # Find two sets with the biggest possible union
    while sets:
        if len(sets) == 1:
            placed = placed.union(sets[first(sets)])
            stations_created += 1
            break
        t1, t2 = biggest_union(sets)

        un = sets[t1].union(sets[t2])
        placed = placed.union(un)
        sets.pop(t1)
        sets.pop(t2)
        stations_created += 2
        # Remove sets I have no use for
        remove_unusable(sets, placed, towns - placed)
        # Remove subsets of bigger sets, filter out unneeded connections
        remove_redundant(sets)
        if len(placed) == len(towns):
            break

    return stations_created


def read_input():
    line = input()
    if not line:
        return read_input()
    line = line.split(' ')
    return tuple(map(lambda x: int(x), filter(lambda x: x, line)))


def read_towns():
    towns, conns = read_input()
    towns = list(map(lambda no: Town(no), range(towns)))
    for conn in range(conns):
        t1, t2 = read_input()
        t1 -= 1  # Start numbering towns from 0 because indices also start from 0
        t2 -= 1
        towns[t1].add_connection(towns[t2])
        towns[t2].add_connection(towns[t1])

    return towns


def run():
    while True:
        towns = read_towns()
        if not towns:
            break
        print(solve(towns))


if __name__ == '__main__':
    try:
        run()
    except EOFError:
        pass 

