#!/usr/bin/env python3
"""Add the 'CV1 Fusion (RiftLinux 0.1.5)' profile to Envision's config.

Appends a Monado profile that builds RiftLinux 0.1.5 (tag v0.1.5) with Xrizer to
~/.config/envision/envision.json. Close Envision before running. Backs up the
config first and is idempotent (won't add a duplicate by name).

Usage:
    python3 add-profile.py
"""
import json, os, sys, uuid, shutil, datetime

NAME = "CV1 Fusion (RiftLinux 0.1.5)"
CFG = os.path.expanduser("~/.config/envision/envision.json")
SHARE = os.path.expanduser("~/.local/share/envision")


def main():
    if not os.path.exists(CFG):
        sys.exit(f"Envision config not found at {CFG} — is Envision installed and run at least once?")

    with open(CFG) as f:
        cfg = json.load(f)

    cfg.setdefault("user_profiles", [])
    for p in cfg["user_profiles"]:
        if p.get("name") == NAME:
            sys.exit(f"Profile already exists: {p['uuid']} ({NAME})")

    # back up first
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = f"{CFG}.bak-{stamp}"
    shutil.copy2(CFG, backup)

    u = str(uuid.uuid4())
    base = os.path.join(SHARE, u)
    prefix = os.path.join(SHARE, "prefixes", u)

    profile = {
        "uuid": u,
        "name": NAME,
        "xrservice_type": "Monado",
        "xrservice_path": os.path.join(base, "xrservice"),
        "xrservice_repo": "https://github.com/AIIX/RiftLinux.git",
        "xrservice_branch": "v0.1.5",
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
        "pull_on_build": False,   # pinned to the v0.1.5 tag
        "lighthouse_driver": "Vive",
        "xrservice_launch_options": "",
        "skip_dependency_check": False,
    }

    cfg["user_profiles"].append(profile)
    with open(CFG, "w") as f:
        json.dump(cfg, f, indent=2)

    print(f"Backed up config to: {backup}")
    print(f"Added profile '{NAME}'  uuid={u}")
    print("Open Envision, select it, Build profile, then Start.")


if __name__ == "__main__":
    main()
