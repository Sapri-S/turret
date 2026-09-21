# Superseded: the moving-camera plan

These files are the **previous** SkyStrike plan, in which a light camera was
centred on a **two-servo pan/tilt mount**. They were superseded on
**2026-09-21** by `plan/SkyStrike_Fixed_Camera_Plan.md`, which states outright
that it "supersedes the earlier moving-camera concept."

Kept for reference and for the advisor trail. **Do not build from these.**

| File | What it was |
| --- | --- |
| `SkyStrike_Project_Plan_With_Software_Build.docx` | The full Parts 1-3 plan. 113 paragraphs, 11 tables. |
| `SkyStrike_Editable_Project_Plan_Updated.docx` | Part 1 source (Sep 17), input to the build script. |
| `build_skystrike_plan_parts_2_and_3.py` | Appended Parts 2 and 3 to that source. |
| `SkyStrike_V3_2026-09-20.docx` | A Sep 20 save-as snapshot. Verified identical in content to the generated plan. |

## What the new plan dropped

Worth knowing, because some of it was load-bearing:

- **The pan/tilt mount and all servo control.** The old plan mentioned servos 39
  times and pan/tilt 10 times each. The new plan has none of it.
- **The <=100 ms camera-to-servo latency target**, explicitly retired.
- **The 8-week schedule**, replaced by two semesters.
- **The AGPL-3.0 warning.** The old Part 3 section G named YOLOv8/YOLO11 as
  AGPL-3.0 and made an advisor ruling a blocker before building on them. The new
  plan asks only whether a model's "labels and permitted uses fit the project" --
  a weaker question that will not reliably surface copyleft reach. **If a YOLO
  model is still a candidate, restore the specific warning.**
