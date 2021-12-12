import collections
import typing

_TESTCASE1 = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""".splitlines()


_TESTCASE2 = """\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""".splitlines()


_TESTCASE3 = """\
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
""".splitlines()


def paths(
    cave_map: dict[str, set[str]], curr_path: list[str]
) -> typing.Iterator[list[str]]:
    for next_cave in cave_map[curr_path[-1]]:
        if next_cave.islower() and next_cave in curr_path:
            continue
        else:
            yield from paths(cave_map, curr_path + [next_cave])
    else:
        if curr_path[-1] == "end":
            yield curr_path


def compute(data):
    """
    >>> compute(_TESTCASE1)
    10
    >>> compute(_TESTCASE2)
    19
    >>> compute(_TESTCASE3)
    226
    """
    cave_map = collections.defaultdict(set)
    for cave1, cave2 in (edge.split("-") for edge in data):
        cave_map[cave1].add(cave2)
        cave_map[cave2].add(cave1)

    return sum(1 for _ in paths(cave_map, ["start"]))


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().splitlines()))


if __name__ == "__main__":
    main()
