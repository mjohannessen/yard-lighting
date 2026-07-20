# Fixture Construction Guide — Fiber-Optic Flower-Stem LED

Build guide for the fixture head: a fixed base enclosure, buried at or just
below grade, holding the LED and coupling optics, feeding a flexible
fiber-optic + spring-wire stem that carries a passive globe. The stem bends
and springs back in the breeze; the globe end carries no electrical
connection at all, only light (fiber) and mechanical support (spring wire).

Fill in `[TBD]` dimensions once bench testing (reflector capture, wire stiffness,
fiber coupling) settles on final numbers — this guide is the assembly procedure
and part boundary, not a dimensioned drawing.

## 1. Design summary

Bottom to top:

1. Underground trunk cable (12V/GND/Data — 3 conductors, no backup line) enters
   a **base enclosure** at or just below grade — no rigid pipe riser, since
   nothing above the base is electrical.
2. **Base enclosure** (printed, ASA production) houses:
   - A **WS2811 12mm diffused pixel node** (DC12V, IP68), cut singly from a
     50pc string.
   - Bare reusable lever nuts (12V/GND/Data — no backup-line pin, since
     WS2811 has none), mounted inside the enclosure itself, splicing the
     node's pigtail leads into the incoming and outgoing trunk runs. Both
     trunk cables enter this same enclosure through their own cable gland —
     no separate external splice box. The enclosure's own sealant seal
     (§1 item 5-style, applied to the enclosure's joints) is what
     waterproofs the splice; the levers themselves don't need to be
     independently waterproof. Opened only on fixture failure, not
     routinely — see §5.
   - A **reflector cone**: mirror-film-lined, ~13mm entrance ID (around the
     node's 12mm dome) narrowing to ~3.2mm exit ID (around the fiber core)
     over a 15–20mm length. Concentrates the diffused node's output into the
     fiber's acceptance cone.
   - A rigid anchor socket that holds the spring wire's fixed (base) end —
     this is the fixed point of the cantilever; any play here undermines the
     whole spring effect.
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
| Base enclosure | Printed part (FreeCAD → PLA prototype → ASA production) | Houses LED node, reflector cone, fiber entry, spring-wire anchor |
| LED node | WS2811, 12mm diffused round pixel, DC12V, IP68 | Cut singly from a 50pc string; re-terminate leads |
| Node lead wire | Silicone-insulated, fine-strand, 26–30AWG | Short static run from node to connector — doesn't flex, so stock leads could work, but silicone is cheap insurance |
| Lever nuts (reusable, e.g. Wago 221 or equivalent) | 4 per fixture: 1 for 12V, 1 for GND, 2 for Data (in-side and out-side kept electrically separate — see §5) | Mounted inside the base enclosure; waterproofing comes from the enclosure's own sealed joints, not from the levers themselves |
| Cable gland, IP68 | 2 per fixture (trunk in, trunk out) | Strain relief + seal where each trunk cable enters the enclosure |
| Reflector/collector cone | Printed insert, entrance ID ~13mm, exit ID ~3.2mm, length 15–20mm | Concentrates diffused node output into the fiber |
| Mirror film | Adhesive-backed Mylar-type reflective film | Interior lining for the reflector cone |
| Fiber optic cable | PMMA (acrylic) end-glow fiber, ~3mm core | Length = stem height + service loop; PMMA for flex-fatigue tolerance |
| Spring wire | 304 stainless steel, straight, full-hard temper, 1.4/1.6/1.8mm (bench-test set) | Cut to stem length; anchored rigidly at the base, free at the globe mount |
| Silicone tubing | Black silicone, 1/4"ID x 3/8"OD | Single lumen. ID sizing: worst-case 3mm fiber + 1.8mm wire = 4.8mm touching; 6.35mm ID gives ~1.5mm working clearance — enough for the two to slip independently in a bend without binding, not so loose they rattle and abrade the tube wall. Don't downsize to 3/16"ID (4.76mm, no clearance) or up to 5/16"ID (7.94mm, excess slack). ~1.6mm wall |
| Diffuser bead | ~10–15mm frosted/opal acrylic bead | Epoxied to the fiber's globe-end tip |
| Fiber tip prep | 400–600 grit sanding or matte spray on the fiber end face | Done before bonding the diffuser bead |
| Globe | 2.5" frosted acrylic ball | Purely passive/optical — no electrical connection inside |
| Sealant | Clear flexible outdoor sealant (GE Silicone II, Sikaflex, Loctite Marine) | Globe seam and base enclosure joints; not epoxy |
| Epoxy | Clear, outdoor-rated | Bonds diffuser bead to fiber tip |

## 3. Tools required

- FreeCAD (base enclosure, reflector cone, anchor socket geometry)
- Anycubic Kobra (open-frame, no enclosure) for **PLA prototypes only** —
  fit-checking the node cavity, cone, fiber, and wire socket before
  committing to production
- Production enclosures printed in **ASA by a third-party print service** —
  ASA's better UV/thermal stability suits a part that lives in full sun
  outdoors for years, but the Kobra's open frame makes ASA's warping and
  fumes impractical to manage without a DIY enclosure, so final parts are
  outsourced rather than printed locally
- Fine sandpaper (400–600 grit) or matte-finish spray, for fiber tip prep
- Wire cutters rated for stainless spring wire
- Soldering iron, fine tip; heat-shrink + heat gun for node lead splices
- Crimper matched to the chosen connector
- Multimeter (continuity/voltage check before burial)

## 4. Step-by-step fabrication

### Step 1 — Print the base enclosure
Prototype in PLA, fit-check the node cavity, cone geometry, connector cavity,
and spring-wire anchor socket on the bench. Once the PLA prototype fits, send
the file to the third-party service for an **ASA test article first — not the
full run.** ASA shrinks more than PLA (~0.3–0.8% vs ~0.2%), so fit validated
on PLA is not guaranteed to carry over exactly in ASA. Re-check fit on that
single ASA part before ordering the rest of the production enclosures.

### Step 2 — Prep and line the reflector cone
Print the cone (or as an integral feature of the enclosure), then apply mirror
film to the interior. Test-fit the node at the large end and confirm the small
end matches the fiber's OD before final assembly.

### Step 3 — Prep the LED node
Cut one node free from the 50pc string. Splice on silicone lead wire, tin and
solder to the node's pads, heat-shrink each joint. Wire the free end to the
head-side half of the waterproof connector.

### Step 4 — Assemble the base
Seat the node at the cone's large end. Seat the connector half in its cavity.
Secure the spring wire's base end in its anchor socket — this joint must be
rigid; any flex here is lost from the stem's usable spring length.

### Step 5 — Cut and seat the fiber
Cut the fiber to stem length plus a short service loop. Clean/polish the base
end and seat it at the cone's small end with as small an air gap as possible —
any gap here is light that misses the fiber entirely.

### Step 6 — Prep the globe-end fiber tip
Sand or matte-spray the fiber's globe-end tip, then epoxy the diffuser bead on
once the tip prep has cured/dried per the epoxy's datasheet.

### Step 7 — Build the stem
Thread the fiber and spring wire through the silicone tubing from base to
globe end. Keep them unbonded to each other along the run — they should be
able to slip slightly relative to one another when the stem bends, rather
than being locked together and straining against each other.

### Step 8 — Mount the globe
Seat the diffuser-bead/fiber assembly and the spring wire's top end in the
globe's cup/neck mount. Run a continuous bead of clear sealant around the
contact rim, tool it to a smooth fillet so water sheets off rather than
pooling at the seam. Orient the seam at or below the globe's equator, never
at the top.

### Step 9 — Cure and bench test
Let sealant cure per datasheet. Power the node and check, at the globe: color
uniformity (no fringing from the node's separate R/G/B dies — the diffused
dome should already handle this), no visible hot-spot opposite the fiber tip,
and adequate brightness for an ambient glow. Hand-flex the stem repeatedly and
confirm it springs back to vertical rather than taking a permanent set.

### Step 10 — Install
Feed the incoming and outgoing trunk cables through their cable glands into
the base enclosure, land them on the lever nuts per the underground wiring
convention in §5, seal the enclosure's joints with sealant, then bury it
at/just below grade.

## 5. Underground wiring convention at each base enclosure

The trunk cable is **3 conductors — 12V, GND, Data** (no backup/redundancy
line; WS2811 doesn't have one, unlike WS2815). All splicing happens **inside
the base enclosure** — both the incoming trunk (from the previous fixture,
or the hub box for the first fixture in a zone) and the outgoing trunk (to
the next fixture) enter the same enclosure, each through its own IP68 cable
gland. There is no separate external junction box and no mate/unmate
connector; the enclosure's own sealed construction is the only waterproof
boundary. This is a deliberate choice given fixtures are only opened on
failure, not routinely — see the trade-off note below.

- **12V and GND**: each gets one lever nut, with three leads landed in it —
  the incoming trunk wire, the outgoing trunk wire, and the node's own lead.
  This is a true common tie; the trunk stays electrically continuous through
  the enclosure whether or not the node is drawing power.
- **Data does not get a common tie** — this is the one place a 3-way lever
  would be wrong. The node fully decodes and regenerates the signal, so
  incoming and outgoing data are two *different* electrical nets, not one:
  - One lever joins the incoming trunk's data wire to the node's DIN lead.
  - A second, separate lever joins the node's DOUT lead to the outgoing
    trunk's data wire.
  - Tying all four of those leads into a single common lever would short
    the node's input and output together — don't do it, even though it
    looks symmetric with how 12V/GND are wired.
- That's **4 lever positions per fixture** (12V, GND, data-in, data-out),
  not 3 — confirm whichever lever-nut product you buy gives you at least
  that many independent positions per enclosure; don't assume a "3-way"
  labeled product has a 4th spare, check the datasheet/packaging.
- Swapping a fixture: dig it up, release the node's four leads from their
  levers (trunk wires stay put — they're not being removed, just the failed
  node's leads), insert the replacement node's leads, reseal the enclosure.
  Downstream fixtures go dark for the duration (they lose data regeneration
  through this hop) — expected, not a fault.
- Trade-off vs. a mate/unmate connector: this is meaningfully slower to
  service (open enclosure, work four levers, reseal) and the enclosure's
  weatherproof seal is fully broken and remade on every failure event
  rather than mating through a connector's dedicated, reuse-rated gasket.
  That's the right trade here specifically *because* fixtures are only
  serviced on failure, not routinely — if that assumption changes (e.g. you
  start swapping fixtures seasonally), reconsider the mate/unmate connector
  approach instead.
- Optional: a small landscape valve box around the enclosure adds mechanical
  protection (abrasion, a spade strike) beyond the enclosure's own seal —
  not required for waterproofing, just cheap insurance, and it makes future
  digging-to-service easier to locate.

Data connections only ever land on the node's own pads or a lever nut —
never as an inline underground splice mid-cable, per `CLAUDE.md`.

## 6. Pre-burial QC checklist (per fixture)

- [ ] Sealant fully cured (per datasheet time)
- [ ] Node addresses and lights correctly on the bench
- [ ] No visible color fringing at the globe
- [ ] No visible hot-spot at the globe (diffuser bead doing its job)
- [ ] Fiber seated at the reflector cone with minimal air gap
- [ ] Spring wire's base anchor is rigid — no play when the stem is flexed by
      hand
- [ ] Stem springs back to vertical after repeated hand-flexing, no permanent
      lean
- [ ] Connector fully mated and seated, not left hanging on strain alone
