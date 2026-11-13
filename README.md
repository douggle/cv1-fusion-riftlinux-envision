# CV1 Fusion (RiftLinux 0.1.5) — Envision profile

An [Envision](https://gitlab.com/gabmus/envision) profile that runs the **Oculus
Rift CV1** with the tracking stack from **[RiftLinux](https://github.com/AIIX/RiftLinux)
0.1.5** (a Monado fork), driving SteamVR/OpenVR titles through
[Xrizer](https://github.com/Supreeeme/xrizer).

This repo is just the **profile + setup notes** — there is no patched source here.
The profile builds RiftLinux 0.1.5 verbatim from its upstream tag `v0.1.5`.

> Personal setup, not affiliated with or endorsed by the RiftLinux, Envision,
> Monado, or Xrizer projects.

## Why the whole RiftLinux stack, not a few files

RiftLinux and the gadLinux `cv1-fusion` Monado fork both descend from the same
Rift CV1 lineage, but their **constellation tracker, sensor layer, and rift
driver have diverged and are tightly coupled**:

- RiftLinux 0.1.5's `t_constellation_tracker` is a large rewrite (~8.8k lines vs
  ~1.5k) and ships a new Touch EKF (`t_touch_ekf.hpp`) and app-pose header.
- The driver/tracker APIs are incompatible **both ways** — e.g. the gadLinux
  driver calls `t_constellation_tracker_correct_camera_pose()` /
  `…_get_camera_pose()` (absent in RiftLinux 0.1.5), while RiftLinux's tracker
  requires `set_device_worn`, `get_tracked_pose`, `cameras_placed`,
  `imu_calibration` (never called by the gadLinux driver).

So you can't graft three folders onto the other fork's driver — to get
RiftLinux 0.1.5's "better Touch tracking with no calibration" you build the whole
RiftLinux rift stack (driver + radio + sensor + constellation). That's what this
profile does.

## Requirements

- A working [Envision](https://gitlab.com/gabmus/envision) install.
- An Oculus Rift CV1 + its sensors + Touch controllers.
- Standard Monado build dependencies (Envision's dependency check covers these;
  `envision -c <profile-uuid>` prints anything missing).

## What the profile is

| Field            | Value                                             |
|------------------|---------------------------------------------------|
| XR service       | Monado                                             |
| Source repo      | `https://github.com/AIIX/RiftLinux.git`           |
| Branch / tag     | `v0.1.5` (pinned; auto-pull off)                  |
| OpenVR runtime   | Xrizer (`https://github.com/Supreeeme/xrizer`, `main`) |
| Environment      | minimal/stock (see below)                          |

RiftLinux is designed to work with **zero `RIFT_*` configuration**, so the
profile keeps a minimal environment:

```
LD_LIBRARY_PATH = <prefix>/lib:<prefix>/lib64   # set automatically per profile
U_PACING_COMP_PRESENT_TO_DISPLAY_OFFSET_MS = 12  # display pacing (tune to taste)
ORT_DISABLE_TELEMETRY = 1
```

See [`example-profile.json`](example-profile.json) for the full profile block.

## Setup

### Option 1 — Envision GUI (recommended)

1. Open Envision, enable **development profiles**, add a new **Monado** profile.
2. Set:
   - **XR service repo**: `https://github.com/AIIX/RiftLinux.git`
   - **Branch**: `v0.1.5`
   - **OpenVR compositor**: Xrizer
3. Select the profile → **Build profile** → **Start**.

### Option 2 — helper script

[`add-profile.py`](add-profile.py) appends the profile to
`~/.config/envision/envision.json` with a fresh UUID and correct per-machine
paths. **Close Envision first**, then:

```bash
python3 add-profile.py
```

It backs up `envision.json` before writing and is idempotent (won't add a
duplicate). Re-open Envision, select **CV1 Fusion (RiftLinux 0.1.5)**, Build, Start.

> To follow future RiftLinux releases instead of staying on 0.1.5, change the
> profile's branch to `main` and turn **pull on build** on.

## Credits

- **RiftLinux** — Aditya Mehra (AIIX) · <https://github.com/AIIX/RiftLinux>
- **Envision** — gabmus / Linux VR Adventures · <https://gitlab.com/gabmus/envision>
- **Monado** — Collabora and contributors · <https://monado.freedesktop.org/>
- **Xrizer** — Supreeeme · <https://github.com/Supreeeme/xrizer>
