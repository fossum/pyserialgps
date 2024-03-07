
from pyserialgps.messages.base import NMEA0183


class GSV(NMEA0183):
    def __init__(self, msg: bytes) -> None:
        super().__init__(msg)

    def __str__(self):
        return f"{self.type} => {self.message}"
