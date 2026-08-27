# yard-lighting

Distributed outdoor RGB LED garden lighting system. See [CLAUDE.md](CLAUDE.md) for the full architecture, hardware, and protocol spec.

## Wiring

Fixture heads use the fiber-optic flower-stem design in
[docs/fixture_construction_fiber.md](docs/fixture_construction_fiber.md) — a
buried base enclosure with a WS2815 node (used single-line, WS2811-style)
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
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
           ┌─────────┐    ┌─────────┐      ┌─────────┐
           │ Pico #1 │    │ Pico #2 │  ...  │ Pico #n │
           │ Zone 1  │    │ Zone 2  │       │ Zone n  │
           └────┬────┘    └────┬────┘       └────┬────┘
                │ GP0          │                 │
                ▼              ▼                 ▼
          74AHCT125      74AHCT125          74AHCT125
        level shifter  level shifter      level shifter
                │              │                 │
                ▼              ▼                 ▼
      underground trunk cable, base enclosure to base enclosure
              (12V · GND · Data — 3 conductors, no backup line)
```

### Per-fixture base enclosure wiring

Each fixture is a buried base enclosure (no rigid pipe riser) housing a
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
