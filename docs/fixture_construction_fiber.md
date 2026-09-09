# Fixture Construction Guide — Fiber-Optic Flower-Stem LED

1.  3d print parts:
    - base and cap = PETG
    - globe cup, led retainer and upper nipple all PLA
2.  Cut silicon tube to desired length
3.  Cut retaining wire (coat hanger wire) to the length of the silicon tube
4.  Cut the fiber 60mm longer than the silicon tube
5.  Cut diffuser rod to 10mm lengths
6.  Drill fiber hole in diffuser 1/2 of length
7.  Polish the fiber end touching the led — this end must stay clear and flat,
    the opposite treatment from the frosted globe-end tip in Step 6:
  - Score and snap, or cut square with a sharp blade/fiber-optic cutting tool,
   as close to perpendicular to the fiber axis as you can get by eye.
  - Wet-sand the end face flat against fine sandpaper on a hard, flat surface
   (a scrap of glass or tile works), fiber held perpendicular to the paper.
   Step through grits: ~400 → 600 → 1000 → 1500 → 2000, a few figure-eight
   strokes per grit, wiping the face clean between grits so a coarser
   scratch doesn't carry forward.
  - Finish with a metal-polish compound (e.g. Brasso) on a soft cloth or
   felt pad, or a plastic-polish compound (e.g. Novus 2/1), until the face
   looks clear rather than frosted — held up to light, you should see
   through it, not a matte scatter.
  - Inspect the finished face against a light source: it should be flat,
   perpendicular, and glassy-clear with no visible scratches, chips, or
   rounding at the edge before seating it against the LED.
8. Glue diffuser to unpolished end of fiber


# Final Assembly
1.  Cut 2 pigtails from the main cable 20cm each, Strip one end 70mm (inside), the other 30mm and strip ends
2.  Feed lond end of supply pigtail through the fixture and bend upwards
3.  Pull led wires and cable wires through the retainer holes
4.  Solder connections (VCC to led, in/out red, GND to led gnd-in-out-white, blue to DIN, DOUT to continued blue)
5.  For first fixture in node, add capacitor to VCC/GND (long wire is +)
6.  Trim cap and based for tight fit
7.  Check nipples for easy tube insertion.
8.  Add globe cap to tube, insert retaining wire and fiber.
9.  insert tube into base with about 10mm inside
10. Align fiber with led hole
11. Lower cap assembly into base
12. Attach globe

- Once assembled correctly seal all joints with silicon sealant

## Stem/globe sub-assembly (moved from docs/fixture_test_jig.md)

1.  Mark DIN on the fixture
2.  Insert the hose into the base cap and pull 1/2 way up hose
3.  Insert fiber into globe cap [glue here? - globe, cap and fiber all in place?]
4.  Insert hose into globe assembly
5.  Insert retaining wire into hose
6.  Push fiber into led holder until set
7.  Seat hose into base nipple
8.  Pull down cap to seat - adjust hose for fit
9.  Add globe to top (see 3)

## Component measurements

**Note:** these predate, and have not been reconciled with, the nipple
bore discrepancy already flagged in freecad.md (spec vs. as-printed mesh) —
treat both as unresolved until checked against current printed parts.

base nipple
  - total depth 35mm - 25mm for hose - additional 10mm for fiber to led hole
globe assembly
  - hose insert depth 10mm
  - from nipple entrance to top of diffuser - 60mm
    - hose insert - 10mm
    - fiber + diffuser - 50mm
    - inside cradle to diffuser top - 35

Example - for fiber 240mm
  - hose/wire 180

# Bill of materials

WS2815, 5050 SMD, DC12V, individually addressable | Cut singly from a [12V WS2815 strip, 60 LEDs/m](https://www.superlightingled.com/12v-ws2815-individually-addressable-5050-rgb-led-lights-strip-60ledsm-p-2133.html); 
Fiber optic cable -  PMMA (acrylic) end-glow fiber, ~3mm core 
Spring wire | 304 stainless steel, straight, full-hard temper, 1.4/1.6/1.8mm (bench-test set) or coathanger wire
Silicone tubing | Black silicone, 1/4"ID x 3/8"OD 
Diffuser bead  ~10–15mm frosted/opal acrylic bead  Epoxied to the fiber's globe-end tip 
Fine grit sandpaper
2.5" frosted acrylic ball
100% silicone sealant — GE Silicone II (or equivalent)
18 AWG 3 conductor underground wire