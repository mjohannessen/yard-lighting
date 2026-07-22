# Globe Cradle

A 3D-printable spherical cradle mount designed to hold a 59mm diameter globe,
with a bottom nipple to accept a 1/4" ID / 3/8" OD tube (glued fit).

## Part Specifications

| Feature              | Dimension          |
|----------------------|--------------------|
| Globe diameter       | 59mm               |
| Inner radius (cup)   | 29.5mm             |
| Outer radius (cup)   | 32mm               |
| Wall thickness       | 2.5mm              |
| Cradle depth         | ~7.4mm (1/8 globe) |
| Nipple outer radius  | 7.36mm             |
| Nipple bore radius   | 4.86mm             |
| Nipple length        | 20mm               |
| Bore depth           | 15mm               |
| Tube OD (slip fit)   | 9.525mm (3/8")     |
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
8. Cylinder primitive for bore (4.86mm radius, 15mm height)
9. Boolean Cut: assembly minus bore cylinder → finished part

## 3D Printing Notes

- Recommended material: PETG or PLA
- Layer height: 0.2mm
- Infill: 40%+ for strength around nipple
- Print orientation: cup opening facing up

## Assembly

1. Insert 3/8" OD tube into nipple bore
2. Apply adhesive (epoxy or PVC cement)
3. Allow to cure fully before loading globe