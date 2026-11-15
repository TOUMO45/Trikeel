# STUDY — Invoice Reminder Bot (worked example)

> A filled-in Chart showing the level of detail that works. `SUPERVISOR.md` here is identical to `template/SUPERVISOR.md`.

## Mission
Help freelancers get paid on time by sending polite, automatic payment reminders for overdue invoices.

## Problem
Freelancers lose hours chasing late payments and avoid doing it because it feels awkward. Late payments hurt cash flow.

## Users & jobs-to-be-done
Solo freelancers with 5–50 active invoices. Job: "Remind my clients without me writing emails or feeling pushy."

## Goals
- Send the first reminder within 24 h of an invoice becoming overdue
- Support 3 escalating reminder tones (friendly, firm, final)
- Let the user approve or skip any reminder before it goes out

## Non-goals
- Not an invoicing system (no invoice creation)
- No payment processing
- No multi-user teams in v1

## Anti-goals
- Sending a reminder for an invoice that was already paid
- Sending without the user's explicit opt-in per client

## Success criteria
- [ ] Overdue invoice triggers exactly one reminder per escalation step
- [ ] Paid invoice never triggers a reminder (covered by test)
- [ ] User can preview, edit, approve or skip each reminder

## Architecture
```
[Invoice CSV import] → [Scheduler] → [Reminder drafter (LLM)] → [Approval queue] → [Email sender]
                                                   ↑
                                          tone templates + client history
```

## Data model
- `Invoice(id, client_id, amount, due_date, status)`
- `Client(id, name, email, opted_in)`
- `Reminder(id, invoice_id, step, tone, status, sent_at)`

## Interfaces
| Name | Input | Output | Errors |
|---|---|---|---|
| `POST /reminders/draft` | invoice_id | draft text | 404 unknown invoice, 409 already paid |
| `POST /reminders/{id}/approve` | reminder id | sent status | 403 client not opted in |

## Security notes
- Email API key is a high-value secret: dev-only sandbox key in development
- Draft text must not include data from other clients
- Rate-limit approve endpoint to prevent accidental mass sends

## Env contract (names only — never values)

| Name | Purpose | Required | Where used |
|---|---|---|---|
| `APP_ENV` | Runtime environment name | yes | app bootstrap |
| `DATABASE_URL` | Primary datastore connection | yes | data layer |
| `EMAIL_API_KEY` | Sends approved reminders | yes | `email/sender` |
| `LLM_API_KEY` | Drafts reminder text | yes | `drafter` |

## Decisions log

| Date | Decision | Why | Rejected alternatives |
|---|---|---|---|
| 2026-01-10 | Human approval before every send | Anti-goal: never send wrongly | Fully automatic sending |
| 2026-01-10 | CSV import first, no accounting integrations | Smallest slice that proves value | Direct integrations in v1 |

## Risks
- LLM tone drift: mitigate with fixed tone templates and a review step
- Duplicate sends on retry: mitigate with idempotency key per (invoice, step)

## Open questions
- Which time zone defines "within 24 h"? (needs the user's decision)

## Current status
- Done: CSV import, data model
- Current slice: scheduler for first reminder
- Next: approval queue
- Blockers: time zone decision (see Open questions)

## Glossary
- **Step**: one rung of the reminder escalation (1 friendly, 2 firm, 3 final)
