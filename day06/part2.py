import collections

TIMER = 8
RESET_TIMER = 6


def fish_count(fish: list[int], days) -> int:
    counter = collections.Counter(fish)

    for d in range(days):
        new_counter = collections.Counter()
        new_counter[RESET_TIMER] = new_counter[TIMER] = counter[0]

        for k, v in counter.items():
            if k == 0:
                continue
            else:
                new_counter[k - 1] += v

        counter = new_counter

    return sum(counter.values())


def compute(data):
    """
    >>> compute("3,4,3,1,2")
    26984457539
    """
    fish = [int(n) for n in data.split(",")]

    return fish_count(fish, 256)


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read()))


if __name__ == "__main__":
    main()
