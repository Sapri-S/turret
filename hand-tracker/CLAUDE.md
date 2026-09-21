# CLAUDE.md — Agent Context (read first, every session)

> Claude Code loads this file automatically from the project root at the start of
> every session. Read it before doing anything else.

## What this project is
**Project A — Dream Cheeky Storm O.I.C. hand tracker.** A personal, hobby webcam
hand-tracking turret. It tracks a hand with MediaPipe, aims a USB foam-dart launcher
by pulsing its pan/tilt motors, and fires one dart when a fist is held inside the aim
box for 1.5 s. Python, Windows, ~780 lines in one file.

**It works.** Tracking, aiming and firing are all confirmed on hardware. The main
outstanding task is **calibrating the aim offset** so the darts actually land where
the tracker is pointing.

This is a **toy, not coursework.** It is deliberately separate from the SkyStrike
senior design project in `../skystrike/`. See `../AI_RULES.md` rules 1–4 before you
consider sharing anything between them.

## Read these before doing anything (source of truth)
- **`../AI_RULES.md`** — hard guardrails. Safety + project separation. Non-negotiable.
- **`docs/hard-won-findings.md`** — seven findings that cost real debugging to learn.
  **Read this before changing timing, transport, or the aim logic.** Ignoring §1 will
  silently break every shot with no error message.
- **PLAN.md** — how the program is put together and why.
- **PROGRESS.md** — what's done, what's next. Update as you go.
- **`.context/hid_protocol.md`** — the verified wire protocol.
- **`.context/tracker_architecture.md`** — stage-by-stage walkthrough + tuning constants.

## How to work here
1. At session start: read `../AI_RULES.md` → `docs/hard-won-findings.md` → PROGRESS.md.
2. Work the **next unchecked item** in PROGRESS.md.
3. Make focused edits. This is one working file — don't rewrite it wholesale.
4. After each chunk: update PROGRESS.md, then summarize what changed in 1–2 lines.
5. Any change to **fire timing, the fire trigger condition, or where the turret is
   allowed to point** → **ask the user.** Those are safety decisions, not code tweaks.

## Layout — do not reorganize
`storm_oic_hand_tracker.py` resolves its vendored dependencies and `hidapi.dll`
relative to its own directory (`HERE = Path(__file__).resolve().parent`). The flat
layout is load-bearing; moving scripts into `src/` breaks the import path and the DLL
load. See `../AI_RULES.md` §8.

| File | What it is |
| --- | --- |
| `storm_oic_hand_tracker.py` | **The main program.** Tracking + aiming + fist-to-fire. |
| `list_cameras.py` | Probes every camera index on both backends, saves a snapshot from each so you can identify which index is which. |
| `run_hand_tracker.bat` | Launcher. `cd`s to its own folder, runs the tracker with `--camera 0`. |
| `hidapi.dll` | Local HIDAPI library, loaded by ctypes. **Required.** |
| `python_deps/vision/` | Vendored OpenCV + MediaPipe, injected into `sys.path`. |
| `python_deps/pyusb-src/` | Vendored PyUSB, used only by the older probe scripts. |
| `storm_oic_probe.py` | Read-only USB enumeration probe. Sends nothing. |
| `storm_oic_windows_hid_test.py` | Movement sweep + one shot via raw `HidD_SetOutputReport`. **Known working** — use as the reference for correct fire timing. |
| `storm_oic_full_test.py` | Same, via PyUSB/libusb `ctrl_transfer`. Needs a libusb backend. |
| `storm_oic_movement_test.py` | Short movement-only test. |
| `usb_missile_control/`, `rocket_launcher/` | Two community reference drivers (git clones). Source of the protocol. |
| `README_LOCAL_TEST.md` | Original packaging notes that shipped with the folder. |

## Run it
```
cd "C:\Users\sapri\Downloads\turret\hand-tracker"
python .\storm_oic_hand_tracker.py
```
`--camera 0` is the default. Keys: `Q`/`Esc` quit, `W/A/S/D` nudge aim, `R` reset aim.
`--aim-offset-x` / `--aim-offset-y` set a starting offset.

A single-instance mutex `Local\StormOICHandTracker` stops two copies fighting over
the camera.

## Do NOT
- Send anything to the device for 4.0 s after FIRE. Not even STOP. Especially not STOP.
- Port any of this into `../skystrike/`. It is a firing device; that project is not.
- Point it at a person as part of coursework — flag the conflict instead.
- Add a `pip install` step. The dependencies are vendored; global site-packages is empty.
- Rebind the USB driver to WinUSB/libusb without a specific reason. It breaks HIDAPI.
