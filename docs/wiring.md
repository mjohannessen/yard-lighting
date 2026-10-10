# Wiring — Bench Test Stage → Field Deployment

## Stage 1: Bench test (current)

Goal: validate the Pico → dispatch → LED signal path against real WS2815
fixtures on the fixture test jig, before scaling up to the full 4-zone
field build.

**Setup:** 1 Pico driving 5 real WS2815 fixtures, daisy-chained through the
fixture test jig — see [docs/fixture_test_jig.md](fixture_test_jig.md) for
the authoritative jig wiring, firmware, and use procedure. Power:
- Pi Zero 2 W powered via GPIO pins 2 (5V) / 6 (GND) from a 20A/300W
  adjustable CC/CV buck converter serving as the 24V→5V rail — this
  bypasses the Pi's onboard USB input fuse/protection, so power-quality
  issues (undervoltage, current fold-back) surface as boot loops /
  unreachable SSH rather than an obvious error; check `vcgencmd
  get_throttled` if SSH access disappears after a power-path change.
- The Pico draws 5V over VBUS from the Pi's USB port (Pi → USB Hub +
  Ethernet HAT → Pico) — same power path as the field build.
- LED power is a real 12V bench PSU, not the 24V→12V CC/CV buck. The 12V
  buck is intentionally left disconnected until a real field-scale 12V
  load exists: wiring its output into a shared breadboard power rail with
  no load previously caused an accidental bridge with the 5V rail and
  current fold-back on that rail; disconnecting it fully restored
  stability.

**Pins (same as field deployment, per Pico):**
| Pin | Function |
|---|---|
| GP0 | Data out → 74AHCT125 input |
| VBUS | 5V in |
| GND | Common ground |

**In use at this stage:**
- **74AHCT125 level shifter**, channel 1 only (1 of the chip's 4 gates) —
  the field build scales this same chip to all 4 gates, one per zone; see
  the pinout table in *Stage 2* below or [pico/README.md](../pico/README.md)
  §4.
- **300–470Ω data-line resistor** (74AHCT125 output → node DI clip lead)
  and **100µF capacitor** (across the 12V/GND clip leads at the node) —
  both now required and in place, matching the field convention (CLAUDE.md
  *Per zone* table). With 5 real nodes in the chain, power-on inrush into
  the first node is a real risk, unlike the earlier single-LED-on-GPIO
  test stage.
- **Common ground across all supplies** — Pi/Pico GND, 74AHCT125 GND, and
  the 12V bench PSU return all have to tie together. Confirmed critical
  the hard way: a floating/missing ground here doesn't leave the node
  dark, it produces a *wrong but plausible* color (e.g. commanding solid
  white renders as green or blue, differently on different runs), because
  the node has no shared zero-volt reference for the data line's
  high/low thresholds. Check continuity between the 12V PSU's negative
  terminal and the Pico's GND pin (should read ~0V) before suspecting the
  resistor, cap, clips, or the node itself. Documented in
  [pico/README.md](../pico/README.md)'s Troubleshooting section and
  [docs/fixture_test_jig.md](fixture_test_jig.md).

**WS2815 BI/BO:** real WS2815 nodes, so the backup-data pins physically
exist — left unwired at the bench too, matching the field convention in
CLAUDE.md (single-line, WS2811-style; BI/BO unused).

**Power draw:** trivial at 5 WS2815 nodes even at full white (~18mA/LED,
~90mA total) off the 12V bench PSU — no special power sequencing needed.
Revisit once the chain scales toward a full zone's node count.

## Stage 1.5: Hub box integration test (current)

Goal: validate Pi↔Pico communication and the real JSON serial protocol
([pico/main.py](../pico/main.py), [pico/effects.py](../pico/effects.py),
[pico/ws2811.py](../pico/ws2811.py) — protocol details in
[pico/README.md](../pico/README.md) §5) against real fixtures inside the
actual hub box, one fixture per zone, before scaling each zone up to its
full LED string.

**Setup (as of 2026-09-16):**
- Hub box fully built: all 4 RP2350 Picos + Pi Zero 2 W installed on the
  powered USB hub. Pi reachable at 192.168.1.120.
- One real WS2815 fixture temporarily wired to node 0 of each Pico's zone.
- `/etc/udev/rules.d/99-garden-picos.rules` written, mapping each Pico's
  USB serial number to a stable `/dev/ttyPICO1`–`4` symlink — the step
  Stage 2 below calls out as a prerequisite for `pi/config.py`. Confirmed
  matching physical Fixtures 1–4 in order by visually identifying each
  node in turn.
- Two of the four Picos needed MicroPython flashed for the first time
  (never previously flashed) — see [pico/README.md](../pico/README.md) §2.

**Confirmed working:**
- Pi↔Pico serial communication on all 4 channels.
- Fixture↔port mapping (Fixture 1 = `ttyPICO1`, etc.).
- `pico/main.py`'s JSON dispatch protocol, bench-tested on Fixture 1 with
  `NUM_LEDS=1`: `solid` effect (correct color confirmed) and `cycle`
  effect (confirmed animating — a single LED cycling through hues reads
  as "pulsing" in perceived brightness even though R+G+B stays numerically
  constant; expected behavior of the color-wheel math, not a bug). The
  malformed-JSON fail-safe (amber pulse) was exercised but not
  conclusively confirmed by visual inspection — re-verify before trusting
  it.

**Not yet done:** `NUM_LEDS` in `pico/main.py` is still a placeholder
(50) — must be set to each zone's real fixture count before field
deployment.

**Update 2026-09-16 (zone 1 scaled to 5 fixtures, `pi/bridge.py` tested
end-to-end for the first time):** wired a full 5-fixture string to zone 1
and brought up `pi/bridge.py` against a fresh Mosquitto install on the Pi
(not installed by default on Raspberry Pi OS Lite — `sudo apt-get install
mosquitto mosquitto-clients`, plus a `pi/venv` for `aiomqtt`/
`pyserial-asyncio` since Bookworm blocks unmanaged system-wide `pip
install`). Found and fixed two real bugs before all 4 zones + all 5
zone-1 fixtures responded correctly:

- **Zones 2–4 had never received the real firmware.** Only zone 1 had
  been deployed with `main.py`/`effects.py`/`ws2811.py` (from the earlier
  single-fixture bench test). Zones 2–4 still had the old
  `test_bench.py` bench-test script sitting at its interactive
  `input("Number of LEDs: ")` prompt — permanently blocked since nothing
  attaches an interactive REPL to answer it, so those three Picos never
  ran any NeoPixel code and never responded to any command. Fix: deploy
  all three files to all four zones, not just the one that was bench-
  tested.
- **Red/green channel swap.** MicroPython's built-in `neopixel.NeoPixel`
  hardcodes GRB wire order (correct for WS2812-style chips), but these
  WS2815 fixtures expect RGB order — confirmed by sending pure red and
  pure green and observing them swapped (white was unaffected, since
  R=G=B is order-invariant, which is why the earlier single-LED bench
  test didn't catch it). Fixed in [pico/ws2811.py](../pico/ws2811.py) by
  swapping R/G before handing the color to `NeoPixel`, so its internal
  GRB conversion lands true RGB on the wire. **Any future non-timing
  change to `ws2811.py` should re-run this red/green/blue check**, not
  just confirm an effect changes state.

**Gotcha — `mpremote` and a running `main.py` don't mix:** any `mpremote`
command (even a failed one) sends Ctrl-C first to sync the REPL, which
kills a running `main.py` without restarting it — the board is left
idle at the REPL until an explicit `mpremote ... reset`. Checking
"is it running?" via `mpremote exec` is itself destructive. Also, running
`mpremote` against a port while `pi/bridge.py` has it open causes the
`mpremote` command to hang until timeout rather than erroring cleanly
(port contention, not a board crash). Correct sequence for any firmware
change: stop `bridge.py` → deploy with `mpremote fs cp` → `mpremote
reset` on every affected zone → restart `bridge.py` → verify only via
MQTT/serial traffic, not further `mpremote` calls.

**Confirmed working end-to-end after fixes:** `pi/bridge.py` relaying
MQTT commands to all 4 zones over `pyserial-asyncio` with zero write
errors; solid red/green/blue/white all render correctly; malformed MQTT
JSON is dropped and logged by the bridge without crashing; zone 1's full
5-fixture chain lights uniformly at both partial and full brightness.
**Still unverified:** the Pico-side malformed-JSON fail-safe (amber
pulse) and the 15s watchdog timeout — both only trigger on raw serial
input, which `bridge.py` never forwards malformed (it validates JSON
itself before sending), so exercising them requires writing malformed
JSON directly to a `/dev/ttyPICOn` device, bypassing the bridge.

**Next:** repeat the 5-fixture-per-zone scale-up for zones 2–4, decide
each zone's real `NUM_LEDS` value as fixtures are wired, and directly
test the amber fail-safe/watchdog path against raw serial before relying
on it in the field.

## Stage 2: Field deployment (Phase 1 — 4 zones)

Real installation, replacing the bench's CC/CV 5V rail + standalone 12V PSU
with the full 24V power system, and scaling from the jig's single-Pico test
to the 4 physical zones leaving the hub box. One 24V/300W PSU feeds two
independent buck converters — nothing downstream shares a raw 24V rail.

```
24V/300W PSU
  │
  ├─► 24V→12V buck (5A) ──► common 12V/GND bus ──► 4× 2A fuse ──► 4× IP67/68 3-pin connector
  │                                                                  └─► zone N trunk (12V + GND)
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
- **One 2A fuse per zone** (blade fuse or resettable PTC) between the 12V bus
  and that zone's connector. A short in one zone — most likely a fixture
  that took on water — then blows its own fuse instead of current-limiting
  the shared 5A buck and darkening all four zones. 2A is several times a
  5-fixture zone's worst-case draw; raise it if a zone grows past ~30
  nodes, keeping it under the buck's 5A.
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

**74AHCT125 pinout, all 4 zones (DIP-14 SN74AHCT125N):**

| Pin | Name | Connects to |
|---|---|---|
| 1 | 1OE | GND (tie low — zone 1 gate always enabled) |
| 2 | 1A | Pico 1 GP0 |
| 3 | 1Y | Zone 1 → 300–470Ω resistor → trunk data |
| 4 | 2OE | GND (tie low — zone 2 gate always enabled) |
| 5 | 2A | Pico 2 GP0 |
| 6 | 2Y | Zone 2 → 300–470Ω resistor → trunk data |
| 7 | GND | Common ground rail |
| 8 | 3Y | Zone 3 → 300–470Ω resistor → trunk data |
| 9 | 3A | Pico 3 GP0 |
| 10 | 3OE | GND (tie low — zone 3 gate always enabled) |
| 11 | 4Y | Zone 4 → 300–470Ω resistor → trunk data |
| 12 | 4A | Pico 4 GP0 |
| 13 | 4OE | GND (tie low — zone 4 gate always enabled) |
| 14 | VCC | 5V rail (24V→5V buck output) |

Every `nOE` pin must be tied to GND, not left floating — a floating
output-enable is undefined and can leave that gate not driving at all,
indistinguishable from a disconnected GP0 (LEDs just stay dark). Pins 7
and 14 are shared across all 4 gates — one physical chip, not one per
zone. Single-channel derivation and bench-test context: [pico/README.md](../pico/README.md) §4.

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
