# ADR-0018 — A read-only scanner role for cross-user job discovery

**Status:** Accepted

## Context

00-decisions §4 says satellites reach data "only through the same scoped repositories" — per-user scoping everywhere. Six background jobs cannot start scoped: 48-hour session expiry, follow-up due hook, target re-check scheduling, Weekly Proof qualification, export-link expiry, and audio purge must first discover *which users* need work. A per-user scheduled task per job avoids cross-user reads but multiplies scheduled runs by the user count and does not scale past a few thousand accounts.

## Decision

One Postgres role, `app_scanner`, used exclusively by discovery steps of scheduled jobs: `BYPASSRLS`, but granted `SELECT` only on the purpose-built scan views enumerated in 06 §7.4 — no base-table access, and no view exposes content columns (IDs, states, timestamps, and category labels only). Discovery fans out to per-user Trigger.dev tasks that run as `app_user` with that user's claim, so all real work remains user-scoped. The enumerated set in 06 §7.4 is the complete inventory of cross-user read paths; the binding constraint is the content-free property and the closed enumeration, not the count.

## Alternatives considered

1. **Per-user scheduled tasks.** Rejected: O(users) scheduled runs, operationally unscalable, and the scheduler itself becomes the cross-user enumerator anyway.
2. **Service role with full bypass for jobs.** Rejected: destroys the structural isolation guarantee; a bug in any job could read any user's content.
3. **Denormalized "work due" queue table written by user-scoped paths.** Rejected for v1: duplicates state that the enumerated scan views derive for free; reconsider only if view scans become a measured bottleneck.

## Consequences

- 00-decisions §4 wording amended to name this single sanctioned exception.
- 08 includes a mechanical test: `app_scanner` can select from exactly the views enumerated in 06 §7.4 and nothing else; every view's column list is content-free.
- Any new cross-user read requires adding the view to 06 §7.4's enumeration in the same change that grants it — the set stays closed and reviewable.
