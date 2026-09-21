# PLAN.md — Scope & Plan Map

> What the project is, what's in the proposal, and what is still blank.
> The proposal itself is the source of truth; this file maps it.
>
> ⚠️ **Rewritten 2026-09-21.** The pan/tilt "moving camera" plan was superseded.
> If you remember this project as a servo turret that centres fruit, that is the
> old plan — see `docs/archive/moving-camera-plan/`.

## 1. Goal
A standalone system using **fixed cameras** plus **approach sensors** to detect
incoming objects, recognise specified artificial fruit and ball classes, maintain
object identities across motion, recover after temporary obstruction, and
automatically report measured performance. An instrumented moving-object test rig
supplies independent reference position and speed.

**The cameras do not move.** Six-person senior design team, two semesters.

## 2. Non-goals (explicit, and binding)
- **No weapon aiming, triggering, or firing controls.** Any connection to them is
  out of scope. See `../AI_RULES.md` rules 1–4.
- **A.S.S. II is background reference only** — not a software dependency, not an
  implementation starting point. Its airsoft targeting and firing functionality is
  outside this plan. Reusing its frame as a non-firing structure is an
  **unselected option**, and no turret speed or firing modification is included.
- **Scene exclusion is not a safety interlock.** Person/animal detection is
  evaluated as a feature; it does not certify that a scene contains no people.
- **Not the hand tracker.** `../test/hand-tracker/` fires a dart at a hand. Separate
  project, separate rules.

## 3. The current proposal
`plan/SkyStrike_Fixed_Camera_Plan.md` — **the source of truth.**
`plan/SkyStrike_Fixed_Camera_Plan.docx` is generated from it for sharing.

Structure: project goal · scope and outputs · system concept · camera arrangement ·
approach sensors · six selected feature requirements · classification and scene
exclusions · six-person ownership · interfaces and working practice · evaluation
plan · two-semester development plan · funding and purchasing · eight open
decisions · definition of done · technical references.

### The six selected features
Persistent multi-object tracking · obstruction recovery · automatic camera
calibration · adaptive tracking modes · a repeatable moving-object test rig ·
automatic performance reporting. Each carries its own demonstration and evidence
requirement.

### Ideas worth not losing
- An approach sensor reports **an event, not a class**. A sensor alert must never
  be promoted directly to confirmed fruit.
- **Classification and identity are separate** — two objects can both be fruit
  without being distinguishable individuals.
- **Two cameras do not automatically give depth.** Metric stereo needs a
  specifically calibrated configuration and synchronised observations.
- Test-rig reference measurements **must not leak into the tracking algorithm**
  during evaluation.
- Zero observed errors does not establish that errors are impossible. Report
  distributions and a high-percentile value, not just averages.

## 4. Build pipeline for the document
```
plan/SkyStrike_Fixed_Camera_Plan.md      <- edit this
        |
        v   python build_fixed_camera_plan.py
plan/SkyStrike_Fixed_Camera_Plan.docx
```
**Edit the Markdown, not the .docx.** The next build overwrites the .docx. The
Markdown is also what renders on GitHub, since GitHub cannot preview .docx.

## 5. Hardware
Raspberry Pi 5 + AI HAT, reported as already owned — **to be verified** as part of
the semester-one inventory. Fixed cameras and mounts. Approach sensors, technology
not yet selected. A controlled-motion test rig with independent feedback.

⚠️ **Exact AI HAT variant still unconfirmed.** Runtime and compiled model must match.

## 6. What is still blank
All eight open decisions, plus: funding (entirely unresearched), term dates, room
dimensions and lighting, prop sizes and speeds, numeric acceptance thresholds, and
which team member is which. See PROGRESS.md.

## 7. Known tension to resolve
The user has stated they want to **use the A.S.S. II frame and modify it**. This
plan makes the cameras fixed, which removes the need for a pan/tilt turret and
demotes frame reuse to an unselected option. **Those two positions do not yet
agree** — worth settling before Member 5 starts mechanical design.

## 8. Success criteria
See the proposal's "Definition of done". Numeric thresholds are deliberately
deferred until after baseline measurements and advisor review.
