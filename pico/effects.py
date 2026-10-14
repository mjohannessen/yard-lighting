"""
Effect implementations (solid, cycle, chase, fireflies, scene, off) plus the
internal amber-pulse fail-safe. main.py owns the serial loop only — all
per-effect animation state and stepping lives here.
"""
import math
import random
import time

AMBER = (255, 70, 0)

# fireflies: each fixture flashes FIREFLY_FLASH_MS about every
# FIREFLY_PERIOD_MS, jittered so the fixtures drift and never sync up
FIREFLY_FLASH_MS = 500
FIREFLY_PERIOD_MS = 10_000
FIREFLY_JITTER_MS = 2_000


def _scale(color, brightness):
    b = brightness / 255
    return (int(color[0] * b), int(color[1] * b), int(color[2] * b))


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


class EffectRunner:
    """
    Holds the currently active effect and its animation state. main.py
    calls step() once per loop iteration; timing of each effect's frame
    rate is handled internally so the caller stays effect-agnostic.
    """

    def __init__(self, strip):
        self.strip = strip
        self.effect = None
        self.color = (255, 255, 255)
        self.brightness = 255
        self.speed = 50
        self._offset = 0
        self._last_step_ms = time.ticks_ms()
        self._last_cmd = None
        self.set_command({"effect": "off"})

    def set_command(self, cmd):
        # The bridge re-sends the last command every few seconds as a
        # keepalive. An identical repeat must not restart the animation
        # (cycle/chase would visibly jump back to frame 0 each time).
        if cmd == self._last_cmd:
            return
        self._last_cmd = cmd
        self.effect = cmd.get("effect", "off")
        self.color = tuple(cmd.get("color", (255, 255, 255)))
        self.brightness = cmd.get("brightness", 255)
        self.speed = cmd.get("speed", 50)
        self._offset = 0
        self._last_step_ms = time.ticks_ms()

        if self.effect == "off":
            self.strip.fill((0, 0, 0))
            self.strip.write()
        elif self.effect in ("solid", "scene"):
            # "scene" has no per-zone composition data on the wire (that
            # logic is openHAB's, per CLAUDE.md) — treat it as solid with
            # whatever color/brightness openHAB resolved it to.
            self.strip.fill(_scale(self.color, self.brightness))
            self.strip.write()
        elif self.effect == "fireflies":
            self.strip.fill((0, 0, 0))
            self.strip.write()
            now = time.ticks_ms()
            n = self.strip.num_leds
            # first flashes spread across one period, not all at once
            self._ff_next = [time.ticks_add(now, random.randint(0, FIREFLY_PERIOD_MS)) for _ in range(n)]
            self._ff_start = [None] * n
            self._ff_hue = [random.randint(0, 255) for _ in range(n)]
        # cycle / chase / fireflies / amber_pulse are animated: first frame
        # drawn on the next step() call rather than here.

    def fail_safe(self):
        """Slow amber pulse — used when serial contact is lost or a
        malformed command is received, per CLAUDE.md's fail-safe
        requirement (never go dark, never raise unhandled)."""
        self.set_command({
            "effect": "amber_pulse",
            "color": AMBER,
            "brightness": 255,
            "speed": 10,
        })

    def status(self):
        """Current state as a dict, for the zone's MQTT status topic."""
        return {
            "effect": self.effect,
            "color": list(self.color),
            "brightness": self.brightness,
            "speed": self.speed,
        }

    def _due(self, interval_ms):
        now = time.ticks_ms()
        if time.ticks_diff(now, self._last_step_ms) >= interval_ms:
            self._last_step_ms = now
            return True
        return False

    def step(self):
        if self.effect == "cycle":
            self._step_cycle()
        elif self.effect == "chase":
            self._step_chase()
        elif self.effect == "fireflies":
            self._step_fireflies()
        elif self.effect == "amber_pulse":
            self._step_amber_pulse()
        # solid / off / scene are static — nothing to do per frame.

    def _step_cycle(self):
        interval = 200 - int((self.speed / 100) * 190)  # 200ms..10ms
        if not self._due(interval):
            return
        n = self.strip.num_leds
        for i in range(n):
            c = wheel((i * 256 // n) + self._offset)
            self.strip[i] = _scale(c, self.brightness)
        self.strip.write()
        self._offset = (self._offset + 1) % 256

    def _step_chase(self):
        interval = 300 - int((self.speed / 100) * 280)  # 300ms..20ms
        if not self._due(interval):
            return
        n = self.strip.num_leds
        self.strip.fill((0, 0, 0))
        self.strip[self._offset % n] = _scale(self.color, self.brightness)
        self.strip.write()
        self._offset += 1

    def _step_fireflies(self):
        if not self._due(20):
            return
        now = time.ticks_ms()
        for i in range(self.strip.num_leds):
            start = self._ff_start[i]
            if start is None:
                if time.ticks_diff(now, self._ff_next[i]) < 0:
                    continue  # dark until its next flash
                # new flash: a clearly different colour from this fixture's last
                start = self._ff_start[i] = now
                self._ff_hue[i] = (self._ff_hue[i] + random.randint(40, 216)) % 256
                self._ff_next[i] = time.ticks_add(
                    now, FIREFLY_PERIOD_MS + random.randint(-FIREFLY_JITTER_MS, FIREFLY_JITTER_MS))
            t = time.ticks_diff(now, start)
            if t >= FIREFLY_FLASH_MS:
                self._ff_start[i] = None
                self.strip[i] = (0, 0, 0)
            else:
                # smooth glow up and back down over the flash
                level = math.sin(math.pi * t / FIREFLY_FLASH_MS)
                self.strip[i] = _scale(wheel(self._ff_hue[i]), int(self.brightness * level))
        self.strip.write()

    def _step_amber_pulse(self):
        if not self._due(30):
            return
        self._offset = (self._offset + 1) % 100
        t = self._offset / 100
        level = (t if t < 0.5 else 1 - t) * 2
        self.strip.fill(_scale(AMBER, int(level * 255)))
        self.strip.write()
