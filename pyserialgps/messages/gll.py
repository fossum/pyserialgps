
from enum import StrEnum

from pyserialgps.messages.base import NMEA0183, Mode


class GLL(NMEA0183):

    class Status(StrEnum):
        NOT_VALID = 'V'
        VALID = 'A'

    def __init__(self, msg: bytes) -> None:
        super().__init__(msg)
        self.lat = float(self.message[0])
        self.lat_dir = self.message[1]
        self.lon = float(self.message[2])
        self.lon_dir = self.message[3]
        self.utc = NMEA0183._str_to_time(self.message[4])
        self.status = GLL.Status(self.message[5])
        self.mode = Mode(self.message[6])

    def __str__(self):
        return (
            f"{self.type} => "
            f"{self.lat}{self.lat_dir}, {self.lon}{self.lon_dir}; "
            f"Status: {self.status.name}; Mode: {self.mode.name}")


if __name__ == "__main__":
    obj = GLL(b'$GPGLL,4742.16226,N,11716.88256,W,060248.00,A,A*76\r\n')
    print(obj)