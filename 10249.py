
class Table:
    counter = 1

    def __init__(self, seats):
        self.number = Table.counter
        Table.counter += 1
        self.seats = seats
        self.seated = []

    def seat(self, team):
        self.seated.append(team)

    @property
    def is_full(self):
        return len(self.seated) == self.seats

    def __contains__(self, team):
        return team in self.seated

    def __str__(self):
        return ' '.join(self.seated)

    def __repr__(self):
        return str(self)


class Team:
    counter = 1

    def __init__(self, members):
        self.number = Team.counter
        Team.counter += 1
        self.members = members
        self.seated = 0

    def next(self):
        self.seated += 1
        return self.number

    @property
    def all_seated(self):
        return self.seated == self.members


def reset_counts():
    Table.counter = 1
    Team.counter = 1


def load_teams():
    line = input().split()
    return [Team(int(i)) for i in line]


def load_tables():
    line = input().split()
    return [Table(int(i)) for i in line]


def read_counts():
    line = input().split()
    return int(line[0]), int(line[1])


def seat(teams, tables):
    for team in teams:
        for table in tables:
            if team.all_seated:
                break
            if table.is_full:
                continue
            table.seat(team.next())
    return all(map(lambda t: t.all_seated, teams))


def run():
    while True:
        count1, count2 = read_counts()
        if count1 == count2 == 0:
            return

        reset_counts()

        teams = load_teams()
        tables = load_tables()
        teams.sort(key=lambda t: t.members, reverse=True)
        tables.sort(key=lambda table: table.seats, reverse=True)

        res = seat(teams, tables)

        print(int(res))

        if not res:
            continue

        teams.sort(key=lambda t: t.number)

        for team in teams:
            sorted_tables = sorted([str(table.number) for table in tables if team.number in table])
            print(' '.join(sorted_tables))


if __name__ == '__main__':
    run()
