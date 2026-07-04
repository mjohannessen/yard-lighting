# CLAUDE.md — Garden LED Lighting Control System

This file provides context for Claude Code sessions on this project. Read it fully before making any changes.

## Project Purpose

Distributed outdoor RGB LED garden lighting system. RP2040 Picos drive WS2815 LED strings via daisy-chained underground 4-wire cable runs. A Raspberry Pi Zero 2 W bridges MQTT (from openHAB on a Mac Mini) to USB serial commands for each Pico. All control hardware is co-located in a weatherproof hub box in the garden.

## Architecture Constraints — Do Not Change Without Discussion

- **One Pico per zone.** Each Pico drives exactly one daisy-chained WS2815 string. Do not attempt to drive multiple strings from one Pico.
- **USB serial only** for Pi↔Pico communication. No WiFi, no RS-485. Picos are co-located with the Pi inside the hub box.
- **MicroPython on Picos.** Do not suggest CircuitPython or C SDK unless there is a hard performance reason.
- **Python asyncio on Pi.** The bridge script uses `aiomqtt` and `pyserial-asyncio`. Do not introduce threading or synchronous serial blocking calls.
- **Two buck converters.** 24V→5V for Pi Zero 2 W/Picos, 24V→12V for LED strings. Do not assume a single shared voltage bus for both.
- **74AHCT125 level shifter** on every Pico data line. Pico outputs 3.3V; WS2815 DIN requires 5V logic. Never connect GP0 directly to a string without the shifter.
- **WS2815 LED protocol.** WS2815 is wire-compatible with WS2812B (same single-wire protocol) but operates at 12V and has a backup data line (DOUT). The MicroPython NeoPixel library works with WS2815. Do not reference WS2812B specs for voltage or current draw.
- **openHAB is the authority** for schedules, scenes, and automation logic. Keep intelligence in openHAB rules, not in the Pi bridge script. The bridge is a dumb forwarder.

## Hardware

### Conduit runs to hub box (pull all three while trench is open)
- **Cat6 #1** — PoE camera #1 (dedicated, direct to camera)
- **Cat6 #2** — Pi Zero 2 W network (via USB-ethernet adapter); reserved for future PoE camera #2. When second camera is added, insert a small PoE-aware switch at the box end — no rewiring needed.
- **12/2 landscape wire** — 24V/300W power feed

### Hub box contents
- Raspberry Pi Zero 2 W
- 1× USB-OTG hub (connects to Pi's single micro-USB OTG port; provides ports for ethernet adapter + Pico USB hub)
- 1× USB-ethernet adapter (connects Pi to Cat6 #2)
- 4–8× RP2040 Pico (standard, not Pico W)
- 1× powered USB hub (7+ port, for Picos)
- 1× 24V→5V buck converter, 5A rated (Pi, Picos, USB hub)
- 1× 24V→12V buck converter, 5A rated (all WS2815 LED strings)
- 2× 74AHCT125 quad level shifter (one chip per two zones, covers up to 8 zones)

### Underground cable per zone (daisy-chain, fixture to fixture)
- Red 18AWG — 12V power
- Black 18AWG — GND
- Yellow 22AWG — Data In (WS2815 DIN)
- White 22AWG — Data Out (WS2815 DOUT backup line)
- Spliced at each fixture with direct burial gel connectors (Dryconn) for power/GND only
- Data connections only at fixture PCB pins — no inline data splices

### Per zone (in hub box)
- 300–470Ω resistor on data line (at 74AHCT125 output, before underground cable)
- 100µF capacitor across 12V/GND at first fixture input connector
- IP67/IP68 4-pin weatherproof connector at hub box exit

### Pico pin assignments
- **GP0** — WS2815 data out (to 74AHCT125 input)
- **VBUS** — 5V in from USB
- **GND** — common ground

## MQTT Topics

```
garden/lights/zone/{n}/set      # command a specific zone (n = 1–8)
garden/lights/zone/{n}/status   # zone heartbeat / status
garden/lights/all/set           # broadcast command to all zones
garden/lights/scene/set         # activate a named scene
```

### Command payload schema
```json
{
  "effect": "cycle",        // solid | cycle | chase | off | scene
  "color": [255, 100, 0],   // RGB, 0–255 each
  "brightness": 128,        // 0–255
  "speed": 50               // effect speed, 0–100
}
```

## File Map

```
pico/main.py          — MicroPython entry point, serial listener, effect dispatcher
pico/effects.py       — Effect implementations (solid, cycle, chase, scene, off)
pico/ws2815.py        — WS2815 driver (NeoPixel-compatible; do not modify)
pi/bridge.py          — asyncio MQTT↔serial bridge
pi/config.py          — Zone→serial port mapping, MQTT broker address, topic prefixes
pi/requirements.txt   — aiomqtt, pyserial-asyncio
openhab/garden_lights.items
openhab/garden_lights.rules
openhab/garden_lights.sitemap
docs/wiring.md        — Detailed wiring, splice locations, connector pinouts
docs/bom.md           — Bill of materials with sourcing notes
```

## Coding Conventions

- **Pico firmware**: MicroPython. Keep `main.py` lean — serial loop + dispatch only. All effect logic in `effects.py`. Use `uasyncio` if adding concurrent behavior.
- **Pi bridge**: Python 3.11+. One async task per zone serial port. Config is all in `config.py` — no hardcoded port names or topic strings in `bridge.py`.
- **JSON everywhere** on the serial wire. Newline-delimited (`\n`). Pico parses with `ujson`, Pi with stdlib `json`.
- **Fail safe**: if a Pico loses serial contact or receives malformed JSON, it should fall back to a slow amber pulse, not go dark or throw an unhandled exception.
- **No secrets in repo.** MQTT broker credentials (if any) go in a `.env` file excluded by `.gitignore`.

## openHAB Integration Notes

- openHAB runs on the Mac Mini on the same LAN as the Pi
- Mosquitto runs on the Pi (not the Mac Mini)
- openHAB uses the MQTT binding pointed at the Pi's IP
- Existing openHAB install has ~100 Z-Wave/Zigbee/MQTT devices — follow existing item naming conventions (camelCase, descriptive)
- Weather-reactive rules can reference existing rtl_433 weather sensor items already in openHAB
- Astro binding already installed for sunset/sunrise triggers

## Deployment

### Pi service
The bridge runs as a systemd service. After changes:
```bash
sudo systemctl restart garden-lights-bridge
journalctl -u garden-lights-bridge -f   # tail logs
```

### Pico updates
Use `mpremote` from the Pi or dev machine:
```bash
mpremote connect /dev/ttyACM0 cp pico/main.py :main.py
mpremote connect /dev/ttyACM0 cp pico/effects.py :effects.py
```

### Serial port stability
Picos enumerate as `/dev/ttyACMn` in connection order, which can shift on reboot. Create udev rules to assign stable names by Pico serial number:
```
/etc/udev/rules.d/99-garden-picos.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="2e8a", ATTRS{serial}=="<pico_serial>", SYMLINK+="ttyPICO1"
```
Run `udevadm info -a -n /dev/ttyACM0 | grep serial` to find each Pico's serial number.

## Known Constraints & Watch-outs

- WS2815 data line is timing-sensitive. Keep the serial→LED dispatch loop tight on the Pico — avoid anything slow between receiving a command and writing to the string.
- Do not drive the data line from the Pico's GP0 directly — always through the 74AHCT125.
- The 100µF cap at the first fixture input is not optional — omitting it risks destroying the first LED on power-on surge.
- WS2815 draws ~18mA per LED at full white (vs ~60mA for WS2812B). Design effects to stay well under full white in normal use.
- The Pi bridge must handle serial port enumeration gracefully at startup — Picos may not all be ready simultaneously on boot.
- Data splices underground will cause signal integrity problems. Data connections must only occur at fixture PCB pins, never mid-cable.
- Raspberry Pi OS Bookworm (Debian 12) on the Zero 2 W is assumed — verify systemd unit file syntax and pip behavior against actual OS version. Use the 32-bit Raspberry Pi OS Lite image for the Zero 2 W (lighter footprint, no desktop needed).