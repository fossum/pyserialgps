
from enum import IntEnum
import re

from pyserialgps.messages.base import NMEA0183, UTCTime


class GGA(NMEA0183):

    _TIME_RE = re.compile(r'^(?P<hour>\d\d)(?P<minute>\d\d)(?P<second>\d\d\.\d+)$')

    class Quality(IntEnum):
        NOT_VALID = 0
        FIX = 1
        DIFF_FIX = 2
        NA = 3
        RTK_FIXED = 4
        RTK_FLOAT = 5
        INS = 6

    def __init__(self, msg: bytes) -> None:
        super().__init__(msg)
        self.utc = GGA._str_to_time(self.message[0])
        self.lat = float(self.message[1])
        self.lat_dir = self.message[2]
        self.lon = float(self.message[3])
        self.lon_dir = self.message[4]
        self.quality = GGA.Quality(int(self.message[5]))
        self.sv_count = int(self.message[6])
        self.hdop = float(self.message[7])
        self.height = float(self.message[8])
        self.height_unit = self.message[9]
        self.geoid_sep = float(self.message[10])
        self.geoid_sep_unit = self.message[11]
        self.age = self.message[12]
        self.station_id = self.message[13]

    def __str__(self):
        return (
            f"{self.type} => "
            f"{self.lat}{self.lat_dir}, {self.lon}{self.lon_dir}; "
            f"elev: {self.height}{self.height_unit}")

    @staticmethod
    def _str_to_time(value: str) -> UTCTime:
        if (match := GGA._TIME_RE.match(value)) is None:
            raise ValueError(f'{value} is an invalid UTC time.')
        return UTCTime(int(match['hour']), int(match['minute']), float(match['second']))


if __name__ == "__main__":
    gga = GGA(b'$GPGGA,014744.00,4742.15468,N,11716.88815,W,1,07,1.09,605.6,M,-17.5,M,,*6F')
    print(gga)