def get_cost(crabs, align_at):
    return int(
        sum(
            # partial sum formula n(n+1)/2
            ((n := abs(align_at - c)) * (n + 1) / 2)
            for c in crabs
        )
    )


def compute(data):
    """
    >>> compute("16,1,2,0,4,2,7,1,2,14")
    168
    """
    crabs = [int(n) for n in data.split(",")]
    min_c, max_c = min(crabs), max(crabs)

    return min(get_cost(crabs, n) for n in range(min_c, max_c + 1))


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read()))


if __name__ == "__main__":
    main()
