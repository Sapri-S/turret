# AGENTS.md — Agent Context (read first, every session)

> Codex loads this file automatically from the project root at the start of
> every session. Read it before doing anything else.

## What this project is
**Project B — SkyStrike.** A university senior design team project, **six people,
two semesters**. A standalone system that uses **fixed cameras** plus **approach
sensors** to detect incoming objects, recognise specified artificial fruit and ball
classes, maintain object identities, recover after temporary obstruction, and
automatically report measured performance. An instrumented moving-object test rig
supplies independent reference position and speed.

**The cameras do not move.**

Six selected features: persistent multi-object tracking · obstruction recovery ·
automatic camera calibration · adaptive tracking modes · a repeatable moving-object
test rig · automatic performance reporting.

Hardware: Raspberry Pi 5 + AI HAT, reported as owned but **to be verified**.

**Status: proposal only. No code written yet.** `src/` is empty.

> ⚠️ **Scope changed 2026-09-21.** An earlier plan had a light camera centred on a
> **two-servo pan/tilt mount**, with a 17-step build and an 8-week schedule. That is
> **superseded** — it lives in `docs/archive/moving-camera-plan/`. If something in
> this project seems to assume a servo turret, it is stale; say so.

## This project has no connection to weapons ⚠️
The proposal states it outright: the system *"has no connection to weapon aiming,
triggering, or firing controls."* `../AI_RULES.md` rules 1–4 enforce it.

- No launcher, no dart, no firing mechanism — at all.
- Never aimed at a person.
- **A.S.S. II is background reference material only.** Not a software dependency,
  not an implementation starting point. Its airsoft targeting and firing
  functionality is outside this plan. Reusing its frame as a non-firing structure
  is an **unselected option**; no turret speed or firing modification is included.
- Person/animal detection is a **scene-exclusion feature under evaluation**, not a
  guarantee and not a physical safety interlock. Never describe it as one.

The hand tracker in `../hand-tracker/` *is* a firing device. Personal toy, **not
part of this academic project.** Written lessons may travel between them; **code may
not.**

## Read these before doing anything (source of truth)
- **`../AI_RULES.md`** — hard guardrails. Non-negotiable.
- **`plan/SkyStrike_Fixed_Camera_Plan.md`** — **the current proposal.** The source
  of truth. Markdown, so it renders on GitHub.
- **PLAN.md** — a map of the proposal, plus what's still blank.
- **PROGRESS.md** — what's done, what's next, every open question.
- **`.context/environment.md`** — the machine, the target hardware, and the lessons
  carried over from the sibling project.
- **`docs/ass-ii-hardware-reference.md`** — what the A.S.S. II release actually
  contains: parts, printed dimensions, BOM, and the two traps in its firmware.
  Read before anyone proposes reusing that hardware.
- **`docs/archive/moving-camera-plan/README.md`** — what the old plan said and, more
  usefully, **what the new one dropped.**

## The plan document is generated — edit the Markdown ⚠️
```
plan/SkyStrike_Fixed_Camera_Plan.md      <- edit this
        |
        v   python build_fixed_camera_plan.py
plan/SkyStrike_Fixed_Camera_Plan.docx    <- generated, for sharing
```
A hand edit to the `.docx` is destroyed by the next build. Needs `python-docx`,
which **is** installed globally. `ROOT` resolves relative to the script.

## How to work here
1. At session start: read `../AI_RULES.md` → PROGRESS.md → the proposal.
2. Work the **next unchecked item** in PROGRESS.md.
3. After each chunk: update PROGRESS.md, then summarise what changed in 1–2 lines.
4. Anything involving **a launcher, a weapon, or pointing at a person** → **stop and
   ask.**
5. Anything an **advisor** must decide — licensing, which features are stretch,
   numeric thresholds, dates — **don't pick for them.** Put it in PROGRESS.md's open
   questions and flag it.

## Two open contradictions — don't paper over them
- **The A.S.S. II frame.** The user has said they want to use and modify it. This
  plan makes the cameras fixed, which removes the reason for a turret. Unresolved.
- **AGPL.** The archived plan named **YOLOv8/YOLO11 as AGPL-3.0** and made an
  advisor ruling a blocker. The new proposal only asks whether a model's "labels and
  permitted uses fit the project" — weaker, and it won't reliably surface copyleft
  reach over your own code. If YOLO is still a candidate, say so explicitly.

## Layout
| Path | What it is |
| --- | --- |
| `plan/` | The current proposal (`.md` source + generated `.docx`) and its build script. |
| `docs/archive/moving-camera-plan/` | The superseded pan/tilt plan, its source and build script. **Reference only, never build from it.** |
| `docs/archive/` | Older first drafts. |
| `docs/starter_BUILD_PLAN.md` | From the original `SkyStrike_Programmable_Turret_Starter/`. |
| `src/` | **Empty.** First code goes here — start with replay mode. |
| `.context/` | Environment notes for the agent. |

## Do NOT
- Hand-edit `plan/SkyStrike_Fixed_Camera_Plan.docx`. Edit the Markdown.
- Build from anything in `docs/archive/`.
- Copy firing code, fire timing, or the launcher class from `../hand-tracker/`.
- Connect a launcher or any weapon, or point a camera at a person as a target.
- Describe scene exclusion as a safety guarantee.
- Install any AI HAT runtime before the **exact variant is confirmed** — runtime and
  compiled model must match.
- Promote a sensor alert directly to a confirmed detection. An approach sensor
  reports **an event, not a class.**
- Let test-rig reference measurements leak into the tracking algorithm during
  evaluation.
- Commit footage that shows teammates.
