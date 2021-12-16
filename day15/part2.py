import collections
import heapq
import sys

_TESTCASE = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""".splitlines()


def compute(data):
    """
    >>> compute(_TESTCASE)
    315
    """
    base_width = len(data[0])
    base_height = len(data)

    grid = {
        (tile_x * base_width + x, tile_y * base_height + y): (
            nn if (nn := (int(n) + tile_x + tile_y)) <= 9 else nn - 9
        )
        for y, line in enumerate(data)
        for x, n in enumerate(line)
        for tile_x in range(5)
        for tile_y in range(5)
    }

    max_x = base_width * 5 - 1
    max_y = base_height * 5 - 1

    def neighbors(x, y):
        for x, y in filter(
            lambda coord: 0 <= coord[0] <= max_x and 0 <= coord[1] <= max_y,
            (
                (x - 1, y),
                (x, y - 1),
                (x + 1, y),
                (x, y + 1),
            ),
        ):
            yield x, y

    dists = collections.defaultdict(lambda: sys.maxsize, {(0, 0): 0})

    queue = [(0, (0, 0))]
    visited = set()

    while queue:
        dist, (x, y) = heapq.heappop(queue)

        if (x, y) in visited:
            continue
        else:
            visited.add((x, y))

        for nb in neighbors(x, y):
            if nb in visited:
                continue
            nb_dist = dist + grid[nb]
            if nb_dist < dists[nb]:
                dists[nb] = nb_dist
                heapq.heappush(queue, (nb_dist, nb))

    return dists[(max_x, max_y)]


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().splitlines()))


if __name__ == "__main__":
    main()
