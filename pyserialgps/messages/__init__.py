
from pyserialgps.messages.base import NMEA0183

from pyserialgps.messages.gga import GGA
from pyserialgps.messages.gsa import GSA
from pyserialgps.messages.gsv import GSV
from pyserialgps.messages.rmc import RMC

_MSG_START_MAP = {
    b'GGA': GGA,
    b'GSV': GSV,
    b'RMC': RMC,
    b'GSA': GSA
}


def get_nmea_msg(msg: bytes) -> NMEA0183:
    if msg.startswith(b'$GP'):
        if func := _MSG_START_MAP.get(msg[3:6]):
            return func(msg)
    raise ValueError(f'Unknown message type: {msg[3:6]}')
