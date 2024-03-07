
from dataclasses import dataclass
from enum import StrEnum
import re


@dataclass
class UTCTime:
    hour: int
    minute: int
    second: float


class LatDir(StrEnum):
    NORTH = 'N'
    SOUTH = 'S'


class LonDir(StrEnum):
    EAST = 'E'
    WEST = 'W'


class Mode(StrEnum):
    AUTONOMOUS = 'A'
    DIFFERENTIAL = 'D'
    ESTIMATED = 'E'
    MANUAL = 'M'
    SIMULATED = 'S'
    NOT_VALID = 'N'


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
    _TIME_RE = re.compile(r'^(?P<hour>\d\d)(?P<minute>\d\d)(?P<second>\d\d\.\d+)$')

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

    def __str__(self) -> str:
        return self.full_message

    @staticmethod
    def _str_to_float_or_none(value: str) -> float | None:
        return None if value == '' else float(value)

    @staticmethod
    def _str_to_time(value: str) -> UTCTime:
        if (match := NMEA0183._TIME_RE.match(value)) is None:
            raise ValueError(f'{value} is an invalid UTC time.')
        return UTCTime(int(match['hour']), int(match['minute']), float(match['second']))
