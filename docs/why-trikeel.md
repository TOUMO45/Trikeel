# Why Trikeel

This document explains the design choices. It makes arguments, not benchmark claims.

## 1. Three things change at three speeds

| Concern | Changes | Risk if mixed in |
|---|---|---|
| **Process** (how to work) | Rarely | Agent rewrites its own rules mid-task |
| **Project truth** (what to build) | Every slice | Stale context contradicts the code |
| **Secrets** (credentials) | Occasionally | Leaks through logs, prompts and commits |

Putting all three in one prompt means every edit risks the others. Separation of concerns is the oldest trick in software; Trikeel applies it to agent instructions.

## 2. Context is a budget

Every token the agent reads is paid for in cost, latency and attention. Two habits waste the most:

- **Re-explaining.** Pasting project background into chat "to remind" the agent.
- **Re-reading.** Loading everything when only one section matters.

Trikeel answers both: the Chart is addressed **by section**, and the Helm is read **once**. State that must survive a session lives in `STUDY.md → Current status`, not in conversation history.

## 3. A supervisor beats a clever prompt

A clever prompt asks for good behaviour. A supervisor **defines the loop** that produces it:

- fixed phases (Orient → Plan → Build → Verify → Review → Record),
- gates with pass/fail checks instead of opinions,
- stop rules that say when a human must decide,
- a 3-strikes rule that ends flailing.

The loop, not the wording, is what makes the result repeatable.

## 4. Bugs are cheapest where they are born

A gate fails in the phase that introduced the problem, while the diff is small. The same bug found after five dependent slices costs far more to untangle. Gates G1–G5 exist to move failure **earlier**.

## 5. One source of truth prevents drift

When chat and code disagree, agents tend to trust whatever they saw last. The Helm states the rule: **`STUDY.md` wins**. If the Study is wrong, the agent fixes the Study first and records why in the Decisions log. That log also stops the agent from re-opening choices that were already made.

## 6. Secrets are a different kind of data

Everything else in the context is instructions or knowledge. Secrets are capabilities. Keeping their **values** out of the context removes a whole class of accidents: a pasted log, a screenshot, a commit that "just worked locally".

## Trade-offs

- **Upfront effort.** Writing a good `STUDY.md` takes time. That time is the point: it is the thinking the agent would otherwise guess at.
- **Discipline required.** The pattern works only if the Study is kept current. The Helm makes that a gate item (P5 Record).
- **Not a security boundary.** See [`security.md`](security.md).
