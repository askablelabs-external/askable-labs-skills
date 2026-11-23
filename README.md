# Askable Labs skills

Skills for engineers who author agentic coding tasks with Askable Labs. They work in Claude Code and Codex.

| Plugin | Skill | What it does |
|---|---|---|
| `agentic-coding` | `author-task` | Connects your agent to Askable, sets up your task workspace, and walks you through each step from idea to closed task. Before you submit, it checks your work against what reviewers look for. |

Your ideas, the wrong fix and the checks are yours. The skill teaches, asks questions and handles the mechanics. It does not write the task for you.

## Install

### Claude Code

```text
/plugin marketplace add askablelabs-external/askable-labs-skills
/plugin install agentic-coding@askable-labs
```

The plugin adds the `askable-labs` MCP server. Run `/mcp`, choose it, select **Authenticate**, then sign in with your Askable participant account. If you already added the server by hand, remove that copy (`claude mcp remove askable-labs`) so that only one is connected.

### Codex

```bash
codex plugin marketplace add askablelabs-external/askable-labs-skills
codex plugin add agentic-coding@askable-labs
codex mcp add askable-labs --url https://spark.platform.askable.com/mcp/participant
codex mcp login askable-labs
```

### Without the plugin

Copy `plugins/agentic-coding/skills/author-task/` into `~/.claude/skills/` (Claude Code) or `~/.agents/skills/` (Codex), and add the MCP server as shown in [setup](plugins/agentic-coding/skills/author-task/references/setup.md#connecting-to-askable).

## Use

```text
/agentic-coding:author-task
```

In Codex, use `$author-task`. You can also just say what you want, for example "I want to start a Frontier code task" or "my version came back too easy". The skill picks up your task wherever it stands.

## What you need

An Askable participant account that Askable has added to an agentic coding project, a GitHub account, Docker, `git`, Python 3, and Claude Code, Codex or OpenCode. The local difficulty test runs on your own model login, so it uses your API key or plan. [Setup](plugins/agentic-coding/skills/author-task/references/setup.md) has the details.

## Feedback

Askable maintains this repository and does not take outside pull requests or issues. For a question or a problem with the skill, ask in the Askable Labs Discord.

## Maintaining

Changes reach `main` through a pull request that passes `validate`. The repository is public, so keep it free of anything private: internal hostnames, links to internal tools, ticket numbers, names, emails, credentials, and reviewer internals beyond the published rubric. Limits, models and thresholds change, and the Askable MCP's `agentic_coding_docs` tool serves the current values, so do not copy them into a skill.

```bash
python3 -I scripts/validate.py
claude plugin validate . --strict
```

CI runs the first check. It also fails on any line that looks private.
