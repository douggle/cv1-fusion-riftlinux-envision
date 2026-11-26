#!/usr/bin/env python3
"""Add a 'CV1 Fusion (RiftLinux <tag>)' profile to Envision's config.

Appends a Monado profile that builds a pinned RiftLinux release tag with Xrizer
to ~/.config/envision/envision.json. Close Envision before running. Backs up the
config first and is idempotent per tag (won't add a duplicate of the same tag).

Usage:
    python3 add-profile.py            # default tag v0.1.6
    python3 add-profile.py v0.1.5     # or any RiftLinux release tag
"""
import json, os, re, sys, uuid, shutil, datetime

DEFAULT_TAG = "v0.1.6"
CFG = os.path.expanduser("~/.config/envision/envision.json")
SHARE = os.path.expanduser("~/.local/share/envision")


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TAG
    if not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        sys.exit(f"Tag should look like v0.1.6, got: {tag!r}")
    name = f"CV1 Fusion (RiftLinux {tag.lstrip('v')})"
    if not os.path.exists(CFG):
        sys.exit(f"Envision config not found at {CFG} — is Envision installed and run at least once?")

    with open(CFG) as f:
        cfg = json.load(f)

    cfg.setdefault("user_profiles", [])
    for p in cfg["user_profiles"]:
        if p.get("name") == name:
            sys.exit(f"Profile already exists: {p['uuid']} ({name})")

    # back up first
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = f"{CFG}.bak-{stamp}"
    shutil.copy2(CFG, backup)

    u = str(uuid.uuid4())
    base = os.path.join(SHARE, u)
    prefix = os.path.join(SHARE, "prefixes", u)

    profile = {
        "uuid": u,
        "name": name,
        "xrservice_type": "Monado",
        "xrservice_path": os.path.join(base, "xrservice"),
        "xrservice_repo": "https://github.com/AIIX/RiftLinux.git",
        "xrservice_branch": tag,
        "xrservice_cmake_flags": {},
        "opencomposite_path": "",
        "opencomposite_repo": None,
        "opencomposite_branch": None,
        "ovr_comp": {
            "mod_type": "Xrizer",
            "repo": "https://github.com/Supreeeme/xrizer",
            "branch": "main",
            "path": os.path.join(base, "xrizer"),
        },
        "features": {
            "libsurvive": {"feature_type": "Libsurvive", "enabled": False, "path": None, "repo": None, "branch": None},
            "basalt":     {"feature_type": "Basalt",     "enabled": False, "path": None, "repo": None, "branch": None},
            "openhmd":    {"feature_type": "OpenHmd",    "enabled": False, "path": None, "repo": None, "branch": None},
            "mercury_enabled": False,
        },
        # RiftLinux works with zero RIFT_* config; keep the environment minimal.
        "environment": {
            "LD_LIBRARY_PATH": f"{prefix}/lib:{prefix}/lib64",
            "U_PACING_COMP_PRESENT_TO_DISPLAY_OFFSET_MS": "12",
            "ORT_DISABLE_TELEMETRY": "1",
        },
        "prefix": prefix,
        "is_system_profile": False,
        "editable": True,
        "pull_on_build": False,   # pinned to the chosen tag
        "lighthouse_driver": "Vive",
        "xrservice_launch_options": "",
        "skip_dependency_check": False,
    }

    cfg["user_profiles"].append(profile)
    with open(CFG, "w") as f:
        json.dump(cfg, f, indent=2)

    print(f"Backed up config to: {backup}")
    print(f"Added profile '{name}'  uuid={u}")
    print("Open Envision, select it, Build profile, then Start.")


if __name__ == "__main__":
    main()
