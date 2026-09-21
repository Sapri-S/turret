# Tracker architecture — how `storm_oic_hand_tracker.py` works

Stage by stage, with the tuning constants that matter.

## Capture
Threaded, keeping only the **newest** frame (`LatestFrameCamera`) — it never queues.
**320×240 MJPG at 30 fps**, `CAP_PROP_BUFFERSIZE = 1`. Dropping stale frames is
deliberate: a queued frame is a frame that aims the turret at where the hand *was*.

`open_camera()` tries **MSMF → DSHOW → CAP_ANY** and takes the first backend that
actually delivers a frame.

## Detection
MediaPipe Hands: `max_num_hands=1`, `model_complexity=0`, detection and tracking
confidence **0.55**.

**Landmark 9** (middle-finger MCP) is the tracked point — the centre of the palm,
which is far steadier than a fingertip. Smoothed with `alpha = 0.85` weighted toward
the newest sample.

## Aiming
An **aim box** of **20% of frame width × 24% of height**, centred on frame centre
**plus the aim offset**.

- Outside the box → pulse the motors, pulse length scaled by how far outside
  (**0.040–0.100 s**), always ending in `STOP`.
- Inside the box → `STOP`.

The **aim offset** exists because the camera sits beside the barrel and doesn't share
its line of sight. It is live-adjustable with `W/A/S/D`, reset with `R`, and seeded by
`--aim-offset-x` / `--aim-offset-y`. See `../docs/hard-won-findings.md` §5 —
**not yet calibrated.**

## Fist detection
`count_curled_fingers()` — a finger counts as **curled** when its fingertip is closer
to the wrist than its own PIP joint. This is **rotation-invariant**, so it doesn't
assume an upright hand.

Needs **≥3 of 4** fingers (`FIST_CURL_THRESHOLD`); the thumb is ignored. The live
count shows on the HUD as `FIST n/4`.

## Firing
Fist closed **AND** inside the aim box, continuously, for
`FIST_HOLD_SECONDS = 1.5` → **one shot.**

Then `FIRE_CYCLE_SECONDS = 4.0` of **total silence** — the movement block is wrapped
in `if time.monotonic() >= fire_cooldown_until:` so the loop sends nothing at all.
This is mandatory, not a nicety (`../docs/hard-won-findings.md` §1).

It then **auto-rearms** if the fist is still held, so you can keep firing without
opening your hand — roughly **one shot every 5.5 s**. Opening the hand or leaving the
box resets the hold timer.

## HUD
Status, `FPS`, `FIST n/4`, the current aim offset values, and countdown / `FIRE!`
states.

## Process guard
Single-instance mutex `Local\StormOICHandTracker` stops two copies fighting over the
camera.

## Constants worth knowing
| Constant | Value | Why |
| --- | --- | --- |
| `FIRE_CYCLE_SECONDS` | `4.0` | Empirical. Shorter silently kills the shot. |
| `FIST_HOLD_SECONDS` | `1.5` | Deliberate-intent gate before firing. |
| `FIST_CURL_THRESHOLD` | `3` of 4 | Thumb ignored. |
| smoothing `alpha` | `0.85` | Weighted toward the newest sample. |
| aim box | 20% W × 24% H | Centred on frame centre + aim offset. |
| pulse length | 0.040–0.100 s | Scaled by distance outside the box. |
| dedupe window | 0.12 s | Must stay under the ~150 ms keep-alive. |
