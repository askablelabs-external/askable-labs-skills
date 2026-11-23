# Setup

## Prerequisites

- An Askable participant account that Askable has added to an agentic coding project.
- A GitHub account to work from.
- Docker, running. Every local check builds the task's image.
- `git` and Python 3.
- A Claude Code, Codex or OpenCode agent. Only these can upload the authoring session.

The task repository's `./setup.sh` installs the rest. Read its output: it names anything still missing.

## Connecting to Askable

The plugin registers the `askable-labs` MCP server at `https://spark.platform.askable.com/mcp/participant`. Without the plugin, add it by hand:

```bash
# Claude Code
claude mcp add --transport http askable-labs https://spark.platform.askable.com/mcp/participant

# Codex
codex mcp add askable-labs --url https://spark.platform.askable.com/mcp/participant
codex mcp login askable-labs
```

In Claude Code, run `/mcp`, choose the server and select Authenticate. Sign in with **Continue with Askable**, using the email you use on Askable as a participant. There is no API key to copy. Use the connection at least once every 30 days, or sign in again.

When sign-in ends on an Askable page instead of returning to the agent:

- "This connection is for Askable participants": you signed in with a researcher login. Sign in with your participant account.
- "Your Askable account is not part of an agentic coding project yet": Askable has not added you to a project. Contact the Askable team.
- "Your Askable account cannot use this connection": your access has been withdrawn.
- Sign-in failed or expired: start again from `/mcp`, and finish in the browser you started from.

A tool missing from the server means your status does not allow it, not that the feature is absent. `participant_whoami` says your status.

## The repository

1. Link GitHub with `agentic_coding_link_github` before submitting an idea that names an upstream.
2. When the idea is accepted, accept the repository invitation on GitHub.
3. Call `agentic_coding_get_workspace_setup` and run its steps yourself: clone, fetch the grader, run `./setup.sh`, and write any secrets the template's tooling needs into the git-ignored `.env`.
4. Read the repository's `AGENTS.md` before building. It owns the layout, the rules and `./check.sh`.

The grader (`task/tests/etask_grade.py`) is never committed. Fetch it again whenever `agentic_coding_get_grader` reports a sha256 different from your copy's.

## The authoring session

The uploader captures the agent session it runs in, and a version passes only once its session is captured. So:

- **One session per version.** Start the agent from the repository root, build the version there, and submit and upload from that same session. Resume it (`claude --continue`, `codex resume`) instead of starting a new one. A session started elsewhere, or a second session that took over halfway, cannot be uploaded, and Askable staff then decide the version by hand.
- **Keep it lean.** The session has a size cap (the `submit` topic states it). Read build and test logs with a tail or a search, never whole. Never paste large files, datasets or binary output into it.
- **Sandbox network.** The uploader PUTs to an S3 host in the links it is given. Allow that host if your agent sandboxes network access.

## Offline tasks

Most tasks run offline: no internet while the model works or while the tests run. Everything the task needs is fetched in the Dockerfile, which still builds online, or committed. Nothing the solution, the tests or the program under test runs may download anything. Read `agentic_coding_docs` topic `network` before writing the Dockerfile.
