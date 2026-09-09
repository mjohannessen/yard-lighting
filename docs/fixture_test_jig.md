# Fixture Test Jig — Pre-Burial Bench Test

A standalone test rig for lighting up one fixture's WS2815 node — via its
bare pigtail leads — before the base enclosure is glued shut and before the
pigtails get spliced to trunk cable. This is what satisfies the "Node
addresses and lights correctly on the bench" line in
[docs/fixture_construction_fiber.md](fixture_construction_fiber.md) §6's
pre-burial QC checklist, done right after Step 3 (pigtails soldered) or
Step 4 (base assembled) — whichever point the enclosure is still open enough
to reach the leads — and again at Step 9 after the globe is mounted.

This is a separate, permanent bench fixture, not a one-off wiring — build it
once and reuse it for every fixture.

## Components

| Part | Notes |
|---|---|
| Pico 2 (RP2350) | Same board as the field build (CLAUDE.md architecture constraint) — running MicroPython, per [pico/README.md](../pico/README.md) |
| 74AHCT125 quad level shifter | Only 1 of 4 channels used; same part as the field build and the bench-test rig ([pico/README.md](../pico/README.md) §4) |
| 300–470Ω resistor | Data line, between the 74AHCT125's output and the node's DI clip lead — matches the field convention (CLAUDE.md *Per zone* table) |
| 100µF capacitor | Across the 12V/GND clip leads, as close to the node as the clips allow — cheap insurance against power-on surge into a single node, same reasoning as CLAUDE.md's *Known Constraints* note (protects the node on connection, when clip contact bounce can spike current briefly) |
| 3× test clip leads (or fine hook probes) | 12V, GND, DI — clip directly to the fixture's bare pigtail leads. Use the **in-pigtail** (DI), never the out-pigtail (DO) — DO is the node's regenerated output toward the next fixture in the chain and carries no signal when nothing is driving it |
| Bench power supply, 12V | Fixture LED power only — set the voltage before connecting, don't rely on the jig to protect against an unset/wrong supply voltage |
| Raspberry Pi (test host) + USB cable | Host for flashing/running the Pico over `mpremote` (see Firmware below); also powers the Pico (VBUS) and, from the Pico's VBUS pin, the 74AHCT125's 5V VCC |
| Alligator clip → bare wire, or a small terminal block | At each of the 3 test leads' fixture end, sized for the pigtails' 26–30AWG silicone lead wire ([fixture_construction_fiber.md](fixture_construction_fiber.md) §2 BOM) |

Everything above except the clip leads and bench PSU is identical to the
existing bench-test 74AHCT125 setup in
[pico/README.md](../pico/README.md) §4 — build this jig on the same
protoboard/breadboard layout if one is already on hand from that setup.

## Wiring

```
Pico VBUS (pin 40)  ──► 5V rail
Pico GND  (pin 23)  ──► 5V rail GND / 74AHCT125 pin 1 (1OE) / pin 7 (GND)
Pico GP0  (pin 1)   ──► 74AHCT125 pin 2 (1A)
74AHCT125 pin 3 (1Y) ──► 300–470Ω resistor ──► DI clip lead
74AHCT125 pin 14 (VCC) ──► 5V rail

Bench 12V PSU (+) ──► 12V clip lead
Bench 12V PSU (–) ──► GND clip lead (common with Pico/74AHCT125 GND)
100µF cap ── across the 12V and GND clip leads, at the clip end
```

(74AHCT125 indentation notch is on the lower left; see
[pico/README.md](../pico/README.md) §4 for the full pinout table.)

Clip order onto the fixture's pigtail: **GND first, then 12V, then DI** —
same reasoning as any live power connection, minimizes the chance of the
data or 12V lead briefly floating against the wrong contact while clipping
on. Unclip in reverse order (DI, then 12V, then GND).

**The three grounds must be common**: bench PSU return, Pico GND, and
74AHCT125 GND all have to tie together, exactly like the field build's
single common ground (CLAUDE.md *Pico pin assignments*). If the bench PSU
and the USB power source are two separate physical supplies (likely, since
one is 12V and the other is 5V-over-USB), run a wire between their two
negative/ground points — don't assume they share a ground just because both
eventually reach the same fixture.

**1OE must be tied to GND**, not left floating — see
[pico/README.md](../pico/README.md) §4 for why a floating output-enable
looks identical to a disconnected data line (LEDs just stay dark).

## Firmware

With the Pico connected via USB to the Pi test host, flash
[pico/test_bench.py](../pico/test_bench.py) using `mpremote` from the Pi
per [pico/README.md](../pico/README.md) §§1–3, then follow that guide's
REPL steps and enter `1` at the **Number of LEDs** prompt (this jig drives
one node at a time). Its normal cycling behavior (red → green → blue →
white → off) is what §6's QC checklist checks color uniformity and
hot-spot issues against — if a solid-color diagnostic variant is in place
instead (swapped in during hardware troubleshooting), restore the cycling
version before using the jig for fixture QC.

## Using the jig

1. Set the bench PSU to 12V, **outputs off**, before clipping on.
2. Clip GND, then 12V, then DI onto the fixture's in-pigtail bare leads
   (never the out-pigtail/DO).
3. Enable the bench PSU output.
4. From the Pi test host, confirm the Pico is running `test_bench.py` and
   showing the color cycle (see [pico/README.md](../pico/README.md) §3 for
   the `mpremote`/REPL steps).
5. At the globe, check per
   [fixture_construction_fiber.md](fixture_construction_fiber.md) §6: color
   uniformity through the cycle, no hot-spot opposite the fiber tip,
   adequate brightness, and — if the stem is already built — that hand-flexing
   the stem doesn't disturb the light (a loose LED-to-fiber contact would
   show up as flicker here).
6. Disable the bench PSU output, then unclip DI, 12V, GND in that order.

If the node doesn't light: check the DI clip is actually on the
**in**-pigtail and not the out-pigtail (both leads look identical once bare
and tinned — mark them at Step 3 of
[fixture_construction_fiber.md](fixture_construction_fiber.md) if this is a
recurring mix-up), then work through
[pico/README.md](../pico/README.md)'s troubleshooting section — the failure
modes (floating 1OE, wrong GP0 wiring) are the same on this jig as on the
bench-test rig.
