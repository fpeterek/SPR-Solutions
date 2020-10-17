
class Town:
    def __init__(self, number):
        self.town = number
        self.connection_list = []
        self.has_station = False
        self.conn_has_station = False

    @property
    def connections(self):
        return len(self.connection_list)

    @property
    def has_access(self):
        return self.has_station or self.conn_has_station

    def set_station(self):
        self.has_station = True
        for conn in self.connection_list:
            conn.conn_has_station = True

    @property
    def neighbours_with_access(self):
        return sum(map(lambda n: n.has_access, self.connection_list))

    @property
    def neighbours_without_access(self):
        return self.connections - self.neighbours_with_access

    @property
    def has_multiple_access(self):
        conns = sum(map(lambda conn: conn.has_station, self.connection_list))
        return (conns + self.has_station) > 1

    def remove_if_redundant(self):
        if self.connection_list and all(map(lambda conn: conn.has_multiple_access, self.connection_list)):
            self.has_station = False

    @property
    def coverage_set(self):
        s = set(map(lambda town: town.town, self.connection_list))
        s.add(self.town)
        return s

    @property
    def highest_neighbour(self):
        if not self.connection_list:
            return self

        neighbour = self.connection_list[0]
        for n in self.connection_list:
            if n.neighbours_without_access > neighbour.neighbours_without_access:
                neighbour = n
        return neighbour if neighbour.neighbours_without_access > self.neighbours_without_access else self 

    def add_connection(self, t2):
        self.connection_list.append(t2)


def solve_recursively(towns, order, current):

    if current >= len(order):
        return

    if not towns[order[current]].has_access:
        towns[order[current]].highest_neighbour.set_station()
    
    return solve_recursively(towns, order, current+1)


def remove_redundant(sets):
    for key, value in sets.items():
        for k2, v2 in sets.items():
            if key == k2:
                continue
            if not (value - v2):
                sets.pop(key)
                return remove_redundant(sets)


def count_occurrences(sets):
    occurrences = {}
    for s in sets.values():
        for val in s:
            occurrences[val] = occurrences.get(val, 0) + 1
    return occurrences


def by_occurrences(towns, sets):
    occurrs_in = dict()
    for town in towns:
        for s in sets.values():
            if town in s:
                if town not in occurrs_in:
                    occurrs_in[town] = [s]
                else:
                    occurrs_in[town].append(s)
    return occurrs_in


# First value in set
def first(s):
    for val in s:
        return val


def remove_unusable(sets, placed, unplaced):
    for k, v in sets.items():
        if not (v - placed):
            sets.pop(k)
            return remove_unusable(sets, placed, unplaced)
        else:
            sets[k] = v.intersection(unplaced)


def union(sets, exclude):
    un = set()
    for k, v in sets.items():
        if k == exclude:
            continue
        un = un.union(v)
    return un


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


def set_intersect(towns):
    sets = {town.town: town.coverage_set for town in towns}
    towns = {town.town for town in towns}
    remove_redundant(sets)
    counts = count_occurrences(sets)
    occurrs_in = by_occurrences(towns, sets)
    placed = set()
    stations_created = 0

    # Remove isolated towns or towns with one neighbour
    '''for town, count in counts.items():
        if count == 1 and town not in placed:
            placed = placed.union(first(occurrs_in[town]))
            stations_created += 1
            for k, v in sets.items():
                if v == first(occurrs_in[town]):
                    sets.pop(k)
                    break'''

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
        # Remove sets I have no use for
        remove_unusable(sets, placed, towns - placed)
        # Remove subsets of bigger sets, filter out unneeded connections
        remove_redundant(sets)
    #for k, v in sets.items():
    # print(v)

    #print('*' * 30)
    copy = sets.copy()
    # Find two sets with the biggest possible union
    while sets:
        if len(sets) == 1:
            placed = placed.union(sets[first(sets)])
            stations_created += 1
            break
        t1, t2 = biggest_union(sets)
        #print(copy[t1])
        #print(copy[t2])
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
    #print('-' * 30)
    #for k, v in sets.items():
    #    print(v)
    '''print('-'*30)
    print('Lack coverage: ', towns - placed)
    print('-'*30)
    for k, v in sets.items():
        print(v)

    print(len(sets), ',', stations_created)
    print('-'*30)'''
    print(stations_created)
    #print('-'*30)



def solve(towns):
    ordered = towns[:] 
    ordered.sort(key=lambda town: town.connections, reverse=False)
    ordered = list(map(lambda town: town.town, ordered))

    # solve_recursively(towns, ordered, 0)
    set_intersect(towns) 

    for town in towns:
        town.remove_if_redundant()

    stations = sum(map(lambda town: town.has_station, towns))
    # print(stations)


def read_input():
    line = input()
    if not line:
        return read_input()
    line = line.split(' ')
    return tuple(map(lambda x: int(x), filter(lambda x: x, line)))
    # return lst[0], lst[1]


def read_towns():
    towns, conns = read_input()
    towns = list(map(lambda no: Town(no), range(towns)))
    for conn in range(conns):
        t1, t2 = read_input()
        t1 -= 1  # indices start from 0
        t2 -= 1
        towns[t1].add_connection(towns[t2])
        towns[t2].add_connection(towns[t1])

    return towns


def run():
    while True:
        towns = read_towns()
        if not towns:
            break
        solve(towns)


if __name__ == '__main__':
    try:
        run()
    except EOFError:
        pass 

