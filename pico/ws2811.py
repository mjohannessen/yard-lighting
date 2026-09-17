"""
WS2815 single-line (WS2811-style) driver — thin wrapper around
MicroPython's built-in neopixel.NeoPixel, exactly as bench-validated in
test_bench.py (see docs/fixture_test_jig.md for the ground-fault
diagnosis that confirmed this timing is sound on the real fixture chain).
Do not modify the timing/write path without re-running that bench
verification.

Color order: MicroPython's built-in NeoPixel hardcodes GRB wire order
(matching WS2812-style chips). These WS2815 fixtures wire RGB order
instead — confirmed 2026-09-16 by sending solid red/green to a real
deployed 5-fixture zone 1 string and observing them swapped. Strip
compensates by swapping R/G before handing off to NeoPixel, whose own
GRB conversion then lands the correct channel on the wire.
"""
from machine import Pin
from neopixel import NeoPixel


def _to_wire_order(color):
    r, g, b = color
    return (g, r, b)


class Strip:
    def __init__(self, data_pin, num_leds):
        self.num_leds = num_leds
        self._np = NeoPixel(Pin(data_pin), num_leds)

    def __setitem__(self, index, color):
        self._np[index] = _to_wire_order(color)

    def __getitem__(self, index):
        r, g, b = self._np[index]
        return (g, r, b)

    def fill(self, color):
        wire_color = _to_wire_order(color)
        for i in range(self.num_leds):
            self._np[i] = wire_color

    def write(self):
        self._np.write()
