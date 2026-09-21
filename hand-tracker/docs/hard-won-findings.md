# Hard-won findings — do not rediscover these the hard way

> Seven things that cost real debugging to learn. Each one is a trap that produces
> **no error message** when you fall into it. Read before changing timing, transport,
> aim logic, or camera handling.

## 1. After FIRE, send absolutely nothing for 4.0 seconds ⚠️ the big one

The launcher's fire mechanism takes several seconds to complete. If **any** other
report — especially `STOP` — reaches the device before it finishes, the shot is
**silently cancelled**: no dart, no error, no USB failure. Everything looks fine.

This cost two full failed debugging rounds. The per-frame tracking loop was sending
`move(0)` → `STOP` a few milliseconds after `FIRE`, which killed every single shot.

A first fix used a **0.3 s** cooldown. **Still failed.** The working value is **4.0 s**,
which matches both known-good standalone test scripts: each sends `FIRE` once, waits a
full 4.0 s doing *nothing*, then sends `STOP`.

In the code: `FIRE_CYCLE_SECONDS = 4.0`, and the movement block is wrapped in
`if time.monotonic() >= fire_cooldown_until:` so the loop goes **fully silent** — not
"sends less", *silent*.

**If shots stop working, check this first.**

## 2. Movement commands need a keep-alive
Re-send an active motion roughly every **150 ms** or the motor stops on its own. The
`send()` method dedupes identical payloads within a **0.12 s** window so that
per-camera-frame calls don't flood the device. The two numbers are a pair: dedupe
window comfortably under the keep-alive interval.

## 3. FIRE must bypass the dedupe
`fire()` calls `send(..., force=True)`. A one-off critical command must never be
suppressed by the dedupe window — if the previous payload happened to be identical,
a deduped FIRE is a silently dropped shot.

## 4. Two working transports exist; one is in use
- **HIDAPI** (`hidapi.dll` via ctypes → `hid_write`), in the `Launcher` class. **This
  is the one in use**, confirmed working for both movement and firing.
- **`WindowsReportLauncher`**, using raw Win32 `HidD_SetOutputReport`. Fully written,
  kept in sync, **not instantiated anywhere.** Dead code.
- **PyUSB/libusb** also works, but needs a libusb/WinUSB driver bound — which
  **conflicts with the native HID driver HIDAPI needs.** Don't switch drivers without
  a reason.

## 5. Camera/barrel parallax makes it miss every shot
Tracking can be **perfectly accurate** and every dart still misses, because the camera
is mounted to one side of the barrel and therefore does not share its line of sight.

Fixed by adding a tunable **aim offset** that shifts the aim box away from frame
centre — exactly like zeroing a rifle scope. Live-adjustable with `W/A/S/D` while
running, `R` resets, and `--aim-offset-x` / `--aim-offset-y` set a starting value.

**Not yet fully calibrated. This is the main outstanding task.** Note that an offset
is only valid **at the distance it was calibrated for**.

> This finding is cited as direct evidence in SkyStrike's plan, Part 3 §A — the same
> trap awaits any device mounted beside a camera.

## 6. Camera indices swap when USB ports change
- Index **0** = Altair USB2.0 Camera — **the turret camera, the one you want.**
- Index **1** = USB2.0 HD UVC WebCam — the laptop's built-in.

Re-identify with `list_cameras.py` after any re-plugging. The mapping is currently
consistent across the MSMF and DSHOW backends, but index numbering is **not**
guaranteed to match between backends in general. `open_camera()` tries
MSMF → DSHOW → CAP_ANY and takes the first that delivers a frame.

## 7. The turret camera is badly overexposed
Washed out and green-tinted. **If fist detection is unreliable, suspect this before
the detection threshold.** Not yet fixed — would need exposure/gain settings applied
at capture, or better lighting.

## 8. MediaPipe will not import without the matplotlib/sounddevice stubs
`import mediapipe` pulls in `matplotlib.pyplot` (via `solutions/drawing_utils.py`) and
`sounddevice` -- neither is vendored, and neither is used by this tracker. A bare
`import mediapipe` therefore dies with
`ModuleNotFoundError: No module named 'matplotlib'`.

`storm_oic_hand_tracker.py` handles this by injecting empty stub modules into
`sys.modules` **before** importing cv2/mediapipe:

```python
if "matplotlib" not in sys.modules:
    matplotlib_stub = types.ModuleType("matplotlib")
    matplotlib_stub.__path__ = []
    ...
if "sounddevice" not in sys.modules:
    sys.modules["sounddevice"] = types.ModuleType("sounddevice")
```

This keeps the vendored install limited to camera vision instead of dragging in a
plotting stack.

**If you write a new script that imports mediapipe, copy the whole prelude** -- the
`sys.path` insert *and* the stubs. Importing mediapipe without them looks like a
broken install; it is not.
