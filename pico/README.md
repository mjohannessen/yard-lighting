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
mpremote connect /dev/ttyACM0 cp ~/test_bench.py :main.py
mpremote connect /dev/ttyACM0 reset
```

Copying to `:main.py` makes it auto-run on every boot/reset — no serial
session needs to stay open. `test_bench.py` drives 2 NeoPixels on GP0
through the color sequence red → green → blue → white → off, repeating
every ~5s, to confirm the signal path end to end.

## 4. 74AHCT125 wiring (bench test / single zone)

The 74AHCT125 is a quad buffer — 4 independent channels, each with an input
(`nA`), output (`nY`), and an **active-low** output-enable (`nOE`). CLAUDE.md
uses one chip per two zones (up to 4 zones per chip, 8 zones across 2 chips);
for a single-zone bench test, channel 1 is enough.

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

## Troubleshooting

- **`mpremote ... TransportError: could not enter raw repl`** — the board
  isn't running MicroPython. Either it still has different firmware from a
  previous project, or the last flash was the wrong chip family (see step
  0). Re-flash with the correct `.uf2`.
- **BOOTSEL drive never appears in `lsblk`** — BOOTSEL timing is finicky
  through a hub. Fully unplug, hold the button *before* plugging back in,
  hold for ~2s after, then release.
- **Script runs but LEDs stay dark** — check GP0 → 74AHCT125 pin 2, and
  confirm pin 1 (1OE) is tied to GND, not floating.
