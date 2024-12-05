from enum import StrEnum

from pyserialgps.messages.base import NMEA0183, LatDir, LonDir, UTCTime


class RMC(NMEA0183):
    """Position, velocity, and time."""

    class Status(StrEnum):
        """GPS status."""
        ACTIVE = 'A'
        VOID = 'V'

    def __init__(self, msg: bytes) -> None:
        """Constructor for RMC.

        Args:
            msg (bytes): Raw NMEA message.
        """
        super().__init__(msg)
        self._utc = NMEA0183._str_to_time(self.message[0])
        self._status = RMC.Status(self.message[1])
        self._lat = float(self.message[2]) if self.message[2] else None
        self._lat_dir = LatDir(self.message[3])
        self._lon = float(self.message[4]) if self.message[4] else None
        self._lon_dir = LonDir(self.message[5])
        self._speed = float(self.message[6]) if self.message[6] else None
        self._heading = NMEA0183._str_to_float_or_none(self.message[7])
        self._date = self.message[8]
        self._magnetic_variation = NMEA0183._str_to_float_or_none(self.message[9])

    @property
    def utc(self) -> UTCTime:
        """UTC time."""
        return self._utc

    @property
    def status(self) -> Status:
        """GPS status."""
        return self._status

    @property
    def lat(self) -> float:
        """Latitude."""
        return self._lat

    @property
    def lat_dir(self) -> LatDir:
        """Latitude direction."""
        return self._lat_dir

    @property
    def lon(self) -> float:
        """Longitude."""
        return self._lon

    @property
    def lon_dir(self) -> LonDir:
        """Longitude direction."""
        return self._lon_dir

    @property
    def speed(self) -> float:
        """Speed over ground."""
        return self._speed

    @property
    def heading(self) -> float | None:
        """True course over ground."""
        return self._heading

    @property
    def date(self) -> str:
        """Date."""
        return self._date

    @property
    def magnetic_variation(self) -> float | None:
        """Magnetic variation."""
        return self._magnetic_variation

    def __str__(self):
        return (
            f"{self.type} => "
            f"{self.lat}{self.lat_dir}, {self.lon}{self.lon_dir}; "
            f"Speed: {self.speed}@{self.heading}")


if __name__ == "__main__":
    for MSG in [
        b'$GPRMC,023803.00,A,4742.15851,N,11716.89021,W,0.889,,070324,,,A*6C\r\n',
        b'$GPRMC,041433.00,A,4742.16061,N,11716.89280,W,1.278,,070324,,,A*63\r\n',
        b'$GPRMC,012706.00,V,,,,,,,041224,,,N*7E\r\n'
    ]:
        gga = RMC(MSG)
        print(gga)
