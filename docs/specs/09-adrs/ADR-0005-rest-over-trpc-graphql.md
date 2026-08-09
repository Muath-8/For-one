# ADR-0005 — REST route handlers over tRPC and GraphQL

**Status:** Accepted · 2026-08-08 · Referenced by `00-decisions.md` §6, `05-tdd.md` §4

## Context

The browser is not the only client of our data path, and the API surface must survive three constraints that are unusual together:

1. **Three consumers, not one.** The React UI, the LiveKit voice agent, and Trigger.dev tasks all need data. The satellites import modules directly, but the browser must go over the network, and that network contract carries auth, rate limits, idempotency, and error semantics.
2. **Mutations that are expensive and duplicated.** Session creation and generation triggering spend real money per call. They need `Idempotency-Key` handling with replay semantics, which is an HTTP-level concern with a well-understood convention.
3. **Media that must not transit the API.** Audio moves through signed Storage URLs and WebRTC. The data API only ever moves JSON.

The product also has strict per-endpoint behaviour: a closed error-code catalog, cursor pagination, and endpoints designed around product behaviour (accept a pitch, get on the line) rather than entity CRUD.

## Decision

**All client-to-server data flows through REST route handlers under `/api/v1/*`**, with JSON camelCase bodies, the Clerk session JWT in `Authorization`, one error envelope `{ error: { code, message, requestId } }` against a closed code catalog, cursor pagination, and `Idempotency-Key` required on session-creating and generation-triggering endpoints.

Server actions are **not** used for data mutation. There is one path from browser to data, and it is a versioned REST endpoint.

## Alternatives considered

**tRPC.** Genuinely attractive for end-to-end type safety inside a TypeScript monorepo, and it lost on three specific points. It couples the wire contract to the TypeScript build, which makes the agent and any future non-TypeScript consumer second-class. It has no natural place for HTTP-level idempotency replay, per-route rate-limit identity, or the closed status-code mapping that `00` §6 fixes. And its procedure-oriented shape encourages fine-grained calls, where this product needs a small number of behaviour-shaped endpoints. Type safety is recovered instead by sharing Zod schemas between handler and client, which is where validation already lives (`00` §3 pins Zod as the single validation library).

**GraphQL.** Lost on cost-to-benefit. Its central benefit is letting varied clients select fields across a large graph; we have one client and a small, behaviour-shaped surface. It would add a schema layer, resolver plumbing, an N+1 problem to solve with dataloaders, per-query complexity limiting to prevent abuse, and a caching story that fights HTTP caching. None of that buys anything the product needs.

**Next.js server actions for mutations.** Lost on the one-path rule. Server actions would create a second, differently-shaped mutation path with no URL, no status codes, no idempotency header, and no uniform rate-limit hook — precisely the duplicated-logic failure mode the standard names. They are also unavailable to the voice agent and to tasks.

**Direct Supabase client calls from the browser.** Rejected separately and permanently in ADR-0012.

## Consequences

- Every route handler passes through one wrapper (`src/platform/http/handler.ts`) that applies auth, user resolution, rate limits, idempotency, Zod parsing, and error mapping in a fixed order. New endpoints get all of it for free, and skipping the wrapper is visible in review.
- Type safety across the wire depends on discipline: request and response schemas are Zod objects exported from the module that owns the endpoint, and the client imports the inferred types. 06 owns the catalog.
- The `/v1` prefix is real versioning. A breaking change ships as `/v2` alongside `/v1`; endpoints are never mutated in place.
- More boilerplate per endpoint than tRPC. Accepted, because the wrapper absorbs the repetitive part and the explicit surface is what makes rate limiting, idempotency, and the error catalog enforceable.
- The API is documented as a catalog in 06 rather than generated from types, which means the catalog can drift from the implementation. 08 MUST include contract tests that validate each handler against its declared schemas.
