#!/usr/bin/env python3
"""Alfred Script Filter: list recent Claude Code or Codex projects."""

import os
import json
import glob
import sys
from datetime import datetime

CLAUDE_PROJECTS_DIR = os.path.expanduser("~/.claude/projects")
CODEX_SESSIONS_DIR = os.path.expanduser("~/.codex/sessions")
MAX_RESULTS = 30

# Icon paths - use folder icon from system
ICON = {"type": "fileicon", "path": "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/GenericFolderIcon.icns"}

def read_cwd(session_path):
    """Extract a working directory from either provider's JSONL format."""
    try:
        with open(session_path, "r", encoding="utf-8", errors="replace") as session:
            for line in session:
                try:
                    obj = json.loads(line)
                except (TypeError, ValueError):
                    continue

                cwd = obj.get("cwd")
                if not cwd and obj.get("type") == "session_meta":
                    cwd = obj.get("payload", {}).get("cwd")
                if cwd:
                    return cwd
    except OSError:
        pass
    return None


def recent_projects(session_paths):
    """Deduplicate projects by cwd, keeping the latest session timestamp."""
    sessions = []
    for session_path in session_paths:
        try:
            sessions.append((os.path.getmtime(session_path), session_path))
        except OSError:
            continue

    seen = set()
    unique = []
    for mtime, session_path in sorted(sessions, reverse=True):
        cwd = read_cwd(session_path)
        if cwd and cwd not in seen and os.path.isdir(cwd):
            seen.add(cwd)
            unique.append((mtime, cwd))
            if len(unique) == MAX_RESULTS:
                break

    return unique


def get_projects(source):
    if source == "codex":
        session_paths = glob.glob(
            os.path.join(CODEX_SESSIONS_DIR, "**", "*.jsonl"), recursive=True
        )
    else:
        session_paths = glob.glob(
            os.path.join(CLAUDE_PROJECTS_DIR, "*", "*.jsonl")
        )

    return recent_projects(session_paths)


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
    source = "codex" if len(sys.argv) > 1 and sys.argv[1] == "codex" else "claude"
    projects = get_projects(source)
    provider_name = "Codex" if source == "codex" else "Claude Code"
    sessions_dir = CODEX_SESSIONS_DIR if source == "codex" else CLAUDE_PROJECTS_DIR

    items = []
    for mtime, cwd in projects:
        name = os.path.basename(cwd)
        subtitle = make_subtitle(mtime, cwd)
        # Match against name + full path (split by / so Alfred matches any segment)
        match_str = f"{name} {cwd.replace('/', ' ')}"

        items.append({
            "uid": f"{source}:{cwd}",
            "title": name,
            "subtitle": subtitle,
            "arg": cwd,
            "match": match_str,
            "autocomplete": name,
            "icon": {"type": "fileicon", "path": cwd},
            "variables": {"action": source},
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
        "title": f"No {provider_name} projects found",
        "subtitle": f"No session data in {sessions_dir.replace(os.path.expanduser('~'), '~')}/",
        "valid": False
    }]}))


if __name__ == "__main__":
    main()
