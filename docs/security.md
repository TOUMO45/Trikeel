# Security notes: the Vault

Trikeel's Vault rule reduces accidental exposure of secrets. It is **not** a security boundary. This page states what it covers and what it does not.

## Threats the pattern helps with

| Threat | How Trikeel helps |
|---|---|
| Secret pasted into chat or a prompt | Agents are instructed to use names only |
| Secret echoed in logs or tool output | Supervisor forbids printing values; G4 inspects the diff |
| Secret committed to git | `.env` is git-ignored; `trikeel_check.py` flags tracked `.env` and key-shaped strings |
| Drift between code and config | Env contract in `STUDY.md` must match `.env.example` |

## What it does NOT do

- **It cannot stop a malicious or prompt-injected agent.** An instruction in a web page or file can ask an agent to read `.env`. A text rule is not an access control.
- **It does not encrypt anything.** `.env` is plaintext on disk.
- **The checker is heuristic.** It catches common key shapes (a few vendors, private-key blocks, long hex strings). It will miss custom formats. Run a dedicated scanner (for example gitleaks or trufflehog) in CI as well.
- **It does not cover runtime exposure**: the agent running code that itself prints a secret.

## Recommended hardening

1. Use a **secret manager** for anything beyond local development.
2. Give the agent **least-privilege, short-lived, dev-only** credentials. Never production keys.
3. Keep `.env` outside any directory the agent can freely read, or deny read access to it in your tool's permission settings where supported.
4. Add secret scanning to CI and a pre-commit hook.
5. Treat any secret that touched a prompt, log or commit as **compromised** and rotate it.

## If a secret leaks

1. Revoke or rotate it at the provider **first**.
2. Then clean history if needed. Rewriting git history does not un-leak a secret.
3. Record the incident in `STUDY.md → Decisions log`.

## Reporting a vulnerability in this repo

Open a private security advisory on GitHub, or an issue without sensitive details.
