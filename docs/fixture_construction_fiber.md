## Fixture Construction Guide — Fiber-Optic Flower-Stem LED

# Base Assembly

1.  3d print parts:
    - base and cap = PETG
    - globe cup, led retainer and upper nipple all PLA
2.  Clean all parts, holes to leds, tube nipples - 3/8" for 10mm holes, 3.53mm for fiber holes, 5.93mm for cable holes
3.  Cut pigtail in/out 40cm each side, trim one end 7cm for inside connection
4.  Wire and glue leds to led retainers - 80mm leads
5.  Glue upper nipple to led retainer using a piece of fiber as a guide
6.  Insert pigtails into fixture and angle up
7.  Insert led retainer into fixture, with pigtail leads and led wires trough side holes.
8.  For first fixture in node, add capacitor to VCC/GND (long wire is +)
9.  Solder and shrinkcap connections
10.  Drill second hole on base for DIN (green to LED)

# Stems preparation

1.  Cut silicon tube to desired length
2.  Cut retaining wire (coat hanger wire) to the length of the silicon tube
3.  Cut the fiber 60mm longer than the silicon tube
4.  Cut diffuser rod to 10mm lengths
5.  Drill fiber hole in diffuser 1/2 of length.

# Fiber Preparation

This is the LED-end face only — the end that seats directly against the
WS2815 node. Use the fiber polishing puck jig
([docs/fiber_polishing_jig.md](fiber_polishing_jig.md),
[freecad.md](../freecad.md) §Fiber Polishing Puck) rather than holding the
fiber by hand — the puck's own flat face gives the cut and every sanding
pass a perpendicularity reference by construction, instead of relying on
eyeballing it. Summary (see the jig doc for the full step-by-step):

1.  Clamp the fiber in the puck with a few mm protruding past the puck's
    bottom face, and cut it flush with that face (blade or fiber-optic
    cutting tool, using the face as a backstop) rather than freehand.
2.  Re-clamp with the fiber advanced ~0.5mm past the face, then wet-sand
    the puck's face flat against fine sandpaper on a hard, flat surface (a
    scrap of glass or tile works). Step through grits: ~400 → 600 → 1000 →
    1500 → 2000, a few figure-eight strokes per grit, wiping the face
    clean between grits so a coarser scratch doesn't carry forward.
    Re-advance the fiber a small amount (~0.2mm) between grits — the puck
    face itself, not the fiber tip, tells you when a grit is done.
3.  Finish with a metal-polish compound (e.g. Brasso) on a soft cloth or
    felt pad, or a plastic-polish compound (e.g. Novus 2/1), until the face
    looks clear rather than frosted — held up to light, you should see
    through it, not a matte scatter.
4.  Loosen the clamp and withdraw the fiber down and out through the
    bottom of the puck (the direction it was polished), not back up
    through the bore, to avoid scratching the finished face.
5.  Inspect the finished face against a light source: it should be flat,
    perpendicular, and glassy-clear with no visible scratches, chips, or
    rounding at the edge before seating it against the LED.

# Final Assembly
1. Glue diffuser to unpolished end of fiber
2. Add globe cap to tube, insert retaining wire and fiber.
3. Insert tube into base with about 10mm inside
4. Align fiber with led hole
5. Lower cap assembly into base
6. Attach globe
7. Once assembled correctly seal all joints with silicon sealant

# Bill of materials

WS2815, 5050 SMD, DC12V, individually addressable | Cut singly from a [12V WS2815 strip, 60 LEDs/m](https://www.superlightingled.com/12v-ws2815-individually-addressable-5050-rgb-led-lights-strip-60ledsm-p-2133.html); 
Fiber optic cable -  PMMA (acrylic) end-glow fiber, ~3mm core 
Spring wire | 304 stainless steel, straight, full-hard temper, 1.4/1.6/1.8mm (bench-test set) 
   or coathanger wire
Silicone tubing | Black silicone, 1/4"ID x 3/8"OD 
Diffuser bead  ~10–15mm frosted/opal acrylic bead  Epoxied to the fiber's globe-end tip 
Fine grit sandpaper (400, 600, 1000, 1500, 2000)
2.5" frosted acrylic ball
100% silicone sealant — GE Silicone II (or equivalent)
18 AWG 3 conductor underground wire