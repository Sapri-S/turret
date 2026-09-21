# Dream Cheeky Storm O.I.C. package and test notes

## Included software

- `usb_missile_control`: Python 3 community controller for Dream Cheeky Thunder and O.I.C. Storm launchers. Upstream commit: `43a0f0b4dbbbe97e2dc36828e1d21d6171bcb76e`.
- `rocket_launcher`: older community controller for the same reported protocol. Upstream commit: `cf561578dd031345f68eab038c78ec2f823668b4`. This source is Python 2 and does not compile under Python 3 without changes.
- `storm_oic_probe.py`: local read-only probe. It enumerates known USB IDs and does not configure, move, stop, or fire a launcher.
- `python_deps/pyusb-src`: PyUSB source used for the local probe because the package installer could not write downloaded wheel metadata in this environment.

## Local test result

Tested on Windows on September 15, 2026.

- The Python 3 `usb_missile_control.MissileLauncher` module loaded successfully.
- PyUSB and a libusb backend enumerated six USB devices.
- No supported launcher was detected.
- The expected ID for these Storm/Thunder packages is USB VID:PID `2123:1010`.
- No USB control transfer, motor movement, reset, or fire command was sent.

The package may not work on Windows until the launcher has a compatible libusb/WinUSB driver. Do not replace a working Windows device driver until the exact USB ID has been confirmed.

## Raspberry Pi setup

On Raspberry Pi OS, install the USB dependency in a virtual environment:

```bash
sudo apt update
sudo apt install -y python3-venv libusb-1.0-0
python3 -m venv .venv
. .venv/bin/activate
python -m pip install pyusb
python storm_oic_probe.py
```

The probe should print a `MATCH` line before any controller is instantiated. The original interactive controller maps arrow keys to movement and Space to fire, so unload the foam missiles during initial hardware tests.

## Important behavior in the original sources

`rocket_launcher/rockets.py` recenters immediately when its controller object is created: right for 10 seconds, down for 4 seconds, then incremental up/left movements. Its main program enters an endless movement loop with a random chance of firing. Do not run it unchanged for initial testing.

`usb_missile_control` is the better starting point, but its interactive CLI fires when Space is pressed. Start by importing the module or running the read-only probe. Add a separate short movement test only after the device ID and stop behavior have been verified.

## Sources

- https://github.com/pwicks86/usb_missile_control
- https://github.com/jcastillocano/rocket_launcher
- https://github.com/pyusb/pyusb
