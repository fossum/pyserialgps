
from enum import IntEnum, StrEnum

from pyserialgps.messages.base import NMEA0183, LatDir, LonDir


class RMC(NMEA0183):
    """Position, velocity, and time."""

    class Status(StrEnum):
        ACTIVE = 'A'
        VOID = 'V'

    def __init__(self, msg: bytes) -> None:
        super().__init__(msg)
        self.utc = self.message[0]
        self.status = RMC.Status(self.message[1])
        self.lat = float(self.message[2])
        self.lat_dir = LatDir(self.message[3])
        self.lon = float(self.message[4])
        self.lon_dir = LonDir(self.message[5])
        self.speed = float(self.message[6])
        self.heading = RMC._str_to_float_or_none(self.message[7])
        self.date = self.message[8]
        self.magnetic_variation = RMC._str_to_float_or_none(self.message[9])

    def __str__(self):
        return (
            f"{self.type} => "
            f"{self.lat}{self.lat_dir}, {self.lon}{self.lon_dir}; "
            f"Speed: {self.speed}@{self.heading}")

    @staticmethod
    def _str_to_float_or_none(value: str) -> float | None:
        return None if value == '' else float(value)


if __name__ == "__main__":
    for msg in [b'$GPRMC,023803.00,A,4742.15851,N,11716.89021,W,0.889,,070324,,,A*6C\r\n',
                b'$GPRMC,041433.00,A,4742.16061,N,11716.89280,W,1.278,,070324,,,A*63\r\n']:
        gga = RMC(msg)
    print(gga)