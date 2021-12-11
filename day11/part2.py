import itertools

_TESTCASE = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""".splitlines()


def neighbors(grid, coord):
    y, x = coord
    for y_n in range(y - 1, y + 2):
        for x_n in range(x - 1, x + 2):
            if (y_n, x_n) != coord and (y_n, x_n) in grid:
                yield y_n, x_n


def compute(data):
    """
    >>> compute(_TESTCASE)
    195
    """
    grid = {}

    for y, row in enumerate(data):
        for x, value in enumerate(row):
            grid[(y, x)] = int(value)

    for step in itertools.count(1):
        flashed = set()
        queue = list(grid.keys())

        while queue:
            coord = queue.pop(0)
            grid[coord] = val = grid[coord] + 1
            if val >= 10:
                if coord not in flashed:
                    queue = list(neighbors(grid, coord)) + queue
                flashed.add(coord)

        if len(flashed) == len(grid):
            break

        for flashed_coord in flashed:
            grid[flashed_coord] = 0

        flashed.clear()

    # noinspection PyUnboundLocalVariable
    return step


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().splitlines()))


if __name__ == "__main__":
    main()
