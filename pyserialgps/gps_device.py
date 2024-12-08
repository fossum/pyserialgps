
import asyncio
import logging
from typing import Callable

from pyserialgps.messages import get_nmea_msg
from pyserialgps.messages.base import NMEA0183
from pyserialgps.messages.gsv import GSV


class GPS(asyncio.Protocol):
    BUF_SIZE = 100

    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger(__name__)
        self._buffer = b''
        self._subscribers: list[Callable[[NMEA0183], None]] = []

    def connection_made(self, transport) -> None:
        self.transport = transport

    def data_received(self, data) -> None:
        self._buffer += data
        lines = self._buffer.split(b'\n')
        self._buffer = lines.pop(-1)  # Store the last incomplete line
        for line in lines:
            msg = self.process_message(line)
            if msg is not None:
                self.notify_subscribers(msg)

    def connection_lost(self, exc: Exception | None) -> None:
        print('port closed')
        if exc is not None:
            self._logger.error(exc)
        raise asyncio.CancelledError

    def notify_subscribers(self, msg: NMEA0183):
        def notify(inner_msg):
            self._logger.debug(f'Calling {str(subscriber)}')
            subscriber(inner_msg)

        for subscriber in self._subscribers:
            if isinstance(msg, GSV):
                if msg.complete_message:
                    notify(msg.complete_message)
                pass
            else:
                notify(msg)

    def process_message(self, line: bytes) -> NMEA0183 | None:
        msg = None
        try:
            msg = get_nmea_msg(line)
        except ValueError:
            self._logger.warning(f"Unknown message: {line!r}")
        return msg

    def add_subscriber(self, func: Callable[[NMEA0183], None]):
        self._subscribers.append(func)
