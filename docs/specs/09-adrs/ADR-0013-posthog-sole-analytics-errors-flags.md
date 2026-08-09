# ADR-0013 — PostHog as the sole analytics, error-tracking, and feature-flag tool

**Status:** Accepted · 2026-08-08 · Referenced by `00-decisions.md` §3, `05-tdd.md` §9.4, §10.6

## Context

Three needs, normally served by three vendors:

1. **Product analytics** — the PRD Part 15 beta targets are all funnel or cohort questions: sessions per user per week, full-cycle completion, call-in participation, week-4 retention among users with a Weekly Proof.
2. **Error tracking** — three runtimes (web, tasks, agent) that all need exception capture with grouping.
3. **Feature flags** — the staged-rollout mechanism `00` §11 sanctions for behaviour no FR mandates. (Amended: v1 launches with zero flags defined — the character-creation and Weekly Proof rollout flags were rejected as contradicting FR-303 and FR-500; see 05 §10.6. The mechanism, its fail-safe defaults, and the CI expiry check remain.)

Two constraints shape the choice. The product has a hard trust contract: no dark patterns, no re-engagement mechanics, no surveillance framing. Any tool that collects more than we deliberately send is a liability, not an asset. And the deletion flow (ADR-0001) must purge the user from every store within 24 hours, which means every additional vendor is another deletion API to call, another failure mode in `JOB-delete-account`, and another place a purge can silently not happen.

There is also a diagnostic reason to prefer one tool: the most valuable question in this system is "did this user get a result?", and answering it requires joining a product funnel to an error. Across two vendors that join is manual; in one tool it is a query.

## Decision

**PostHog is the sole tool for analytics, error monitoring, and feature flags.** No Sentry, no Amplitude, no LaunchDarkly, no separate flag service.

Configuration is deliberately minimal:

- `posthog-js` on the client with **autocapture off**, **session recording off**, and `person_profiles: 'identified_only'`. Nothing is collected that we did not name in the taxonomy.
- `posthog-node` server-side in route handlers, tasks, and the agent, keyed on `users.id`.
- Every event carries `trace_id`, so a funnel drop-off leads directly to the trace, the stage, and the `cost_events` rows for that user action.
- Exceptions are captured from all three runtimes with `traceId`, `runtime`, `module`, and `errorCode` tags.
- Flags are read server-side through `posthog-node` with a 60 s local cache and a **hard-coded default per flag**, so a PostHog outage never changes product behaviour.
- `JOB-delete-account` calls the PostHog person-deletion API with `POSTHOG_PERSONAL_API_KEY` and does not report deletion complete until it succeeds.

## Alternatives considered

**Sentry for errors alongside PostHog for analytics.** Sentry's grouping, release tracking, and stack-trace ergonomics are better. It lost on three counts: a second vendor in the deletion path, correlation between an error and a product funnel that becomes a manual cross-tool join, and a second SDK in all three runtimes for a beta whose error volume is small. The evidence trigger for revisiting is written down in `05-tdd.md` §12.4 — PostHog error volume exceeding its plan, or a grouping-quality complaint across two consecutive incidents.

**LaunchDarkly or a dedicated flag service.** Lost on scope. v1 defines zero flags (05 §10.6), and `00` §11 restricts any future flag to staged rollouts with expiry dates, forbidding configuration or pedagogy experiments. Percentage rollout and a kill default is the entire requirement, and PostHog covers it.

**Amplitude or Mixpanel for analytics.** Lost because they solve only one of the three needs, add a vendor to the deletion path, and bring no capability the Part 15 metrics require.

**Self-hosted analytics.** Lost on operational cost. Running and backing up an analytics store is work that buys nothing for a 90-day beta, and it would put user event data under our own retention and deletion implementation rather than a vendor's tested one.

**No analytics in v1.** Lost because PRD Part 18's milestone gate and the Part 15 targets are the mechanism by which the product thesis is tested. Building the product without measuring whether people come back is the one thing that would make the beta meaningless.

## Consequences

- One deletion call, one dashboard, one SDK per runtime. "Did this user get a result" is answerable by filtering on `trace_id` across events and exceptions.
- Error-tracking ergonomics are weaker than a dedicated tool. Accepted, and partly compensated by the durable domain record: `generation_jobs` holds per-stage state and `cost_events` holds every provider call with prompt version, model, latency, cost, validation outcome, and disposition. For this product's most common failure question, those tables are more useful than a stack trace.
- Autocapture being off means every event is deliberate. A missing event is a code change, not a filter change. That is the intended trade: the taxonomy in `05-tdd.md` §9.4 is the complete list, and it is reviewable against the trust contract.
- Session recording being off removes an entire class of privacy risk on a product handling voice and language-learning data, and it is consistent with a product that refuses surveillance framing.
- Flag defaults are in code. A flag whose PostHog definition is deleted falls back to its hard-coded default — `off` for any staged-rollout flag, which is the safe direction.
- v1 defines no flags. Any future staged-rollout flag MUST name behavior that no FR mandates, carry an expiry date, and fail CI after that date, so the flag set cannot quietly become permanent configuration (05 §10.6).
