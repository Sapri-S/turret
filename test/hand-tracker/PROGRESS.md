# PROGRESS.md — Checklist

> Work the **next unchecked item**. Update this file as you go.
> `[ ]` todo · `[~]` in progress · `[x]` done · ⚠️ needs a user decision.

## Done
- [x] USB enumeration probe; device identified as VID `0x2123` / PID `0x1010`.
- [x] HID protocol reverse-engineered from the two community reference drivers.
- [x] Movement confirmed on hardware via raw `HidD_SetOutputReport`
      (`storm_oic_windows_hid_test.py`).
- [x] Firing confirmed on hardware. **The 4.0 s post-FIRE silence was the whole
      problem** — two debugging rounds lost to it, and a 0.3 s cooldown was not
      enough. See `docs/hard-won-findings.md` §1.
- [x] Threaded newest-frame-only capture (`LatestFrameCamera`), 320×240 MJPG @30.
- [x] MediaPipe hand tracking on landmark 9, EMA smoothed.
- [x] Rotation-invariant fist detection (`count_curled_fingers`, ≥3 of 4).
- [x] Fist-to-fire state machine with a 1.5 s hold and auto-rearm (~1 shot / 5.5 s).
- [x] Aim-offset mechanism added to compensate camera/barrel parallax — live `W/A/S/D`,
      `R` to reset, `--aim-offset-x` / `--aim-offset-y` to seed.
- [x] Camera indices identified: **0 = Altair (turret)**, 1 = laptop built-in.
- [x] Single-instance mutex so two copies can't fight over the camera.
- [x] Vendored OpenCV + MediaPipe so the program runs with an empty global env.
- [x] Folder relocated to `turret/hand-tracker/` with agent context (2026-09-21).
      Originals left in place at the old Codex path; `camera_probe/` snapshots were
      deliberately **not** carried over.

## Next

### 0. MEASURE THE CAMERA-TO-BARREL BASELINE ⚠️ blocks everything below
- [ ] **Altair (camera 0), lens centre to barrel axis, with a ruler:**
      horizontal ___ cm, vertical ___ cm. This is bolted to the turret, so the
      number never changes -- measure once, correct forever.
- [ ] Logitech (camera 2), same two numbers. Changes whenever the laptop screen
      is tilted, so it is worth far less. Measure only if you keep testing on it.
- [ ] Put the real values into `range_compensation.py`, replacing the estimates.

      **The values in that file right now are NOT measurements.** They were
      derived on 2026-09-22 from a single photo scaled against the ROG Strix
      G18's 39x24 cm display. The turret sat nearer the phone than the screen
      did, so it was magnified by an unknown amount -- honest error is +/-30%.
      The Altair numbers are worse still: it was not even visible in the photo,
      so 5cm/3cm is a guess about typical mounting, not an observation.

      Photo estimates, for reference until replaced:
      | Camera | Horizontal | Vertical | Basis |
      | --- | --- | --- | --- |
      | Logitech | ~18 cm (15-22) | ~30 cm (24-35) | photo, +/-30% |
      | Altair | 5 cm | 3 cm | **guess, not observed** |

- [ ] While measuring, note the working distance you actually fire from.

> **Why this matters more than it looks.** With the Logitech's ~18/30 cm
> baseline, the correction needed at 60 cm is 0.21 of frame width and 0.47 of
> frame height. The aim box is only 0.20 wide, and 0.47 is essentially the frame
> edge -- there is no valid correction to apply. That placement only works from
> about 2 m back. The Altair's small baseline needs roughly 0.06 and 0.05 at the
> same distance, which is comfortable. This is the quantitative reason the
> Altair is the aiming camera and the Logitech is the detection camera.

### 1. Calibrate the aim offset ⚠️ main task
- [ ] Pick a working distance and **write it down** — the offset is only valid there.
- [ ] Set up a safe target (paper on cardboard). Launcher pointed somewhere safe, no
      one downrange.
- [ ] Fire test shots; nudge with `A`/`D` for horizontal, `W`/`S` for vertical until
      they land true.
- [ ] Record the final `(x, y)` **and the distance** here.
- [ ] Set them as the defaults for `--aim-offset-x` / `--aim-offset-y` in the script.
- [ ] Optional: repeat at a second distance and note how much the offset moves — that
      tells you how sensitive the zero is to range.

**Range compensation is now implemented** (`range_compensation.py`), so the zero no
longer has to be redone per distance:
- [ ] Zero the aim at any convenient distance with `W/A/S/D`.
- [ ] Press **K** to capture that hand distance as the reference.
- [ ] The offset then scales itself as you move in and out. `C` clears it, `R`
      resets both offset and reference.
- [ ] Verify by firing at two distances without re-zeroing.

It works by exploiting the fact that required offset and apparent knuckle width
both scale as 1/Z, so their ratio cancels Z, the focal length and hand size
alike -- no camera calibration and no ruler needed *for this part*. The knuckle
span used is landmark 5 to landmark 17, which does not change when the hand
closes into a fist.

### 2. Fix the overexposed turret camera
- [ ] The Altair camera is washed out and green-tinted (`docs/hard-won-findings.md` §7).
- [ ] Try `CAP_PROP_EXPOSURE` / `CAP_PROP_GAIN` / `CAP_PROP_AUTO_EXPOSURE` at capture
      — note that not every property is honoured on every backend.
- [ ] If the driver ignores them, fall back to changing the lighting.
- [ ] **Re-check fist-detection reliability afterwards** — suspect the exposure before
      the detection threshold.

### 3. Select the camera by device name (optional)
- [ ] Index-based selection breaks whenever USB ports change. Resolve "Altair" by name
      so re-plugging stops breaking it. `list_cameras.py` already knows how to identify
      devices — reuse that.

### 4. Decide what to do with `WindowsReportLauncher` (optional)
- [ ] It is fully written, kept in sync, and **instantiated nowhere**. Either delete it
      or wire it up as a `--transport` fallback. ⚠️ ask the user which.

## Log
- **2026-09-21** — Copied out of the Codex output folder into `turret/hand-tracker/`.
  Added `CLAUDE.md`/`AGENTS.md`, `PLAN.md`, this file, `docs/hard-won-findings.md`, and
  `.context/`. **No code was changed** and the flat layout was preserved, because the
  script resolves `python_deps/` and `hidapi.dll` relative to its own directory.
  **Verified from the new location:** OpenCV 4.10.0 and MediaPipe 0.10.14 import,
  `mp.solutions.hands.Hands(...)` constructs, and `hidapi.dll` loads. Not yet run
  against the actual turret hardware from here.
- **2026-09-21** — Documented finding #8 (the matplotlib/sounddevice import stubs),
  which was in the code but not in the handoff notes.
