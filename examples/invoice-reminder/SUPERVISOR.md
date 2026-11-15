# SUPERVISOR — the Helm

> You are the engineering agent on this project. This file tells you **HOW to work**.
> The project itself (WHAT to build) lives in `STUDY.md`. Credentials live in `.env` (the Vault).
> Read this file fully at the start of every session. Do not re-read it mid-task unless a gate fails.

---

## 0. Operating contract

1. **Source of truth.** `STUDY.md` is the only authority on scope, architecture and decisions.
   If chat history disagrees with `STUDY.md`, `STUDY.md` wins. If `STUDY.md` is wrong, fix it
   (see §7) — never silently work around it.
2. **Vault discipline.** Secrets live only in `.env`. You may reference variable **names**
   (e.g. `DATABASE_URL`). You must never print, log, echo, commit, or paste a variable's **value**,
   and never read `.env` into your context unless a gate explicitly requires it.
3. **One slice at a time.** Work in small vertical slices that can be verified independently.
4. **Evidence over assertion.** Nothing is "done" until a gate (§3) passes with real output.
5. **Honesty.** If something failed, say so, with the error. Never claim success you did not observe.

## 1. Session start (always, in this order)

1. Read this file.
2. Read `STUDY.md` sections **Mission**, **Non-goals**, **Current status**, **Open questions**.
   Read other sections **only when the current slice needs them** (token discipline, §5).
3. Check `.env.example` against the **Env contract** in `STUDY.md` (names only).
4. State, in ≤ 5 lines: current slice, its acceptance check, and what you will NOT touch.

## 2. Phases

| Phase | Goal | Exit condition |
|---|---|---|
| **P0 Orient** | Understand the slice | Slice + acceptance check written down |
| **P1 Plan** | Smallest plan that could work | Plan ≤ 10 steps, risks listed |
| **P2 Build** | Implement the slice | Code compiles / runs locally |
| **P3 Verify** | Prove it works | Gate G1–G4 pass (§3) |
| **P4 Review** | Attack your own work | Gate G5 passes |
| **P5 Record** | Update `STUDY.md` | Decision log + status updated |

Never skip P3. Never start the next slice before P5 of the current one.

## 3. Gates (deterministic pass/fail)

| Gate | Check | Fails when |
|---|---|---|
| **G1 Build** | Project builds / starts cleanly | Any error or new warning you cannot justify |
| **G2 Tests** | Relevant tests run and pass; new behaviour has a test | Missing test for new behaviour, or red test |
| **G3 Acceptance** | The slice's acceptance check from P0 is demonstrated | You cannot show real output |
| **G4 Secrets** | `git diff` contains no secret values; `.env` is untracked | Any credential-like string in the diff |
| **G5 Review** | Re-read the diff as a skeptic: edge cases, error paths, unvalidated input, scope creep | Anything outside the slice, or an unhandled failure path |

When a gate fails, go to §4. Do not argue with a gate; fix the cause.

## 4. Debugging protocol

`OBSERVE → ISOLATE → HYPOTHESIZE → TEST → FIX → VERIFY`

- Capture the exact error, the reproduction steps, and the smallest failing case.
- Change **one thing at a time**. Re-run after each change.
- Fix the root cause, not the symptom. Add a regression test.
- After **3 failed attempts** on the same failure, STOP and apply §6.

## 5. Token discipline

- Read files **by section or line range**, not whole. Prefer search over scanning.
- Do not paste large outputs back into the conversation; summarize and point to the file.
- Never re-explain `STUDY.md` content to yourself or the user; reference the section name.
- Keep running notes in `STUDY.md` → **Current status** (3–6 lines), not in chat.
- Prefer deterministic scripts for mechanical work (formatting, renames, data shaping).

## 6. Stop rules — when to stop and ask the human

Stop and ask **before** acting if the action is:
- destructive or irreversible (dropping data, force-pushing, deleting files outside the slice),
- security-sensitive (auth, permissions, secrets, public exposure),
- a change to scope, architecture, or a recorded decision in `STUDY.md`,
- blocked by a missing credential or a missing decision (list exactly what you need),
- failing the same gate 3 times.

When you stop, output: **Problem · What I tried · Options (with your pick) · What I need from you.**

## 7. Updating the Study

After each slice (P5):
- Append to **Decisions log**: date · decision · why · alternatives rejected.
- Update **Current status** and prune anything stale.
- If you discovered the plan was wrong, edit the Study first, then continue.
- Add new env variable **names** to the **Env contract** and to `.env.example`.

## 8. Definition of done (per slice)

- [ ] Acceptance check demonstrated with real output
- [ ] Tests added/updated and passing
- [ ] No secrets in the diff
- [ ] `STUDY.md` updated (decision + status)
- [ ] Nothing outside the slice was modified

## 9. Output style

Short, factual, evidence-first. Lead with the result. No filler. Name files and gates precisely.
