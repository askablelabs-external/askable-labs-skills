#!/usr/bin/env python3
"""Check catalog parity, skill metadata and links, and that nothing private is published."""

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

# This repository is public. Anything that names private systems, people's machines or credentials fails CI.
PRIVATE = {
    "private GitHub org": r"\baskableorg/",
    "internal hostname": r"platform-dev\.|spark\.private|\.internal\b|\blocalhost:\d",
    "internal workspace link": r"notion\.(so|com)|slack\.com|linear\.app|datadoghq|app\.inngest",
    "internal service name": r"\blabs-spark\b|\bpython-events-service\b|\bagentic-coding-task-verifier\b|\bturbopuffer\b",
    "ticket reference": r"\b(LAB|ENG|AIR|FND|PPT)-\d+\b",
    "personal path": r"/Users/|/home/[a-z]",
    "email address": r"[\w.+-]+@[\w-]+\.[a-z]{2,}",
    "credential": r"sk-ant-|\bghp_|github_pat_|\bAKIA[0-9A-Z]{16}\b|\bxox[abp]-|-----BEGIN",
}
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".toml", ".txt", ""}


def load(relative):
    return json.loads((ROOT / relative).read_text())


def check_catalogs():
    claude = load(".claude-plugin/marketplace.json")
    codex = load(".agents/plugins/marketplace.json")
    assert claude["name"] == codex["name"], "marketplace names differ"
    codex_entries = {p["name"]: p for p in codex["plugins"]}
    assert set(codex_entries) == {p["name"] for p in claude["plugins"]}, "plugin sets differ"
    plugins = []
    for entry in claude["plugins"]:
        peer = codex_entries[entry["name"]]
        assert entry["source"] == peer["source"]["path"], "hosts resolve different plugin folders"
        plugin = (ROOT / entry["source"]).resolve()
        assert plugin.is_relative_to(ROOT)
        a = json.loads((plugin / ".claude-plugin/plugin.json").read_text())
        b = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
        for key in ("name", "version", "description"):
            assert a[key] == b[key], f"plugin {key} differs across hosts"
        assert a["name"] == entry["name"] and a["version"] == entry["version"]
        assert re.fullmatch(r"\d+\.\d+\.\d+", a["version"])
        assert b["skills"] == "./skills/"
        plugins.append(plugin)
    return plugins


def check_skills(plugin):
    count = 0
    for skill in sorted(p for p in (plugin / "skills").iterdir() if p.is_dir()):
        text = (skill / "SKILL.md").read_text()
        assert text.startswith("---\n"), f"{skill}: no frontmatter"
        frontmatter = text.split("---", 2)[1]
        name = re.search(r"^name: (.+)$", frontmatter, re.M).group(1)
        assert name == skill.name and re.fullmatch(r"[a-z0-9-]{1,64}", name), f"{skill}: bad name"
        description = re.search(r"^description: (.+)$", frontmatter, re.M).group(1)
        assert 10 < len(description) < 1024, f"{skill}: description length"
        assert "$" + name in (skill / "agents/openai.yaml").read_text(), f"{skill}: openai.yaml prompt"
        for file in skill.rglob("*.md"):
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", file.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                destination = (file.parent / target.split("#")[0]).resolve()
                assert destination.is_relative_to(plugin / "skills"), f"{file}: link escapes the skills: {target}"
                assert destination.exists(), f"{file}: broken link: {target}"
        count += 1
    return count


def private_findings():
    for file in sorted(ROOT.rglob("*")):
        if not file.is_file() or ".git" in file.parts or file.resolve() == SELF:
            continue
        if file.suffix not in TEXT_SUFFIXES:
            continue
        for number, line in enumerate(file.read_text(errors="replace").splitlines(), 1):
            for label, pattern in PRIVATE.items():
                if re.search(pattern, line):
                    yield f"{file.relative_to(ROOT)}:{number}: {label}: {line.strip()[:120]}"


def main():
    skills = sum(check_skills(plugin) for plugin in check_catalogs())
    findings = list(private_findings())
    for finding in findings:
        print(finding, file=sys.stderr)
    if findings:
        sys.exit(f"{len(findings)} line(s) may expose private information.")
    print(f"Validated both catalogs, {skills} skill(s), and found nothing private.")


if __name__ == "__main__":
    main()
