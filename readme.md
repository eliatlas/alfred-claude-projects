# Alfred Claude & Codex Projects

Alfred workflow for quickly jumping into recent Claude Code and Codex projects.

Type `clp` to see a fuzzy-searchable list of your recent Claude Code projects, sorted by last used. Hit Enter to open iTerm in that directory and automatically start `claude`.

Type `cxp` for the same experience with projects from your recent Codex sessions. Hit Enter to open the selected workspace in the Codex desktop app.

## Install

1. Download `ClaudeProjects.alfredworkflow`
2. Double-click to install in Alfred

## Usage

- `clp` — list all recent Claude Code projects
- `clp <query>` — fuzzy filter by project name or path (matches any path segment)
- `cxp` — list all recent Codex projects
- `cxp <query>` — fuzzy filter Codex projects by name or path
- `Enter` — open the selected project in Claude or Codex, according to the keyword
- `Cmd+Enter` — reveal the selected project in Finder
- `Alt+Enter` — copy the selected project path

## How it works

Zero configuration. The workflow reads `~/.claude/projects/` and `~/.codex/sessions/`, extracts the real working directory from session JSONL files, and keeps the two project lists separate. There is no manual project list to maintain.

Projects are sorted by the last modification time of their session data.

## Requirements

- [Alfred](https://www.alfredapp.com/) with Powerpack
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (for the project data)
- [Codex CLI](https://developers.openai.com/codex/cli/) and the Codex desktop app
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
