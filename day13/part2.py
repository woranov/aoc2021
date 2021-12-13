_TESTCASE = """\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""


def compute(data):
    """
    >>> res = compute(_TESTCASE)
    >>> print(res)
    # # # # #
    #       #
    #       #
    #       #
    # # # # #
    """

    dots_s, folds_s = data.split("\n\n")

    dots = set()
    for dot in dots_s.splitlines():
        dots.add(tuple(map(int, dot.split(","))))

    folds = []
    for fold in folds_s.splitlines():
        _, _, fold_s = fold.rpartition(" ")
        fold_dim, val = fold_s.split("=")
        folds.append((fold_dim, int(val)))

    for fold in folds:
        fold_dim, fold_val = fold
        coord_idx = 0 if fold_dim == "x" else 1

        for dot in dots.copy():
            v = dot[coord_idx]
            if v >= fold_val:
                dots.remove(dot)
                new_dot = list(dot)
                fold_delta = v - fold_val
                new_dot[coord_idx] = fold_val - fold_delta
                dots.add(tuple(new_dot))

    width = max(x for x, _ in dots)
    height = max(y for _, y in dots)

    return "\n".join(
        " ".join("#" if (x, y) in dots else " " for x in range(width + 1))
        for y in range(height + 1)
    )


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read()))


if __name__ == "__main__":
    main()
