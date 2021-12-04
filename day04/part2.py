import typing

_TESTCASE = """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""


class Board(typing.NamedTuple):
    rows: list[list[int | None]]

    @property
    def columns(self) -> list[list[int | None]]:
        return [list(c) for c in zip(*self.rows)]

    def won(self) -> bool:
        for row in self.rows:
            if all(n is None for n in row):
                return True
        for col in self.columns:
            if all(n is None for n in col):
                return True
        return False

    @classmethod
    def from_string(cls, s: str) -> "Board":
        return cls(rows=[[*map(int, row.split())] for row in s.splitlines()])

    def mark(self, number: int) -> None | int:
        for row in self.rows:
            for i, num in enumerate(row):
                if num == number:
                    row[i] = None
        if self.won():
            return sum(n for row in self.rows for n in row if n is not None) * number
        else:
            return None


def compute(data):
    """
    >>> compute(_TESTCASE)
    1924
    """
    numbers_drawn, *boards = data.split("\n\n")
    numbers_drawn = [int(n) for n in numbers_drawn.split(",")]

    boards = [Board.from_string(b) for b in boards]

    for num in numbers_drawn:
        for board in boards[:]:
            if result := board.mark(num):
                boards.remove(board)
                if len(boards) == 0:
                    return result
    else:
        raise AssertionError("game should have finished")


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read()))


if __name__ == "__main__":
    main()
