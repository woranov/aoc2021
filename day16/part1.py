from __future__ import annotations

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
    value: int | None = None
    sub_packets: tuple[Packet, ...] = ()

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
                value=int(literal_value_bin_s, 2),
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
    >>> compute("8A004A801A8002F478")
    16
    >>> compute("620080001611562C8802118E34")
    12
    >>> compute("C0015000016115A2E0802F182340")
    23
    >>> compute("A0016C880162017C3686B18A3D4780")
    31
    """
    bin_s = StrView("".join(f"{int(c, 16):04b}" for c in data))
    packet = Packet.parse(bin_s)

    def sum_version_numbers(p: Packet) -> int:
        return p.version_number + sum(
            sum_version_numbers(sub_p) for sub_p in p.sub_packets
        )

    return sum_version_numbers(packet)


def main():
    import pathlib

    input_path = pathlib.Path(__file__).with_name("input.txt")

    with input_path.open() as f:
        print(compute(f.read().strip()))


if __name__ == "__main__":
    main()
