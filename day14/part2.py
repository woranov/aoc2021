import collections
import functools

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
    2188189693529
    """
    template, rules_s = data.split("\n\n")
    rules = dict(line.split(" -> ") for line in rules_s.splitlines())

    counts = collections.Counter()
    pairs = list(zip(template, template[1:]))

    @functools.lru_cache(maxsize=None)
    def calc_pair(c1, c2, n):
        if n == 0:
            return collections.Counter(c1)

        new_c = rules[c1 + c2]
        return calc_pair(c1, new_c, n - 1) + calc_pair(new_c, c2, n - 1)

    counts[pairs[-1][-1]] += 1
    for pair in pairs:
        counts.update(calc_pair(*pair, 40))

    most_common, *_, least_common = [count for _, count in counts.most_common()]

    return most_common - least_common


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read()))


if __name__ == "__main__":
    main()
