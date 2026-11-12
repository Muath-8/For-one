# For one: engineering handbook

Written 2026-11-06 for a team of engineers; revised 2026-11-12 for ADR-24 and then ADR-25. Since ADR-25 the reader is **an AI coding agent that builds For one story by story under Muath** (ADR-25.2). The handbook covers everything needed to set up and run the build that is not product, architecture or design: those live in `PRD-v3.md`, `concept-v2.md`, `decisions.md`, `architecture/`, `technical-design/` and `design/`. The build has no calendar dates; work runs in the dependency order of `backlog/00-release-plan.md`, and version 1 launches once, publicly, when every v1 story passes and the launch checklist (page 10 §4) is green.

The readable entry point is the handbook page: https://claude.ai/artifact/CafNuoUdqfKawrPo8LbCRp (source: `engineering/handbook.html`). These Markdown files are the source of truth and are edited by pull request like code.

## Who does what

| Who | Does | Never does |
|---|---|---|
| **The coding agent** | picks up one story at a time, writes its acceptance criteria as tests first, writes the code, runs CI, answers the review pass, opens the pull request, runs a runbook when Muath asks | invents architecture (it escalates), merges to `main`, applies a migration, changes a prompt or bible version in prod, deploys to prod, reads learner content, holds a prod secret |
| **The AI review pass** | a second, independent model session that reads every pull request against the cited story, the laws, the data rules and page 08 §5, and posts its findings on the PR | writes the code it reviews; approves |
| **Muath** | owns the product and the decisions; approves merges to `main`, migrations, prompt and bible changes and production deploys (register A8); receives every alert; opens the vendor accounts | is paged at night for anything the product's fallbacks already cover |

## The pages

| # | Page | One line |
|---|---|---|
| 01 | [Repository layout](01-repository-layout.md) | One monorepo, four deployables, eight packages, where prompts live, and the two kinds of language package (target and native, ADR-02). |
| 02 | [Local development](02-local-development.md) | A full day of the product on one machine, for free: docker compose, seeds, the fake vendors, every environment variable with its owner. |
| 03 | [Environments and deployment](03-environments-and-deployment.md) | dev, staging, prod; Terraform; Secrets Manager with OIDC; the home region (`eu-central-1`); how a deploy happens and who approves it. |
| 04 | [CI and CD](04-ci-cd.md) | The workflows, the checks on every PR, the eval gate, the AI review pass, branch protection, the nightly, the release process. |
| 05 | [Testing strategy](05-testing-strategy.md) | Tests first; five layers; verbatim-first voice testing; the simulated caller and the scripted calls; golden sets from synthetic learners and open clips. |
| 06 | [Observability and operations](06-observability-and-on-call.md) | Postgres as the metrics store, alerts as SQL with runbooks, the cost-per-session dashboard, fallbacks first and alerts to Muath. |
| 07 | [Vendor accounts and cost controls](07-vendor-accounts-and-cost-controls.md) | The accounts Muath opens, keys per environment, vendor-side retention switches, spend caps, spend modes, the stop line. |
| 08 | [Coding standards and review](08-coding-standards-and-review.md) | Python and TypeScript rules, PR shape, the rules for prompt changes, what the review pass checks in this product. |
| 09 | [Data handling](09-data-handling.md) | Data classes, the promises the code keeps, what the agent may and may not look at, where data may go, consent, fixtures, research use, incidents. |
| 10 | [Definition of done](10-definition-of-done.md) | Checklists for a story, a prompt change, a release, and the launch. |

Starter files, ready to copy into the code repository:

- [`starter-files/AGENTS.md`](starter-files/AGENTS.md): the instructions the coding agent reads first in the code repository.
- [`starter-files/ci.yml`](starter-files/ci.yml): the PR pipeline from page 04.
- [`starter-files/.env.example`](starter-files/.env.example): every variable from page 02 with dev values.
- [`starter-files/CODEOWNERS`](starter-files/CODEOWNERS): every path is Muath's to approve.

## The ten rules, if you read nothing else

1. **Tests before code.** A story's acceptance criteria become automated tests first; the code is written to make them pass.
2. **Never invent architecture.** If the canon (AGENTS.md lists its order) does not answer a question, the agent stops and asks Muath; it does not guess and build.
3. **Fakes by default.** No real vendor is called in dev unless the story is about that vendor; `FORONE_FAKE_VENDORS=1` is the default and every fake call is still priced.
4. **Prompts are code.** A file, a version, an eval run, a review pass, Muath's approval. No prompt editor in the admin UI.
5. **Synthetic learners everywhere.** Dev, staging, cassettes, canaries and load tests use invented people. Real learners live in prod and nowhere else.
6. **Learner text stays home.** Ids and enums may travel to Inngest, Sentry, Slack and the logs; names, transcripts, facts and audio never do, and prompts reach Langfuse only with the opt-in.
7. **Every promise is verified by a second job.** Deletion windows are checked hourly by code that does not share the doer's bugs.
8. **Every vendor call is a priced row.** Through the middleware, on the cost page, with a fallback and a degrade path in `vendors.yaml`.
9. **Fallbacks first, then an alert.** Every failure the product can absorb (yesterday's episode stays, voice notes) is absorbed automatically; Muath is told; a runbook says what to do next.
10. **Muath approves what cannot be undone quietly.** Merges to `main`, migrations, prompt and bible changes, production deploys.

## Decisions this handbook makes that the architecture did not

| Decision | Where | Why |
|---|---|---|
| Terraform with an S3 state backend, not Terraform Cloud or CDK | 03 §3 | the most widely read code for exactly this infrastructure, which an agent writes and reviews well; one fewer processor |
| GitHub OIDC to AWS; no long-lived keys anywhere, for a person, the agent or CI | 03 §4 | nothing to leak |
| The agent holds no prod credential; prod changes run only through approved workflows | 03 §5, 06 §6 | Muath's approval is the control, and it cannot be bypassed from a session |
| Eval-gate cost ceiling of $25 per PR without a label | 04 §3 | a prompt PR should not silently cost a day of the product's budget |
| Error-preservation rate gates a recognizer before word error rate | 05 §5 | speech-to-text smooths learner errors |
| Model-judged eval metrics with noise above their regression allowance are advisory, not gating | 05 §6 | a gate that fails on noise gets disabled; an advisory metric gets fixed |
| A story without a kill switch is not done | 10 §1 | the first move in any runbook is a switch |

## Owner actions that touch the build

From the register in `architecture/10-decision-records.md` §10 A. None carries a date; each says what it must happen before.

| # | Action | Needed before |
|---|---|---|
| A1 | Open the vendor accounts in page 07 §1, accept each vendor's standard DPA, request zero data retention from Anthropic | the first deploy to staging |
| A2 | Record about 30 volunteer clips and rate the voice blind test (ADR-25.6) | the vendor choice |
| A3 | Read and approve the English bibles and Salma's lines (ADR-25.7) | the writer and host prompts are tuned |
| A4 | Complete the self-review checklist and approve the legal texts (ADR-25.3) | public launch |
| A5 | Open the Paddle account | checkout is built against the live API (the sandbox works before) |
| A6 | Choose and register the domain (`APP_DOMAIN`, ADR-25.8) | email sending and the first public deploy |
| A8 | Approve merges, migrations, prompt changes and production deploys as the agent asks | each one |
