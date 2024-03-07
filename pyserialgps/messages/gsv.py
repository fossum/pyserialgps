
from dataclasses import dataclass

from pyserialgps.messages.base import NMEA0183


class GSV(NMEA0183):

    @dataclass
    class PRN:
        number: int
        elevation: int
        azimuth: int
        snr: int | None

    def __init__(self, msg: bytes) -> None:
        super().__init__(msg)
        self.total = int(self.message[0])
        self.number = int(self.message[1])
        self.sv_count = int(self.message[2])
        self.prns = []
        index = 3
        while len(self.message) >= index + 4:
            self.prns.append(GSV.PRN(
                int(self.message[index]),
                int(self.message[index + 1]),
                int(self.message[index + 2]),
                GSV._str_to_int_or_none(self.message[index + 3])
            ))
            index += 4

    @staticmethod
    def _str_to_int_or_none(value: str) -> int | None:
        return None if value == '' else int(value)

    def __str__(self):
        return f"{self.type} => Tracking: {', '.join([str(p.number) for p in self.prns])}"
