
import logging

import asyncio

from pyserialgps.gps_device import GPS


logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-9s) %(message)s',)


async def main():
    gps = GPS('COM4')
    gps.add_subscriber(print)

    while True:
        input()
        del gps


if __name__ == "__main__":
    asyncio.run(main())
