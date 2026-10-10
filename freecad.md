# Globe Cradle

A 3D-printable spherical cradle mount designed to hold a 59mm diameter globe,
with a bottom nipple to accept a 1/4" ID / 3/8" OD tube (interference/pressure
fit, no adhesive — see Assembly below; confirmed with the user 2026-07-29,
superseding the glued fit this part originally shipped with).

## Part Specifications

| Feature              | Dimension          |
|----------------------|--------------------|
| Globe diameter       | 59mm               |
| Inner radius (cup)   | 29.5mm             |
| Outer radius (cup)   | 32mm               |
| Wall thickness       | 2.5mm              |
| Cradle depth         | ~7.4mm (1/8 globe) |
| Nipple outer radius  | 7.36mm             |
| Nipple bore radius   | 4.5mm (interference fit — was 4.86mm slip-fit-for-glue) |
| Nipple length        | 20mm               |
| Bore depth           | 15mm               |
| Tube OD (press fit)  | 9.525mm (3/8")     |
| Tube ID              | 6.35mm (1/4")      |

## Files

- `models/light-cradle-top-refined.3mf` — current printable export (FreeCAD-generated mesh); this is the file actually in the repo and the one that's been printed and fit-tested
- No `.FCStd` source is currently checked into this repo — if it lives only in a local FreeCAD session or another location, add it here so the mesh isn't the only copy

## Suppliers

- Globe: https://www.superiorlighting.com/6-inch-plastic-globe-plain-lip-opening-white-opal-acrylic/

## As-built vs. this doc (2026-09-02)

Measured directly from `models/light-cradle-top-refined.3mf`'s mesh (2051 vertices /
4102 triangles), since no `.FCStd` source is in-repo to check against:

- **Globe stays 59mm** — confirmed with the user 2026-09-02, not changing.
- **Cup/rim diameter checks out.** The spec table's "outer radius (cup) 32mm" is the
  *sphere primitive's* radius used in the boolean construction (Construction Method
  step 1), not the finished rim's opening size — those are different numbers by
  design, and the table didn't distinguish them. For a 1/8-height cap of a 59mm
  globe, the rim opening's actual radius works out to ≈19.5mm (`sqrt(R² - (R-h)²)`
  with R=29.5mm, h=7.4mm), i.e. ≈39mm diameter — and the mesh measures a 40mm
  overall diameter at that rim. These agree; no design change here, just a doc
  ambiguity worth this note so it doesn't get mis-read as a mismatch again.
- **Nipple bore does not match this doc's spec, and this one is unresolved.** The
  doc specifies a 4.5mm bore radius (9mm diameter) sized for an interference press-fit
  against the 9.525mm-OD tube (see the Nipple bore radius row and the note below the
  spec table). The mesh's nipple, however, has a ~2.8mm-diameter (r≈1.4mm) center
  bore through most of its ~19mm length — sized like the *fiber-only* hole from the
  LED holder insert in
  [docs/fixture_construction_fiber.md](docs/fixture_construction_fiber.md) §1, not a
  tube-interference bore. The nipple's outer shaft also reads ~9.6mm OD (close to the
  tube's own 9.525mm OD), with a wider collar near the cup and a small flange at the
  tip. A triangle mesh doesn't preserve feature intent, so this could be: (a) the tube
  design changed to slide over the nipple rather than press into a bore, with the fiber
  routed through a separate small channel, or (b) this file is genuinely a different
  part (closer to the LED holder insert) that inherited the "cradle" name. Since the
  user has printed and fit-confirmed the current cradles, whichever it is clearly
  works — but the written spec below (Nipple bore radius, and the interference-fit
  note) is stale relative to the actual file and should be corrected once the intent
  is confirmed against the `.FCStd` source rather than the exported mesh.

## Construction Method

Built in FreeCAD 1.1.1 using the Part workbench:

1. Outer sphere primitive (32mm radius, full sphere)
2. Inner sphere primitive (29.5mm radius, full sphere)
3. Boolean Cut: outer minus inner → hollow shell
4. Box primitive (100x100x100mm) positioned to crop upper portion
5. Boolean Cut: shell minus box → cradle cup shape
6. Cylinder primitive for nipple outer wall (7.36mm radius, 20mm height)
7. Boolean Union: cup + nipple cylinder
8. Cylinder primitive for bore (4.5mm radius, 15mm height)
9. Boolean Cut: assembly minus bore cylinder → finished part

Bore radius revised from an earlier 4.86mm (a slip fit sized for adhesive)
down to 4.5mm — roughly 0.5mm diametral interference against the 9.525mm
tube OD, confirmed with the user 2026-07-29 in favor of a pressure-only
push-fit (no epoxy/PVC cement) per the Assembly section below. This
joint doesn't need to be watertight — nothing above the base enclosure is
electrical — it only needs to hold mechanically under the globe's weight
and wind-driven stem flex. FDM prints commonly come out slightly
undersized on holes, so test-fit the bore on the PLA prototype first and
adjust the radius before committing to an ASA production run.

## 3D Printing Notes

- Recommended material: PETG or PLA
- Layer height: 0.2mm - cups use 0.12mm reduce outer wall speed to 30-40mm/s
- Infill: 40%+ for strength around nipple
- Print orientation: cup opening facing up

## Assembly

1. Assemble base/led mount
2. Connect incoming/outgoing 12v/ground/data to led leads
3. Tubing/wire retainer are the same length, fiber is 50mm longer than tubing
4. Insert tubing through lid via compression seal and insert into nipple (pressure only)
5. Thread fiber through top of globe cup
6. Thread retaining wire into tube until flush with tube.
7. Adjust fiber so it seats into the led housing hole
8. Attach globe cup to tubing (pressure only)
9. Attach globe to holder

## Disassembly

1. Open base and disconnect incoming/outgoing wires
2. Remove globe from globe cup
3. Remove globe cup from tube
4. Remove fiber/wire from tubing
5. Remove tube from led retainer
6. Remove led retainer from base

## Base Housing

Weatherproof lower enclosure that sits flat on top of the ground, holding the
30mm x 30mm x 10mm LED/fiber-alignment mount and the base of the stem.
Pinned to the ground with common drip-irrigation metal loop stakes rather
than buried, since burial was moved to the trunk cable only — the housing
itself stays on the surface, exposed to sprinklers and rain but not
flooding, and must be watertight since it contains the LED. Bark mulch may
be spread over the housing for looks (stem and globe stay clear), which
keeps its floor and lower walls damp for days after each watering — see
*Water protection* below.

Design decisions locked in for this part, confirmed with the user
2026-07-29:
- **One-piece, sealant-sealed shell, but sealed once on the bench, not in
  the field.** The node's 4 leads (12V, GND, DIN, DOUT) are permanently
  soldered inside the housing to two short pigtails *before* the housing is
  closed and sealed — this whole assembly happens at build time, not at
  install time. Each pigtail ends in bare tinned lead wire, not a
  connector — the connection to the trunk cable is made later, at install,
  outside the housing (see connector decision below). Superseded 2026-08-27:
  the box is no longer field-swappable as a sealed unit; "failure" now means
  cutting the splices open and re-splicing, not unplug-and-swap. See the
  trade-off note there.
- **Cylindrical puck** shape — simplest Part-workbench boolean sequence
  (concentric cylinders), no corners to catch a mower/trimmer at ground level.
- **Gel-filled direct-bury splice connectors at each of the two cable
  penetrations, spliced *outside* the housing, not through a bulkhead
  cutout.** Superseded 2026-08-27 — this section originally specified
  Deutsch DT-series quick-disconnect connectors (DT04-3P plug / DT06-3S
  socket) for field-swappability without cutting/resplicing wire; that
  decision was reversed in favor of lower cost and no dedicated crimp tool,
  accepting slower field service in exchange (rare fixture failures don't
  justify the added connector/tooling cost). Each pigtail exits the housing
  through a small sealed grommet bore and ends in bare wire a short distance
  outside the shell. The buried trunk cable's in/out ends are joined to the
  pigtails there with gel-filled direct-bury connectors (ZONE INDUSTRY CORP
  silicone-filled, UL 486G — see
  [docs/fixture_construction_fiber.md](docs/fixture_construction_fiber.md)
  §2 BOM), twist-on, no tool required. A coiled service loop of extra trunk
  cable at each box allows a future cut/re-splice without pulling new wire.
  Servicing a fixture = lift the box, dig up the splices beneath it, cut
  them open, splice in a replacement box's pigtails using the service
  loop's slack, rebury the splices. This still eliminates the lever-nut-inside-the-box splice
  cavity from the earliest design — the splice just moved outside the box
  and changed connector technology twice since — see
  [docs/fixture_construction_fiber.md](docs/fixture_construction_fiber.md)
  §5 for the full wiring convention and BOM.
- **Stem port keeps the mount's stem boss fully inside the housing.** The
  mount's stem-side boss is 15mm dia x 10mm tall; the silicone tube itself
  is 9.525mm OD. Rather than letting the 15mm boss poke through the housing
  top (which would need an ~16mm port and leave the boss exposed to
  weather), the housing top port is sized to the **tube**, just above where
  it seats on the boss. This keeps the boss-to-tube joint fully enclosed and
  protected, and only the plain tube crosses the watertight boundary. If
  bench-fit shows the tube needs to seat *above* the housing top instead
  (e.g. the boss has to sit proud for stem geometry reasons), widen the
  port and revisit — flagged here so the trade-off isn't silently
  re-decided later.
- **Stem port seals with a compression grommet, not a sealant bead directly
  on the tube.** Confirmed with the user 2026-07-29: cured silicone sealant
  doesn't reliably bond to the tube's own cured-silicone surface (both are
  chemically the same inert, low-surface-energy material, so a sealant bead
  applied there mostly sits on top rather than adhering — a real risk at a
  joint that flexes every time the stem moves in the wind). Instead, the
  port holds a small rubber compression grommet (same category part as the
  IP68 cable glands used elsewhere in this project) sized to the tube's
  9.525mm OD, sealing by mechanical squeeze rather than adhesion. Sealant
  is still used, but only as a secondary bead around the grommet's own
  flange-to-cap joint — rigid printed plastic to rigid grommet body, which
  sealant bonds to fine, unlike the tube itself.

### Part Specifications

| Feature                     | Dimension                        | Notes |
|------------------------------|-----------------------------------|-------|
| Overall shape                | Cylindrical puck                  | Sits flat on the ground surface, floor down |
| Outer diameter                | 70mm                              | Shrunk from an earlier lever-nut-based draft (95mm) now that the node wires straight to pigtails with no in-box splice hardware — encloses the 30x30mm mount + pigtail dressing with margin |
| Overall height                | 40mm                              | 30mm cup + 10mm cap, before final trim |
| Wall thickness                 | 3mm                               | Thicker than the globe cradle's 2.5mm — this part carries stake-down load at the flanges |
| Mount cavity (on internal boss)| 34mm x 34mm x 12mm                | 2mm clearance around the 30x30x10mm mount block on each side and above |
| Stem port (in cap)             | ~4mm tall collar, counterbored for a compression grommet | Grommet ID matches 9.525mm tube OD, seals by mechanical squeeze; grommet OD/flange size is [TBD] — confirm against the actual grommet product before finalizing the counterbore |
| Pigtail exit bores (in floor)  | 2x ~8mm bore, small grommet/potted seal | Trunk-in-side, trunk-out-side pigtail; offset to the side of the mount boss. Not a full trunk-cable gland — the actual splice (gel-filled direct-bury connector) sits outside the housing |
| Stake-mount flanges            | 2x, opposite sides, 18mm x 12mm, 4.5mm through-hole | Sized for typical drip-irrigation loop-stake wire (~3mm dia) |
| Cap-to-cup joint               | 2mm deep overlapping lip           | Sealant-bead seam, sealed once at bench-assembly time |

### suppliers
- underground wire: https://cheapsprinklers.com/products/18-3x250-wire-18-3-x-250ft

### Construction Method

Built in FreeCAD 1.1.1 using the Part workbench — two separate solids (cup
and cap), same boolean-first approach as the globe cradle:

**Cup (lower body):**
1. Outer cylinder, 35mm radius, 30mm height
2. Inner cylinder cut, 32mm radius, positioned to leave a 3mm floor →
   hollow cup
3. Box or cylinder **union** for the internal mount boss (raised platform
   inside the cup floor, ~5mm tall, footprint sized to the 34mm x 34mm
   mount cavity) — a boss, not a recess, so the LED sits above any water
   that reaches the true floor
4. Two cylinder cuts through the floor for the pigtail exit bores (~8mm),
   offset to the side of the mount boss
5. Two box **unions** for the stake-mount flanges at the outer rim (opposite
   sides), then two cylinder cuts through each flange for the stake
   through-holes

**Cap (lid):**
6. Outer cylinder matching the cup's outer lip diameter, ~10mm height
7. Inner cylinder cut sized to the cup's 2mm overlap lip → thin disc that
   seats over the cup
8. Cylinder **union** for the stem-port collar (~4mm tall boss centered over
   where the mount's stem boss will sit)
9. Cylinder cut through the collar for the stem port, sized to the chosen
   grommet's insertion OD
10. Shallow counterbore cut at the collar's top face, sized to the
    grommet's flange OD and thickness, so the grommet seats flush and can't
    push through under stem movement

### 3D Printing Notes

- Prototype in PLA on the Anycubic Kobra to fit-check the mount cavity,
  pigtail exit bores, and stake-flange spacing before committing to ASA,
  per the existing fixture fabrication workflow's two-material process
- Recommended production material: ASA (UV/thermal stability for a
  surface-sited, full-sun part) — not PLA, per established workflow
- Layer height: 0.2mm; reduce outer wall speed near the stem-port collar
  and stake-flange holes for cleaner small-feature detail
- Infill: 40%+, especially through the stake-flange bosses — these carry
  the pinning load from the ground stakes
- Print orientation: cup opening facing up; cap printed flat, port collar
  facing up

### Bench Assembly (done once per box, before install)

1. Fit-check the mount block and stem boss dry in the cup's mount boss and
   cap's stem port before any sealant goes on
2. Solder the node's 4 leads to two short pigtails (in-side: 12V, GND, DIN;
   out-side: 12V, GND, DOUT), heat-shrink each joint, tin the free end of
   each pigtail wire — these stay bare leads until spliced to the trunk
   cable at install, not terminated in a connector at bench time
3. Feed each pigtail through its floor exit bore, seat the mount block on
   the internal boss, feed the stem up through the cap's port and seat the
   compression grommet in its counterbore around the tube
4. Run a continuous bead of clear flexible outdoor sealant (GE Silicone II,
   Sikaflex, Loctite Marine — not epoxy, matching the globe-seam convention)
   around the cup-to-cap lip, the grommet's flange-to-cap joint, and each
   pigtail exit bore — the grommet itself, not sealant, is what seals
   against the tube
5. Seat the cap onto the cup, tool the sealant fillets so water sheets off
   each joint rather than pooling; let cure per datasheet
6. Bench-test the node before it goes out to the garden

### Field Install / Service

1. Strip the buried trunk cable's in/out ends and splice each to the
   corresponding pigtail leads with gel-filled direct-bury connectors
   (ZONE INDUSTRY CORP, per BOM), outside the housing. The pigtails leave
   through the housing floor, so they run straight down into the ground
   to the splices
2. Coil a service loop of extra trunk cable beside the splices, then bury
   the splices and loop, so a future re-splice doesn't require pulling new
   wire
3. Set the housing flat on the soil surface over the splice hole (not sunk
   into it) and pin it with a loop stake through each of the two flange
   holes, prongs pushed fully into soil
4. Confirm it sits level, then spread bark mulch over the housing if
   wanted, keeping the stem port and stem clear
5. **To service a failed fixture**: pull back the mulch, unstake and lift
   the box, dig up the splices beneath it, cut them open, splice in a
   replacement box's pigtails using the service loop's slack, rebury the
   splices

### Water protection

The housing sits on the surface, so water reaches it from sprinklers and
rain, and bark mulch keeps its floor and lower walls wet long after. If
water gets in, the 12V DC across the node's pads corrodes them within
weeks, a wet 12V-to-DIN leak puts 12V on the data line, and the dead node
blacks out every fixture downstream of it in the zone (BI/BO unwired). So:

- **Coat the node.** After the bench test, brush conformal coating (or a
  thin layer of the same clear silicone) over the WS2815's back, its pads
  and the solder/heat-shrink joints, keeping the LED face clear for the
  fiber. This is the main protection — the electronics survive a seal that
  fails. The strip's own IP rating doesn't carry over once a single LED is
  cut from it.
- **Pot the pigtail floor bores**, not just a grommet: fill each bore around
  the pigtail with silicone from inside the housing. The floor sits on damp
  soil under mulch, so these are the most-exposed joints. Seal the cut end
  of each pigtail's outer jacket inside the housing with adhesive-lined
  heat-shrink so water can't creep along the conductors under the jacket.
- **No weep hole.** A drain hole in a floor that sits on wet ground under
  mulch lets water and insects in rather than out. The housing stays fully
  sealed; the coating covers what condensation gets in.
- **Keep the stem port shedding water.** Rain and sprinkler water run down
  the stem to the compression grommet, the only upward-facing joint. Keep
  mulch from piling against it so it isn't sitting wet.
- **Aim sprinkler heads away from fixtures** where possible — a close-range
  jet can force water past seals that rain never would.

# Fiber Polishing Puck

Use #12-24 screw through side to retain fiber
Fiber bore 3.53mm
bottom inset .3mm deep, 6mm diameter
30mmx30mmx20mm

## Files

No `.FCStd` source exists yet for this part — model it fresh from the
Construction Method below; there's no earlier draft to reconcile against
like the globe cradle's.

## Construction Method

Built in FreeCAD 1.1.1 using the Part workbench, same boolean-first
approach as the other parts in this file:

1. Outer cylinder, 15mm radius, 6mm height, coaxial with the global Z
   axis → base disc blank
2. Outer cylinder, 6mm radius, 10mm height, coaxial, stacked on top of the
   base disc (z = 6 to 16mm) → collar blank
3. Boolean Union: base disc + collar → puck blank (16mm overall height)
4. Cylinder cut, 1.765mm radius (3.53mm dia), full height (through both
   the base disc and the collar), coaxial with the blank → fiber bore
5. Cone frustum cut, coaxial with the bore, sitting at the bottom face:
   2.5mm radius at the bottom face tapering to 1.765mm radius (matching
   the bore from step 4) over 0.3mm of height → bore exit chamfer, blended
   into the straight bore rather than stepped
6. Cylinder cut, 1.7mm radius (3.4mm dia), axis horizontal (perpendicular
   to the puck's main axis), positioned 4mm below the collar's top face
   (i.e. z ≈ 12mm), from one side of the collar's outer wall in to the
   fiber bore → clamp screw clearance hole. The collar is only 12mm
   across, so this only needs to travel ~4.2mm to hit the bore — nowhere
   near the base disc's full 15mm radius
7. At the same height, on the collar's opposite (far) side: a hex pocket
   for an M3 nut, open at the collar's outer surface, ~2.6mm deep —
   approximate the hex shape with two or three box cuts at 60° to each
   other, same box+cylinder combination technique used for the Base
   Housing's stake-flange holes. It opens outward, not inward, so the nut
   can be dropped in from outside before final assembly
8. Continue a second, smaller cylinder cut (same 1.7mm radius as step 6)
   from the bottom of that hex pocket in to the fiber bore → pilot hole
   connecting the nut trap to the bore, so the screw's shank has a
   continuous path from the near-side clearance hole, across the bore,
   through to the nut. Full span from the near-side clearance hole's outer
   opening to the far side, through the nut, is ~11.8mm — inside the
   M3x14mm screw's length with a couple mm to spare, so the screw doesn't
   protrude past the collar's outer surface fully driven in
9. Two shallow box cuts on the collar's outer wall, opposite each other →
   grip flats

## 3D Printing Notes

- Print with the base disc's bottom (reference) face down against the
  bed — this is the flattest surface FDM printing can give you, and it's
  the face the whole jig depends on. The stepped base-disc-then-collar
  shape sits stably in this orientation with no overhangs, so no supports
  needed
- The bore may print slightly undersized right at the first layer or two
  from elephant's-foot squish; ream lightly with a 3.53mm drill bit by
  hand if the fiber doesn't slide freely, same as the fiber holes in the
  LED holder insert
- Prototype in PLA on the Anycubic Kobra to confirm the fiber slip-fit and
  clamp-screw/nut-trap engagement; print the puck kept on the bench
  long-term in PETG — better abrasion and polish-compound resistance than
  PLA for a part that gets wet-sanded against repeatedly
- Layer height 0.2mm, 40%+ infill — no fine cosmetic features here, this
  part just needs to be dimensionally solid and hold the nut trap under
  clamp-screw torque
- True the printed face flat before first use — see
  [docs/fiber_polishing_jig.md](docs/fiber_polishing_jig.md)'s calibration
  step; don't skip this even on a good-looking print
