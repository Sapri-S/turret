# PLAN.md — Scope & Design

> What Project A is, what it is not, and how it fits together.

## 1. Goal
A webcam-driven turret that tracks a hand, aims a Dream Cheeky Storm O.I.C. USB
foam-dart launcher at it, and fires one dart when the user holds a fist steady inside
the aim box. Built for fun; the interesting engineering is the aiming, not the vision.

## 2. Status
**Working.** Tracking, aiming and firing are all confirmed on hardware. What's left is
calibration and polish, not architecture.

## 3. Non-goals (explicit)
- **Not coursework.** This is a personal toy, deliberately kept out of the SkyStrike
  senior design project. See `../AI_RULES.md` §1–4.
- **Not a platform.** One file, one device, one gesture. No plugin system, no config
  format, no packaging.
- **Not a multi-target tracker.** `max_num_hands=1` on purpose — one hand, one shot.
- **Not portable.** Windows-only by design: HIDAPI DLL, Win32 mutex, MSMF/DSHOW.

## 4. Architecture
```
Altair USB camera
      │  320x240 MJPG @30fps, newest-frame-only (never queues)
      ▼
LatestFrameCamera (capture thread)
      │  frame
      ▼
MediaPipe Hands ── landmark 9 (palm centre), EMA alpha=0.85
      │  smoothed (x, y) + per-finger curl count
      ├──────────────────────────────┐
      ▼                              ▼
Aim: is the point inside the      Fist: >=3 of 4 fingers curled
aim box (frame centre +           (fingertip closer to wrist
the aim offset)?                   than its own PIP joint)
      │                              │
      └──────────┬───────────────────┘
                 ▼
        both true, held 1.5 s  ──► FIRE (0x10, force=True)
                 │                      │
                 │                      ▼
        else: pulse motors       4.0 s of TOTAL SILENCE
        toward centre,           (movement block skipped
        always ending in STOP     entirely — see findings §1)
                 ▼                      │
          Launcher (HIDAPI)  ◄──────────┘
          hidapi.dll -> hid_write
                 ▼
        Storm O.I.C. (VID 0x2123 / PID 0x1010)
```

Details: `.context/tracker_architecture.md`. Wire format: `.context/hid_protocol.md`.

## 5. Key design decisions
- **Newest-frame-only capture.** A queued frame aims at where the hand *was*. Latency
  matters more than completeness.
- **Landmark 9, not a fingertip.** The palm centre is far steadier under a closing fist.
- **Rotation-invariant curl test.** Comparing fingertip-to-wrist against PIP-to-wrist
  avoids assuming an upright hand, which a "fingertip is below its knuckle" test does.
- **Aim offset instead of a camera remount.** Software zeroing is adjustable live and
  costs nothing; a mechanical fix is one-shot and needs tools. See findings §5.
- **1.5 s fist hold.** A deliberate-intent gate — it makes an accidental fist harmless.
- **HIDAPI over PyUSB.** No driver rebinding, so the device stays a normal HID device.

## 6. Stack
- Python 3.11.9 (Windows Store build).
- **Vendored** OpenCV + MediaPipe in `python_deps/vision/`, injected into `sys.path`
  at import time. Global site-packages is empty — this is the only reason it runs.
- `hidapi.dll` loaded by ctypes from the script's own directory.
- Win32 `HidD_SetOutputReport` path exists as `WindowsReportLauncher` but is unused.

## 7. Success criteria
- Darts land on the aim point at a **recorded, stated distance** (not yet met).
- Fist detection reliable under the turret camera's actual lighting (not yet met — the
  camera is overexposed, findings §7).
- The program survives a USB re-plug without a code edit (not yet met — camera is
  selected by index, not by device name).
