
import logging

from pyserialgps.gps_device import GPS


logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-9s) %(message)s',)
gps = GPS('COM3')

while True:
    input()
    del(gps)
