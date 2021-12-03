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
    230
    """

    def find_value(numbers, *, check_for_most_common):
        bit_cnt = len(numbers[0])

        for i in range(bit_cnt):
            one_bit_count = sum(1 for num in numbers if num[i] == "1")
            most_common = 1 if one_bit_count >= len(numbers) / 2 else 0

            if check_for_most_common:
                bit_check = str(most_common)
            else:
                bit_check = str(most_common ^ 1)

            numbers = [num for num in numbers if num[i] == bit_check]

            if len(numbers) == 1:
                break

        return int(numbers[0], 2)

    oxygen = find_value(data.copy(), check_for_most_common=True)
    co2 = find_value(data.copy(), check_for_most_common=False)

    return oxygen * co2


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().splitlines()))


if __name__ == "__main__":
    main()
