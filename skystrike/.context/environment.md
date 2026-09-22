# Environment

## Development machine
- Windows 11, **PowerShell**. ⚠️ **`&&` and `||` do not work** in this PowerShell
  version — use `;` or `if ($?) { }`.
- Python 3.11.9 at
  the Windows Store build (`...\WindowsApps\PythonSoftwareFoundation.Python.3.11_*\python.exe`)
- **Global site-packages is essentially empty** — no OpenCV, no MediaPipe.
  **`python-docx` is the one thing installed globally**, which is what the plan build
  script needs.
- A PowerShell profile fails to load on every shell start because script execution is
  disabled. **Harmless, ignore it.**

Note how the sibling project solved the empty-environment problem: `../../test/hand-tracker/`
vendors OpenCV + MediaPipe into `python_deps/` and injects them into `sys.path` at
import time. Worth knowing about, though this project's vision code targets the Pi.

## Target hardware
- **Raspberry Pi 5 + AI HAT**, already owned.
  ⚠️ **Exact HAT variant not yet confirmed.** The runtime and the compiled model must
  match it — confirm before installing anything.
- **Fixed** camera mounts. No pan/tilt -- the cameras do not move.
- Approach sensors, technology not yet selected.
- A controlled-motion test rig with independent position/speed feedback.

## Borrowed lesson, not borrowed code
The superseded moving-camera plan cited `../../test/hand-tracker/`'s **parallax failure**:
tracking can be perfectly accurate and every shot still miss, because a device
mounted beside the camera does not share its line of sight. It was fixed there with
a software aim offset, scope-zeroed live, and **an offset is only valid at the
distance it was calibrated for**.

**Fixed cameras change the shape of this, they do not remove it.** With nothing
being aimed there is no barrel to zero, but the same class of error reappears as:
cross-view association between two cameras that see the scene from different
places, and **sensor-to-workspace mapping** — an approach sensor's crossing point
is not where the camera thinks the object is. The current proposal covers both
under Calibration, and keeps them as separate tests on purpose.

A second lesson worth carrying: the hand tracker's aiming loop blocked on
`time.sleep()` for 40-100 ms per frame, throwing away ~87% of its achievable frame
rate. The proposal's insistence on measuring **capture-to-displayed-result** as a
distribution, not an average, is exactly what catches that class of bug.

**Written lessons travel between the two projects. Code does not** — see
`../../AI_RULES.md` rules 1-4.
