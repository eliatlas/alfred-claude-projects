#!/usr/bin/env python3
"""Alfred Script Filter: list recent Claude Code projects sorted by last use."""

import os
import json
import glob
import sys
from datetime import datetime

PROJECTS_DIR = os.path.expanduser("~/.claude/projects")
MAX_RESULTS = 30

# Icon paths - use folder icon from system
ICON = {"type": "fileicon", "path": "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/GenericFolderIcon.icns"}

def get_projects():
    results = []
    for entry in os.scandir(PROJECTS_DIR):
        if not entry.is_dir():
            continue
        jsonls = glob.glob(os.path.join(entry.path, "*.jsonl"))
        if not jsonls:
            continue
        newest = max(jsonls, key=os.path.getmtime)
        cwd = None
        with open(newest, "r") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    if "cwd" in obj:
                        cwd = obj["cwd"]
                        break
                except Exception:
                    continue
        if cwd and os.path.isdir(cwd):
            mtime = entry.stat().st_mtime
            results.append((mtime, cwd))

    # Deduplicate by cwd, keep most recent
    seen = set()
    unique = []
    for mtime, cwd in sorted(results, key=lambda x: -x[0]):
        if cwd not in seen:
            seen.add(cwd)
            unique.append((mtime, cwd))

    return unique[:MAX_RESULTS]


def make_subtitle(mtime, cwd):
    dt = datetime.fromtimestamp(mtime)
    ago = datetime.now() - dt
    if ago.days == 0:
        time_str = "today"
    elif ago.days == 1:
        time_str = "yesterday"
    else:
        time_str = f"{ago.days}d ago"
    # Shorten home prefix
    display_path = cwd.replace(os.path.expanduser("~"), "~")
    return f"{time_str}  ·  {display_path}"


def main():
    projects = get_projects()

    items = []
    for mtime, cwd in projects:
        name = os.path.basename(cwd)
        subtitle = make_subtitle(mtime, cwd)
        # Match against name + full path (split by / so Alfred matches any segment)
        match_str = f"{name} {cwd.replace('/', ' ')}"

        items.append({
            "uid": cwd,
            "title": name,
            "subtitle": subtitle,
            "arg": cwd,
            "match": match_str,
            "autocomplete": name,
            "icon": {"type": "fileicon", "path": cwd},
            "mods": {
                "cmd": {
                    "subtitle": f"Reveal in Finder: {cwd}",
                    "arg": cwd,
                    "variables": {"action": "finder"}
                },
                "alt": {
                    "subtitle": f"Copy path: {cwd}",
                    "arg": cwd,
                    "variables": {"action": "copy"}
                }
            }
        })

    print(json.dumps({"items": items or [{
        "title": "No Claude Code projects found",
        "subtitle": "No session data in ~/.claude/projects/",
        "valid": False
    }]}))


if __name__ == "__main__":
    main()
