# Fiber End-Face Polishing Jig

A hand-held jig that holds a stem's fiber perpendicular through cutting,
sanding, and polishing of the **LED-end face** (the end that seats
directly against the WS2815 node — see
[docs/fixture_construction_fiber.md](fixture_construction_fiber.md)'s
Fiber Preparation section, which this jig replaces the freehand technique
for). The globe-end face is never polished — it gets the diffuser bead
glued on per that doc's Final Assembly step 1.

This is a reusable bench tool, built once, same as the electrical
[fixture_test_jig.md](fixture_test_jig.md) — not a per-fixture consumable.

## Principle

This is the same self-limiting "polishing puck" technique used for
telecom fiber-optic connectors: the fiber is clamped inside a puck so it
protrudes a small amount past the puck's own flat bottom face, then that
face — not the fiber tip — is what registers flat against the sandpaper.
Once sanding wears the fiber down flush with the puck's face, the puck's
own (much larger, rigid) face starts carrying the sanding pressure instead
of the fiber tip, and further removal on that fiber all but stops on its
own. Because the puck's bottom face and its fiber bore are machined
coaxial and perpendicular to each other by construction, the fiber's end
face inherits that same flatness and perpendicularity — with much better
repeatability than eyeballing it by hand.

The puck also stands in for the current "cut square with a sharp
blade/fiber-optic cutting tool, as close to perpendicular as you can get
by eye" step: its bottom face gives the blade a flat backstop to cut
against, instead of cutting freehand.

## Parts

| Part | Notes |
|---|---|
| Fiber polishing puck (printed) | See [freecad.md](../freecad.md) §Fiber Polishing Puck for the part design |
| M3 x 14mm screw + M3 nut | Radial clamp — captured nut, not a self-tapped hole (see freecad.md; this screw gets tightened/loosened dozens of times across a project's worth of fixtures) |
| Hard flat surface (glass or tile scrap) | Same reference surface already used for freehand sanding |
| Fine grit sandpaper (400, 600, 1000, 1500, 2000) | Same as [fixture_construction_fiber.md](fixture_construction_fiber.md) BOM |
| Metal- or plastic-polish compound (Brasso, or Novus 2/1) | Same as existing BOM |
| Sharp blade or fiber-optic cutting tool | For the initial score/cut, same as existing step 1 |
| Water + soft cloth | Wet-sanding and cleaning the face between grits |

## First use / after any drop — true the puck's own face

The whole jig depends on the puck's bottom face actually being flat. FDM
prints can have a slightly proud edge or elephant's-foot bulge at the
first layer, so before using a new puck (and again if it's ever dropped or
gouged), true it up against the same reference surface you'll use for
fibers:

1. With no fiber loaded, wet-sand the bare puck face on 400 grit against
   the glass/tile, flat, figure-eight strokes.
2. Continue until the entire face shows uniform matte contact — no shiny
   untouched islands anywhere on the ring around the bore.
3. Wipe clean. The puck is now trued and ready.

## Using the jig

1. Slide the fiber through the puck's bore from the top until roughly
   8mm protrudes past the bottom face — enough working length to cut
   outside the puck body.
2. Snug the M3 clamp screw against the fiber, finger-tight — just enough
   to stop it sliding. This clamp point is in the scrap length that gets
   cut away, so marking the fiber there doesn't matter.
3. Score the fiber flush with the puck's bottom face, using the face
   itself as the cutting backstop, and snap off the excess (or cut it
   there directly with a fiber-optic cutting tool).
4. Loosen the clamp, advance the fiber ~0.5mm past the face, and
   re-tighten.
5. Wet-sand on 400 grit: puck face flat against the paper, figure-eight
   strokes, same as the existing procedure. Once the puck's face itself
   is riding flat on the paper — even resistance across the whole face,
   not just at the fiber — that grit is done; further strokes mostly
   polish the puck, not the fiber.
6. Loosen, advance the fiber another ~0.2mm, re-tighten, wipe the face
   clean, and repeat step 5 for 600 → 1000 → 1500 → 2000 grit. Small,
   repeated advances keep each grit's cut shallow, which is what makes the
   flush-with-the-puck result reliable — one big advance reintroduces the
   same by-eye squareness problem the jig exists to remove.
7. Finish with polish compound on a soft cloth or felt pad, puck face
   still registering flat against the backing, until the face looks
   clear rather than frosted — same finish criterion as the existing doc.
8. Loosen the clamp fully and withdraw the fiber **down and out through
   the bottom** — the same direction it was polished — not back up
   through the top. Pulling the finished tip back up through 8mm of
   3.53mm bore risks scratching the face you just finished against the
   bore wall or its top edge.
9. Inspect the face against a light source per the existing criteria:
   flat, perpendicular, glassy-clear, no visible scratches, chips, or
   rounding at the edge.
