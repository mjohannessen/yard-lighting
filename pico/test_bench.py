"""
Bench-test-stage hardware smoke test — see docs/wiring.md Stage 1.

Confirms the physical signal path (Pico GP0 -> 74AHCT125 -> 2x NeoPixel)
before any serial/MQTT protocol exists. Not part of the pico/main.py
dispatch loop.
"""
from machine import Pin
from neopixel import NeoPixel
import time

NUM_LEDS = 2
DATA_PIN = 0

np = NeoPixel(Pin(DATA_PIN), NUM_LEDS)

COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 255),
]


def set_all(color):
    for i in range(NUM_LEDS):
        np[i] = color
    np.write()


while True:
    for color in COLORS:
        set_all(color)
        time.sleep(1)
    set_all((0, 0, 0))
    time.sleep(1)
