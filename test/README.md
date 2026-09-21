# test/

Working hardware that exists to be experimented on, rather than delivered.

| Folder | What it is |
| --- | --- |
| `hand-tracker/` | **Project A** — the Dream Cheeky Storm O.I.C. webcam hand tracker. A personal hobby toy that works, and the only thing here that has actually met hardware. |

## Why the hand tracker lives here

It is the testbed, not a deliverable. Two of the findings the SkyStrike proposal
now rests on were learned here first, on real hardware, by getting them wrong:

- **Parallax.** Tracking can be perfectly accurate and every shot still miss,
  because a device mounted beside the camera does not share its line of sight.
  That is why SkyStrike specifies calibration, sign conventions and an aim point
  up front instead of discovering them late.
- **Latency measured at the wrong endpoint.** Its aiming loop blocked on
  `time.sleep()` for 40–100 ms per frame and threw away roughly 87% of its
  achievable frame rate, while the vision itself ran in under 9 ms. That is why
  SkyStrike now measures capture-to-result-available separately from
  capture-to-displayed-result.

## It is still a separate project

Living under `test/` does not fold it into SkyStrike. This is a **firing device**
— it aims a foam-dart launcher at a human hand and fires on a held fist. SkyStrike
commits to having no connection to weapon aiming, triggering or firing controls.

**Written lessons travel out of this folder. Code does not.** See
`../AI_RULES.md` rules 1–4.

## Most of it is not in the repository

Only the documentation is committed. The source, `hidapi.dll`, the launcher
scripts and the 273 MB of vendored OpenCV/MediaPipe in `python_deps/` are
gitignored and exist only on this machine — a clone will not run the tracker.

The layout inside `hand-tracker/` is flat and load-bearing:
`storm_oic_hand_tracker.py` resolves `python_deps/` and `hidapi.dll` relative to
its own directory. Moving that folder as a whole is safe; rearranging its
contents is not.
