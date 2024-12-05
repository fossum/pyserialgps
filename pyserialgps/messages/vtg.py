
from pyserialgps.messages.base import NMEA0183, Mode


class VTG(NMEA0183):

    def __init__(self, msg: bytes) -> None:
        super().__init__(msg)
        self.true_track = NMEA0183._str_to_float_or_none(self.message[0])
        self.true_track_unit = self.message[1]
        self.mag_track = NMEA0183._str_to_float_or_none(self.message[2])
        self.mag_track_unit = self.message[3]
        self.speed = float(self.message[4]) if self.message[4] else None
        self.speed_unit = self.message[5]
        self.speed_ground = float(self.message[6]) if self.message[6] else None
        self.speed_ground_unit = self.message[7]
        self.mode = Mode(self.message[8])

    def __str__(self):
        return (
            f"{self.type} => {self.mode.name} {self.true_track}deg @ {self.speed_ground}KPH")


if __name__ == "__main__":
    for msg in [
        b'$GPVTG,,T,,M,0.765,N,1.416,K,A*25\r\n',
        b'$GPVTG,,T,,M,1.734,N,3.212,K,A*20\r\n',
        b'$GPVTG,,,,,,,,,N*30\r\n'
    ]:
        obj = VTG(msg)
        print(obj)
