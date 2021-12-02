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
    900
    """
    aim, horizontal, depth = 0, 0, 0

    for command in data:
        instruction, units = command.split()
        units = int(units)

        match instruction:
            case "forward":
                horizontal += units
                depth += aim * units
            case "down":
                aim += units
            case "up":
                aim -= units
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
