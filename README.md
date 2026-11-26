# CV1 Fusion (RiftLinux) — Envision profile

An [Envision](https://gitlab.com/gabmus/envision) profile that runs the **Oculus
Rift CV1** with the tracking stack from **[RiftLinux](https://github.com/AIIX/RiftLinux)**
(a Monado fork), driving SteamVR/OpenVR titles through
[Xrizer](https://github.com/Supreeeme/xrizer).

This repo is just the **profile + setup notes** — there is no patched source here.
The profile builds RiftLinux verbatim from a pinned upstream release tag. Current
tag: **`v0.1.6`**; any release tag works the same way (see [Versions](#versions)).

> Personal setup, not affiliated with or endorsed by the RiftLinux, Envision,
> Monado, or Xrizer projects.

## Why the whole RiftLinux stack, not a few files

RiftLinux and the gadLinux `cv1-fusion` Monado fork both descend from the same
Rift CV1 lineage, but their **constellation tracker, sensor layer, and rift
driver have diverged and are tightly coupled**:

- RiftLinux's `t_constellation_tracker` is a large rewrite (~8.8k lines vs ~1.5k)
  and ships a new Touch EKF (`t_touch_ekf.hpp`) and app-pose header.
- The driver/tracker APIs are incompatible **both ways** — e.g. the gadLinux
  driver calls `t_constellation_tracker_correct_camera_pose()` /
  `…_get_camera_pose()` (absent in RiftLinux), while RiftLinux's tracker
  requires `set_device_worn`, `get_tracked_pose`, `cameras_placed`,
  `imu_calibration` (never called by the gadLinux driver).

So you can't graft three folders onto the other fork's driver — to get
RiftLinux's "better Touch tracking with no calibration" you build the whole
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
| Branch / tag     | a release tag, pinned, auto-pull off (e.g. `v0.1.6`) |
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
   - **Branch**: the release tag, e.g. `v0.1.6`
   - **OpenVR compositor**: Xrizer
3. Select the profile → **Build profile** → **Start**.

### Option 2 — helper script

[`add-profile.py`](add-profile.py) appends the profile to
`~/.config/envision/envision.json` with a fresh UUID and correct per-machine
paths. **Close Envision first**, then:

```bash
python3 add-profile.py            # latest documented tag (v0.1.6)
python3 add-profile.py v0.1.5     # or pin any RiftLinux release tag
```

It backs up `envision.json` before writing and is idempotent per version (won't
add a duplicate of the same tag). Re-open Envision, select **CV1 Fusion
(RiftLinux &lt;tag&gt;)**, Build, Start.

> To follow future RiftLinux releases instead of pinning a tag, set the profile's
> branch to `main` and turn **pull on build** on.

## Versions

Each release of RiftLinux is a tag (`v0.1.0` … `v0.1.6`). Pin the one you want;
this profile has been used with:

- **v0.1.6** — panel uniformity from the headset's factory calibration, steadier
  text when supersampling, headset fully off at quit, safety hardening.
- **v0.1.5** — better Touch controller tracking with no calibration, SteamVR Home
  with the newest Steam client, Rift Home support.

> Tip (multi-sensor USB): give **each** Rift sensor its own USB controller. Two
> CV1 sensors on one controller can exhaust isochronous bandwidth
> (`uvc_fs_stream_start … errno 11`), so the cameras never stream and tracking
> never locks. Check with `lsusb -t` — the three `2833:0211` sensors should sit
> on three different `Bus` numbers.

## Credits

- **RiftLinux** — Aditya Mehra (AIIX) · <https://github.com/AIIX/RiftLinux>
- **Envision** — gabmus / Linux VR Adventures · <https://gitlab.com/gabmus/envision>
- **Monado** — Collabora and contributors · <https://monado.freedesktop.org/>
- **Xrizer** — Supreeeme · <https://github.com/Supreeeme/xrizer>
