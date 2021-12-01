_TESTCASE = """\
199
200
208
210
200
207
240
269
260
263
""".splitlines()


def compute(data):
    """
    >>> compute(_TESTCASE)
    7
    """
    nums = [int(n) for n in data]
    return sum(n2 > n1 for n1, n2 in zip(nums, nums[1:]))


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().splitlines()))


if __name__ == "__main__":
    main()
