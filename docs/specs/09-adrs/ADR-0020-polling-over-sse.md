# ADR-0020 — Polling over Server-Sent Events for session progress

**Status:** Accepted

## Context

Phase-3 review (RB-01/02/03) found the one place in the corpus where four documents failed to converge: the channel that tells the client about generation readiness, After-show host replies, and voice-note replies. 05 specified polling with a four-tier cadence; 06 specified a fully provisioned SSE channel (EP-23) with its own rate-limit class and reconnect semantics; 04's FR-110 normatively mandated polling with a 5-second floor in a document that does not own transport; 08 tested neither. Each spec carried a rationale rejecting the other's choice, and no ADR existed.

## Decision

**Polling.** One endpoint, owned and catalogued by 06 (`GET /api/v1/sessions/{sessionId}/state`, with its own EP-##), reading `session:{sessionId}:runtime` and `gen:{episodeId}:state` from Redis with Postgres fallback, returning an ETag. Client cadence: 1 s while a determinate wait is on screen, 3 s while the session is foregrounded but not waiting, 10 s backgrounded, suspended when hidden. The payload carries generation readiness, pending After-show reply state, and pending voice-note reply state, so the three signals share one path. 04's requirement becomes transport-neutral: the waiting surface must reflect readiness within 5 s of the state change.

## Alternatives considered

1. **Server-Sent Events (06's EP-23).** Rejected: on serverless, an SSE stream holds a function invocation open for the whole wait (06 budgeted `maxDuration = 120`) and requires `Last-Event-ID` reconnect plumbing and a per-user concurrent-stream rate class — real complexity purchased for latency the product does not need. All three carried signals are "arrives when it arrives" events with a 5-second freshness bound; a sub-10 ms Redis read on a 1–3 s cadence meets that bound with headroom.
2. **LiveKit data channel.** Rejected: couples ordinary session progress to the realtime voice dependency, which is deliberately scoped to the call-in alone.

## Consequences

- 06 deletes EP-23 (SSE, `RL-SSE`, the pub/sub publisher contract) and catalogues the state endpoint with request/response schema, ETag semantics, cadence guidance, and a rate limit sized to the 1 s tier.
- 05 §6.4 cites the 06 endpoint by EP-## instead of defining a path; the Redis key inventory keeps the two keys the endpoint reads.
- 04 FR-110 drops transport verbs and the `[decided here]` interval; the 5 s freshness bound stays as the behavioral requirement.
- 08 adds test coverage for the endpoint (correctness, ETag/304 behavior, cadence-tier budget under load) — the review found neither candidate path had a test, which is how the contradiction survived.
