_TESTCASE = """\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""".splitlines()


def compute(data):
    """
    >>> compute(_TESTCASE)
    61229
    """
    n = 0

    for patterns, output in [line.split(" | ") for line in data]:
        patterns = patterns.split()
        output = output.split()

        nums: dict[int, frozenset] = {}
        five_segments = set()
        six_segments = set()

        for pattern in map(frozenset, patterns):
            match len(pattern):
                case 2:
                    nums[1] = pattern
                case 3:
                    nums[7] = pattern
                case 4:
                    nums[4] = pattern
                case 7:
                    nums[8] = pattern
                case 5:
                    five_segments.add(pattern)
                case 6:
                    six_segments.add(pattern)
                case _ as seg_count:
                    raise AssertionError(f"invalid segment count: {seg_count}")

        # fmt:off
        # 4 proper subset of 9
        nums[9], = (pat for pat in six_segments if pat > nums[4])
        # 6 and 1 share a single segment
        nums[6], = (pat for pat in six_segments if len(nums[1] - pat) == 1)
        nums[0], = six_segments - {nums[6], nums[9]}

        # 5 proper subset of 6
        nums[5], = (pat for pat in five_segments if pat < nums[6])
        # 3 proper subset of 9
        nums[3], = (pat for pat in five_segments - {nums[5]} if pat < nums[9])
        nums[2], = five_segments - {nums[3], nums[5]}
        # fmt:on

        pattern_to_num = {pat: n for n, pat in nums.items()}

        n += sum(
            pattern_to_num[frozenset(digit)] * 10 ** exp
            for exp, digit in zip(range(len(output) - 1, -1, -1), output)
        )

    return n


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().splitlines()))


if __name__ == "__main__":
    main()
