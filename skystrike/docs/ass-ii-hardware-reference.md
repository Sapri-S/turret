# A.S.S. II — hardware reference

Reference notes on the **A.S.S. II ("Automated Sentry System II")** Patreon release
from the YouTube channel *The Woodshed TV*, recorded 2026-09-21.

> **Why this file exists and what it is not.** The SkyStrike proposal names A.S.S. II
> as *"background reference material, not a software dependency or implementation
> starting point,"* and states that reusing its frame as a non-firing structure
> *"remains an unselected option."* This file records what the release actually
> contains so that decision can be made from facts rather than memory.
>
> **A.S.S. II is a person-tracking airsoft sentry turret.** Its bill of materials
> ends with an airsoft rifle, its firmware drives a trigger servo, and its software
> detects people. None of that belongs in SkyStrike — see `../../AI_RULES.md`
> rules 1–4. The mechanical frame is neutral; everything downstream of it is not.

**The release files are not in this repository.** They are ~54 MB of paid
third-party content, including a 31 MB CAD archive and a 23 MB model file. Committing
them would redistribute someone's Patreon release and bloat a docs-only repo. They
live locally at:

```
C:\Users\sapri\Downloads\A.S.S. II Patreon Release-20260921T202453Z-1-001\
```

## What is in the release

| Path | Size | Notes |
| --- | --- | --- |
| `Hardware/Fusion360Files/ASS II Fusion Files.f3z` | 31.8 MB | **8 parametric `.f3d` components** + manifest. Genuinely editable in Fusion 360, not exported meshes. |
| `Hardware/3DPrintFiles/*.stl` | 10 files, ~1.2 MB | Print-ready meshes. Dimensions below. |
| `Hardware/FrameDrawing.pdf` | 120 KB | Frame drawing. |
| `Hardware/BillOfMaterials/` | PDF + XLSX | 21 line items. Transcribed below. |
| `Software/ASS_II/ASS_II_Python.py` | 8 KB | MobileNet-SSD **person** detection, drives serial. |
| `Software/ASS_II/ASS_II_ArduinoFile/*.ino` | 1.3 KB | Three-servo firmware: pitch, yaw, **trigger**. |
| `Software/ASS_II/mobilenet_iter_73000.caffemodel` | 23.3 MB | Caffe MobileNet-SSD weights. |
| `Software/ASS_II/deploy.prototxt` | 45 KB | Model definition. |
| `README.txt` | 4.5 KB | Author's setup guide. States the project is educational and incomplete. |

## Printed part dimensions (measured from the STL binaries)

| Part | X × Y × Z (mm) | Triangles |
| --- | --- | --- |
| LeftPitchBracket | 65.9 × 117.6 × **224.1** | 5,630 |
| RightPitchBracket | 26.6 × 117.6 × **224.1** | 1,624 |
| UpperYawMotorPlate | **154.4** × 7.6 × **152.4** | 1,052 |
| PowerSupplyEnclosure | 104.1 × 38.2 × 139.6 | 5,962 |
| RightPitchArm_Upper_WServo | 38.9 × 120.2 × 98.5 | 2,034 |
| RightPitchArm_Upper_WOServo | 38.9 × 120.2 × 98.5 | 3,432 |
| LowerYawMotorPlate | 52.1 × 18.4 × 113.5 | 1,192 |
| PitchBracketAttachBracket (print ×4) | 18.9 × 89.1 × 26.0 | 560 |
| LaserClipMain | 30.9 × 12.2 × 34.0 | 1,540 |
| LaserClipSide | 5.8 × 12.2 × 34.0 | 364 |

⚠️ **The pitch brackets are 224.1 mm in their longest axis.** That does not fit a
220 mm bed (Ender 3, Bambu A1) in every orientation. Check before committing to a
print. Everything else fits comfortably.

## Bill of materials (21 items, as listed)

| Qty | Item |
| --- | --- |
| 1 | Terminal Block and Strip |
| 1 | Arduino Nano |
| 1 | RC Servo 25KG |
| 2 | Polymaker PLA Pro Black |
| 3 | T-Slot 2020 Aluminium Extrusion, 4 pcs, 600 mm |
| 1 | Silicone Wire, Stranded Tinned Copper |
| 1 | 608-RS Ball Bearing, 10 pack |
| 1 | 8 mm threaded rod and nuts |
| 1 | 35KG High Torque RC Servo (2 pack) |
| 1 | Pan Tilt Servo Mount |
| 1 | Lazy Susan Turntable |
| — | Metric Screw Assortment |
| 1 | Aluminium Profile Connector Set |
| 1 | Screw Terminal Adapter |
| 1 | Ultra Thin Power Supply, 5 V 40 A 200 W |
| 1 | Power Cord |
| 1 | Razer Kiyo X Full HD Streaming Webcam |
| 1 | 2-Pack 10 ft + 10 ft USB 3.0 Extension Cable |
| 1 | Camera Wall Mount, 3 pack |
| 1 | **HK416 AEG 6 mm BB Rifle Airsoft Gun** |

The original listing carries Amazon affiliate links; they are omitted here.

## What is reusable, and what is not

**Mechanically neutral — reuse is an open option:**
2020 extrusion frame, lazy susan turntable, 608 bearings, 8 mm rod, the yaw and pitch
plates and brackets, the power supply enclosure, and the camera wall mounts.

**Not reusable for SkyStrike, on scope grounds:**

- The **trigger servo** and everything that drives it.
- The **airsoft rifle** and its mount.
- `ASS_II_Python.py` — it detects **people** and steers a weapon at them.
- `ASS_II_Arduino.ino` — see below.

## Two things worth knowing before anyone reuses this

**1. The firmware fires on a side effect, not on a decision.** From
`ASS_II_Arduino.ino`:

```cpp
// Check if yaw is not 80
if (yaw != 80) {
  servoTrigger.write(90);
} else {
  servoTrigger.write(0);
}
```

The trigger is pulled whenever yaw is anything other than its centre value. There is
no confirmation, no target check, no arming state, and no interlock — the weapon
fires because the turret is not centred. The author's own README calls the project
*"by no means complete"* and made by *"a certified idiot."* Take that at face value.
This is a clear example of what a firing decision must **not** look like.

**2. It is over-built for a camera-only payload.** The frame swings an airsoft rifle
using 25 kg and 35 kg servos off a 200 W supply. A Pi 5 with a light camera is a
fraction of that mass. If the frame is reused as a static mount, the servos and much
of the power budget are unnecessary; if it is reused at all, that is a sizing decision
to make deliberately rather than inherit.

## Relevance to SkyStrike

The current proposal makes the cameras **fixed**, which removes the reason for a
pan/tilt turret and leaves only the frame and mounts as candidates for reuse. That
sits in tension with the stated intent to build on this hardware — recorded as an
open question in `../PROGRESS.md`. Nothing here resolves it; this file exists so the
decision is made against the actual contents.
