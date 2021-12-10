import collections

_TESTCASE = """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""".splitlines()


PAIRS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def compute(data):
    """
    >>> compute(_TESTCASE)
    26397
    """
    errors = collections.Counter()
    for line in data:
        stack = []
        for c in line:
            if c in PAIRS:
                stack.append(c)
            elif PAIRS[stack[-1]] == c:
                stack.pop()
            else:
                errors[c] += 1
                break

    return sum(cnt * POINTS[c] for c, cnt in errors.items())


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().splitlines()))


if __name__ == "__main__":
    main()
