# PLAN.md — Scope & Plan Map

> What the project is, what's in the plan document, and what is still blank.
> The plan document itself is the source of truth; this file maps it.

## 1. Goal
A Raspberry Pi 5 + AI HAT camera rig that recognises moving fake fruit, rejects tennis
balls, and centres the fruit on a two-servo pan/tilt mount. Senior design team project.

- **Milestone 1** — recognise moving fake fruit on screen, ignore tennis balls.
- **Milestone 2** — light camera on a two-servo pan/tilt frame, centring the fruit.

## 2. Non-goals (explicit, and binding)
- **Non-firing.** No launcher connected during development. No automatic release.
- **Never aimed at a person.** Not a hand, not a body, not with a foam dart.
- **Not the hand tracker.** `../hand-tracker/` is a personal toy that fires at a hand.
  Separate project, separate rules — see `../AI_RULES.md` rules 1–4.
- Any optional dart-accuracy trial is supervised, on a printed paper target, with a
  human manually releasing the dart.

## 3. Hardware
Raspberry Pi 5 + AI HAT, **already owned**. Two-servo pan/tilt mount, light camera.

⚠️ **The exact AI HAT variant is not yet confirmed** — the runtime and the compiled
model must match it. Confirm before installing anything.

## 4. What the plan document contains
`plan/SkyStrike_Project_Plan_With_Software_Build.docx` — Parts 1, 2 and 3.
113 paragraphs, 11 tables, 26 headings.

### Part 1 — Project direction *(written earlier, not in the handoff session)*
Project direction, hardware table, a **12-step build**, vision and data choices,
safety and scope boundaries, the optional supervised foam-dart accuracy test,
open decisions for the advisor, and **7 numbered sources**.

### Part 2 — Software build plan
- **What "fast enough" means**, with target numbers: **≥30 fps**, **≤100 ms**
  camera-to-servo delay, **<1 s** centring, **zero** tennis-ball-as-fruit errors.
- A **4-stage threaded architecture**: capture → detect → track → control.
- **17 numbered software steps**, each with a "Done when" line.
- A test/metrics table, an **8-week schedule**, and a risks-and-fallbacks table.

### Part 3 — Gaps to close before the build starts
- **A. Calibration** — degrees-per-pixel, sign conventions, aim point, scope-zeroing,
  re-calibration. **Cites Project A's parallax failure as direct evidence** — the same
  trap awaits any device mounted beside a camera.
- **B.** Thermal, power, and long runs.
- **C.** Fallback if the AI HAT path stalls — including **classical HSV colour
  detection**, which suits bright plastic fruit and doubles as an accuracy baseline.
- **D.** Team roles, deliverables, dates.
- **E.** Git, backups, working practice.
- **F.** Recordings, storage, and **consent** when teammates appear in footage.
- **G.** Licensing, attribution, ordering. ⚠️ **YOLOv8/YOLO11 are AGPL-3.0 — this needs
  an advisor decision before anything is built on them.**
- **H.** Definition of done.
- **I.** Six questions only the advisor can answer.

## 5. Build pipeline for the document
```
plan/SkyStrike_Editable_Project_Plan_Updated.docx     Part 1 source (Sep 17)
        |
        v   build_skystrike_plan_parts_2_and_3.py     appends Parts 2 + 3
plan/SkyStrike_Project_Plan_With_Software_Build.docx
```

**Edit the script, not the output.** Verified reproducible on 2026-09-21: the generated
file matches the Sep 20 snapshot in `docs/archive/` paragraph-for-paragraph and
table-for-table.

## 6. What is still blank
Team roles, deliverable dates, budget, demo room, the six advisor answers, the
confirmed AI HAT variant, and the AGPL licensing decision. See PROGRESS.md.

## 7. Success criteria
The plan's Part 3 section H is the real definition of done. Working targets from
Part 2: ≥30 fps, ≤100 ms camera-to-servo, <1 s to centre, zero tennis-ball false
positives.
