
import logging
from queue import Queue
import threading
import time
from typing import Callable

from serial import Serial

from pyserialgps.messages import get_nmea_msg
from pyserialgps.messages.base import NMEA0183
from pyserialgps.messages.gsv import GSV


class GPS:
    BUF_SIZE = 100

    def __init__(self, port: str) -> None:
        self._queue: Queue = Queue(GPS.BUF_SIZE)
        self.device = Serial(port)
        self.producer = GPS._ProducerThread(name='producer', args=(self.device, self._queue))
        self.consumer = GPS._ConsumerThread(name='consumer', args=(self._queue))

        self.producer.start()
        self.consumer.start()

    def __del__(self):
        self.producer.stop()
        self.consumer.stop()

    def add_subscriber(self, func: Callable[[NMEA0183], None]):
        self.consumer.add_subscriber(func)

    class _ProducerThread(threading.Thread):
        def __init__(self, group=None, target=None, name=None,
                     args=(), kwargs=None, _verbose=None):
            super(GPS._ProducerThread, self).__init__()
            self.target = target
            self.name = name
            self.gps: Serial = args[0]
            self._stop = False
            self._queue = args[1]
            self._logger = logging.getLogger(self.name)

        def stop(self):
            self._stop = True

        def run(self):
            while not self._stop:
                if not self._queue.full():
                    line = self.gps.readline()
                    self._queue.put(line)
                    self._logger.debug(f'Putting {line} : {str(self._queue.qsize())} items in queue')
            return

    class _ConsumerThread(threading.Thread):
        def __init__(self, group=None, target=None, name=None,
                     args=(), kwargs=None, _verbose=None):
            super(GPS._ConsumerThread, self).__init__()
            self.target = target
            self.name = name
            self._stop = False
            self._queue = args
            self._subscribers = []
            self._logger = logging.getLogger(self.name)

        def stop(self):
            self._stop = True

        def add_subscriber(self, func: Callable[[NMEA0183], None]):
            self._subscribers.append(func)

        def run(self):
            while not self._stop:
                if not self._queue.empty():
                    item = self._queue.get()
                    try:
                        gps_msg = get_nmea_msg(item)
                    except ValueError as exc:
                        gps_msg = f"{exc} => {item}"
                    self._logger.debug(f'Getting {str(gps_msg)} : {str(self._queue.qsize())} items in queue')
                    if isinstance(gps_msg, NMEA0183):
                        for subscriber in self._subscribers:
                            logging.debug(f'Calling {str(subscriber)}')
                            if isinstance(gps_msg, GSV):
                                if gps_msg.complete_message:
                                    subscriber(gps_msg.complete_message)
                            else:
                                subscriber(gps_msg)
                else:
                    time.sleep(5)
