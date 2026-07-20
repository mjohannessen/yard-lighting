# Wiring — Bench Test Stage → Field Deployment

## Stage 1: Bench test (current)

Goal: validate the Pico → dispatch → LED signal path for one zone before
adding the field-scale power system (buck converters, underground runs,
WS2815 strings).

**Setup:** 1 Pico, single 5V bench supply, 2 standard 5V NeoPixels (WS2812B-type)
wired to 2 test fixtures.

**Pins (same as field deployment):**
| Pin | Function |
|---|---|
| GP0 | Data out → 74AHCT125 input |
| VBUS | 5V in |
| GND | Common ground |

**Still required at bench scale:**
- **74AHCT125 level shifter** between GP0 and the NeoPixel data line. This
  isn't a 12V-vs-5V power concern — it's that the Pico's 3.3V logic sits
  below the ~5V (0.7×Vdd) data threshold NeoPixel-protocol pixels expect,
  whether they're WS2815 or plain WS2812B-style. A short bench wire may
  *appear* to work without it, but that's out of spec and won't validate the
  real signal path used in the field build.

**Not needed at this stage:**
- 24V→5V and 24V→12V buck converters — a single 5V bench supply covers the
  Pico and both NeoPixels directly.
- 300–470Ω data-line resistor / 100µF cap — cheap insurance if on hand, but
  not required for a 2-pixel bench test.
- WS2815 DOUT (backup data line) — a WS2815-only feature; standard 5V
  NeoPixels only need DIN.

**Power draw:** trivial at 2 pixels even at full white (~60mA/LED for
WS2812B-style vs ~18mA/LED for WS2815) — no special power sequencing needed
on bench supply.

## Stage 2: Field deployment

Full per-zone wiring (24V feed, 74AHCT125, underground 4-conductor run,
100µF cap, data resistor, WS2815 DOUT) is specified in CLAUDE.md under
*Hardware* and *Pico pin assignments*. Port this section into a full
diagram once bench testing confirms the signal path.
