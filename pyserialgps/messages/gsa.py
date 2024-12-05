
from enum import IntEnum, StrEnum

from pyserialgps.messages.base import NMEA0183


class GSA(NMEA0183):

    class Mode(StrEnum):
        MANUAL = 'M'
        AUTOMATIC = 'A'

    class FixType(IntEnum):
        NA = 1
        D2 = 2
        D3 = 3

    def __init__(self, msg: bytes) -> None:
        super().__init__(msg)
        self.mode = GSA.Mode(self.message[0])
        self.fix_type = GSA.FixType(int(self.message[1]))
        self.prn_number = int(self.message[2]) if self.message[2] else None
        self.pdop = float(self.message[3]) if self.message[3] else None
        self.hdop = float(self.message[4]) if self.message[4] else None
        self.vdop = float(self.message[5]) if self.message[5] else None

    def __str__(self):
        return (
            f"{self.type} => "
            f"Mode: {self.mode}, Type: {self.type}, PRN: {self.prn_number}")


if __name__ == "__main__":
    for test_msg in [
        b'$GPGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*30\r\n'
    ]:
        obj = GSA(test_msg)
        print(obj)
