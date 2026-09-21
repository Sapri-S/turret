# SkyStrike Programmable Foam-Dart Turret

## Goal

Build a Raspberry Pi 5 turret that can track fruit, tennis balls, or a printed
marker and smoothly center the selected target. The first version is tracking
only. A foam-dart module can be added after the motion and safety interlocks
have been validated.

## Recommended architecture

```text
Camera Module 3 Wide
        |
Raspberry Pi 5 + AI HAT
  - object detection
  - target selection
  - person/face exclusion
  - tracking controller
        |
    USB serial
        |
Raspberry Pi Pico or Arduino Nano
  - motion watchdog
  - servo limits
  - physical ARM input
  - manual trigger input
        |
Servo controller + separate servo power
        |
Pan servo + tilt servo
```

The small controller keeps the motors stopped if the Pi crashes or stops
sending updates. The Pi never powers the servos directly.

## Provisional parts list

| Item | Quantity | Purpose |
|---|---:|---|
| Raspberry Pi 5 and AI HAT | 1 | Vision and high-level control |
| Raspberry Pi Camera Module 3 Wide | 1 | Wide view and high-frame-rate capture |
| Pi 5 standard-to-mini camera cable | 1 | Camera connection |
| Raspberry Pi Pico or Arduino Nano | 1 | Real-time motor and safety controller |
| goBILDA 25-3 speed servo or equivalent | 2 | Pan and tilt |
| PCA9685 servo controller | 1 | Stable servo PWM |
| Standard-size servo brackets | 2 sets | Mechanical mounting |
| Custom aluminum or 3D-printed mounting plate | 1 | Holds the launcher and camera |
| Regulated 6 V servo supply, at least 6 A | 1 | Separate servo power |
| Inline fuse, main power switch, and emergency-stop button | 1 each | Hardware shutdown |
| ARM toggle switch and indicator LED | 1 each | Visible launch enable state |
| Large cardboard or fabric backstop | 1 | Captures foam darts during testing |

Do not order the servos or fabricate the mounting plate until the moving
assembly has been weighed and its center of gravity measured.

## Control behavior

1. The camera detects a fruit, tennis ball, or printed marker.
2. The Pi sends desired pan and tilt positions to the motor controller.
3. The controller applies acceleration and speed limits for smooth movement.
4. If the target disappears, communication stops, or a person enters the
   firing area, the controller centers or stops and disables launching.
5. Holding the target centered for three seconds changes the display to
   `READY`; it does not launch automatically.
6. While the target is settling, the operator may hold a separate REV control
   to bring a stock flywheel blaster up to speed. `READY` is shown only when
   the target and launcher are both ready.
7. Launching requires the physical ARM switch and a separate manual FIRE
   button. Releasing REV stops the flywheels.

## Development phases

### Phase 1: Pan and tilt

- Build the servo frame without a launcher or darts.
- Add software angle limits before attaching the payload.
- Test centering, acceleration limiting, emergency stop, and watchdog behavior.

### Phase 2: Low-latency camera

- Install Camera Module 3 Wide on the moving frame.
- Capture at 720p/120 or a smaller low-latency mode.
- Keep only the newest frame; never process a queued camera backlog.
- Measure camera FPS, inference FPS, and end-to-end control delay.

### Phase 3: Target tracking

- Begin with a bright printed marker or tennis ball.
- Add fruit detection after motion is stable.
- Add face/person detection as an independent exclusion check.
- Tune proportional control, acceleration, braking distance, and the center
  dead zone.

### Phase 4: Foam-dart module

- Mount a low-energy, commercially manufactured foam-dart mechanism.
- Keep automatic launching disabled.
- Add the physical ARM switch, indicator, manual trigger, and backstop.
- Prefer a commercially manufactured, low-energy flywheel foam-dart mechanism
  with a magazine if first-shot delay and repeat shots matter. The original
  Dream Cheeky spring/plunger cycle is the wrong mechanism for this goal.
- Use separate manual REV and FIRE controls: start the flywheels before the
  intended shot, then feed one dart only after they reach operating speed.
  A cold first shot still has spin-up delay; keeping the wheels running while
  armed trades lower delay for noise, heat, and battery use.
- Keep feed rate within the blaster's stock specification. Do not increase
  dart velocity or bypass its mechanical or electrical protections.
- Validate that loss of video, software failure, emergency stop, or person
  detection immediately disables both REV and FIRE outputs.

### Phase 5: Evaluation

- Compare latency and detection accuracy on the laptop and Raspberry Pi 5.
- Test target distances of 6, 9, and 12 feet.
- Record centering time, overshoot, missed detections, and false detections.
- Measure cold-start-to-first-dart delay, already-revved trigger-to-dart delay,
  and the interval between repeat shots separately. Use slow-motion video or
  a microphone recording so the numbers are repeatable.
- Test only with inert targets and an empty area behind the backstop.

## Measurements needed for the mechanical design

- Weight of the launcher or foam-dart module
- Width, length, and mounting-hole locations
- Horizontal and vertical center of gravity
- Required pan and tilt angles
- Available base dimensions
- Desired camera position relative to the launcher centerline

## Reference design

The Arduino Project Hub Bluetooth Nerf Turret is useful as a reference for a
3D-printed frame and separate pan, tilt, and feed mechanisms:

https://projecthub.arduino.cc/Little_french_kev/bluetooth-nerf-turret-ea2fac
