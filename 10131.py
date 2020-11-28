import sys


class Elephant:
    def __init__(self, weight, iq):
        self.weight = weight
        self.iq = iq

    def __str__(self):
        return 'Elephant (weight={}, iq={})'.format(self.weight, self.iq)

    def __repr__(self):
        return str(self)


def add_to_subs(subs, elephant):

    new = {}

    for k, v in subs.items():
        if elephant.iq > v[-1].iq and (len(v) <= 1 or elephant.iq < v[-2].iq):
            v[-1] = elephant
        if elephant.iq < v[-1].iq and elephant.weight > v[-1].weight:
            # print('{} < {}'.format(elephant.iq, v[-1].iq))
            copy = v[:]
            copy.append(elephant)
            new[len(copy)] = copy

    for k, v in new.items():
        if k not in subs or subs[k][-1].iq < v[-1].iq:
            subs[k] = v


def longest_decreasing_subsequence(elephants):
    subsequences = {1: [elephants[0]]}

    for elephant in elephants:
        add_to_subs(subsequences, elephant)

    return subsequences[max(subsequences.keys())]


def run():
    elephants = []

    for line in sys.stdin:
        line = line.rstrip('\n')
        if line:
            split = line.split()
            elephants.append(Elephant(weight=int(split[0]), iq=int(split[1])))

    copy = elephants[:]
    elephants = sorted(elephants, key=lambda e: e.weight)
    lds = longest_decreasing_subsequence(elephants)

    print(len(lds))
    for el in lds:
        print(copy.index(el)+1)


if __name__ == '__main__':
    run()
