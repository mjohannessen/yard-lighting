# Fixture Construction Guide — Fiber-Optic Flower-Stem LED

Build guide for the fixture head: a fixed base enclosure, buried at or just
below grade, holding the LED and coupling optics, feeding a flexible
fiber-optic + spring-wire stem that carries a passive globe. The stem bends
and springs back in the breeze; the globe end carries no electrical
connection at all, only light (fiber) and mechanical support (spring wire).

Fill in `[TBD]` dimensions once bench testing (holder alignment, wire stiffness,
fiber coupling) settles on final numbers — this guide is the assembly procedure
and part boundary, not a dimensioned drawing.

## 1. Design summary

Bottom to top:

1. Underground trunk cable (12V/GND/Data — 3 conductors, no backup line) enters
   a **base enclosure** at or just below grade — no rigid pipe riser, since
   nothing above the base is electrical.
2. **Base enclosure** (printed, ASA production) houses:
   - A **WS2815 LED holder insert** — a separate printed sub-part, populated
     on the bench, then glued into the base enclosure as a unit (§4). It
     holds the **WS2815 5050 SMD individually-addressable LED** (DC12V), cut
     singly from a 12V WS2815 strip, 60 LEDs/m
     ([superlightingled.com](https://www.superlightingled.com/12v-ws2815-individually-addressable-5050-rgb-led-lights-strip-60ledsm-p-2133.html)) —
     chosen over a domed WS2811 pixel node specifically because the flat SMD
     package lets the fiber's polished base end seat flush against the
     emitter face, where a domed lens would only touch a flat fiber tip at
     one point on the curve. WS2815 exposes a BI/BO backup-data pair for its
     "breakpoint resume" redundancy feature; **this project does not use
     it** — see §5. The holder's geometry, top to bottom:
     - A **nipple** at the top, sized for a snug slip fit with the silicone
       stem tube's OD (9.525mm) — no threads, no cable gland. The tube is
       bonded and sealed to the nipple with a bead of 100% silicone sealant
       (GE Silicone II) once the stem is built, per §4/Step 7. A threaded
       gland was considered and dropped: fine-pitch PG threads are risky to
       print reliably at this scale, and a glued joint using a sealant
       already in the BOM needs no new hardware.
     - Just below the nipple, inside the holder, a small hole passes the
       **fiber only** through — the spring wire terminates above this point,
       at the separate rigid anchor socket (see below), not down into the
       LED chamber.
     - The **LED**, retained face-up so it can't shift position, positioned
       so the fiber descending through the hole above lands in direct
       contact against its flat acrylic face — no reflector cone, no mirror
       film, no air gap. The fiber is end-glow (light only couples in
       through the end face via total internal reflection down the core),
       so a wide-angle mirrored concentrator doesn't help — light landing on
       the fiber's side surface is wasted regardless of how reflective the
       surrounding walls are; only proximity at the end face matters.
       Bench-confirmed as the design (superseding the earlier reflector
       cone). Hole-to-LED alignment is now the critical dimension, since a
       straight hole doesn't self-center the LED over the fiber the way the
       old cone's taper did — verify on the PLA prototype before committing
       to ASA.
     - The LED's leads exit through the holder's **side wall** and are glued
       in place there for strain relief and sealing before being soldered to
       the two pigtails (below).
     - The holder's **bottom edge is raised**, glued to the base enclosure's
       floor once the LED is seated and its leads glued and routed — this
       lets the holder be fully populated and checked on the bench before
       it's committed into the housing.
   - Two short **pigtails** off the LED's leads (12V/GND/DI on one,
     12V/GND/DO on the other — the BI/BO backup pins are left
     unconnected), soldered inside the enclosure at bench-assembly time and
     each exiting the enclosure through a small hole, snug-fit to the
     pigtail's bundle OD and sealed with a bead of 100% silicone sealant
     (GE Silicone II) rather than a threaded gland — same reasoning as the
     nipple, above. Each pigtail ends in bare tinned lead wire, joined to
     the corresponding trunk-cable end **outside** the enclosure with a
     gel-filled direct-bury connector (ZONE INDUSTRY CORP silicone-filled
     waterproof wire nut, UL 486G, 20–8 AWG — see §2 BOM) — a permanent splice,
     not a field disconnect. This trades field-swappability for cost and
     simplicity: a failed fixture is serviced by cutting the splice open
     and re-splicing rather than unplugging, so each fixture gets a coiled
     service loop of extra trunk cable at install to allow that without
     pulling new wire. See §5.
   - A rigid anchor socket, alongside the holder's nipple, that holds the
     spring wire's fixed (base) end — this is the fixed point of the
     cantilever; any play here undermines the whole spring effect.
3. **Flexible stem**: 1/4"ID x 3/8"OD (6.35mm x 9.525mm) black silicone tubing, containing (loose,
   not bonded to each other so they can slip slightly in a bend):
   - PMMA (acrylic) end-glow fiber, ~3mm core — glass fiber is not used here;
     it fatigues under repeated flex.
   - 304 stainless spring wire, straight/full-hard temper, diameter selected
     by bench test from 1.4/1.6/1.8mm — provides the cantilever stiffness and
     spring-back. Stiffness scales with diameter^4, so this choice matters
     more than it looks.
4. **Globe end**: the fiber's tip is sanded/frosted (400–600 grit or matte
   spray) and capped with a ~10–15mm frosted/opal acrylic diffuser bead,
   epoxied on — this kills the hot-spot a bare fiber tip would otherwise throw
   on the globe wall. The spring wire's top end anchors into a mount inside
   the globe's neck/cup, carrying the globe's weight and setting its sway.
5. **2.5" frosted globe**, seated over the diffuser bead + wire mount, bonded
   at the rim with a continuous bead of clear flexible sealant, tooled to a
   smooth fillet so water sheets off rather than pooling at the seam. Seam
   oriented at or below the globe's equator, never at the top.

No electrical connection exists anywhere above the base enclosure. Only optics
(fiber) and mechanics (spring wire) cross the flex zone — this is the point of
the design: the moving joint has nothing in it that can fatigue and fail
electrically.

## 2. Bill of materials — per fixture

| Part | Spec | Notes |
|---|---|---|
| Base enclosure | Printed part (FreeCAD → PLA prototype → ASA production) | Houses the LED holder insert (glued in), connector cavities, spring-wire anchor |
| LED holder insert | Printed part, same material path as base enclosure | Top nipple accepts the silicone stem tube; internal hole below the nipple passes the fiber only through to the LED; retains the LED face-up; LED leads exit the side wall (glued in place); bottom has a raised edge, glued into the base enclosure floor |
| LED node | WS2815, 5050 SMD, DC12V, individually addressable | Cut singly from a [12V WS2815 strip, 60 LEDs/m](https://www.superlightingled.com/12v-ws2815-individually-addressable-5050-rgb-led-lights-strip-60ledsm-p-2133.html); re-terminate DI/DO leads only — BI/BO backup pads left unconnected |
| Node lead wire | Silicone-insulated, fine-strand, 26–30AWG | Short static run from node to its two pigtails — doesn't flex, so stock leads could work, but silicone is cheap insurance |
| Gel-filled direct-bury connector | ZONE INDUSTRY CORP waterproof wire nut, silicone-filled, UL 486G, 20–8 AWG copper ([amazon.com/dp/B0GTYKXWRC](https://www.amazon.com/ZONE-INDUSTRY-CORP-Waterproof-Wire/dp/B0GTYKXWRC)) | Final pick — chosen for cost over the established DryConn brand; not yet field-proven for this project. If it fails in practice (splice corrosion, moisture ingress, mechanical failure), revisit and swap to DryConn or equivalent. 4 per fixture: 12V (3-way: node + trunk-in + trunk-out), GND (3-way), data-in (2-way: trunk-in → node DI), data-out (2-way: node DO → trunk-out) — data never shares a connector with the opposite direction. Twist-on, no crimp tool needed. Permanent splice, done *outside* the base enclosure — see §5 |
| Fiber optic cable | PMMA (acrylic) end-glow fiber, ~3mm core | Length = stem height + service loop; PMMA for flex-fatigue tolerance |
| Spring wire | 304 stainless steel, straight, full-hard temper, 1.4/1.6/1.8mm (bench-test set) | Cut to stem length; anchored rigidly at the base, free at the globe mount |
| Silicone tubing | Black silicone, 1/4"ID x 3/8"OD | Single lumen. ID sizing: worst-case 3mm fiber + 1.8mm wire = 4.8mm touching; 6.35mm ID gives ~1.5mm working clearance — enough for the two to slip independently in a bend without binding, not so loose they rattle and abrade the tube wall. Don't downsize to 3/16"ID (4.76mm, no clearance) or up to 5/16"ID (7.94mm, excess slack). ~1.6mm wall |
| Diffuser bead | ~10–15mm frosted/opal acrylic bead | Epoxied to the fiber's globe-end tip |
| Fiber tip prep | 400–600 grit sanding or matte spray on the fiber end face | Done before bonding the diffuser bead |
| Globe | 2.5" frosted acrylic ball | Purely passive/optical — no electrical connection inside |
| Sealant | 100% silicone sealant — GE Silicone II (or equivalent) | Required at the stem-tube-to-nipple joint and both pigtail wall exits — those surfaces (silicone tubing, silicone-insulated wire) need a true silicone-chemistry sealant; polyurethane/MS-polymer sealants like Sikaflex or Loctite Marine don't bond reliably to cured silicone rubber. Not epoxy |
| Sealant (general) | Clear flexible outdoor sealant (GE Silicone II, Sikaflex, or Loctite Marine — any of the three) | Globe seam and other acrylic/printed-plastic joints, where the silicone-specific bonding requirement above doesn't apply; not epoxy |
| Epoxy | Clear, outdoor-rated | Bonds diffuser bead to fiber tip |

## 3. Tools required

- FreeCAD (base enclosure, LED holder insert, anchor socket geometry)
- Anycubic Kobra (open-frame, no enclosure) for **PLA prototypes only** —
  fit-checking the holder insert, its nipple/fiber-hole/LED cavity, and the
  wire socket before committing to production
- Production enclosures printed in **ASA by a third-party print service** —
  ASA's better UV/thermal stability suits a part that lives in full sun
  outdoors for years, but the Kobra's open frame makes ASA's warping and
  fumes impractical to manage without a DIY enclosure, so final parts are
  outsourced rather than printed locally
- Fine sandpaper (400–600 grit) or matte-finish spray, for the globe-end fiber
  tip (frosted, diffusing)
- Fine sandpaper set (400/600/1000/1500/2000 grit) + metal- or plastic-polish
  compound (Brasso, Novus 2/1) or a small flame source, for the base-end fiber
  face (clear, flat, polished — opposite finish from the globe end)
- Wire cutters rated for stainless spring wire
- Soldering iron, fine tip; heat-shrink + heat gun for node lead splices
- Crimper matched to the chosen connector
- Multimeter (continuity/voltage check before burial)

## 4. Step-by-step fabrication

### Step 1 — Print the base enclosure and LED holder insert
Prototype both in PLA, fit-check the holder's nipple against the silicone tube,
its internal fiber hole, the LED cavity, the connector cavities, and the
spring-wire anchor socket on the bench. Once the PLA prototype fits, send the
files to the third-party service for an **ASA test article first — not the
full run.** ASA shrinks more than PLA (~0.3–0.8% vs ~0.2%), so fit validated
on PLA is not guaranteed to carry over exactly in ASA. Re-check fit on that
single ASA part before ordering the rest of the production enclosures.

### Step 2 — Seat the LED in its holder
Cut one WS2815 LED free from the strip and seat it face-up in the holder
insert's retention feature — confirm it sits flush with no rock or tilt, since
hole-to-LED alignment (not a cone taper) is what centers the LED under the
fiber now. Route the LED's leads out through the holder's side wall and glue
them in place there for strain relief and sealing, leaving the top nipple and
internal fiber hole clear.

### Step 3 — Splice the LED's leads to pigtails
Splice on silicone lead wire, tin and solder to the LED's pads, heat-shrink
each joint. Solder the LED's 12V and GND leads into a 3-way joint with the
in-pigtail's and out-pigtail's 12V (and separately GND) wires — this keeps the
trunk's power continuous fixture-to-fixture whenever the box is installed, per
§5. Solder the LED's DI lead to the in-pigtail's data wire only, and the DO
lead to the out-pigtail's data wire only — these two stay on separate joints,
never combined with each other. Leave the LED's BI and BO pads unconnected —
this project doesn't use WS2815's backup-data feature. Heat-shrink every
joint, then tin the free end of each pigtail wire — these stay bare leads
until they're gel-spliced to the trunk cable at install (§5), not terminated
in a connector at bench time.

### Step 4 — Assemble the base
Glue the holder insert's raised bottom edge into the base enclosure floor, now
that the LED is seated and its leads glued and spliced. Feed each pigtail
through its floor exit hole, leaving enough bare lead outside the enclosure
to reach the trunk-cable splice, then run a bead of 100% silicone sealant
(GE Silicone II) around each pigtail where it passes through the wall. Secure the spring wire's base end in its
anchor socket, alongside the holder's nipple — this joint must be rigid; any
flex here is lost from the stem's usable spring length.

### Step 5 — Cut and seat the fiber
Cut the fiber to stem length plus a short service loop. Polish the base end,
then feed it down through the holder's nipple and internal fiber hole until it
makes direct contact with the LED's flat face — zero air gap, not just "as
small as possible": any gap here is light that misses the fiber entirely, and
there's no cone or mirror lining to recapture it.

**Polishing the base (input) end face** — this end must stay clear and flat,
the opposite treatment from the frosted globe-end tip in Step 6:

1. Score and snap, or cut square with a sharp blade/fiber-optic cutting tool,
   as close to perpendicular to the fiber axis as you can get by eye.
2. Wet-sand the end face flat against fine sandpaper on a hard, flat surface
   (a scrap of glass or tile works), fiber held perpendicular to the paper.
   Step through grits: ~400 → 600 → 1000 → 1500 → 2000, a few figure-eight
   strokes per grit, wiping the face clean between grits so a coarser
   scratch doesn't carry forward.
3. Finish with a metal-polish compound (e.g. Brasso) on a soft cloth or
   felt pad, or a plastic-polish compound (e.g. Novus 2/1), until the face
   looks clear rather than frosted — held up to light, you should see
   through it, not a matte scatter.
4. Optional, PMMA-specific alternative to steps 2–3: pass the cut end
   briefly through a small flame (lighter/alcohol lamp) to flame-polish it —
   PMMA melts and self-levels to an optically clear face in about a second
   of exposure. Fast but easy to overdo: too long scorches/discolors the
   fiber or rounds the face, killing the flat coupling surface. Sand/polish
   by hand instead if you don't trust your control on the first attempt.
5. Inspect the finished face against a light source: it should be flat,
   perpendicular, and glassy-clear with no visible scratches, chips, or
   rounding at the edge before seating it against the LED.

### Step 6 — Prep the globe-end fiber tip
Sand or matte-spray the fiber's globe-end tip, then epoxy the diffuser bead on
once the tip prep has cured/dried per the epoxy's datasheet.

### Step 7 — Build the stem
Thread the fiber and spring wire through the silicone tubing from base to
globe end. Keep them unbonded to each other along the run — they should be
able to slip slightly relative to one another when the stem bends, rather
than being locked together and straining against each other. Slide the tube's
base end over the nipple (snug slip fit) and run a bead of 100% silicone
sealant (GE Silicone II) around the joint — this is the permanent bond between
the stem and the base enclosure, so let it fully cure per datasheet before any
handling that stresses the joint.

### Step 8 — Mount the globe
Seat the diffuser-bead/fiber assembly and the spring wire's top end in the
globe's cup/neck mount. Run a continuous bead of clear sealant around the
contact rim, tool it to a smooth fillet so water sheets off rather than
pooling at the seam. Orient the seam at or below the globe's equator, never
at the top.

### Step 9 — Cure and bench test
Let sealant cure per datasheet. Power the node and check, at the globe: color
uniformity (no fringing from the node's separate R/G/B dies — with the cone
gone, there's no diffusing dome or mixing distance between the LED and the
fiber's end face to blend them, so check this carefully, not just assume it's
handled), no visible hot-spot opposite the fiber tip, and adequate brightness
for an ambient glow. Hand-flex the stem repeatedly and confirm it springs back
to vertical rather than taking a permanent set.

### Step 10 — Install
Strip the buried trunk cable's incoming and outgoing ends and splice each to
the corresponding pigtail leads with gel-filled direct-bury connectors, per
the underground wiring convention in §5. Coil a service loop of extra trunk
cable near the fixture before backfilling, so a future re-splice doesn't
require pulling new wire. Bury the trunk cable (not the enclosure itself —
see `freecad.md`'s Base Housing section for the at-grade mounting decision).

## 5. Underground wiring convention at each base enclosure

The trunk cable is **3 conductors — 12V, GND, Data** (no backup/redundancy
line — the WS2815 node has a BI/BO pair for that, but this project leaves it
unconnected; see §1). Splicing happens in two stages:

1. **At bench-assembly time, inside the enclosure** — the node's leads are
   permanently soldered to two short pigtails before the enclosure is ever
   closed and sealed (see Step 3). Each pigtail exits the enclosure through
   its own small sealed grommet and ends in bare tinned lead wire — no
   connector is fitted at this stage.
2. **At install time, outside the enclosure** — each pigtail's bare leads
   are joined to the corresponding trunk-cable end (incoming, from the
   previous fixture or the hub box for the first fixture in a zone; or
   outgoing, to the next fixture) with a gel-filled direct-bury connector
   (ZONE INDUSTRY CORP silicone-filled, UL 486G — see §2 BOM). This is a
   **permanent splice, not a field disconnect** —
   deliberate choice, confirmed with the user 2026-08-27, favoring lower
   cost and simplicity over field-swappability, since a fixture failure is
   expected to be rare over the system's life. See the trade-off note
   below.

- **12V and GND**: the node's 12V lead, in-pigtail 12V, and out-pigtail 12V
  all land in one gel-filled connector (and separately for GND). This is a
  true common tie — the trunk stays electrically continuous
  fixture-to-fixture once the splice is made, whether or not the node
  itself is drawing power.
- **Data does not get a common tie** — this is the one place a 3-way splice
  would be wrong. The node fully decodes and regenerates the signal, so
  incoming and outgoing data are two *different* electrical nets, not one:
  - The in-pigtail's data wire splices only to the incoming trunk's data
    conductor.
  - The out-pigtail's data wire splices only to the outgoing trunk's data
    conductor, in a separate gel-filled connector.
  - Tying both data leads into a single connector would short the node's
    input and output together — don't do it, even though it looks
    symmetric with how 12V/GND are wired.
  - The node's BI/BO backup-data pins are left unconnected — this project
    doesn't wire WS2815's redundant-path feature, so electrically the node
    behaves like a plain WS2811 node: one live data-in, one live data-out,
    nothing else.
- That's **4 gel-filled connectors per fixture**: 12V, GND, data-in,
  data-out — not one shared connector for both trunk ends, and not one
  connector per trunk direction (data and power splice separately even
  within the same direction).
- **Service loop**: coil extra trunk cable near each fixture at install
  (Step 10) so a future fixture swap can cut the old splices, pull the
  failed enclosure's pigtails free, and re-splice a replacement without
  needing to pull new cable through the run.
- Swapping a fixture: dig down to the enclosure, cut all four splices open,
  remove the failed enclosure, splice in a replacement enclosure's pigtails
  using the service loop's slack, rebury. Downstream fixtures go dark
  **and** lose power for the duration (removing the enclosure breaks both
  the 12V/GND common tie and data regeneration through this hop) —
  expected, not a fault.
- Trade-off vs. a field-disconnect (Deutsch DT connector) design: this
  trades faster field service (unplug/replug) for lower per-fixture cost
  and no dedicated crimp tool — gel-filled connectors are twist-on, no
  special tooling required. The cost is that service means cutting and
  re-splicing rather than unplugging, which the service loop is sized to
  absorb.
- Optional: a small landscape valve box around the enclosure and its
  splices adds mechanical protection (abrasion, a spade strike) beyond the
  connectors' own direct-bury rating — not required for waterproofing,
  just cheap insurance, and it makes future digging-to-service easier to
  locate.
- The chosen splice connector (ZONE INDUSTRY CORP, §2 BOM) is a lower-cost,
  less field-proven pick than the landscape-lighting-industry-standard
  DryConn — accepted as the final spec pending real-world validation. If it
  fails in service (splice corrosion, moisture ingress, mechanical
  failure), swap to DryConn or equivalent; nothing else in this convention
  changes if that substitution happens.

Data connections only ever land on the node's own pads or inside a
gel-filled connector at a base enclosure — never as an inline underground
splice mid-cable elsewhere on the run, per `CLAUDE.md`.

## 6. Pre-burial QC checklist (per fixture)

- [ ] Sealant fully cured (per datasheet time), including the stem-to-nipple
      joint and both pigtail wall exits
- [ ] Node addresses and lights correctly on the bench
- [ ] No visible color fringing at the globe
- [ ] No visible hot-spot at the globe (diffuser bead doing its job)
- [ ] Fiber seated through the holder's nipple, in direct contact with the
      LED face — zero air gap
- [ ] Spring wire's base anchor is rigid — no play when the stem is flexed by
      hand
- [ ] Stem springs back to vertical after repeated hand-flexing, no permanent
      lean
- [ ] All 4 gel-filled splices (12V, GND, data-in, data-out) fully closed
      and twisted snug, not left hanging on strain alone
- [ ] Service loop of extra trunk cable coiled near the fixture before
      backfilling
