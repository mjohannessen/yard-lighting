"""
Bench-test-stage hardware smoke test — see docs/wiring.md Stage 1.

Confirms the physical signal path (Pico GP0 -> 74AHCT125 -> NUM_LEDS x NeoPixel)
before any serial/MQTT protocol exists. Not part of the pico/main.py
dispatch loop.

Sets all LEDs to a single solid color ONCE and holds it — no repeated
writes, no color cycling. Isolates whether flicker is caused by the
repeated np.write() calls / color-change timing, or is present even with
a single static frame (pointing instead at power, ground, or connection
issues that have nothing to do with the data protocol).

Prompts for the number of LEDs over the serial REPL on each run, so the
jig can be repointed at 1 node without editing this file. Requires an
attached REPL session (e.g. `mpremote connect /dev/ttyACM0 repl`, press
Ctrl-D to run) to answer the prompt.
"""
from machine import Pin
from neopixel import NeoPixel

DATA_PIN = 0
COLOR = (255, 255, 255)

while True:
    try:
        NUM_LEDS = int(input("Number of LEDs: "))
        if NUM_LEDS > 0:
            break
    except ValueError:
        pass
    print("Enter a positive integer.")

np = NeoPixel(Pin(DATA_PIN), NUM_LEDS)
for i in range(NUM_LEDS):
    np[i] = COLOR
np.write()

print("Set once to", COLOR, "- holding with no further writes.")
while True:
    pass
