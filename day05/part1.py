import collections
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

    def straight_line_connected_points(self) -> typing.Iterator[Point]:
        if self.point1.x == self.point2.x:
            start_y, end_y = sorted((self.point1.y, self.point2.y))
            for y in range(start_y, end_y + 1):
                yield Point(self.point1.x, y)
        elif self.point1.y == self.point2.y:
            start_x, end_x = sorted((self.point1.x, self.point2.x))
            for x in range(start_x, end_x + 1):
                yield Point(x, self.point1.y)


def compute(data):
    """
    >>> compute(_TESTCASE)
    5
    """
    lines = [Line.from_string(s) for s in data]
    grid = collections.Counter(
        p for line in lines for p in line.straight_line_connected_points()
    )

    return sum(1 for cnt in grid.values() if cnt >= 2)


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().splitlines()))


if __name__ == "__main__":
    main()
