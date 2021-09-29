import math


def run():
    count = int(input())
    i = 0
    while i < count:
        line = input().split()
        if not line:
            continue
        i += 1
        piece, rows, cols = line[0], int(line[1]), int(line[2])
        if piece == 'k':
            print(math.ceil(rows * cols * 0.5))
        elif piece in 'Qr':
            print(min(rows, cols))
        else:
            print(math.ceil(rows/2) * math.ceil(cols/2))


if __name__ == '__main__':
    run()

