_TESTCASE = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
""".splitlines()


def compute(data):
    """
    >>> compute(_TESTCASE)
    198
    """
    gamma = ""
    epsilon = ""

    n = len(data)

    for pos in zip(*data):
        one_bit_count = pos.count("1")
        if one_bit_count >= n / 2:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"

    return int(gamma, 2) * int(epsilon, 2)


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().splitlines()))


if __name__ == "__main__":
    main()
