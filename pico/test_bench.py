"""
Bench-test-stage hardware smoke test — see docs/wiring.md Stage 1.

Confirms the physical signal path (Pico GP0 -> 74AHCT125 -> NUM_LEDS x NeoPixel)
before any serial/MQTT protocol exists. Not part of the pico/main.py
dispatch loop.

Displays a rotating rainbow across all LEDs: each position gets a distinct
hue, and the whole pattern shifts over time. With NUM_LEDS=1 this sweeps
that single fixture through the full color wheel. Useful for confirming
per-position data integrity (each fixture should show a different, stable
color, not a corrupted one) and for exercising repeated np.write() calls
at a steady pace, unlike a single static write.

Prompts for the number of LEDs over the serial REPL on each run, so the
jig can be repointed at 1 node or the full daisy-chained count without
editing this file. Requires an attached REPL session (e.g. `mpremote
connect /dev/ttyACM0 repl`, press Ctrl-D to run) to answer the prompt.
"""
from machine import Pin
from neopixel import NeoPixel
import time

DATA_PIN = 0


def wheel(pos):
    """(r, g, b) for a position 0-255 on the color wheel."""
    pos = pos % 256
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


while True:
    try:
        NUM_LEDS = int(input("Number of LEDs: "))
        if NUM_LEDS > 0:
            break
    except ValueError:
        pass
    print("Enter a positive integer.")

np = NeoPixel(Pin(DATA_PIN), NUM_LEDS)

offset = 0
while True:
    for i in range(NUM_LEDS):
        np[i] = wheel((i * 256 // NUM_LEDS) + offset)
    np.write()
    offset = (offset + 1) % 256
    time.sleep(0.05)
