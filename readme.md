# alfred-claude-projects

Alfred workflow for quickly jumping into recent Claude Code projects.

Type `clp` to see a fuzzy-searchable list of your recent Claude Code projects, sorted by last used. Hit Enter to open iTerm in that directory and automatically start `claude`.

## Install

1. Download `ClaudeProjects.alfredworkflow`
2. Double-click to install in Alfred

## Usage

- `clp` — list all recent Claude Code projects
- `clp <query>` — fuzzy filter by project name or path (matches any path segment)
- `Enter` — open iTerm in the selected directory and run `claude`

## How it works

Zero configuration. The workflow reads `~/.claude/projects/` (auto-maintained by Claude Code) and extracts the real working directory from session JSONL files — no manual project list to maintain.

Projects are sorted by last modification time of their Claude Code session data.

## Requirements

- [Alfred](https://www.alfredapp.com/) with Powerpack
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (for the project data)
- [iTerm2](https://iterm2.com/)
- Python 3 (uses `/usr/bin/python3`)

## Development

The source files:

- `info.plist` — Alfred workflow definition
- `claude_projects.py` — Script Filter that extracts recent projects

To rebuild the `.alfredworkflow` bundle:

```bash
zip -j ClaudeProjects.alfredworkflow info.plist claude_projects.py
```
