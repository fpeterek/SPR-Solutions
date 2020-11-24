import math

lowest = 0


def backtrack(lst, first_index=0, bits=0, header=0):

    power = 1

    global lowest
    while True:
        bits_cpy = bits
        covered = 2**power
        last_index = first_index + covered-1

        if last_index < len(lst)-1:
            covered -= 1
            last_index -= 1

        for i in range(covered):
            if first_index+i >= len(lst):
                break
            bits_cpy += lst[first_index+i][1] * (header+power)
            if bits_cpy > lowest:
                return

        if last_index >= len(lst)-1:
            lowest = min(bits_cpy, lowest)
            return

        backtrack(lst, last_index+1, bits_cpy, header+power)

        power += 1


def guess(lst):
    global lowest

    if not lst:
        lowest = 0
        return

    power = max(1, math.ceil(math.log2(len(lst))))

    total = 0

    for char, count in lst:
        total += count * power

    lowest = total


def handle_input():

    num_lines = int(input())
    lines = ''

    for i in range(num_lines):
        lines += input()

    occurrences = {}

    for c in lines:
        occurrences[c] = occurrences.get(c, 0) + 1

    occurrences = sorted(occurrences.items(), key=lambda t: t[1], reverse=True)

    guess(occurrences)
    backtrack(occurrences)
    print(lowest)


def run():
    inputs = int(input())
    for i in range(inputs):
        handle_input()


if __name__ == '__main__':
    run()
