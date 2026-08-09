# ADR-0012 — No client-side database access

**Status:** Accepted · 2026-08-08 · Referenced by `00-decisions.md` §4, §6, `05-tdd.md` §1.2, §11.1

## Context

Supabase's default pattern is a browser client that queries Postgres directly through PostgREST, with row-level security as the authorization boundary. It is fast to build and it removes a layer. Since we already run Supabase Postgres with RLS on every user-owned table, the pattern is available to us at no extra cost.

Three properties of this product make it the wrong choice anyway.

**Authorization is not the only server-side rule.** Reading a pitch set is not just "rows where `user_id` matches". Creating a session enforces the two-session cap in the user's stored timezone, the email-verification gate before session 2, the endpoint's named rate limit, the separate daily money guard, and idempotency replay — then triggers a job. Named onboarding and quality-gate regeneration caps apply at their own writers; there is no universal generation-count budget. None of that is expressible as an RLS policy, and a client that can read and write tables directly can reach the data underneath those rules.

**The schema would become a public contract.** Direct table access makes every column name and shape part of the client API. `00` §5 forbids `level_band`, `level_step`, and `level_confidence` from ever appearing in an API response, and the product laws forbid surfacing the CEFR anchoring in any form. With direct access, that prohibition depends on a column-level grant staying correct through every migration, forever.

**Auth is Clerk, not Supabase.** ADR-0014 puts identity in Clerk. Using RLS as the browser's authorization boundary would require minting and refreshing Supabase-compatible JWTs from Clerk sessions, keeping the third-party JWT configuration in sync, and reasoning about two token lifetimes — infrastructure that exists solely to enable a pattern we do not want.

## Decision

**The browser never talks to Postgres.** All client-to-server data flows through REST route handlers under `/api/v1/*` (ADR-0005). `supabase-js` appears in the codebase only in `src/platform/storage` for Storage operations and signed-URL minting, and only server-side.

RLS remains enabled on every user-owned table, but its role is explicit: it is the **structural backstop** behind repository-layer `userId` scoping, not the primary authorization control (`00` §4). Two independent layers, neither trusted alone.

Media is the one exception to "everything through the API", and it is not an exception to this decision: the browser fetches audio directly from Supabase Storage through **signed URLs minted server-side after an ownership check**. Audio never transits our API, and the browser never holds a credential that would let it enumerate anything.

## Alternatives considered

**Browser reads direct, writes through the API.** Lost because it is the worst of both. The schema still becomes a public contract, RLS still has to be perfect for every column forever, and the codebase gains a second read path with different caching, error, and pagination semantics — while every business rule still lives on the server. Two paths, one benefit.

**Supabase Realtime subscriptions for generation progress.** Genuinely tempting: it would replace polling with push. It lost because it requires exactly the browser-side database credential this decision removes, and it would expose row shapes for `generation_jobs` and `sessions` to the client. The polling endpoint in `05-tdd.md` §6.4 delivers the same user experience at a sub-10 ms Redis read, for a product with two sessions per user per day.

**RLS as the sole authorization boundary, with no repository scoping.** Lost on defence in depth. A single mistaken policy, or a table added without one, silently exposes every user's rows. Repository-layer scoping means a policy mistake is caught by the application layer and an application mistake is caught by the policy — and 08's per-resource "A cannot read B" tests verify both.

## Consequences

- Every data need has exactly one path, which is what makes rate limiting, idempotency, the closed error catalog, and the ban on exposing level data enforceable in one place.
- The schema is free to evolve without breaking clients, because the API response shape is a deliberate mapping owned by 06 rather than a projection of table columns.
- More endpoints to write than the direct-access pattern. Accepted; the route-handler wrapper absorbs the repetition.
- Real-time push is not available in v1. Progress is polled, and the evidence trigger for revisiting is recorded in `05-tdd.md` §12.4 — p95 perceived readiness lag above 2 s attributable to poll interval, or polling above 5% of function invocations. Revisiting means server-sent events from our own API, not a browser database credential.
- Offline behaviour is explicit rather than emergent: loaded transcripts, notes, and buffered audio remain usable because the client holds them, and anything requiring new data is disabled with an inline explanation, per the design doc's offline rules.
- `SUPABASE_SERVICE_ROLE_KEY` and `DATABASE_URL` are structurally absent from the client bundle, because `src/config/env.ts` accepts only `NEXT_PUBLIC_*` names in the client schema and CI fails if a non-public secret name appears in the bundle.
