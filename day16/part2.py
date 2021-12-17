from __future__ import annotations

import functools
import typing


class StrView:
    def __init__(self, s: str, i=0):
        self.s = s
        self.i = i

    def read(self, n: int) -> str:
        ret = self.s[self.i : self.i + n]
        self.i += n
        return ret

    def __len__(self):
        return len(self.s) - self.i

    def __str__(self):
        return self.s[self.i :]

    def __repr__(self):
        return f"{type(self).__name__}({self.__str__()!r}, i={self.i!r})"


class Packet(typing.NamedTuple):
    version_number: int
    type_id: int
    literal_value: int | None = None
    sub_packets: tuple[Packet, ...] = ()

    def value(self) -> int:
        match self.type_id:
            case 0:  # sum
                return sum(p.value() for p in self.sub_packets)
            case 1:  # product
                return functools.reduce(
                    lambda a, b: a * b, (p.value() for p in self.sub_packets), 1
                )
            case 2:  # min
                return min(p.value() for p in self.sub_packets)
            case 3:  # max
                return max(p.value() for p in self.sub_packets)
            case 4:  # value
                return self.literal_value
            case 5:  # greater-than
                return int(self.sub_packets[0].value() > self.sub_packets[1].value())
            case 6:  # less than
                return int(self.sub_packets[0].value() < self.sub_packets[1].value())
            case 7:  # equal
                return int(self.sub_packets[0].value() == self.sub_packets[1].value())
            case _:
                raise NotImplementedError(f"invalid type id: {self.type_id}")

    @classmethod
    def parse(cls, bin_s: StrView) -> Packet:
        version_number = int(bin_s.read(3), 2)
        type_id = int(bin_s.read(3), 2)

        if type_id == 4:
            literal_value_bin_s = ""
            while True:
                group = bin_s.read(5)
                literal_value_bin_s += group[1:]
                if group[0] == "0":
                    break

            return cls(
                version_number=version_number,
                type_id=type_id,
                literal_value=int(literal_value_bin_s, 2),
            )
        else:
            if bin_s.read(1) == "0":
                sub_packets_len = int(bin_s.read(15), 2)
                max_i = bin_s.i + sub_packets_len
                sub_packets = []
                while bin_s.i < max_i:
                    sub_packet = Packet.parse(bin_s)
                    sub_packets.append(sub_packet)

                return cls(
                    version_number=version_number,
                    type_id=type_id,
                    sub_packets=tuple(sub_packets),
                )
            else:
                num_sub_packets = int(bin_s.read(11), 2)
                sub_packets = []
                for _ in range(num_sub_packets):
                    sub_packet = Packet.parse(bin_s)
                    sub_packets.append(sub_packet)
                return cls(
                    version_number=version_number,
                    type_id=type_id,
                    sub_packets=tuple(sub_packets),
                )


def compute(data):
    """
    >>> compute("C200B40A82")
    3
    >>> compute("04005AC33890")
    54
    >>> compute("880086C3E88112")
    7
    >>> compute("CE00C43D881120")
    9
    >>> compute("D8005AC2A8F0")
    1
    >>> compute("F600BC2D8F")
    0
    >>> compute("9C005AC2F8F0")
    0
    >>> compute("9C0141080250320F1802104A08")
    1
    """
    bin_s = StrView("".join(f"{int(c, 16):04b}" for c in data))
    packet = Packet.parse(bin_s)

    return packet.value()


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().strip()))


if __name__ == "__main__":
    main()
