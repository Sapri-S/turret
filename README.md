# turret/

Two **separate** camera-tracking turret projects that happen to share hardware
intuition, a parallax lesson, and an owner. They live side by side for convenience.
They are **not one project** and their code does not mix — see `AI_RULES.md`.

| Folder | Project | Status |
| --- | --- | --- |
| `test/hand-tracker/` | **Project A** — Dream Cheeky Storm O.I.C. webcam hand tracker. Personal hobby toy and testbed. Aims a USB foam-dart launcher, fires on a fist gesture. | **Working.** Main open task: calibrate the aim offset. |
| `skystrike/` | **Project B** — SkyStrike senior design project. Raspberry Pi 5 + AI HAT, **fixed** cameras plus approach sensors, tracking artificial fruit and balls. Six-person university team, two semesters. | **Proposal only, no code yet.** |

## The separation rule (read this before writing anything)

Project A auto-fires a foam dart at a human hand. That is why it is a **personal toy
and not coursework**.

Project B's own plan commits to being **non-firing**: no launcher connected during
development, no aiming or firing at anyone's hand or body even with a foam dart, and
no automatic release. Any dart-accuracy trial must be supervised, aimed at a printed
paper target, with a human manually releasing the dart.

So:
- Do **not** copy Project A's firing code, fire timing, or HID launcher class into
  Project B.
- Do **not** merge the folders or share a package between them.
- If a coursework request would point Project A at a person, **stop and flag it.**

What *may* travel from A to B is **written knowledge, not code**: the parallax
finding, calibration method, and threading/latency lessons. Project B's plan
(Part 3 §A) already cites A's parallax failure as evidence, which is the right shape
for that borrowing.

## Each project is its own session root
Open `test/hand-tracker/` or `skystrike/` as the working directory — not this parent — so
that project's `CLAUDE.md` loads and its context stays scoped.

## Where this came from
Copied 2026-09-21 from
`C:\Users\sapri\Documents\Codex\2026-09-15\can\outputs\`. **Originals were left in
place** — nothing was moved or deleted. Once you've confirmed this folder works, the
originals can go.

`docs/` holds the paper trail for how this folder came to exist:

| File | What it is |
| --- | --- |
| `HANDOFF_2026-09-21.md` | The session brief this folder was built from. |
| `session-transcript-2026-09-21.md` | Readable transcript of that session — what was asked, what was found, what was decided. Tool calls are summarised. |
| `session-transcript-2026-09-21.zip` | The full machine-readable export (JSONL + metadata). |

Not copied: `camera_probe/` (snapshots containing photos of you — the handoff marked
them safe to delete), `__pycache__/`, and `ASS_II_Safe_Review/` +
`ASS_II_camera_pan_tilt_only.zip` (32 MB, unreferenced by the handoff — say the word
if those belong to SkyStrike and I'll bring them over).

## Environment (applies to both projects)
- Windows 11, PowerShell. **`&&` and `||` do not work** in this PowerShell version —
  use `;` or `if ($?) { }`.
- Python 3.11.9 at
  `C:\Users\sapri\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\python.exe`
- **Global site-packages is essentially empty** — no OpenCV, no MediaPipe. Project A
  works *only* because its dependencies are vendored in `test/hand-tracker/python_deps/`
  and injected into `sys.path` at runtime. Don't assume imports work outside that
  folder. `python-docx` is the one thing installed globally (Project B needs it).
- A PowerShell profile fails to load on every shell start because script execution is
  disabled. Harmless, ignore it.
