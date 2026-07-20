# CLAUDE.md — Garden LED Lighting Control System

This file provides context for Claude Code sessions on this project. Read it fully before making any changes.

## Project Purpose

Distributed outdoor RGB LED garden lighting system. RP2040 Picos drive WS2811 fixture nodes via daisy-chained underground 3-wire trunk cable runs. Each fixture is a buried base enclosure (WS2811 node + reflector cone) feeding a passive fiber-optic + spring-wire stem up to a frosted globe — no electrical connection above the base enclosure. See [docs/fixture_construction_fiber.md](docs/fixture_construction_fiber.md) for the full fixture build. A Raspberry Pi Zero 2 W bridges MQTT (from openHAB on a Mac Mini) to USB serial commands for each Pico. All control hardware is co-located in a weatherproof hub box in the garden.

## Architecture Constraints — Do Not Change Without Discussion

- **One Pico per zone.** Each Pico drives exactly one daisy-chained WS2811 node string. Do not attempt to drive multiple strings from one Pico.
- **USB serial only** for Pi↔Pico communication. No WiFi, no RS-485. Picos are co-located with the Pi inside the hub box.
- **MicroPython on Picos.** Do not suggest CircuitPython or C SDK unless there is a hard performance reason.
- **Python asyncio on Pi.** The bridge script uses `aiomqtt` and `pyserial-asyncio`. Do not introduce threading or synchronous serial blocking calls.
- **Two buck converters.** 24V→5V for Pi Zero 2 W/Picos, 24V→12V for LED strings. Do not assume a single shared voltage bus for both.
- **74AHCT125 level shifter** on every Pico data line. Pico outputs 3.3V; WS2811 DIN requires 5V logic. Never connect GP0 directly to a string without the shifter.
- **WS2811 LED protocol.** WS2811 is wire-compatible with WS2812B/WS2815 (same single-wire protocol) but operates at 12V and has **no backup data line** — unlike WS2815, there is no DOUT. Each node fully decodes and regenerates the signal, so trunk-in-data and trunk-out-data are separate electrical nets at every fixture, not a shared bus. The MicroPython NeoPixel library works with WS2811. Do not reference WS2812B specs for voltage or current draw.
- **openHAB is the authority** for schedules, scenes, and automation logic. Keep intelligence in openHAB rules, not in the Pi bridge script. The bridge is a dumb forwarder.

## Hardware

### Conduit runs to hub box (pull all three while trench is open)
- **Cat6 #1** — PoE camera #1 (dedicated, direct to camera)
- **Cat6 #2** — Pi Zero 2 W network (via USB Hub + Ethernet HAT's RJ45 port); reserved for future PoE camera #2. When second camera is added, insert a small PoE-aware switch at the box end — no rewiring needed.
- **12/2 landscape wire** — 24V/300W power feed

### Hub box contents
- Raspberry Pi Zero 2 W
- 1× Pi Zero USB Hub + Ethernet HAT (RTL8152B-based; RJ45 + 3× USB-A; stacks on GPIO header, taps Pi's USB via pogo pins, powered from GPIO 5V; RJ45 connects to Cat6 #2, one USB-A port feeds the powered USB hub)
- 4–8× RP2040 Pico (standard, not Pico W)
- 1× powered USB hub (7+ port, for Picos)
- 1× 24V→5V buck converter, 5A rated (Pi, Picos, USB hub)
- 1× 24V→12V buck converter, 5A rated (all WS2811 fixture strings)
- 2× 74AHCT125 quad level shifter (one chip per two zones, covers up to 8 zones)

### Underground trunk cable per zone (daisy-chain, base enclosure to base enclosure)
- 12V power
- GND
- Data (single wire — WS2811 has no backup/DOUT line, unlike WS2815)
- 3 conductors total, no backup line
- Spliced only inside each fixture's base enclosure, on reusable lever nuts (e.g. Wago 221): 12V and GND get a common-tie lever (trunk-in + trunk-out + node lead); data gets **two separate levers** (trunk-in→node DIN, node DOUT→trunk-out) since the node regenerates the signal — never tie all four data leads into one lever
- No inline splices mid-cable — data and power both land only at a base enclosure's levers
- Full convention: [docs/fixture_construction_fiber.md](docs/fixture_construction_fiber.md) §5

### Per zone (in hub box)
- 300–470Ω resistor on data line (at 74AHCT125 output, before underground cable)
- 100µF capacitor across 12V/GND at the first base enclosure's node leads
- IP67/IP68 3-pin weatherproof connector at hub box exit

### Pico pin assignments
- **GP0** — WS2811 data out (to 74AHCT125 input)
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
pico/ws2811.py        — WS2811 driver (NeoPixel-compatible; do not modify)
pico/test_bench.py    — Bench-test-stage smoke test (2 LEDs, no serial protocol)
pico/README.md        — MicroPython flashing + bench-test-stage setup guide
pi/bridge.py          — asyncio MQTT↔serial bridge
pi/config.py          — Zone→serial port mapping, MQTT broker address, topic prefixes
pi/requirements.txt   — aiomqtt, pyserial-asyncio
openhab/garden_lights.items
openhab/garden_lights.rules
openhab/garden_lights.sitemap
docs/wiring.md                       — Bench-test-stage vs field-deployment wiring reference
docs/fixture_construction_fiber.md   — Fixture head build guide: base enclosure, WS2811 node, fiber/spring-wire stem, globe
docs/bom.md                          — Bill of materials with sourcing notes
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

- WS2811 data line is timing-sensitive. Keep the serial→LED dispatch loop tight on the Pico — avoid anything slow between receiving a command and writing to the string.
- Do not drive the data line from the Pico's GP0 directly — always through the 74AHCT125.
- The 100µF cap at the first base enclosure's node leads is not optional — omitting it risks destroying the first node on power-on surge.
- WS2811 has no backup data line — a single node failure breaks data regeneration to every fixture downstream of it in that zone until it's swapped. Design effects to stay well under full white in normal use to manage node heat and PSU headroom.
- The Pi bridge must handle serial port enumeration gracefully at startup — Picos may not all be ready simultaneously on boot.
- Data splices underground will cause signal integrity problems. Data connections must only occur at a node's own pads or a lever nut inside a base enclosure, never mid-cable.
- Raspberry Pi OS Bookworm (Debian 12) on the Zero 2 W is assumed — verify systemd unit file syntax and pip behavior against actual OS version. Use the 32-bit Raspberry Pi OS Lite image for the Zero 2 W (lighter footprint, no desktop needed).

# Globe Cradle Project

## Project Overview

Spherical cradle mount for a 59mm globe in FreeCAD 1.1.1.
Cups the bottom 1/8 of the globe with a bottom nipple for a
1/4" ID / 3/8" OD tube (glued slip fit).

## FreeCAD Version

- FreeCAD 1.1.1 (stable, April 2026)
- Workbench: Part (not Part Design)
- Platform: macOS

## Key Design Decisions

### Why Part Workbench (not Part Design)
Part Design revolution requires sketches entirely on one side of the
revolution axis. The spherical profile crosses the axis causing errors.
Part workbench boolean approach avoids this entirely.

### Construction Order (Critical)
1. Cut inner sphere from outer sphere FIRST (hollow shell)
2. Cut box from shell SECOND (crops to cradle shape)
3. Union nipple cylinder THIRD
4. Cut bore cylinder LAST

### Mac-Specific Notes
- Boolean operations: Click first object, Cmd+click second object
- Union: Part > Boolean > Union (not "Fuse")
- Cut: Part > Boolean > Cut
- TechDraw projection group centering via Python console:
  group.X = page.PageWidth / 2
  group.Y = page.PageHeight / 2

## Critical Dimensions

| Parameter           | Value    | Notes                     |
|---------------------|----------|---------------------------|
| Globe radius        | 29.5mm   | Must match actual globe   |
| Inner cup radius    | 29.5mm   | Exact fit to globe        |
| Outer cup radius    | 32mm     | 2.5mm wall thickness      |
| Nipple bore radius  | 4.86mm   | Slip fit for 3/8" OD tube |
| Nipple outer radius | 7.36mm   | 2.5mm wall around bore    |
| Bore depth          | 15mm     | Glue surface area         |
| Nipple length       | 20mm     | Total nipple protrusion   |
| Box crop Z          | -22.1mm  | Sets cradle depth         |

## Known Issues / Gotchas

- TechDraw Projection Group X/Y properties do not update via Properties
  panel — use Python console instead
- Boolean Cut greyed out if objects are not proper closed solids
- Use full sphere primitives (default angles) for boolean operations
- Print preview print button nearly invisible on Mac
- Use File > Print > Save as PDF (not File > Export > PDF) for 1:1 scale

## Modifying the Design

### To change globe size:
1. Outer sphere radius = new_globe_radius + 2.5mm
2. Inner sphere radius = new_globe_radius
3. Box crop Z = -(new_globe_radius) + (new_globe_diameter / 8)
4. Update README dimensions table

### To change tube size:
1. Nipple bore radius = (tube_OD / 2) + 0.1mm glue clearance
2. Nipple outer radius = nipple_bore_radius + 2.5mm

## FreeCAD Shortcuts (Mac)

| Action              | Shortcut        |
|---------------------|-----------------|
| Fit all in view     | V then F        |
| Fit selection       | V then S        |
| Undo                | Cmd+Z           |
| Boolean second obj  | Cmd+click       |
| Python console      | View > Panels   |