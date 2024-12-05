
from enum import StrEnum

from timezonefinder import TimezoneFinder

from pyserialgps.messages.base import NMEA0183, Coordinate, LatDir, LonDir, Mode


class Status(StrEnum):
    NOT_VALID = 'V'
    VALID = 'A'


class GLL(NMEA0183):

    _timezone_finder = TimezoneFinder()

    def __init__(self, msg: bytes) -> None:
        super().__init__(msg)
        self.lat = Coordinate.from_nmea_coordinate(self.message[0]) if self.message[0] else None
        self.lat_dir = LatDir(self.message[1])
        self.lon = Coordinate.from_nmea_coordinate(self.message[2]) if self.message[2] else None
        self.lon_dir = LonDir(self.message[3])
        self.utc = NMEA0183._str_to_time(self.message[4])
        self.status = Status(self.message[5])
        self.mode = Mode(self.message[6])

    def __str__(self):
        return (
            f"{self.type} => "
            f"{self.lat}{self.lat_dir}, {self.lon}{self.lon_dir}; "
            f"Status: {self.status.name}; Mode: {self.mode.name}; "
            f"UTC Time: {self.utc}; Zone: {self.timezone}"
        )

    @property
    def timezone(self) -> str | None:
        return GLL._timezone_finder.timezone_at(
            lng=self.lon.to_degrees(self.lon_dir),
            lat=self.lat.to_degrees(self.lat_dir)
        ) if self.status == Status.VALID else None


if __name__ == "__main__":
    for test_msg in [
        b"$GPGLL,,,,,011622.00,V,N*4C\r\n",
        b"$GPGLL,4742.16226,N,11716.88256,W,060248.00,A,A*76\r\n"
    ]:
        print(GLL(test_msg))
