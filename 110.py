
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        line = ''

        if self.left:
            line += str(self.left)
        line += str(self.value)
        if self.right:
            line += str(self.right)

        return line

    def __repr__(self):
        return str(self)

    @property
    def left_rightmost(self):
        if not self.left:
            return self.value
        return self.left.rightmost

    @property
    def rightmost(self):
        if not self.right:
            return self.value
        return self.right.righmost

    def iterate(self):
        if self.right:
            for node in self.right.iterate():
                yield node
        if (not self.right) or (not self.left):
            yield self
        if self.left:
            for node in self.left.iterate():
                yield node


def header(variables):
    print('program sort(input,output);')
    print('var')
    print(','.join(variables), ': integer;')
    print('begin')
    print('  readln({});'.format(','.join(variables)))


def end():
    print('end.')


def print_if(tree, current, indent):
    s = str(tree)
    if s[0] == current:
        print(indent*' ', 'else', sep='')
    elif s[-1] == current:
        print(indent*' ', 'if {} < {} then'.format(s[-2], current), sep='')
    else:
        index = s.index(current)
        print(indent*' ', 'else if {} < {} then'.format(s[index-1], current), sep='')


def gen_comparisons(tree, variables, indent=2):
   
    if not variables:
        comma_sep = ','.join(list(str(tree)))
        return print(indent*' ', 'writeln(', comma_sep, ')', sep='')

    first = variables[0]
    variables = variables[1:]

    for node in tree.iterate():
        if not node.right:
            node.right = Node(first)

            print_if(tree, first, indent)

            gen_comparisons(tree, variables, indent+2)
            node.right = None
        if not node.left:
            node.left = Node(first)
           
            print_if(tree, first, indent)

            gen_comparisons(tree, variables, indent+2)
            node.left = None


def generate(nums):
    variables = 'abcdefgh'[0:nums]

    header(variables)

    gen_comparisons(Node(variables[0]), variables[1:], 2)

    end()


if __name__ == '__main__':
    cases = int(input())
    for i in range(cases):
        input()
        numbers = int(input())
        generate(numbers)
        if i < cases-1:
            print()

