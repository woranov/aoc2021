import collections
import itertools
import typing

_TESTCASE = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""".splitlines()


class Point(typing.NamedTuple):
    x: int
    y: int

    @classmethod
    def from_string(cls, s: str) -> "Point":
        return cls(*(int(n) for n in s.split(",")))


class Line(typing.NamedTuple):
    point1: Point
    point2: Point

    @classmethod
    def from_string(cls, s: str) -> "Line":
        return cls(*(Point.from_string(p_s) for p_s in s.split(" -> ")))

    def straight_or_diag_connected_points(self) -> typing.Iterator[Point]:
        diff_x = self.point2.x - self.point1.x
        diff_y = self.point2.y - self.point1.y

        xs_step = 1 if diff_x >= 0 else -1
        xs = range(self.point1.x, self.point1.x + diff_x + xs_step, xs_step)

        ys_step = 1 if diff_y >= 0 else -1
        ys = range(self.point1.y, self.point1.y + diff_y + ys_step, ys_step)

        if 0 in (diff_x, diff_y):
            for x, y in itertools.zip_longest(
                xs, ys, fillvalue=(self.point1.x if diff_x == 0 else self.point1.y)
            ):
                yield Point(x, y)
        elif abs(diff_x) == abs(diff_y):
            for x, y in zip(xs, ys):
                yield Point(x, y)


def compute(data):
    """
    >>> compute(_TESTCASE)
    12
    """
    lines = [Line.from_string(s) for s in data]
    grid = collections.Counter(
        p for line in lines for p in line.straight_or_diag_connected_points()
    )

    return sum(1 for cnt in grid.values() if cnt >= 2)


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().splitlines()))


if __name__ == "__main__":
    main()
