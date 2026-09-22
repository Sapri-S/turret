# PROGRESS.md — Checklist

> Work the **next unchecked item**. Update this file as you go.
> `[ ]` todo · `[~]` in progress · `[x]` done · ⚠️ needs a user or advisor decision.

> **Status: proposal. No code written yet.** `src/` is deliberately empty.
> ⚠️ **Scope changed 2026-09-21** — fixed cameras replaced the pan/tilt concept.

## Done
- [x] Moving-camera plan written (Parts 1–3): pan/tilt, 17 software steps, 8-week
      schedule, calibration/thermal/licensing gap analysis. **Now superseded** —
      archived to `docs/archive/moving-camera-plan/` with a note on what it dropped.
- [x] **Fixed-camera proposal written** (2026-09-21): six-person ownership,
      two-semester phasing, funding plan, six selected features with evidence
      requirements, eight open decisions.
- [x] Markdown made the source of truth, with `build_fixed_camera_plan.py`
      generating the .docx. Verified: 88 paragraphs, 7 tables, all sections.
- [x] Moved into `turret/skystrike/` with agent context (2026-09-21).

## Next

### 1. Resolve the hardware contradiction ⚠️ needs you
- [ ] You said you want to **use and modify the A.S.S. II frame**. This plan makes
      the cameras **fixed**, which removes the reason for a pan/tilt turret and
      calls frame reuse "an unselected option."
- [ ] Decide which holds. It changes Member 5's entire mechanical scope.

### 2. Restore the AGPL warning if YOLO is still a candidate ⚠️
- [ ] The old plan named **YOLOv8/YOLO11 as AGPL-3.0** and made an advisor ruling a
      blocker. The new plan asks only whether "labels and permitted uses fit."
- [ ] That weaker question will not reliably surface copyleft reach over your own
      code. If a YOLO model is in play, name the licence explicitly.

### 3. Get advisor decisions ⚠️ advisor only — don't decide these
- [ ] The eight open decisions in the proposal.
- [ ] **Which features are deliverable and which are stretch.** Six evaluated
      features across two semesters is ambitious; get this ranked, in writing.
- [ ] Confirm the no-weapon-connection scope boundary in writing.

### 3b. Record physical measurements properly from day one ⚠️
- [ ] Every distance entering a calculation gets measured with an instrument,
      with its uncertainty and the instrument noted. Camera separation,
      camera-to-sensor offsets, mount positions, workspace extent.
- [ ] Never scale a physical quantity off a photograph that has no ruler at the
      subject's own distance.

> Learned the hard way on the sibling project (2026-09-22): a camera-to-barrel
> offset was estimated from one photo, scaled against a laptop screen of known
> size. The turret sat nearer the phone than the screen, so it was magnified by
> an unknown factor and the answer carried +/-30% error. The component that
> mattered most was not even visible in the frame. Thirty seconds with a ruler
> would have given +/-0.5 mm. Member 5 owns metrology -- this belongs in that
> role's working practice before any hardware is mounted.

### 4. Semester-one groundwork
- [ ] Assign the six members to the six roles.
- [ ] Inventory owned and borrowable equipment; **verify the Pi 5 and AI HAT**.
- [ ] Confirm the exact AI HAT variant — blocks all runtime installation.
- [ ] Confirm room, lighting, term dates, prop sizes and speeds.
- [ ] Agree the shared records (frame ID, timestamps, track ID/state, sensor event,
      reference position, config/calibration versions) **before** anyone implements.
- [ ] Build the costed BOM and the three budget options.

### 5. Start building
- [ ] Replay mode first, so recognition/tracking/reporting can progress without rig
      access.
- [ ] One-camera recognition baseline.
- [ ] Sensor event logging, independent of camera classification.
- [ ] Set up git + backups before there's work worth losing.

## Open questions
- A.S.S. II frame: still in, or out? (blocks mechanical design)
- AGPL ruling if YOLO is a candidate? (blocks model choice)
- Exact AI HAT variant? (blocks installation)
- The eight proposal decisions; which features are stretch; funding; term dates.

## Log
- **2026-09-21** — Copied out of the Codex output folder into `turret/skystrike/`.
  Added agent context. Made the old build script path-relative and confirmed it
  reproduced its Sep 20 snapshot exactly.
- **2026-09-21** — **Scope change.** Fixed-camera proposal added as the current
  plan; moving-camera plan archived. PLAN.md and this file rewritten — they had
  described the pan/tilt project and were wrong the moment the scope changed.
