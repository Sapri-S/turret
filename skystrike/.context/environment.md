# Environment

## Development machine
- Windows 11, **PowerShell**. ⚠️ **`&&` and `||` do not work** in this PowerShell
  version — use `;` or `if ($?) { }`.
- Python 3.11.9 at
  `C:\Users\sapri\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\python.exe`
- **Global site-packages is essentially empty** — no OpenCV, no MediaPipe.
  **`python-docx` is the one thing installed globally**, which is what the plan build
  script needs.
- A PowerShell profile fails to load on every shell start because script execution is
  disabled. **Harmless, ignore it.**

Note how the sibling project solved the empty-environment problem: `../hand-tracker/`
vendors OpenCV + MediaPipe into `python_deps/` and injects them into `sys.path` at
import time. Worth knowing about, though this project's vision code targets the Pi.

## Target hardware
- **Raspberry Pi 5 + AI HAT**, already owned.
  ⚠️ **Exact HAT variant not yet confirmed.** The runtime and the compiled model must
  match it — confirm before installing anything.
- Two-servo pan/tilt mount, with a light camera on it.

## Borrowed lesson, not borrowed code
The plan's Part 3 section A cites `../hand-tracker/`'s **parallax failure**: tracking
can be perfectly accurate and every shot still miss, because a device mounted beside
the camera does not share its line of sight. It was fixed there with a software aim
offset, scope-zeroed live, and **an offset is only valid at the distance it was
calibrated for**.

That finding is why Part 3 section A specifies degrees-per-pixel, sign conventions, an
aim point, and a re-calibration procedure up front rather than discovering them late.

**Written lessons travel between the two projects. Code does not** — see
`../AI_RULES.md` rules 1–4.
