import collections

_TESTCASE = """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""


def compute(data):
    """
    >>> compute(_TESTCASE)
    1588
    """
    template, rules_s = data.split("\n\n")
    rules = dict(line.split(" -> ") for line in rules_s.splitlines())

    for _ in range(10):
        new_template = template[0]
        for c1, c2 in zip(template, template[1:]):
            new_template += rules[c1 + c2] + c2
        template = new_template

    counts = collections.Counter(template)
    most_common, *_, least_common = [count for _, count in counts.most_common()]

    return most_common - least_common


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read()))


if __name__ == "__main__":
    main()
