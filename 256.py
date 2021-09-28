from functools import lru_cache
import math


def find_quirky(begin, magnitude, digits):

    if ((begin/magnitude)+(magnitude-1))**2 < begin+magnitude-1 or (begin/magnitude)**2 > begin+magnitude-1:
        return

    bsearch_half = int(magnitude/2)
    number = begin

    while True:
        if bsearch_half == 0:
            return
        number += bsearch_half

        left = int(number / magnitude)
        right = number % magnitude
        square = (left + right)**2

        if square != number:
            if bsearch_half == 1:
                return
            bsearch_half = int(math.ceil(abs(bsearch_half)/2) * (-1 if square > number else 1))
        if square == number:
            return '{{0:0{digits}}}'.format(digits=digits).format(number)


@lru_cache(maxsize=None)
def quirksome(digits):
    half = int(10 ** (digits/2))
    end = int(10 ** digits)

    numbers = {'0' * digits, '0' * (digits - 1) + '1'}

    for i in range(half, end, half):
        num = find_quirky(i, half, digits)
        if num:
            numbers.add(num)

    lst = list(numbers)
    lst.sort()
    return lst


def read_input():
    try:
        return input()
    except EOFError:
        return None


def run():
    while True:
        line = read_input()
        if not line:
            return
        number = int(line)
        numbers = quirksome(number)
        for num in numbers:
            print(num)


if __name__ == '__main__':
    run()

