
from enum import IntEnum

from pyserialgps.messages.base import NMEA0183, LatDir, LonDir


class GGA(NMEA0183):

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
        self.utc = NMEA0183._str_to_time(self.message[0])
        self.lat = float(self.message[1]) if self.message[1] else None
        self.lat_dir = LatDir(self.message[2])
        self.lon = float(self.message[3]) if self.message[3] else None
        self.lon_dir = LonDir(self.message[4])
        self.quality = GGA.Quality(int(self.message[5]))
        self.sv_count = int(self.message[6])
        self.hdop = float(self.message[7]) if self.message[7] else None
        self.height = float(self.message[8]) if self.message[8] else None
        self.height_unit = self.message[9]
        self.geoid_sep = float(self.message[10]) if self.message[10] else None
        self.geoid_sep_unit = self.message[11]
        self.age = self.message[12]
        self.station_id = self.message[13]

    def __str__(self):
        return (
            f"{self.type} => "
            f"{self.lat}{self.lat_dir}, {self.lon}{self.lon_dir}; "
            f"elev: {self.height}{self.height_unit}")


if __name__ == "__main__":
    for test_msg in [
        b'$GPGGA,014744.00,4742.15468,N,11716.88815,W,1,07,1.09,605.6,M,-17.5,M,,*6F',
        b'$GPGGA,012706.00,,,,,0,00,99.99,,,,,,*64\r\n'
    ]:
        obj = GGA(test_msg)
        print(obj)
