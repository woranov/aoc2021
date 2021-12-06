def cycle(fish: list[int]) -> list[int]:
    new_l = []

    for f in fish:
        f -= 1
        if f == -1:
            new_l.extend([6, 8])
        else:
            new_l.append(f)
    return new_l


def compute(data):
    """
    >>> compute("3,4,3,1,2")
    5934
    """
    fish = [int(n) for n in data.split(",")]

    for _ in range(80):
        fish = cycle(fish)

    return len(fish)


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read()))


if __name__ == "__main__":
    main()
