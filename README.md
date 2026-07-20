# yard-lighting

Distributed outdoor RGB LED garden lighting system. See [CLAUDE.md](CLAUDE.md) for the full architecture, hardware, and protocol spec.

## Wiring

Fixture heads use the fiber-optic flower-stem design in
[docs/fixture_construction_fiber.md](docs/fixture_construction_fiber.md) — a
buried base enclosure with a WS2811 node feeding a flexible fiber-optic +
spring-wire stem up to a passive frosted globe. There is no rigid pipe riser
and no electrical connection above the base enclosure.

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
WS2811 node, reflector cone, and the fixed end of the fiber/spring-wire stem.
Incoming and outgoing trunk cables both enter this same enclosure, each
through its own IP68 cable gland — there is no separate external splice box.

```
  trunk in ──────────┬────────── trunk out
  (from prev fixture,│           (to next fixture,
   or hub box)        │            or none if last in zone)
  12V / GND / Data    │           12V / GND / Data
                       │
                       ▼
                ┌─────────────────────┐
                │   Base enclosure     │
                │  ┌────┐  ┌────┐     │
                │  │12V │  │GND │  3-way lever nuts:
                │  │lever│ │lever│ trunk-in + trunk-out + node lead
                │  └────┘  └────┘     │
                │  ┌───────┐┌───────┐ │
                │  │DIN lev││DOUT lev│ 2 separate levers — NOT tied together
                │  └───┬───┘└───┬───┘ │
                │      ▼        ▲     │
                │   ┌─────────────┐   │
                │   │  WS2811 node │   │
                │   └──────┬──────┘   │
                │          │ reflector cone → fiber → spring wire → globe
                └──────────┼──────────┘
                           ▼
                    (flex zone: optics + mechanics only,
                     no electrical connection above this point)
```

Notes:
- **12V and GND** are a true common tie — one lever each, with trunk-in,
  trunk-out, and the node's own lead all landed together.
- **Data is never a common tie.** The node fully decodes and regenerates the
  signal, so trunk-in-data→node-DIN and node-DOUT→trunk-out-data are two
  separate levers. Tying all four data leads into one lever shorts the
  node's input and output together.
- The last fixture in a zone has no trunk-out — its levers only carry
  trunk-in + node lead (or trunk-in + node-DIN, with no downstream DOUT
  consumer).
- Data conductors must reach the node's own pads or a lever nut only — never
  spliced mid-cable underground. See §5 of the fixture construction guide for
  the full convention.

### Wire/conductor legend

| Signal | Splice rule                                              |
|--------|-----------------------------------------------------------|
| 12V    | Common-tie lever nut inside the base enclosure            |
| GND    | Common-tie lever nut inside the base enclosure            |
| Data   | Two separate levers (in→DIN, DOUT→out) — never a common tie, never mid-cable |
