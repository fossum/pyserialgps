
from enum import IntEnum

from pyserialgps.messages.base import NMEA0183


class TXT(NMEA0183):

    class MsgType(IntEnum):
        ERROR = 0
        WARNING = 1
        NOTICE = 2
        USER = 3

    def __init__(self, msg: bytes) -> None:
        super().__init__(msg)
        self.total = int(self.message[0])
        self.number = int(self.message[1])
        self.msg_type = TXT.MsgType(int(self.message[2]))
        self.msg = NMEA0183.SEPARATOR.join(self.message[3:])

    def __str__(self):
        return (
            f"{self.type} => {self.msg_type.name}: {self.msg}")


if __name__ == "__main__":
    print(str(TXT(b'$GPTXT,01,01,02,ROM CORE 1.00 (59842) Jun 27 2012 17:43:52*59')))
