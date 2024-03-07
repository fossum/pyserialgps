
from enum import StrEnum
import re


class LatDir(StrEnum):
    NORTH = 'N'
    SOUTH = 'S'


class LonDir(StrEnum):
    EAST = 'E'
    WEST = 'W'


class NMEA0183:
    START = '$GP'
    SEPARATOR = ','
    CHKSUM_SEPARATOR = '*'
    MSG_RE = re.compile(
        fr'''
            {re.escape(START)}
            (?P<type>\w+),
            (?P<message>[^*]+)
            \*(?P<checksum>[0-9A-F]{{2}})
        ''',
        re.VERBOSE)

    def __init__(self, msg: bytes) -> None:
        self.full_message = msg.decode(encoding='ASCII')
        if (match := NMEA0183.MSG_RE.match(self.full_message)) is None:
            raise ValueError('Could not parse.')
        self.type: str = match['type']
        self.message: list[str] = match['message'].split(NMEA0183.SEPARATOR)
        self.checksum: str = match['checksum']
        if not self.is_checksum_valid():
            raise ValueError(f'Checksum did not match: "{self.full_message}"')

    @staticmethod
    def is_valid(msg: bytes) -> bool:
        full_message = msg.decode(encoding='ASCII')
        return NMEA0183.MSG_RE.match(full_message) is not None

    def is_checksum_valid(self) -> bool:
        return True
