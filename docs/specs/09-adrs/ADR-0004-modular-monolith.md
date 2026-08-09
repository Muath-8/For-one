# ADR-0004 — Modular monolith with exactly two satellite runtimes

**Status:** Accepted · 2026-08-08 · Referenced by `00-decisions.md` §4, `05-tdd.md` §1–§3

## Context

For one has three genuinely different execution profiles: interactive HTTP requests that must return in well under a second, a real-time voice loop with a 1.5 s end-to-end budget, and expensive asynchronous pipelines that run for minutes and call several paid providers per run. Those profiles cannot share one process model — a serverless function cannot hold a WebRTC session, and a voice agent must not be blocked by a 15-minute generation job.

That is an argument for separate *runtimes*. It is not an argument for separate *services*. The system has fourteen domain concerns (identity, learner file, cast, planner, generation, session, realtime, assessment, proof, archive, trust, telemetry, language packages, lexicon) that share one small, tightly coupled data model: nearly every concern reads the learner file, and the learner file is a single user's row set. Splitting those into services would mean distributed transactions over data that lives in one Postgres instance, for a product with a hard cap of two sessions per user per day.

The team is small and the v1 scope is fixed. Operational surface area is the scarcest resource.

## Decision

**One repository, one npm package, one Next.js application, plus exactly two satellite runtimes deployed from the same codebase:** the LiveKit voice agent (`src/agent`) and the Trigger.dev task set (`src/trigger`).

- Domain code lives in `src/modules/<module>` — folder is boundary. Cross-module imports go only through each module's `index.ts`, enforced by `eslint-plugin-boundaries` (`boundaries/entry-point` plus a tiered `boundaries/element-types` rule) in CI, not by convention.
- Each census table has exactly one owning module, and the Drizzle table definition physically lives in that module's `schema.ts`.
- No message bus, no event streaming, no queue other than Trigger.dev. Module-to-module communication is a function call; runtime-to-runtime communication is a Trigger.dev trigger or a LiveKit room.
- Satellites import the same modules. They are deployment targets, not services with their own model of the world.

## Alternatives considered

**Microservices per domain.** Lost decisively. It would impose network boundaries, versioned internal contracts, distributed tracing infrastructure, and eventual consistency on a data model that is one user's rows in one database — buying independent scaling nobody needs at 2,000 sessions per day, and costing the ability to write a post-session update as a single transaction.

**One deployable for everything (Next.js only).** Lost on physics. Vercel functions cannot hold a WebRTC peer connection for a five-minute call, and generation jobs would either exceed function limits or hold an invocation open at cost. `00` §4 forbids generation in request handlers for exactly this reason.

**Separate repositories per runtime.** Lost because the three runtimes share domain logic that must not drift: the recast policy, the session state machine, and the learner-file gate are single definitions. Three repos would produce three copies, and the copies would diverge under deadline pressure. One repo with lint-enforced boundaries gets the same isolation with none of the synchronisation cost.

**npm workspaces or Turborepo inside the monorepo.** Lost because the only boundary that matters — the module public API — is enforced by lint. Workspaces would add internal package manifests, a build-order tool, and duplicated dependency graphs to buy an isolation guarantee we already have, for a codebase with one shared dependency set.

**Adding a message bus for module decoupling.** Lost because the "events" in this system are all in-process handoffs inside one transaction boundary or one Trigger.dev run. A bus would convert reliable function calls into at-least-once deliveries requiring their own idempotency and dead-letter handling, and the standard names unbounded queues as a failure mode to avoid.

## Consequences

- Any engineer can trace a user action from the browser to the database in one codebase, which is the definition-of-done for `05-tdd.md`.
- The boundary is only as strong as the lint rule. CI MUST run lint as a blocking stage; a boundary violation is a build failure, not a review comment.
- The Vercel build installs agent and task dependencies it does not use, costing install time. Accepted as cheaper than repository splitting.
- Deploying a change to shared module code redeploys all three runtimes. Release order is fixed: migrations, then app, then tasks, then agent, which expand-and-contract makes safe.
- Scaling is per-runtime, which is what the load profile actually needs: agent workers scale with concurrent calls, task concurrency scales with generation volume, and the app scales with page traffic.
- Extracting a service later remains possible module-by-module, because each module already has a single public API and owns its tables. Nothing in this decision forecloses that; it just refuses to pay for it now.
