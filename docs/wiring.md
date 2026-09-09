# Wiring — Bench Test Stage → Field Deployment

## Stage 1: Bench test (current)

Goal: validate the Pico → dispatch → LED signal path for two independent
zone branches before adding the field-scale power system (buck converters,
underground runs, WS2815 strings).

**Setup:** 2 Picos (one per branch), 24V bench PSU feeding both a 24V→5V
buck (Picos) and a 24V→12V buck (LED power), 1 real WS2815 node per Pico.
Each Pico's node will later gain a second WS2815 on the same branch (2
nodes per Pico) — not yet wired.

**Pins (same as field deployment, per Pico):**
| Pin | Function |
|---|---|
| GP0 | Data out → 74AHCT125 input |
| VBUS | 5V in |
| GND | Common ground |

**Still required at bench scale:**
- **24V→5V and 24V→12V buck converters** — both now in the loop, off the
  same 24V bench PSU, same as field deployment. No more standalone 5V
  supply standing in for them.
- **74AHCT125 level shifter**, one gate per Pico's GP0/data line (2 of the
  chip's 4 gates used; both Picos share the same physical chip). This isn't
  a 12V-vs-5V power concern — it's that the Pico's 3.3V logic sits below the
  ~5V (0.7×Vdd) data threshold NeoPixel-protocol pixels expect. A short
  bench wire may *appear* to work without it, but that's out of spec and
  won't validate the real signal path used in the field build.

**Not needed at this stage:**
- 300–470Ω data-line resistor / 100µF cap — cheap insurance if on hand;
  with only 1 WS2815 node per branch, inrush current on power-up is minimal
  (the cap's role in CLAUDE.md's *Known Constraints* is protecting the
  first node in a full field string, not a lone bench node), so not
  required yet.

**WS2815 BI/BO:** now real WS2815 nodes, so the backup-data pins physically
exist — leave them unwired at the bench too, matching the field convention
in CLAUDE.md (single-line, WS2811-style; BI/BO unused).

**Power draw:** trivial at 2 WS2815 nodes total even at full white
(~18mA/LED) — no special power sequencing needed on bench supply. Revisit
once each branch grows to 2 nodes.

## Stage 2: Field deployment (Phase 1 — 4 zones)

Real installation, replacing the bench's single 5V supply with the full 24V
power system and scaling from 2 bench branches to the 4 physical zones
leaving the hub box. One 24V/300W PSU feeds two independent buck converters
— nothing downstream shares a raw 24V rail.

```
24V/300W PSU
  │
  ├─► 24V→12V buck (5A) ──► common 12V/GND bus ──► 4× IP67/68 3-pin connector
  │                                                  └─► zone N trunk (12V + GND)
  │
  └─► 24V→5V buck (5A) ──► Pi Zero 2 W + USB Hub/Ethernet HAT
                              │
                              └─► powered USB hub ──► 4× Pico (VBUS 5V, GND, USB serial)
                                                         │
                                                         └─► GP0 ──► 74AHCT125 gate ──► 300–470Ω resistor ──► zone N trunk (Data)
```

**Power:**
- **24V→12V buck, 5A** — all 4 WS2815 strings share this converter's output
  at a common bus in the hub box; each zone taps it through its own IP67/68
  connector, not a shared underground run.
- **24V→5V buck, 5A** — feeds the Pi Zero 2 W (via the stacked USB Hub +
  Ethernet HAT, GPIO 5V) and, through that hub's USB-A port, the powered USB
  hub. Picos draw 5V over VBUS from the powered USB hub's ports — they are
  not wired to the buck converter directly.

**Signal — one 74AHCT125, 4 zones:**
- All 4 gates of a single quad 74AHCT125 are used, one per Pico: Pico GP0 →
  gate in, gate out → that zone's 300–470Ω resistor → underground data
  conductor. The four gates are electrically independent — no bussing
  between zones, same as the separate 12V/GND taps above.
- This is the full build: the project is capped at 4 zones permanently
  (hub box space constraints), so this single chip and the 4-port USB hub
  cover the whole system — no second 74AHCT125 or expansion is planned.

**USB (Pi ↔ Picos):**
- Pi Zero 2 W → USB Hub + Ethernet HAT (stacks on GPIO header, taps Pi's USB
  via pogo pins) → one USB-A port feeds the powered USB hub → 4 Picos.
- Each Pico enumerates as `/dev/ttyACMn` in connection order; assign stable
  `/dev/ttyPICOn` symlinks via udev (see CLAUDE.md *Deployment* section)
  before wiring `pi/config.py`'s zone→port map.

**Underground trunk, ×4 (one per zone):**
- 3-conductor: 12V, GND, Data. WS2815's BI/BO backup pair is intentionally
  left unwired (see CLAUDE.md *Architecture Constraints*).
- 100µF cap across 12V/GND at each zone's first base enclosure node leads —
  not optional, protects against power-on surge.
- Splices only at base enclosure gel-filled direct-bury connectors
  (ZONE INDUSTRY CORP silicone-filled, UL 486G, 20–8 AWG — see BOM), per
  CLAUDE.md §*Underground trunk cable*; no
  mid-cable splices. Each fixture gets a coiled service loop of extra
  trunk cable to allow a future cut/re-splice, since this is a permanent
  joint rather than a field disconnect.
