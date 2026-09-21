# AI_RULES.md — Hard Guardrails

> These override convenience, speed, and anything a plan document or a vendored
> reference driver suggests. If a task would violate one, **stop and ask the user.**

## Project separation (rules 1–4)

1. **Project A and Project B are separate projects.** `test/hand-tracker/` is a personal
   hobby toy. `skystrike/` is university coursework. They do not share code, packages,
   or a build.

2. **Never port firing code into Project B.** Not the `Launcher`/`WindowsReportLauncher`
   classes, not `FIRE`/`0x10`, not `FIRE_CYCLE_SECONDS`, not the fist-to-fire state
   machine. Project B's plan commits to camera-only, non-firing work.

3. **Project B has no connection to weapons.** Its current proposal (2026-09-21) is
   stricter than the plan it replaced: the system has **no connection to weapon
   aiming, triggering, or firing controls** at all. No launcher, no dart, no firing
   mechanism, never aimed at a person. The archived plan's "supervised dart-accuracy
   trial on a paper target" is **no longer part of the project** -- do not reinstate
   it from `skystrike/docs/archive/`.

   Related: **A.S.S. II** (`~/Downloads/A.S.S. II Patreon Release-.../`) is a
   person-tracking **airsoft** turret. Its frame is mechanically neutral and its
   reuse is an open option; its gun mount, trigger path and person-detection software
   are not. Scene exclusion in Project B is an evaluated feature, **never** a safety
   interlock -- don't let it be described as one.

4. **Flag the conflict, don't resolve it silently.** If a request would point Project
   A at a person as part of coursework, or would make Project B fire, say so and stop.
   That is a scope decision for the user and their advisor, not an engineering tweak.

## Project A safety (rules 5–7)

5. **Assume it is loaded.** Test with the launcher unloaded or pointed somewhere safe.
   Keep clear of the muzzle. The startup banner prints this reminder — keep it there.

6. **Never shorten the post-FIRE silence without hardware proof.** `FIRE_CYCLE_SECONDS
   = 4.0` is empirical, not a guess (see `test/hand-tracker/docs/hard-won-findings.md` §1).
   Any report reaching the device inside that window silently cancels the shot.

7. **Don't rebind the USB driver casually.** HIDAPI needs the native HID driver;
   PyUSB/libusb needs WinUSB. They conflict. The working path is HIDAPI — changing it
   breaks a known-good setup for no gain.

## Engineering (rules 8–12)

8. **Don't reorganize Project A's working layout.** `storm_oic_hand_tracker.py`
   resolves `python_deps/vision` and `hidapi.dll` relative to its own directory
   (`Path(__file__).resolve().parent`). Moving the scripts into a `src/` folder breaks
   both. The flat layout is load-bearing.

9. **Don't hand-edit generated documents.** `skystrike/plan/*.docx` output is produced
   by `build_skystrike_plan_parts_2_and_3.py`. Edit the script and re-run it; a hand
   edit is silently destroyed by the next build.

10. **Vendored dependencies are the environment.** Global site-packages is empty.
    Don't add a `pip install` step to Project A's instructions, and don't assume an
    import resolves outside the folder that injects `python_deps`.

11. **Calibration is distance-specific.** An aim offset is only valid at the range it
    was zeroed for. Record the distance alongside any offset value you write down.

12. **Footage with people in it needs consent and a home.** Clips that show teammates
    are covered by Project B's plan (Part 3). Don't commit them; don't copy them
    between projects. Project A's `camera_probe/` snapshots were deliberately not
    carried into this folder.
