# Pico Firmware — MicroPython Setup & Bench Test

Covers flashing MicroPython onto a Pico and running the bench-test script
(`test_bench.py`) to validate the Pico → 74AHCT125 → LED signal path before
any serial/MQTT protocol exists. See [docs/wiring.md](../docs/wiring.md) for
the bench-test-stage vs. field-deployment wiring context.

## 0. Identify the board before flashing

- Pi zero is at 192.168.1.120

CLAUDE.md specifies RP2350 Pico 2 (standard, not Pico 2 W) as the architecture
constraint, but **confirm the actual chip on each board** before flashing —
don't assume, since earlier boards bought before the fleet standardized may
still be RP2040. Put the Pico in BOOTSEL mode (see step 2) and check:

```bash
dmesg | tail -20
```

Look at the `Product:` string:
- `Pico Boot` → RP2040 → use the `RPI_PICO` firmware
- `RP2350 Boot` → RP2350 (Pico 2 generation) → use the `RPI_PICO2` firmware

Flashing the wrong family's `.uf2` doesn't brick the board, but the
bootloader silently rejects the mismatched image — the board just stays in
BOOTSEL mode with no error and no `/dev/ttyACM0` ever appears, which looks
identical to a stuck/failed flash.

## 1. Install mpremote (on the Pi)

Raspberry Pi OS Bookworm blocks bare `pip install` outside a venv (PEP 668),
so use `pipx`:

```bash
sudo apt update && sudo apt install -y pipx
pipx install mpremote
pipx ensurepath
# reopen the shell (or `source ~/.bashrc`) so mpremote is on PATH
mpremote --version
```

If `pipx` isn't available, fall back to:
```bash
sudo apt install -y python3-pip
python3 -m pip install --user --break-system-packages mpremote
```

## 2. Flash MicroPython

1. Unplug the Pico's USB cable.
2. **Press and hold BOOTSEL**, plug the cable back in while still holding
   it, wait ~2 seconds, then release. It enumerates as a USB mass-storage
   drive instead of a serial port.
3. Confirm with `lsblk` — a new small (~128MB) disk appears (e.g. `sda1`).
4. Download the firmware matching the chip identified in step 0 (check
   https://micropython.org/download/ for the current release if these exact
   URLs have moved on):
   ```bash
   # RP2040 ("Pico Boot"):
   wget https://micropython.org/resources/firmware/RPI_PICO-20260406-v1.28.0.uf2 -O ~/micropython-pico.uf2

   # RP2350 ("RP2350 Boot", Pico 2 generation):
   wget https://micropython.org/resources/firmware/RPI_PICO2-20260406-v1.28.0.uf2 -O ~/micropython-pico2.uf2
   ```
5. Mount and copy:
   ```bash
   sudo mkdir -p /mnt/pico
   sudo mount /dev/sda1 /mnt/pico   # adjust device name per lsblk
   sudo cp ~/micropython-pico2.uf2 /mnt/pico/   # or micropython-pico.uf2 for RP2040
   sync
   ```
   The Pico reboots on its own once the copy finishes and the mass-storage
   drive disappears — that's normal, not an error.
6. Confirm it's back as a serial device:
   ```bash
   ls /dev/ttyACM*
   ```

## 3. Deploy and run the bench test

```bash
cd ~/Documents/yard-lighting
git pull
mpremote connect /dev/ttyACM0 cp pico/test_bench.py :main.py
mpremote connect /dev/ttyACM0 repl
[enter]
[>>>]
CTRL-D
[enter number of leds]

```

Copying to `:main.py` makes it run on every boot/reset — but copying alone
doesn't trigger that reset, so after `repl` connects you'll just see a
blank prompt. Press **Ctrl-D** to soft-reset the board; that runs
`main.py`, which immediately prints:

```
Number of LEDs:
```

Type the count of NeoPixels currently wired on GP0 (e.g. `1` when
isolating a single fixture on the test jig) and press Enter. It then
drives a rotating rainbow across all of them — each LED position gets a
distinct hue, and the pattern shifts continuously — to confirm the signal
path end to end. With a single LED it just sweeps that one fixture through
the full color wheel.

To disconnect the REPL without resetting the board, press **Ctrl-]**. To
re-run with a different LED count, reconnect (`mpremote connect
/dev/ttyACM0 repl`) and press Ctrl-D again.

## 4. 74AHCT125 wiring (bench test / single zone)

The 74AHCT125 is a quad buffer — 4 independent channels, each with an input
(`nA`), output (`nY`), and an **active-low** output-enable (`nOE`). CLAUDE.md's
build uses a single chip, all 4 channels, one per zone (the project is capped
at 4 zones); for a single-zone bench test, channel 1 is enough.

DIP-14 SN74AHCT125N pinout, channel 1:

| Signal | Pin | Connects to |
|---|---|---|
| 1A (input) | 2 | Pico GP0 |
| 1Y (output) | 3 | → 300–470Ω resistor → LED strip DIN |
| 1OE (output enable, active-low) | 1 | Tie to GND |
| VCC | 14 | 5V rail |
| GND | 7 | Common ground (Pico GND + LED GND) |

**1OE must be tied to GND**, not left floating — floating output-enable is
undefined logic and can leave the channel not driving at all, which looks
identical to a GP0-not-connected fault (LEDs just stay dark with no error
anywhere).

For additional zones on the same chip, repeat with channel 2 (2A=pin5,
2Y=pin6, 2OE=pin4), channel 3 (3A=pin9, 3Y=pin8, 3OE=pin10), and channel 4
(4A=pin12, 4Y=pin11, 4OE=pin13) — VCC/GND (pins 14/7) are shared across all
four channels on the chip.

## 5. Serial JSON protocol (main.py / effects.py / ws2811.py)

These three files replace `test_bench.py` as the actual field firmware.
They implement the JSON command protocol matching CLAUDE.md's MQTT
payload schema, so a command received over serial has the same shape as
what openHAB publishes to `garden/lights/zone/{n}/set`.

- **`ws2811.py`** — thin wrapper around MicroPython's built-in
  `neopixel.NeoPixel`, exactly as bench-validated in `test_bench.py`. Do
  not modify without re-running that bench verification.
- **`effects.py`** — `EffectRunner` holds the active effect
  (`solid` | `cycle` | `chase` | `scene` | `off`) and its animation
  state; `step()` is called once per loop iteration and internally
  decides when to advance a frame. Also owns the internal `amber_pulse`
  fail-safe (not part of the MQTT schema — used only when serial contact
  is lost or a command fails to parse).
- **`main.py`** — the lean serial loop: `uasyncio` runs three tasks —
  `serial_listener()` (reads newline-delimited JSON off `sys.stdin` via
  `asyncio.StreamReader`, dispatches to `EffectRunner.set_command()`),
  `animate()` (calls `EffectRunner.step()` every 10ms), and `watchdog()`
  (triggers the fail-safe if no valid command arrives within
  `CONTACT_TIMEOUT_MS`, 15s by default).

**`NUM_LEDS` in `main.py` is a placeholder (50)** — set it to this zone's
actual fixture count before deploying to the field. It's per-file, not
derived from the wire protocol, so it has to be edited per zone if zones
differ in fixture count.

**Deploy:**
```bash
mpremote connect /dev/ttyPICOn cp pico/ws2811.py :ws2811.py
mpremote connect /dev/ttyPICOn cp pico/effects.py :effects.py
mpremote connect /dev/ttyPICOn cp pico/main.py :main.py
mpremote connect /dev/ttyPICOn reset
```

**`mpremote` always interrupts a running `main.py`.** Every `mpremote`
command — `fs ls`, `exec`, even a failed one — sends Ctrl-C first to sync
the REPL, which raises `KeyboardInterrupt` in whatever's running and
drops the board to an idle REPL. It does **not** restart `main.py`
afterward; the board just sits idle until you explicitly run `mpremote
connect /dev/ttyPICOn reset`. So checking "is it running?" via any
`mpremote` command is itself destructive — don't use it as a health
check. After any `mpremote` session touches a port, always follow with
`reset` before assuming the firmware is live again.

**Never run `mpremote` against a port while `pi/bridge.py` has it open.**
Both processes can technically open the same `/dev/ttyPICOn`, but the
concurrent access causes `mpremote` to hang until it times out rather
than fail cleanly — it looks like the board is unresponsive when it's
actually just port contention. Stop `bridge.py` first, do the `mpremote`
work, reset, then restart `bridge.py`.

**Sending a test command** (what `pi/bridge.py` will eventually do via
`pyserial-asyncio`) — a single newline-terminated JSON line to the port:
```bash
echo '{"effect":"solid","color":[0,255,0],"brightness":180}' > /dev/ttyPICOn
```

**Fail-safe:** malformed JSON, or 15s with no valid command, switches to
a slow amber breathing pulse rather than going dark or crashing, per
CLAUDE.md's fail-safe requirement.

**Keepalive + status:** `pi/bridge.py` re-sends each zone's last command
every `KEEPALIVE_INTERVAL_S` (5s, in `pi/config.py`) so the 15s watchdog
only fires on a real outage, not between openHAB commands. `EffectRunner`
ignores a command identical to the current one, so repeats don't restart
`cycle`/`chase` animations. After every command it receives, the Pico
prints one JSON status line (`effect`, `color`, `brightness`, `speed`),
which the bridge publishes to `garden/lights/zone/{n}/status`. With the
keepalive, that's a heartbeat every 5s per zone. Until a zone has received
its first command after a bridge restart, it has nothing to repeat and
falls back to amber after 15s.

**Bench-tested 2026-09-16** on Fixture 1 (zone 1) with `NUM_LEDS=1`:
`solid` and `cycle` confirmed working end-to-end (JSON → serial → parse →
LED). The amber-pulse fail-safe was exercised but not conclusively
confirmed visually — re-check before relying on it.

**Update 2026-09-16 (later, all 4 zones + `pi/bridge.py`):** scaling to
a real 5-fixture zone-1 string and all 4 zones surfaced two bugs the
single-LED test above didn't catch — see
[docs/wiring.md](../docs/wiring.md) Stage 1.5 for the full writeup:
zones 2–4 had never actually been deployed with this firmware (still
running the old `test_bench.py`, blocked forever at its `input()`
prompt), and `ws2811.py` had a red/green channel swap (fixed — see its
docstring). Full color test (red/green/blue/white) and all 4 zones now
confirmed correct through `pi/bridge.py` end-to-end.

## Troubleshooting

- **`mpremote ... TransportError: could not enter raw repl`** — usually
  means another process (most likely `pi/bridge.py`) already has that
  port open; stop it and retry. If that's not it, the board may not be
  running MicroPython at all (different firmware from a previous
  project, or the last flash was the wrong chip family — see step 0);
  re-flash with the correct `.uf2`.
- **BOOTSEL drive never appears in `lsblk`** — BOOTSEL timing is finicky
  through a hub. Fully unplug, hold the button *before* plugging back in,
  hold for ~2s after, then release.
- **Script runs but LEDs stay dark** — check GP0 → 74AHCT125 pin 2, and
  confirm pin 1 (1OE) is tied to GND, not floating.
- **LED shows a wrong color instead of the one commanded** (e.g. solid
  white comes out green or blue, and it's a *different* wrong color on a
  different run of the same script) — check that the LED's power supply
  ground and the Pico/74AHCT125 ground are actually tied together, not
  just both eventually routed to the same fixture. Without a common
  ground the node has no shared reference for the data signal's high/low
  thresholds, so it latches whatever crosses threshold rather than the
  intended value — confirmed root cause on the bench jig, see
  [docs/fixture_test_jig.md](../docs/fixture_test_jig.md).
