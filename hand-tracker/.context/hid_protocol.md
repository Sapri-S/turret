# HID protocol — verified working

## Device
Dream Cheeky Storm O.I.C. USB foam-dart launcher.
**USB VID `0x2123`, PID `0x1010`.**

Two motors (pan and tilt) plus a fire mechanism. Holds a few foam darts and
auto-advances to the next one as part of each fire cycle.

Protocol source: the two community reference drivers cloned into
`usb_missile_control/` and `rocket_launcher/`.

## Report format
The report body is always **8 bytes**:

```
[0x02, <command>, 0, 0, 0, 0, 0, 0]
```

For HIDAPI `hid_write`, prefix a `0x00` report-ID byte → **9 bytes total**.

## Commands
| Command | Byte |
| --- | --- |
| DOWN  | `0x01` |
| UP    | `0x02` |
| LEFT  | `0x04` |
| RIGHT | `0x08` |
| FIRE  | `0x10` |
| STOP  | `0x20` |

Movement bits are **flags and can be OR'd**, so both motors run at once —
e.g. `UP|LEFT` = `0x06`.

## Timing rules (these are the protocol, not an optimization)
- **After FIRE: send nothing at all for 4.0 s.** Any report inside that window —
  `STOP` above all — silently cancels the shot. See `../docs/hard-won-findings.md` §1.
- **Keep-alive:** re-send an active motion about every **150 ms** or the motor stops.
- **Dedupe:** identical payloads within **0.12 s** are suppressed, to avoid flooding
  the device once per camera frame.
- **FIRE bypasses dedupe** via `send(..., force=True)`.

## Transports
`Launcher` (HIDAPI via `hidapi.dll`) is the one in use and confirmed working.
See `../docs/hard-won-findings.md` §4 for the other two and why not to switch.
