
import logging

import asyncio

import serial_asyncio

from pyserialgps.gps_device import GPS


logging.basicConfig(
    level=logging.INFO,
    format='(%(threadName)-9s) %(message)s',
)


async def main():
    loop = asyncio.get_event_loop()
    transport, gps = await serial_asyncio.create_serial_connection(
        loop, lambda: GPS(), "COM4", baudrate=115200
    )
    gps.add_subscriber(print)

    await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
