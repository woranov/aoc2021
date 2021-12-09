_TESTCASE = """\
2199943210
3987894921
9856789892
8767896789
9899965678
""".splitlines()


def adj(grid, coord):
    y, x = coord
    for adj_y, adj_x in (
        (y - 1, x),
        (y + 1, x),
        (y, x - 1),
        (y, x + 1),
    ):
        try:
            yield grid[(adj_y, adj_x)]
        except KeyError:
            pass


def compute(data):
    """
    >>> compute(_TESTCASE)
    15
    """
    grid = {}
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            grid[(y, x)] = int(value)

    n = 0

    for coord, value in grid.items():
        if all(adj_v > value for adj_v in adj(grid, coord)):
            n += value + 1

    return n


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().splitlines()))


if __name__ == "__main__":
    main()
