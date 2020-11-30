
def scenario_size():
    pn = list(map(lambda x: int(x), input().split()))
    return pn[0], pn[1]


def load_papers(papers):
    relations = {}

    for i in range(papers):
        line = input().split(':')[0]
        line = line.replace('., ', '.;').split(';')
        line = set(line)
        for person in line:
            relations[person] = relations.get(person, set()) | (line - {person})

    return relations


def load_names(names):
    return [input() for _ in range(names)]


def load_table(relations):
    erdos = 'Erdos, P.'
    cache = {erdos: 0}

    handled = set()
    to_handle = {erdos}

    while to_handle:
        new = set()

        for current in to_handle - handled:
            current_num = cache[current]
            for person in relations[current]:
                cache[person] = min(cache.get(person, current_num+1), current_num + 1)
                new = new | {person}
            handled.add(current)

        to_handle = new - handled

    return cache


def run_scenario(scenario):

    papers, names = scenario_size()

    papers = load_papers(papers)
    names = load_names(names)

    cache = load_table(papers)

    print('Scenario', scenario)

    for name in names:
        number = cache.get(name)
        print(name, 'infinity' if number is None else number)


def run():
    scenarios = int(input())

    for scenario in range(1, scenarios+1):
        run_scenario(scenario)


if __name__ == '__main__':
    run()
