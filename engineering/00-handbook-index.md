# For one: engineering handbook

Written 2026-11-06 (revised 2026-11-12: the items open for Muath are decided in ADR-24; see the last section) for the team that builds For one between 2026-11-18 and 2027-03-12 and runs the paid beta from 2027-03-17 (ADR-24.11; build-week dates in `backlog/00-release-plan.md`). The handbook covers everything needed to set up and run the build that is not product, architecture or design: those live in `PRD-v2.md`, `concept-v2.md`, `decisions.md`, `architecture/` and `design/`.

The readable entry point is the handbook page: https://claude.ai/artifact/CafNuoUdqfKawrPo8LbCRp (source: `engineering/handbook.html`). These Markdown files are the source of truth and are edited by pull request like code.

## The pages

| # | Page | One line |
|---|---|---|
| 01 | [Repository layout](01-repository-layout.md) | One monorepo, four deployables, eight packages, where prompts live, and the two kinds of language package (target and native, ADR-02). |
| 02 | [Local development](02-local-development.md) | A full day of the product on a laptop in under an hour, for free: docker compose, seeds, the fake vendors, every environment variable with its owner. |
| 03 | [Environments and deployment](03-environments-and-deployment.md) | dev, staging, prod; Terraform; Secrets Manager with OIDC; the home region (`eu-central-1`, ADR-24.8); staging up from build week 2 through the beta (ADR-16); how a deploy happens and when it may not. |
| 04 | [CI and CD](04-ci-cd.md) | The four workflows, the checks on every PR, the eval gate that runs by diff and prints its cost, branch protection, the nightly, the release process. |
| 05 | [Testing strategy](05-testing-strategy.md) | Five layers; verbatim-first voice testing; the simulated caller and the 50 calls; golden sets from Milestone 0; porting the coverage checker. |
| 06 | [Observability and on-call](06-observability-and-on-call.md) | Postgres as the metrics store, alerts as SQL with runbooks, the cost-per-session dashboard defined line by line, the on-call rota for two people. |
| 07 | [Vendor accounts and cost controls](07-vendor-accounts-and-cost-controls.md) | The 25 accounts and who opens them, keys per environment and per engineer, vendor-side retention switches, spend caps, spend modes, the stop line, the risk calendar. |
| 08 | [Coding standards and review](08-coding-standards-and-review.md) | Python and TypeScript rules, PR shape, the ten rules for prompt changes, what a reviewer checks in this product. |
| 09 | [Data handling](09-data-handling.md) | Data classes, the promises the code keeps, what engineers may and may not look at, where data may go, consent, fixtures, research use, incidents. |
| 10 | [Definition of done](10-definition-of-done.md) | Checklists for a story, a prompt change, a release, and the build. |

Starter files, ready to copy into the repository root and `.github/workflows/`:

- [`starter-files/ci.yml`](starter-files/ci.yml): the PR pipeline from page 04.
- [`starter-files/.env.example`](starter-files/.env.example): every variable from page 02 with dev values.
- [`starter-files/CODEOWNERS`](starter-files/CODEOWNERS): review routing from pages 04 and 08.

## The ten rules, if you read nothing else

1. **Fakes by default.** Nobody calls a real vendor from a laptop unless they are working on that vendor; `FORONE_FAKE_VENDORS=1` is the default and every fake call is still priced.
2. **Prompts are code.** A file, a version, an eval run, a reviewer who is not the author. No prompt editor in the admin UI.
3. **Synthetic learners everywhere.** Dev, staging, cassettes, canaries and load tests use invented people. Real learners live in prod and nowhere else.
4. **Learner text stays home.** Ids and enums may travel to Inngest, Sentry, Slack and the logs; names, transcripts, facts and audio never do, and prompts reach Langfuse only with the opt-in.
5. **Every look is logged.** A human reading learner content writes a reason the learner can read in their export.
6. **Every promise is verified by a second job.** Deletion windows are checked daily by code that does not share the doer's bugs.
7. **Every vendor call is a priced row.** Through the middleware, on the cost page, with a fallback and a degrade path in `vendors.yaml`.
8. **A deploy never cuts a call.** Drain then replace, outside the drop window, inside the release window, after a canary, with one human name on it.
9. **Every alert has a runbook; every runbook has a kill switch.** If a fix needs SQL at 05:40, the runbook gets an admin action instead.
10. **Green on day one.** CI, Terraform, the fakes and the first eval baseline exist before the first feature.

## Decisions this handbook makes that the architecture did not

| Decision | Where | Why |
|---|---|---|
| Language packages are per target language (`packages/languages/en/`), with the learner's own language in `packages/native/<lang>/` (adopted by the architecture as ADR-02) | 01 §4 | Muath's 2026-10-23 decision: no launch country or group; languages open by the gate |
| Terraform with an S3 state backend, not Terraform Cloud or CDK | 03 §3 | the most widely read code for exactly this infrastructure; one fewer processor |
| GitHub OIDC to AWS; no long-lived keys anywhere, human or CI | 03 §4 | nothing to leak |
| Eval-gate cost ceiling of $25 per PR without a label | 04 §3 | a prompt PR should not silently cost a day of the beta's budget |
| Error-preservation rate gates a recognizer before word error rate | 05 §5 | the Milestone 0 finding that STT smooths learner errors |
| Model-judged eval metrics with noise above their regression allowance are advisory, not gating | 05 §6 | a gate that fails on noise gets disabled; an advisory metric gets fixed |
| Milestone 0 fixtures beyond the 30 clips stay out of the public repository until the learner signs part 2 of the consent addendum (ADR-24.16, 24.B10) | 09 §6 | the repository is public today |
| A story without a kill switch is not done | 10 §1 | the on-call's first move is always a switch |

## Decided for Muath (ADR-24, 2026-11-12), collected from these pages

These items were open for Muath when the handbook was written. On 2026-11-12 Muath delegated them, and each is now decided in ADR-24 (`architecture/10-decision-records.md` §3). What only a person can still do is an owner action in that document's register (§10 A, `A#`); the dates below are the register's.

| Item | Page | Decision | Owner action still due |
|---|---|---|---|
| The vendor accounts, in the company's name | 07 §1 | Every processor in 07 §1 is approved (ADR-24.17) | Muath opens them from build week 1; the brand domain and the Apple and Google developer applications by 2026-11-18 (A3); Paddle by 2026-12-02 (A6) |
| The home region | 03 §2 | `eu-central-1`, final for the beta; `me-central-1` is a one-variable move only counsel can trigger; standard contractual clauses with a transfer impact assessment as the transfer basis, never consent (ADR-24.8, 24.B13) | Counsel confirms by 2026-11-17 (A1); if late, prod is built in `eu-central-1` anyway |
| Whether the Milestone 0 consent covers fixtures and the end-to-end run | 09 §6 | It does not; a two-part addendum goes to the 15 pilot learners, and a learner who does not sign is excluded (ADR-24.16, 24.B10) | Part 1 (vendor tests) signed before any pilot clip goes to a vendor; part 2 (re-onboarding and fixtures) by 2026-12-15 (A9; the pilot consent deletes pilot data by 2026-12-31, ADR-24.B28); `make fixtures` publishes nothing unsigned |
| On-call: primary in the first days, escalation at any hour, the Better Stack plan | 06 §7 | The one-engineer rota is accepted for the beta; overnight P1s are answered by the product's fallbacks and a human at the next working hour, with phone escalation for a systemic drop failure; Better Stack (about $30 a month) approved (ADR-24.12) | none |
| The brand domain | 03 §8 | One variable (`<domain>`, `APP_DOMAIN`); email codes work without it | Muath registers it by 2026-11-18 (A3) |
| The payment processor | 07 §1 #23 | Paddle as merchant of record; Stripe with Stripe Tax only if Paddle declines the account (ADR-24.4) | Paddle account under the legal entity by 2026-12-02 (A6); if late, the Stripe test-mode scaffold stays and the processor is swapped in build week 5 |
| The second engineer, and therefore the one-engineer review exception | 04 §5 | Two engineers from build start (2026-11-18) is the plan of record, with the beta opening 2027-03-17 (2027-02-17 with a third engineer); the date is re-forecast every build week; the single-engineer cut list applies from day one, except Terraform (ADR-24.11, 24.B19) | A second engineer working from 2026-11-18 (each week later moves the open a week), a third from 2026-12-01 recommended (A2); without a second engineer the date is recomputed. The review exception ends the day the second starts |
| The daily spend cap formula and the 48-hour plan window as policy | 07 §4 | Architecture 08's formula, `max(50, Σ plan.episodes_per_day × $1.00)` over learners in a trial or subscription (ADR-15), and its 48-hour plan window (08 §4.5.3), adopted as policy (ADR-24.23), inside the approved budget: fixed infrastructure $1,000 to $1,300 a month and a $2,500 Anthropic prepaid balance for the first beta month (ADR-24.13) | none |
| Anthropic zero data retention | 07 §1 #4 | Requested (ADR-24.17) | Muath sends the request by 2026-12-15 (A7) |
