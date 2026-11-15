# STUDY — the Chart

> The single source of truth for **WHAT** we are building and **WHY**.
> The Supervisor (`SUPERVISOR.md`) decides HOW to work. Secrets live in `.env`, never here.
> Keep this file tight: every sentence should change a decision. Delete what stops being true.

---

## Mission
<!-- One or two sentences. Who is this for, and what changes for them? -->

## Problem
<!-- The real pain. Who feels it, how often, what does it cost? -->

## Users & jobs-to-be-done
<!-- Primary user, their situation, the outcome they want. -->

## Goals
<!-- 3–5 measurable outcomes. Prefer numbers or observable behaviours. -->
-

## Non-goals
<!-- What we are deliberately NOT doing. This protects scope and tokens. -->
-

## Anti-goals
<!-- What would make this a failure even if it technically works? -->
-

## Success criteria
<!-- How will we know it works? Each item should be checkable. -->
- [ ]

## Architecture
<!-- Components, data flow, trust boundaries. A small diagram or list is enough. -->

```
[Client] → [API] → [Service] → [Datastore]
```

## Data model
<!-- Key entities and relationships. -->

## Interfaces
<!-- APIs, CLI commands, events. Method · path/name · input · output · errors. -->

## Security notes
<!-- Auth model, roles, sensitive operations, abuse cases worth testing. -->

## Env contract (names only — never values)
<!-- Every variable the project needs. Values live in `.env`; mirror names in `.env.example`. -->

| Name | Purpose | Required | Where used |
|---|---|---|---|
| `APP_ENV` | Runtime environment name | yes | app bootstrap |
| `APP_PORT` | Port the app listens on | no | server start |
| `DATABASE_URL` | Primary datastore connection | yes | data layer |
| `EXAMPLE_API_KEY` | Third-party API access | yes | `src/client.ts` |
| `EXAMPLE_WEBHOOK_SECRET` | Verifies inbound webhooks | yes | webhook handler |

## Decisions log
<!-- Newest first. date · decision · why · alternatives rejected -->

| Date | Decision | Why | Rejected alternatives |
|---|---|---|---|
| YYYY-MM-DD |  |  |  |

## Risks
<!-- What could fail, and the mitigation. -->
-

## Open questions
<!-- Things only the human can answer. The Supervisor stops and asks on these. -->
-

## Current status
<!-- 3–6 lines. Last completed slice · current slice · next · blockers. -->
-

## Glossary
<!-- Project terms the agent must use consistently. -->
-
