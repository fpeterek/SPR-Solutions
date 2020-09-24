# Shell sort - https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1093

def read_list(size):
    lst = []
    for i in range(size):
        lst.append(input())
    return lst


def out_of_place(lst, offset, length):
    oop = []
    
    # print('Offset: ', offset)
    for i in range(0, length):
        if not lst.count(i):
            continue
        index = lst.index(i) + offset
        if index != i:
            lst.remove(i)
            oop.append(i)
            offset += 1

    return oop

def shell_sort(current_order, desired):

    current_order = [desired.index(i) for i in current_order]
    length = len(desired)

    misplaced = []
    while True:
        oop = out_of_place(current_order, len(misplaced), length)
        if not oop:
            break
        misplaced += oop
    misplaced.sort()
    misplaced = misplaced[::-1]
    return [desired[i] for i in misplaced]

def handle_block():
    size = int(input())
    current = read_list(size)
    desired = read_list(size)

    move_order = shell_sort(current, desired)

    for i in move_order:
        print(i)

    print()


if __name__ == '__main__':
    blocks = int(input())
    for i in range(blocks):
        handle_block()

