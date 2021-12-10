import bisect

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
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def compute(data):
    """
    >>> compute(_TESTCASE)
    288957
    """
    scores = []
    for line in data:
        stack = []
        for c in line:
            if c in PAIRS:
                stack.append(c)
            elif PAIRS[stack[-1]] == c:
                stack.pop()
            else:
                stack.clear()
                break
        if stack:
            score = 0
            for c in reversed(stack):
                score *= 5
                score += POINTS[PAIRS[c]]
            bisect.insort(scores, score)

    return scores[len(scores) // 2]


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().splitlines()))


if __name__ == "__main__":
    main()
