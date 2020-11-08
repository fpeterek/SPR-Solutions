
class LineSolver:
    def __init__(self, line, word):
        self.line = line
        self.word = word
        self.current_opts = {index: [index] for index, char in enumerate(self.line) if char == word[0]}
        self.opt_list = []
        self.cache = {}  # depth: cache

    def find_letter(self, index):
        begin = min(self.current_opts.keys())
        char = self.word[index]
        new_opts = {}
        indices = []

        for i in range(len(self.line)-1, begin-1, -1):
            if i in self.current_opts.keys():
                if len(indices):
                    self.current_opts[i] = indices[:]
                else:
                    self.current_opts.pop(i)
            if self.line[i] == char:
                new_opts[i] = 0
                indices.append(i)

        # print('Current  ', self.word[:index], '[', self.word[index], ']', sep='')
        # print(self.current_opts)
        # print(new_opts)

        return new_opts

    def get_cache(self, depth):
        if depth not in self.cache:
            self.cache[depth] = {}
        return self.cache[depth]

    def count_solutions(self, depth, index):
        if depth >= len(self.word):
            return 1

        if index not in self.opt_list[depth]:
            return 0

        cache = self.get_cache(depth)
        total = 0

        for opt in self.opt_list[depth][index]:
            optval = cache.get(opt, -1)
            if optval == -1:
                optval = self.count_solutions(depth+1, opt)
                cache[opt] = optval

            total += optval

        return total

    def solve(self):
        # print('Current  [', self.word[0], ']', sep='')
        # print(self.current_opts)

        for i in range(1, len(self.word)):
            self.opt_list.append(self.current_opts)
            self.current_opts = self.find_letter(i)

        self.opt_list.insert(0, {-1: list(self.opt_list[0].keys())})

        # for i in self.opt_list:
        #     print(i)

        return self.count_solutions(0, -1)


def run_case():
    line = input()
    word = input()
    print(LineSolver(line, word).solve())
    # print(LineSolver(line[::-1], word[::-1]).solve())


def run():
    cases = int(input())
    for _ in range(cases):
        run_case()


if __name__ == '__main__':
    run()

