
from dataclasses import dataclass
import logging

from pyserialgps.messages.base import NMEA0183

_last_complete_message: "CompleteGSV | None" = None
_temp_series: "list[GSV]" = []


class GSV(NMEA0183):

    @dataclass
    class PRN:
        number: int
        elevation: int
        azimuth: int
        snr: int | None

    def __init__(self, msg: bytes) -> None:
        super().__init__(msg)
        self.total = int(self.message[0])
        self.number = int(self.message[1])
        self.sv_count = int(self.message[2])
        self.prns = []
        index = 3
        while len(self.message) >= index + 4:
            self.prns.append(GSV.PRN(
                int(self.message[index]),
                int(self.message[index + 1]),
                int(self.message[index + 2]),
                GSV._str_to_int_or_none(self.message[index + 3])
            ))
            index += 4
        self._complete_msg = _update_series(self)

    @staticmethod
    def _str_to_int_or_none(value: str) -> int | None:
        return None if value == '' else int(value)

    def __str__(self):
        return f"{self.type}({self.number}:{self.total}) => Tracking: {', '.join([str(p.number) for p in self.prns])}"

    @property
    def complete_message(self) -> "CompleteGSV | None":
        return self._complete_msg


class CompleteGSV:
    def __init__(self, msgs: list[GSV]) -> None:
        self.msgs = msgs

    @property
    def prns(self) -> tuple[GSV.PRN, ...]:
        return tuple([p for msg in self.msgs for p in msg.prns])

    def __str__(self):
        return f"GSV(complete) => Tracking: {', '.join([str(p.number) for p in self.prns])}"


def _update_series(msg: GSV) -> CompleteGSV | None:
    global _last_complete_message
    global _temp_series

    if msg.number == 1:
        _temp_series = []
    elif len(_temp_series) and msg.number != _temp_series[-1].number + 1:
        logging.getLogger(__name__).warning("GSV message out of order, resetting series")
        _temp_series = []

    _temp_series.append(msg)
    if msg.number == msg.total:
        _last_complete_message = CompleteGSV(_temp_series)
        return _last_complete_message
    return None
