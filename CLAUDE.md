# CLAUDE.md — Garden LED Lighting Control System

This file provides context for Claude Code sessions on this project. Read it fully before making any changes.

## Project Purpose

Distributed outdoor RGB LED garden lighting system. RP2350 Picos (Pico 2) drive WS2815 fixture nodes (wired single-line, WS2811-style — the chip's backup data feature is unused) via daisy-chained underground 3-wire trunk cable runs. Each fixture is a buried base enclosure (WS2815 node + direct-contact fiber pocket) feeding a passive fiber-optic + spring-wire stem up to a frosted globe — no electrical connection above the base enclosure. See [docs/fixture_construction_fiber.md](docs/fixture_construction_fiber.md) for the full fixture build. A Raspberry Pi Zero 2 W bridges MQTT (from openHAB on a Mac Mini) to USB serial commands for each Pico. All control hardware is co-located in a weatherproof hub box in the garden.

## Architecture Constraints — Do Not Change Without Discussion

- **One Pico per zone.** Each Pico drives exactly one daisy-chained WS2815 node string (wired as a plain single-line chain — backup data feature unused). Do not attempt to drive multiple strings from one Pico.
- **USB serial only** for Pi↔Pico communication. No WiFi, no RS-485. Picos are co-located with the Pi inside the hub box.
- **MicroPython on Picos.** Do not suggest CircuitPython or C SDK unless there is a hard performance reason.
- **Python asyncio on Pi.** The bridge script uses `aiomqtt` and `pyserial-asyncio`. Do not introduce threading or synchronous serial blocking calls.
- **Two buck converters.** 24V→5V for Pi Zero 2 W/Picos, 24V→12V for LED strings. Do not assume a single shared voltage bus for both.
- **74AHCT125 level shifter** on every Pico data line. Pico outputs 3.3V; WS2815 DI requires 5V logic. Never connect GP0 directly to a string without the shifter.
- **WS2815 LED chip, used single-line (WS2811-style).** Fixtures use WS2815 5050 SMD individually-addressable LEDs (12V, driver integrated per LED — see [docs/fixture_construction_fiber.md](docs/fixture_construction_fiber.md) BOM for the sourced part) rather than the earlier WS2811 pixel nodes: WS2815's flat SMD package lets the fiber tip seat flush against the emitter face for direct-contact coupling, where a domed WS2811 node's curved lens only touched the fiber at one point. WS2815 exposes a BI/BO backup-data pair for its "breakpoint resume" redundancy feature — **this project does not use it.** Only DI/DO are wired, exactly like WS2811's DIN/DOUT; BI/BO are left unconnected at every node. This keeps the 3-conductor trunk, the two-separate-nets data-splice convention, and the original failure mode (one dead node breaks the chain downstream) unchanged — the chip changed, the wiring convention and its trade-offs did not. The MicroPython NeoPixel library works with WS2815 run this way; verify timing against `pico/ws2811.py` on the bench before field deployment. Do not reference WS2812B specs for voltage or current draw.
- **openHAB is the authority** for schedules, scenes, and automation logic. Keep intelligence in openHAB rules, not in the Pi bridge script. The bridge is a dumb forwarder.

## Hardware

### Conduit runs to hub box (pull all three while trench is open)
- **Cat6 #1** — PoE camera #1 (dedicated, direct to camera)
- **Cat6 #2** — Pi Zero 2 W network (via USB Hub + Ethernet HAT's RJ45 port); reserved for future PoE camera #2. When second camera is added, insert a small PoE-aware switch at the box end — no rewiring needed.
- **12/2 landscape wire** — 24V/300W power feed

### Hub box contents
- Raspberry Pi Zero 2 W
- 1× Pi Zero USB Hub + Ethernet HAT (RTL8152B-based; RJ45 + 3× USB-A; stacks on GPIO header, taps Pi's USB via pogo pins, powered from GPIO 5V; RJ45 connects to Cat6 #2, one USB-A port feeds the powered USB hub)
- 4× RP2350 Pico 2 (standard, not Pico 2 W)
- 1× powered USB hub (4-port, for Picos) — project is capped at 4 zones permanently due to hub box space constraints, confirmed with the user 2026-08-29; not a phase-1 placeholder
- 1× 24V→5V buck converter, 5A rated (Pi, Picos, USB hub)
- 1× 24V→12V buck converter, 5A rated (all WS2815 fixture strings)
- 1× 74AHCT125 quad level shifter (all 4 channels used, one per zone)

### Underground trunk cable per zone (daisy-chain, base enclosure to base enclosure)
- 12V power
- GND
- Data (single wire — WS2815's BI/BO backup pair is intentionally left unwired; treated as a plain single-line chain, same as WS2811)
- 3 conductors total, no backup line
- Spliced only inside each fixture's base enclosure, on gel-filled direct-bury connectors — ZONE INDUSTRY CORP silicone-filled waterproof wire nuts, UL 486G, 20–8 AWG (final pick, per docs/fixture_construction_fiber.md §2 BOM): 12V and GND get a common-tie connector (trunk-in + trunk-out + node lead); data gets **two separate connectors** (trunk-in→node DIN, node DOUT→trunk-out) since the node regenerates the signal — never tie all four data leads into one connector. This is a permanent splice, not a field disconnect — swapping a fixture means cutting and re-splicing, not unplugging. Deliberate trade-off, confirmed with the user 2026-08-27: field swaps are expected to be rare, so each fixture gets a coiled service loop of extra trunk cable to allow a future cut/re-splice without pulling new wire.
- No inline splices mid-cable — data and power both land only at a base enclosure's gel-filled connectors
- Full convention: [docs/fixture_construction_fiber.md](docs/fixture_construction_fiber.md) §5

### Per zone (in hub box)
- 300–470Ω resistor on data line (at 74AHCT125 output, before underground cable)
- 100µF capacitor across 12V/GND at the first base enclosure's node leads
- IP67/IP68 3-pin weatherproof connector at hub box exit

### Pico pin assignments
- **GP0** — WS2815 data out (to 74AHCT125 input)
- **VBUS** — 5V in from USB
- **GND** — common ground

## MQTT Topics

```
garden/lights/zone/{n}/set      # command a specific zone (n = 1–4)
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
pico/ws2811.py        — NeoPixel-protocol driver, used for WS2815 in single-line mode (do not modify)
pico/test_bench.py    — Bench-test-stage smoke test (2 LEDs, no serial protocol)
pico/README.md        — MicroPython flashing + bench-test-stage setup guide
pi/bridge.py          — asyncio MQTT↔serial bridge
pi/config.py          — Zone→serial port mapping, MQTT broker address, topic prefixes
pi/requirements.txt   — aiomqtt, pyserial-asyncio
openhab/garden_lights.items
openhab/garden_lights.rules
openhab/garden_lights.sitemap
docs/wiring.md                       — Bench-test-stage vs field-deployment wiring reference
docs/fixture_construction_fiber.md   — Fixture head build guide: base enclosure, WS2815 node, fiber/spring-wire stem, globe
docs/fixture_test_jig.md             — Pre-burial per-fixture bench test rig: clip leads onto pigtails before splicing/closing
docs/bom.md                          — Bill of materials with sourcing notes
freecad.md                           — Globe cradle + base housing part specs, dimensions, construction steps, as-built notes
freecad/                             — FreeCAD sources (.FCStd), drafts/, and exported .3mf print files — see "FreeCAD Design Files" below
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
- The 100µF cap at the first base enclosure's node leads is not optional — omitting it risks destroying the first node on power-on surge.
- WS2815's BI/BO backup data line is intentionally left unwired (see Architecture Constraints) — so, same as plain WS2811, a single node failure still breaks data regeneration to every fixture downstream of it in that zone until it's swapped. Design effects to stay well under full white in normal use to manage node heat and PSU headroom.
- The Pi bridge must handle serial port enumeration gracefully at startup — Picos may not all be ready simultaneously on boot.
- Data splices underground will cause signal integrity problems. Data connections must only occur at a node's own pads or a gel-filled direct-bury connector inside a base enclosure, never mid-cable.
- Raspberry Pi OS Bookworm (Debian 12) on the Zero 2 W is assumed — verify systemd unit file syntax and pip behavior against actual OS version. Use the 32-bit Raspberry Pi OS Lite image for the Zero 2 W (lighter footprint, no desktop needed).

# FreeCAD Design Files

CAD sources for the project's 3D-printed parts (globe cradle, base
enclosure, LED mount inserts) live in `freecad/`. Part-specific
overviews, dimensions, construction steps, printing notes, and as-built
status live in [freecad.md](freecad.md) — that file is the source of
truth for individual parts; update it, not this section, when a part's
design changes.

### Directory layout

```
freecad/
├── *.FCStd                      — current working sources, one file per part
├── *.FCBak                      — FreeCAD auto-backups (not authoritative; only for recovery)
├── drafts/                      — earlier/abandoned part iterations
└── outdoor led final models/    — exported .3mf meshes used for slicing/printing
```

## FreeCAD Environment

- FreeCAD 1.1.1 (stable, April 2026)
- Workbench: Part (not Part Design) — Part Design's revolution feature requires sketches entirely on one side of the revolution axis, and this project's spherical/cylindrical profiles cross the axis, so parts are built from Part-workbench booleans instead
- Platform: macOS

### Boolean construction pattern

Parts are built by combining primitives (spheres/cylinders/boxes) with Boolean Cut and Union in sequence rather than sketch-based features — typically: cut inner from outer shape first (hollow shell), cut a box to crop it, union additional geometry (nipples, bosses, flanges), cut bores last. See [freecad.md](freecad.md) for each part's actual step-by-step sequence.

### Mac-specific notes
- Boolean operations: click first object, Cmd+click second object
- Union: Part > Boolean > Union (not "Fuse")
- Cut: Part > Boolean > Cut
- TechDraw projection group centering via Python console:
  group.X = page.PageWidth / 2
  group.Y = page.PageHeight / 2

### Known issues / gotchas

- TechDraw Projection Group X/Y properties do not update via the Properties panel — use the Python console instead
- Boolean Cut is greyed out if objects are not proper closed solids
- Use full sphere/cylinder primitives (default angles) for boolean operations
- Print preview's print button is nearly invisible on Mac
- Use File > Print > Save as PDF (not File > Export > PDF) for 1:1 scale

### FreeCAD shortcuts (Mac)

| Action              | Shortcut        |
|---------------------|-----------------|
| Fit all in view     | V then F        |
| Fit selection       | V then S        |
| Undo                | Cmd+Z           |
| Boolean second obj  | Cmd+click       |
| Python console      | View > Panels   |