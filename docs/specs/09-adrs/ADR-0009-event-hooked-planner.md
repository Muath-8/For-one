# ADR-0009 — Event-hooked planner over a nightly cron

**Status:** Accepted · 2026-08-08 · Supersedes the "nightly planner" wording in PRD v2.0 Part 1.1 and Part 9 · Referenced by `00-decisions.md` §1, `05-tdd.md` §5.1, §5.5

## Context

The source documents described the planner as a nightly batch job, one run per user per night, producing the next day's pitches. Three things make that wrong.

**Nightly means nothing to a multi-timezone product.** Users span every timezone supported by the TTS and STT providers (ADR-0002). "Overnight" is a different wall-clock hour for each user, so a cron either runs 24 times a day partitioned by timezone, or it runs once and is midday for a large fraction of users. Both are worse than not having a schedule.

**The freshest moment is immediately after a session, not eight hours later.** The post-session analysis pass updates all four sections of the learner file within 10 minutes of session end (PRD Part 8). Planning at that moment uses a file that has just absorbed today's errors, uptake, energy signal, and target movement. Planning at 03:00 uses the same data, later, with nothing added.

**Some triggers are not time-based at all.** A follow-up seed coming due ("interview Friday") must change the pitch set when it comes due. A user who has not had a session for two days needs fresh pitches when they open the app, not when a cron last happened to run.

Meanwhile the planner is expensive: a world check, pitch writing, pedagogy threading, prediction, and full pre-generation of the predicted pick including audio. Running it on a schedule for every user runs it for users who will not open the app.

## Decision

**The planner is event-hooked, never scheduled.** Three triggers, in priority order:

1. **Post-session** (primary) — fires when the post-session analysis pass completes, inside the same 10-minute window.
2. **Staleness** — at app open, when the pitch set is older than 20 hours. The refresh runs before pitches render, with a 5 s budget for pitch text; pre-generation of the predicted pick continues in the background.
3. **Follow-up due** — a follow-up seed reaching its date refreshes the pitch set regardless of the other two.

Concurrent triggers coalesce into one run. Every run produces a complete fresh pitch set; partial patches are prohibited.

Character retirement is not a planner trigger. Acceptance of a stale affected pitch performs the deterministic, package-authored pitch revision owned by FR-706 and 06 in the same refusal transaction, then directs the client to read the current set. That repair calls no model, writes no `planner_runs` row, and cannot add a fourth reason to the pending register.

These are exactly the three **steady-state replacement** triggers. The one-pitch onboarding initialization is a separate, one-time initialization workflow governed by FR-026; it does not replace a daily set, does not write a `planner_runs.trigger`, and does not enter this trigger register. A user-initiated manual refresh is out of scope under F-14 and FR-122; the retired `EP-13` identifier MUST NOT be reused.

Coalescing is two-layered: a Trigger.dev idempotency key `planner-{userId}-{reason}-{5-minute bucket}` collapses duplicate triggers at the queue, and a Redis lock `planner:lock:{userId}` with a pending-reason value collapses concurrent triggers of *different* reasons into one run followed by at most one re-run. That value retains the highest-priority pending reason in the order above; a boolean flag is insufficient because it loses the required ordering.

## Alternatives considered

**Nightly cron per user timezone.** Lost on all three counts above. It also creates a thundering herd at each timezone boundary — every user in a zone planned in the same minute, each run calling Exa and several models — which would need its own smoothing mechanism to solve a problem the event model does not create.

**Cron plus event hooks together.** Lost because the cron would be pure waste: after a post-session run, the nightly run has no new evidence and would regenerate the same set at real cost, and the staleness hook already covers users who did not have a session. Two mechanisms producing the same artifact also doubles the coalescing surface.

**Fully lazy — plan only at app open.** Lost on the < 5 s staleness budget and on the < 2 s pre-generated start. Planning at open means the user waits for a world check, pitch writing, and pedagogy threading before seeing anything, and pre-generation of the predicted pick has had no opportunity to run, so no pitch is ever "Ready now". The post-session hook exists precisely so the common path is already done before the user arrives.

**Precompute pitches for every plausible interest ahead of time.** Lost on cost and on quality. The pitch set depends on the current edge, energy state, target queue, and due follow-ups, all of which move after every session; precomputed variants would be stale on arrival, and full pre-generation of several would multiply cost far beyond the $1.50 p50 per-cycle envelope.

## Consequences

- The staleness hook is on the app-open critical path and therefore has the rendezvous budget owned by `00-decisions.md` §8. On expiry EP-04 returns the existing set using the exact stale-state response owned by 06, and the client keeps the dated programme frame rather than blocking. The budget is a *response* budget, not a work budget.
- `INV-PLAN-1` (atomic replacement) is what makes coalescing safe: two runs can never interleave into a mixed pitch set, because the set is replaced in one transaction.
- `INV-PLAN-2` (a world-check failure never fails a run) is required, because the planner now sits on a user-visible path. Exa failure falls back to interests, follow-ups, and the wildcard with no banner.
- Users who never complete a session are still served: the staleness hook covers them at 20 hours.
- Planner cost scales with engagement rather than with registration, which matters directly against the per-cycle cost envelope.
- There is no scheduled stale-set safety net. `JOB-reconcile` may recover only a durable, representable lost outcome of one of the three authorized triggers; it MUST NOT discover users by pitch-set age or create a fourth scheduled planning trigger.
