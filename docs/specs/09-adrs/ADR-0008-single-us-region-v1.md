# ADR-0008 — Single US region for v1

**Status:** Accepted · 2026-08-08 · Referenced by `00-decisions.md` §3, `05-tdd.md` §12.3

## Context

The product is multilingual from launch (ADR-0002: every language supported by both `eleven_flash_v2_5` and `scribe_v2`), so users will not be geographically concentrated. That is a real argument for distributing infrastructure — and it collides with the tightest budget in the system.

The call-in loop has 1,450 ms of allocated p95 budget against a 1,500 ms requirement, split across five hops (`05-tdd.md` §5.4). Only 200 ms of that is transport. Any architecture that adds a cross-region hop inside the loop — agent in one region, database or LLM gateway in another — spends the entire transport allocation on network alone and breaks the budget outright.

Meanwhile every other latency budget in the product is either asynchronous (post-session ≤ 10 min), generous relative to network time (on-selection playable < 30 s), or served from a CDN rather than an origin (pre-generated start < 2 s, audio via signed Storage URLs).

The v1 target is a 90-day beta with roughly 1,000 users. Multi-region Postgres means either read replicas with stale reads against a learner file that must never contradict the user, or a distributed database we have not pinned.

## Decision

**Single region for v1: Vercel `iad1`, Supabase `us-east-1`, Upstash `us-east-1`, LiveKit Cloud US East, Trigger.dev US.** The voice agent, the database, and the Redis instance are co-located, so no in-loop hop crosses a region.

Perceived latency for distant users is handled where it actually matters — media delivery — by the Supabase Storage CDN with content-immutable object paths, which serves audio from an edge near the user regardless of origin region.

## Alternatives considered

**Multi-region from day one.** Lost on cost and on correctness. It requires a multi-region database story (replicas with stale-read risk against the learner file, or a distributed Postgres we have not selected), region-aware routing, and a replication-lag failure mode in every runbook — for a beta whose entire population would fit in one instance. The standard names premature distribution as a failure mode.

**Agent in a region near the user, database in `us-east-1`.** Lost on arithmetic. The agent reads the host brief and learner-file slice at connect and writes a `call_turn` per turn. A 90 ms cross-Atlantic round trip is 45% of the entire transport allocation, and connect-time reads would push call setup past the point where "Connecting" stops feeling instant.

**Europe as the primary region instead of the US.** Lost because our providers' lowest-latency and highest-availability footprints are US East, LiveKit Cloud's US East region is co-located with the rest of the stack, and no launch-market decision exists that would justify the swap. It remains a swap, not a re-architecture, if a market decision later says otherwise.

**Edge runtime for route handlers with a regional database.** Lost because handlers that read Postgres would run at the edge and immediately reach back across regions, which is slower than running in `iad1` next to the database. Edge placement helps only for handlers that touch no origin data, and we have none worth splitting the deployment model over.

## Consequences

- Users far from US East see higher API latency, roughly 150–250 ms of added round trip from Europe and Asia. This is acceptable because no interactive budget in `00` §8 is tight enough to break, and because audio — the dominant payload — is CDN-served.
- The call-in budget holds with margin, which is the point.
- Every runbook is single-region: no failover procedure, no replication-lag alert, no split-brain reasoning. Operational simplicity is a direct product of this decision.
- A regional outage at Supabase `us-east-1` is a full outage. Accepted for v1 beta; the mitigation is the provider's own availability posture plus honest user-visible failure states, not our own redundancy.
- The 10× path in `05-tdd.md` §12.3 records the multi-region step: app and CDN served from a second region with the database staying primary in `us-east-1`, and the voice agent staying co-located. Written, not built.
- Data residency is US-only in v1. If a market requires EU residency, that is a new ADR and a genuine architecture change, not a configuration flag.
