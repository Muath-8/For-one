# For one: technical design (TDD)

The level below `/architecture/`: what an engineer opens to start coding. Written 2026-11-06 against concept v2, decisions.md (2026-10-23), the nine architecture documents and PRD-v2 (v3.1).

| File | Area |
|---|---|
| [00-overview.md](00-overview.md) | what the system is, module map, laws as code, build order |
| [01-data-model.md](01-data-model.md) | every table and column, ERD, encryption classes, retention, roles |
| [02-api-contracts.md](02-api-contracts.md) | REST, SSE, LiveKit data channels, Inngest events, schemas, errors, auth |
| [03-generation-pipeline.md](03-generation-pipeline.md) | episode production: steps, prompts, coverage check, caching, cost per step |
| [04-live-call.md](04-live-call.md) | room lifecycle, governor and turn machines, recasts, verbatim re-transcription, latency |
| [05-learner-model.md](05-learner-model.md) | facts with sources, words and structures, replanning, briefs, notebook |
| [06-after-session-and-proof.md](06-after-session-and-proof.md) | the after-session pass, claim gate, weekly proof, then-and-now |
| [07-client.md](07-client.md) | routes, state, player, call screen, offline PWA, feed |
| [08-security-privacy.md](08-security-privacy.md) | keys, isolation, consent, deletion jobs, crisis protocol |
| [09-observability.md](09-observability.md) | tracing, measures, alarms, cost controls, evals, flags, ops |
| [10-open-questions.md](10-open-questions.md) | contradictions with the architecture, decisions owed, assumptions |

Readable entry page: `technical-design.html` in this folder (published as an Artifact; link in the thread).
