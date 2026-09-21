# AGENTS.md — Agent Context (read first, every session)

> Codex loads this file automatically from the project root at the start of
> every session. Read it before doing anything else.

## What this project is
**Project B — SkyStrike.** A university senior design team project. A **Raspberry Pi 5
with an AI HAT** (both already owned) runs a camera that recognises **moving fake
fruit** and **ignores tennis balls**, then centres it on a **two-servo pan/tilt mount**.

- **Milestone 1:** recognise moving fake fruit on screen, reject tennis balls.
- **Milestone 2:** mount a light camera on the pan/tilt frame and have it centre the fruit.

**Both milestones are camera-only and non-firing.**

**Status: plan only. No code has been written yet.** Part 2 step 1 (project skeleton)
is the starting point.

## This project does not fire ⚠️
The plan commits to this, and `../AI_RULES.md` §1–4 enforce it:
- No launcher connected during development.
- No aiming or firing at anyone's hand or body, even with a foam dart.
- No automatic release.
- Any dart-accuracy trial is **supervised**, on a **printed paper target**, with a
  **human manually releasing** the dart.

The hand tracker in `../hand-tracker/` *is* a firing device. It is a personal toy and
**not part of this academic project**. Do not copy its launcher class, its fire timing,
or its fist-to-fire logic into here. Written lessons may travel; code may not.

## Read these before doing anything (source of truth)
- **`../AI_RULES.md`** — hard guardrails. Non-negotiable.
- **`plan/SkyStrike_Project_Plan_With_Software_Build.docx`** — **the current full plan**,
  Parts 1, 2 and 3. Generated; see below.
- **PLAN.md** — what's in each part of that document, and what's still blank.
- **PROGRESS.md** — what's done, what's next, and every open question.
- **`.context/environment.md`** — the machine this is built on and its traps.
- **`docs/starter_BUILD_PLAN.md`** — the original starter-folder build plan.

## The plan document is generated — do not hand-edit it ⚠️
```
plan/SkyStrike_Editable_Project_Plan_Updated.docx   (Part 1, the Sep 17 source)
        │
        ▼  python build_skystrike_plan_parts_2_and_3.py
plan/SkyStrike_Project_Plan_With_Software_Build.docx  (Parts 1 + 2 + 3)
```
To change Parts 2 or 3, **edit the script and re-run it.** A hand edit to the output is
destroyed by the next build. To change Part 1, edit the source `.docx`.

Run it with:
```
cd "C:\Users\sapri\Downloads\turret\skystrike\plan"
python build_skystrike_plan_parts_2_and_3.py
```
Needs `python-docx`, which **is** installed globally. `ROOT` now resolves relative to
the script, so the folder can move without an edit.

## How to work here
1. At session start: read `../AI_RULES.md` → PROGRESS.md → the current plan document.
2. Work the **next unchecked item** in PROGRESS.md.
3. After each chunk: update PROGRESS.md, then summarize what changed in 1–2 lines.
4. Anything involving **a launcher, a dart, or pointing at a person** → **stop and ask.**
5. Anything an **advisor** must decide (licensing, scope, deliverable dates) → don't
   pick for them. Put it in PROGRESS.md's open-questions list and flag it.

## Layout
| Path | What it is |
| --- | --- |
| `plan/` | The live plan: Part 1 source, the build script, and the generated full plan. |
| `docs/archive/` | Older drafts and dated snapshots. Reference only, never edit. |
| `docs/starter_BUILD_PLAN.md` | From the original `SkyStrike_Programmable_Turret_Starter/`. |
| `src/` | **Empty.** Part 2 step 1 (project skeleton) goes here. |
| `.context/` | Environment notes for the agent. |

## Do NOT
- Hand-edit `plan/SkyStrike_Project_Plan_With_Software_Build.docx`. Edit the script.
- Copy firing code, fire timing, or the launcher class from `../hand-tracker/`.
- Connect a launcher, or point the camera rig at a person as a target.
- Install any AI HAT runtime before the **exact HAT variant is confirmed** — the
  runtime and the compiled model must match it.
- Build on YOLOv8/YOLO11 before the advisor rules on the **AGPL-3.0** question.
- Commit footage that shows teammates.
