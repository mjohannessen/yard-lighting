"""
MicroPython entry point — serial listener + effect dispatcher only.
Keep this file lean: WS2815 timing is sensitive to anything slow between
receiving a command and driving the string. All effect logic lives in
effects.py.
"""
import sys
import time

import uasyncio as asyncio
import ujson

from ws2811 import Strip
from effects import EffectRunner

DATA_PIN = 0
NUM_LEDS = 50  # set to this zone's actual fixture count before deployment
CONTACT_TIMEOUT_MS = 15_000  # no valid command this long -> fail-safe pulse

strip = Strip(DATA_PIN, NUM_LEDS)
runner = EffectRunner(strip)
last_contact_ms = time.ticks_ms()


async def serial_listener():
    global last_contact_ms
    reader = asyncio.StreamReader(sys.stdin)
    while True:
        line = await reader.readline()
        if not line:
            continue
        try:
            cmd = ujson.loads(line)
        except (ValueError, TypeError):
            runner.fail_safe()
            continue
        runner.set_command(cmd)
        last_contact_ms = time.ticks_ms()
        # One status line per command received. The bridge's keepalive
        # makes this a steady heartbeat on the zone's status topic.
        print(ujson.dumps(runner.status()))


async def watchdog():
    lost = False
    while True:
        await asyncio.sleep_ms(1000)
        timed_out = time.ticks_diff(time.ticks_ms(), last_contact_ms) > CONTACT_TIMEOUT_MS
        if timed_out and not lost:
            runner.fail_safe()
            lost = True
        elif not timed_out:
            lost = False


async def animate():
    faulted = False
    while True:
        try:
            runner.step()
            faulted = False
        except Exception:
            if not faulted:
                runner.fail_safe()
                faulted = True
        await asyncio.sleep_ms(10)


async def main():
    await asyncio.gather(serial_listener(), watchdog(), animate())


asyncio.run(main())
