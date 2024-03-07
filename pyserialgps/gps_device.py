
import logging
from queue import Queue
import threading
import time

from serial import Serial

from pyserialgps.messages import get_nmea_msg


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

    class _ProducerThread(threading.Thread):
        def __init__(self, group=None, target=None, name=None,
                     args=(), kwargs=None, verbose=None):
            super(GPS._ProducerThread, self).__init__()
            self.target = target
            self.name = name
            self.gps: Serial = args[0]
            self._stop = False
            self._queue = args[1]

        def stop(self):
            self._stop = True

        def run(self):
            while not self._stop:
                if not self._queue.full():
                    line = self.gps.readline()
                    self._queue.put(line)
                    logging.debug(f'Putting {line} : {str(self._queue.qsize())} items in queue')
            return

    class _ConsumerThread(threading.Thread):
        def __init__(self, group=None, target=None, name=None,
                     args=(), kwargs=None, verbose=None):
            super(GPS._ConsumerThread, self).__init__()
            self.target = target
            self.name = name
            self._stop = False
            self._queue = args

        def stop(self):
            self._stop = True

        def run(self):
            while not self._stop:
                if not self._queue.empty():
                    item = self._queue.get()
                    try:
                        gps_msg = get_nmea_msg(item)
                    except ValueError as exc:
                        gps_msg = f"{exc} => {item}"
                    logging.info(f'Getting {str(gps_msg)} : {str(self._queue.qsize())} items in queue')
                    time.sleep(0.1)
