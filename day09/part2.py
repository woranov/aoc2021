import functools

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
        if (adj_coord := (adj_y, adj_x)) in grid:
            yield adj_coord


def compute(data):
    """
    >>> compute(_TESTCASE)
    1134
    """
    # this could be way simple probably

    grid = {}
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            grid[(y, x)] = int(value)

    basin_centers = set()

    for coord, value in grid.items():
        adj_coords = list(adj(grid, coord))
        if all(grid[adj_coord] > value for adj_coord in adj_coords):
            basin_centers.add(coord)

    basins = []

    for basin_center in basin_centers:
        basin = set()
        basin_neighbors = {basin_center}
        while basin_neighbors:
            p = basin_neighbors.pop()
            basin.add(p)
            basin_neighbors |= {
                coord for coord in adj(grid, p) if grid[coord] < 9 if coord not in basin
            }
        basins.append(basin)

    return functools.reduce(
        int.__mul__,
        sorted(map(len, basins), reverse=True)[:3],
        1,
    )


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().splitlines()))


if __name__ == "__main__":
    main()
