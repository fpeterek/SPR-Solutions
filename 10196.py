# https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=29&page=show_problem&problem=1137

# I humbly apologize for the atrocity I've created.
# However, I'm writing this just before going to sleep
# and I don't have the time to refactor this,
# nor do I believe refactoring this code is a good use
# of my time. It works and I have plenty of other work
# to do, which means I'm happy with this.
# It's not going to be maintained anyway.


class Check:
    none = 0
    black = 1
    white = 2


def is_blank(b):
    return all(map(lambda line: line == '.' * 8, b))


def load_board():
    board = []
    for i in range(8):
        board.append(input())

    return board

def check_straight(px, py):
    white = board[py][px].isupper()
    
    for x in range(px+1, 8):
        if board[py][x] == '.':
            continue
        if board[py][x] == ('k' if white else 'K'):
            return Check.black if white else Check.white
        break
    
    for x in range(px-1, -1, -1):
        if board[py][x] == '.':
            continue
        if board[py][x] == ('k' if white else 'K'):
            return Check.black if white else Check.white
        break

    for y in range(py+1, 8):
        if board[y][px] == '.':
            continue
        if board[y][px] == ('k' if white else 'K'):
            return Check.black if white else Check.white
        break
    
    for y in range(py-1, -1, -1):
        if board[y][px] == '.':
            continue
        if board[y][px] == ('k' if white else 'K'):
            return Check.black if white else Check.white
        break

    return Check.none


def check_dia(px, py):
    white = board[py][px].isupper()
   
    y = py
    for x in range(px+1, 8):
        y += 1
        if y > 7:
            break
        if board[y][x] == '.':
            continue
        if board[y][x] == ('k' if white else 'K'):
            return Check.black if white else Check.white
        break
   
    y = py
    for x in range(px-1, -1, -1):
        y -= 1
        if y < 0:
            break
        if board[y][x] == '.':
            continue
        if board[y][x] == ('k' if white else 'K'):
            return Check.black if white else Check.white
        break

    x = px
    for y in range(py+1, 8):
        x -= 1
        if x < 0:
            break
        if board[y][x] == '.':
            continue
        if board[y][x] == ('k' if white else 'K'):
            return Check.black if white else Check.white
        break
   
    x = px
    for y in range(py-1, -1, -1):
        x += 1
        if x > 7:
            break
        if board[y][x] == '.':
            continue
        if board[y][x] == ('k' if white else 'K'):
            return Check.black if white else Check.white
        break

    return Check.none

def check_pawn(x, y):
    white = board[y][x].isupper()

    delta = -1 if white else 1
    y = y + delta

    if y not in range(8):
        return Check.none
   
    target = 'k' if white else 'K'

    if x-1 in range(8) and board[y][x-1] == target:
        return Check.black if white else Check.white

    if x+1 in range(8) and board[y][x+1] == target:
        return Check.black if white else Check.white

    return Check.none

def check_queen(x, y):
    return check_dia(x, y) + check_straight(x, y)

def check_knight(px, py):
    white = True if board[y][x].isupper() else False
    target = 'k' if white else 'K'

    if py-2 in range(0, 8):
        if px-1 in range(0, 8) and board[py-2][px-1] == target:
            return Check.black if white else Check.white
        if px+1 in range(0, 8) and board[py-2][px+1] == target:
            return Check.black if white else Check.white
    
    if py+2 in range(0, 8):
        if px-1 in range(0, 8) and board[py+2][px-1] == target:
            return Check.black if white else Check.white
        if px+1 in range(0, 8) and board[py+2][px+1] == target:
            return Check.black if white else Check.white
    
    if px-2 in range(0, 8):
        if py-1 in range(0, 8) and board[py-1][px-2] == target:
            return Check.black if white else Check.white
        if py+1 in range(0, 8) and board[py+1][px-2] == target:
            return Check.black if white else Check.white
    
    if px+2 in range(0, 8):
        if py-1 in range(0, 8) and board[py-1][px+2] == target:
            return Check.black if white else Check.white
        if py+1 in range(0, 8) and board[py+1][px+2] == target:
            return Check.black if white else Check.white

    return Check.none


if __name__ == '__main__':

    c = 1

    while True:
        board = load_board()

        if is_blank(board):
            break

        check = Check.none

        for y, line in enumerate(board):
            for x, char in enumerate(line):
                if char == '.':
                    continue
                if char in ('q', 'Q') and check == Check.none:
                    check = check_queen(x, y)
                if char in ('p', 'P') and check == Check.none:
                    check = check_pawn(x, y)
                if char in ('n', 'N') and check == Check.none:
                    check = check_knight(x, y)
                if char in ('r', 'R') and check == Check.none:
                    check = check_straight(x, y)
                if char in ('b', 'B') and check == Check.none:
                    check = check_dia(x, y)

                if check != Check.none:
                    break
            if check != Check.none:
                break

        king = 'no' if check == Check.none else ('white' if check == Check.white else 'black')
        print('Game #{}: {} king is in check.'.format(c, king))
        c += 1
        input()  # ignore empty line

