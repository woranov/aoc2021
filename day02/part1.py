_TESTCASE = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2
""".splitlines()


def compute(data):
    """
    >>> compute(_TESTCASE)
    150
    """
    horizontal, depth = 0, 0

    for command in data:
        match command.split():
            case ["forward", units]:
                horizontal += int(units)
            case ["down", units]:
                depth += int(units)
            case ["up", units]:
                depth -= int(units)
            case _:
                assert False

    return horizontal * depth


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().splitlines()))


if __name__ == "__main__":
    main()
