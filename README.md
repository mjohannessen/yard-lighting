# yard-lighting

Distributed outdoor RGB LED garden lighting system. See [CLAUDE.md](CLAUDE.md) for the full architecture, hardware, and protocol spec.

## Controlling the lights

Lights are controlled by publishing JSON to MQTT topics on the Mosquitto
broker running on the Pi (`192.168.1.120`, port 1883).
[pi/bridge.py](pi/bridge.py) forwards each command over USB serial to the
Pico for that zone. openHAB turns all zones on in a rainbow cycle at dusk
and off at 23:00 (house-brain's `GardenLights_Power`), and hauss-backend's
`/garden.html` page controls them by hand. For testing, use
`mosquitto_pub` from any machine on the LAN — the broker listens on the
LAN via [pi/mosquitto-lan.conf](pi/mosquitto-lan.conf).

### Topics

| Topic | Purpose |
|---|---|
| `garden/lights/zone/{n}/set` | Command one zone (`n` = 1–4) |
| `garden/lights/all/set` | Send the same command to all four zones |
| `garden/lights/scene/set` | Same as `all/set`; openHAB resolves the scene to a color first |
| `garden/lights/pattern` | Retained `rainbow` or `fireflies`: the pattern openHAB turns the lights on with. Set from openHAB or the hauss-backend garden page; the bridge ignores it |
| `garden/lights/zone/{n}/status` | The zone's current state, published by the Pico |

### Command payload

```json
{"effect": "solid", "color": [255, 100, 0], "brightness": 128, "speed": 50}
```

| Field | Values | Default |
|---|---|---|
| `effect` | `solid`, `cycle` (rainbow), `chase` (one lit fixture moving down the string), `fireflies` (each fixture flashes a new random colour for 0.5 s about every 5 s, out of step with the others), `scene`, `off` | `off` |
| `color` | `[r, g, b]`, 0–255 each; used by `solid`, `chase`, `scene` | `[255, 255, 255]` |
| `brightness` | 0–255 | 255 |
| `speed` | 0–100, for `cycle` and `chase` | 50 |

Keep brightness well below full white in normal use, to manage node heat
and power-supply headroom.

### Examples

```bash
# Zone 1 warm white at half brightness
mosquitto_pub -h 192.168.1.120 -t garden/lights/zone/1/set \
  -m '{"effect":"solid","color":[255,180,100],"brightness":128}'

# Slow rainbow on every zone
mosquitto_pub -h 192.168.1.120 -t garden/lights/all/set \
  -m '{"effect":"cycle","brightness":120,"speed":20}'

# Everything off
mosquitto_pub -h 192.168.1.120 -t garden/lights/all/set -m '{"effect":"off"}'

# Watch every zone's status
mosquitto_sub -h 192.168.1.120 -v -t 'garden/lights/zone/+/status'
```

### Status and fail-safe behavior

- The bridge resends each zone's last command every 5 seconds, so each
  zone publishes a status message (current `effect`, `color`, `brightness`,
  `speed`) about every 5 seconds. If a zone's status stops, its Pico or the
  bridge is down.
- If a Pico receives no command for 15 seconds, it falls back to a slow
  amber pulse. It never goes dark. This happens if the bridge or its USB
  link is down, or after a bridge restart until the zone gets its next
  command. Publish `set` commands with `-r` (retain) so the bridge picks up
  the last command as soon as it reconnects.
- The bridge runs as the systemd service `garden-lights-bridge` on the Pi:

  ```bash
  sudo systemctl restart garden-lights-bridge
  journalctl -u garden-lights-bridge -f
  ```

## Wiring

Fixture heads use the fiber-optic flower-stem design in
[docs/fixture_construction_fiber.md](docs/fixture_construction_fiber.md) — a
base enclosure sitting flat on the ground (staked, optionally under bark
mulch; only the trunk cable is buried) with a WS2815 node (used single-line, WS2811-style)
feeding a flexible fiber-optic + spring-wire stem up to a passive frosted
globe. The fiber's polished base end seats in direct contact against the
node's flat SMD face — no reflector cone, no air gap. There is no rigid pipe
riser and no electrical connection above the base enclosure.

### System overview

```
                     ┌──────────────────────┐
                     │  Mac Mini: openHAB   │
                     │ (schedules, scenes,  │
                     │  astro/weather rules)│
                     └──────────┬───────────┘
                                │ MQTT (LAN)
                                ▼
                     ┌──────────────────────┐
                     │  Hub Box             │
                     │  Pi Zero 2 W         │
                     │  Mosquitto broker +  │
                     │  MQTT↔serial bridge  │
                     └──────────┬───────────┘
                                │ USB (Hub+Ethernet HAT → powered USB hub)
          ┌─────────────┬─────────────┬─────────────┐
          ▼             ▼             ▼             ▼
     ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
     │ Pico #1 │   │ Pico #2 │   │ Pico #3 │   │ Pico #4 │
     │ Zone 1  │   │ Zone 2  │   │ Zone 3  │   │ Zone 4  │
     └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘
          │ GP0         │ GP0         │ GP0         │ GP0
          ▼             ▼             ▼             ▼
     ┌───────────────────────────────────────────────────┐
     │       74AHCT125 — one chip, 4 channels             │
     │   (single quad level shifter; all 4 Picos share    │
     │            it, one channel per zone)                │
     └────┬────────────┬────────────┬────────────┬────────┘
          ▼             ▼             ▼             ▼
      100Ω          100Ω          100Ω          100Ω
      resistor on   resistor on   resistor on   resistor on
      zone 1 data   zone 2 data   zone 3 data   zone 4 data
      lead, at      lead, at      lead, at      lead, at
      chip output   chip output   chip output   chip output
          │             │             │             │
          ▼             ▼             ▼             ▼
      trunk cable,  trunk cable,  trunk cable,  trunk cable,
      zone 1        zone 2        zone 3        zone 4
      (12V·GND·Data, base enclosure to base enclosure)
          │             │             │             │
          ▼             ▼             ▼             ▼
      1st fixture,  1st fixture,  1st fixture,  1st fixture,
      zone 1:       zone 2:       zone 3:       zone 4:
      +100µF cap    +100µF cap    +100µF cap    +100µF cap
      across        across        across        across
      12V/GND at    12V/GND at    12V/GND at    12V/GND at
      node's leads  node's leads  node's leads  node's leads
```

### Per-fixture base enclosure wiring

Each fixture is a base enclosure sitting flat on the ground (no rigid pipe riser) housing a
WS2815 node (LED holder insert, direct-contact fiber coupling) and the fixed
end of the fiber/spring-wire stem. The node's leads are permanently soldered
to two short pigtails at bench-assembly time, before the enclosure is ever
closed and sealed. Each pigtail exits through its own small sealed grommet
and ends in bare tinned lead wire — no connector is fitted at bench time.
Splicing to the trunk cable happens later, at install, **outside** the
enclosure, using gel-filled direct-bury connectors — a permanent splice, not
a field disconnect. A coiled service loop of extra trunk cable at each
fixture allows a future cut/re-splice without pulling new wire.

```
  trunk in ──────────┐                       ┌────────── trunk out
  (from prev fixture,│                       │           (to next fixture,
   or hub box)        │                       │            or none if last
  12V / GND / Data    │                       │            in zone)
                       ▼                       ▼           12V / GND / Data
         gel-filled direct-bury splices (outside enclosure)
      ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌──────────┐
      │   12V   │ │   GND   │ │ data-in  │ │ data-out │
      │ 3-way tie│ │ 3-way tie│ │ 2-way    │ │ 2-way    │  NOT tied together
      └────┬────┘ └────┬────┘ └────┬─────┘ └────┬─────┘
           │           │           │            │
           │  (pigtail leads — bare wire, exit through sealed grommets)
           │           │           │            │
           ▼           ▼           ▼            ▲
        ┌───────────────────────────────────────────┐
        │     Base enclosure (sealed once, on the     │
        │             bench, at build time)            │
        │        ┌───────────────────────────┐        │
        │        │  WS2815 node (LED holder   │        │
        │        │  insert, direct-contact    │        │
        │        │  fiber coupling)           │        │
        │        └─────────────┬───────────────┘        │
        └──────────────────────┼───────────────────────┘
                                ▼
                    fiber → spring wire → globe
                    (flex zone: optics + mechanics only,
                     no electrical connection above this point)
```

Notes:
- Mark fixtures with one small hole on the DIN side, 2 holes indicate the first fixture in the node which has the capacitor between + and -
- **12V and GND** are a true common tie — one gel-filled connector each,
  with trunk-in, trunk-out, and the node's own pigtail lead all landed
  together.
- **Data is never a common tie.** The node fully decodes and regenerates the
  signal, so trunk-in-data→node-DI and node-DO→trunk-out-data are two
  separate gel-filled connectors. Tying all four data leads into one
  connector shorts the node's input and output together.
- The last fixture in a zone has no trunk-out — its connectors only carry
  trunk-in + node lead (or trunk-in + node-DI, with no downstream DO
  consumer).
- Data conductors must reach the node's own pads or a gel-filled connector
  only — never spliced mid-cable underground. See §5 of the fixture
  construction guide for the full convention.

### Wire/conductor legend

| Signal | Splice rule                                              |
|--------|-----------------------------------------------------------|
| 12V    | Common-tie gel-filled direct-bury connector, outside the base enclosure |
| GND    | Common-tie gel-filled direct-bury connector, outside the base enclosure |
| Data   | Two separate gel-filled connectors (in→DI, DO→out) — never a common tie, never mid-cable |

### Fixture configuration

Globes are clear or white. The LED is visible through a clear globe in
daylight; a white globe is semi-opaque and hides it, so daytime checks only
work on the clear fixtures.

#### Zone 1

- 1 - Clear large
- 2 - Clear small
- 3 - White
- 4 - White
- 5 - White
- 6 - Clear large
- 7 - White
- 8 - Clear small
- 9 - White
- 10 - Clear small

## 3D-printed parts

The globe cradle and base enclosure are designed in FreeCAD; part specs,
dimensions, and construction steps are in [freecad.md](freecad.md).
Sources (`.FCStd`) and exported print files live in [freecad/](freecad/).
