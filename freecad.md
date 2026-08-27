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

- `globe_cradle.FCStd` — FreeCAD 1.1.1 source file
- `globe_cradle.stl`  — STL export for 3D printing

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

Weatherproof lower enclosure that sits at (not below) grade, holding the
30mm x 30mm x 10mm LED/fiber-alignment mount and the base of the stem.
Pinned to the ground with common drip-irrigation metal loop stakes rather
than buried, since burial was moved to the trunk cable only — the housing
itself stays at the surface, exposed to sprinklers and rain but not
flooding, and must be watertight since it contains the LED.

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
  (concentric cylinders), no corners to catch a mower/trimmer at grade.
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
  Servicing a fixture = dig down to the box, cut all splices open, lift the
  box, splice in a replacement box's pigtails using the service loop's
  slack, rebury. This still eliminates the lever-nut-inside-the-box splice
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
| Overall shape                | Cylindrical puck                  | Sits flush at grade |
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
6. Bench-test the node before it ever goes in the ground

### Field Install / Service

1. Strip the buried trunk cable's in/out ends and splice each to the
   corresponding pigtail leads with gel-filled direct-bury connectors
   (ZONE INDUSTRY CORP, per BOM), outside the housing
2. Coil a service loop of extra trunk cable near the box before
   backfilling, so a future re-splice doesn't require pulling new wire
3. Pin the housing to grade with a loop stake through each of the two
   flange holes, prongs pushed fully into soil
4. Confirm level and flush-to-grade seating, then backfill up to (not over)
   the housing
5. **To service a failed fixture**: dig down to the box, cut all splices
   open, lift the box out, splice in a replacement box's pigtails using the
   service loop's slack, rebury
