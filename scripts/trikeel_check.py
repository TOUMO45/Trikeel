#!/usr/bin/env python3
"""trikeel-check: validate a Trikeel project (Supervisor + Study + Vault).

Checks (stdlib only, no network):
  1. The three parts exist: SUPERVISOR.md, STUDY.md, .env.example
  2. .gitignore ignores `.env`, and `.env` is not tracked by git
  3. Env contract in STUDY.md matches the names in .env.example
  4. No secret-looking values inside SUPERVISOR.md / STUDY.md / .env.example
  5. Prints an approximate token footprint per file (heuristic: chars / 4)

Usage:
  python3 scripts/trikeel_check.py [PROJECT_DIR] [--strict]

Exit code: 0 = pass, 1 = failures (or warnings with --strict).
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REQUIRED = ["SUPERVISOR.md", "STUDY.md", ".env.example"]

# Conservative patterns for credential-looking strings.
SECRET_PATTERNS = {
    "OpenAI/Anthropic-style key": re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "AWS access key id": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    "Slack token": re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b"),
    "Private key block": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "Long hex secret": re.compile(r"\b[a-f0-9]{40,}\b"),
}

PLACEHOLDERS = {"replace-me", "changeme", "your-key-here", "placeholder", "password", "user"}


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.warnings: list[str] = []

    def fail(self, msg: str) -> None:
        self.failures.append(msg)
        print(f"  FAIL  {msg}")

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)
        print(f"  WARN  {msg}")

    def ok(self, msg: str) -> None:
        print(f"  ok    {msg}")


def env_names(path: Path) -> set[str]:
    names: set[str] = set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        names.add(line.split("=", 1)[0].strip())
    return names


def study_contract_names(path: Path) -> set[str]:
    """Names listed in the `## Env contract` table (first backticked UPPER_CASE cell)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^##\s+Env contract.*?$(.*?)(?=^##\s|\Z)", text, re.S | re.M)
    if not m:
        return set()
    names: set[str] = set()
    for row in m.group(1).splitlines():
        cell = re.match(r"\|\s*`([A-Z][A-Z0-9_]*)`\s*\|", row)
        if cell:
            names.add(cell.group(1))
    return names


def git(args: list[str], cwd: Path) -> tuple[int, str]:
    try:
        p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
        return p.returncode, p.stdout.strip()
    except FileNotFoundError:
        return 127, ""


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a Trikeel project.")
    ap.add_argument("project_dir", nargs="?", default=".")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = ap.parse_args()

    root = Path(args.project_dir).resolve()
    r = Report()
    print(f"Trikeel check: {root}\n")

    # 1. Required parts
    print("[1] Three parts present")
    for name in REQUIRED:
        if (root / name).is_file():
            r.ok(name)
        else:
            r.fail(f"missing {name}")

    # 2. Vault hygiene
    print("\n[2] Vault hygiene")
    gi = root / ".gitignore"
    if gi.is_file():
        lines = [l.strip() for l in gi.read_text(errors="replace").splitlines()]
        if any(l in (".env", "/.env", ".env*", "*.env") for l in lines):
            r.ok(".gitignore ignores .env")
        else:
            r.fail(".gitignore does not ignore .env")
    else:
        r.fail("no .gitignore (the Vault must be ignored)")
    code, out = git(["ls-files", "--error-unmatch", ".env"], root)
    if code == 0:
        r.fail(".env is TRACKED by git: remove it with `git rm --cached .env` and rotate its secrets")
    elif code == 127:
        r.warn("git not available; could not check whether .env is tracked")
    else:
        r.ok(".env is not tracked")

    # 3. Env contract
    print("\n[3] Env contract <-> .env.example")
    study, example = root / "STUDY.md", root / ".env.example"
    if study.is_file() and example.is_file():
        a, b = study_contract_names(study), env_names(example)
        if not a:
            r.warn("STUDY.md has no parseable `## Env contract` table")
        else:
            for n in sorted(b - a):
                r.warn(f"{n} is in .env.example but not in STUDY.md Env contract")
            for n in sorted(a - b):
                r.warn(f"{n} is in STUDY.md Env contract but not in .env.example")
            if a == b:
                r.ok(f"{len(a)} variable names match")

    # 4. Secret scan
    print("\n[4] Secret scan (Supervisor, Study, example)")
    for name in REQUIRED:
        p = root / name
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        hit = False
        for label, pat in SECRET_PATTERNS.items():
            if pat.search(text):
                r.fail(f"{name}: looks like a {label}")
                hit = True
        if name == ".env.example":
            for line in text.splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, v = (s.strip() for s in line.split("=", 1))
                    if re.search(r"(KEY|SECRET|TOKEN|PASSWORD)", k) and v and v.lower() not in PLACEHOLDERS \
                            and not v.startswith(("<", "${")):
                        r.warn(f".env.example: {k} has a non-placeholder value (use `replace-me`)")
        if not hit:
            r.ok(f"{name}: clean")

    # 5. Token footprint
    print("\n[5] Approx. token footprint (chars / 4)")
    total = 0
    for name in ("SUPERVISOR.md", "STUDY.md"):
        p = root / name
        if p.is_file():
            t = len(p.read_text(encoding="utf-8", errors="replace")) // 4
            total += t
            flag = "  <- consider trimming" if t > 4000 else ""
            print(f"        {name:<14} ~{t:>5} tokens{flag}")
    print(f"        {'total':<14} ~{total:>5} tokens (loaded once per session)")

    print()
    bad = len(r.failures) + (len(r.warnings) if args.strict else 0)
    print(f"Result: {len(r.failures)} failure(s), {len(r.warnings)} warning(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
