# 01. Repository layout

Part of the For one engineering handbook. Written 2026-11-06 against architecture 01 §4.1 (monorepo), 08 §4.7 (adapters), 09 §4.3 (versions) and the decisions of 2026-10-23. Where this page and an architecture document differ, this page is the newer word and says why.

## 1. One repository, four deployables

For one is one Git repository, `Muath-8/for-one`, holding product documents and code side by side. The code is a monorepo with four deployable services and eight internal packages. The reason is the team size: one to two engineers plus Muath cannot keep several repositories in step, and every change that touches a prompt, an adapter and a test must land as one pull request so the eval gate can judge it as one change.

| Deployable | Directory | Runtime | Hosted on |
|---|---|---|---|
| `web` | `apps/web/` | Next.js 15 App Router, TypeScript, PWA | Vercel |
| `api` | `apps/api/` | FastAPI, Python 3.12 | ECS Fargate |
| `workflows` | `apps/workflows/` | FastAPI serving Inngest functions | ECS Fargate |
| `call-worker` | `apps/call-worker/` | LiveKit Agents worker, Python 3.12 | ECS Fargate |

The three Python services build into **one Docker image**, `forone-python`, with the entrypoint chosen by `FORONE_SERVICE`. One image means one build, one scan, one set of baked-in weights (ffmpeg, the spaCy English model, the LiveKit multilingual turn detector, Silero VAD) and one thing to roll back.

## 2. The tree

```
for-one/
├── README.md                      what this is, how to run it in ten minutes (links to engineering/02)
├── CODEOWNERS                     see engineering/starter-files/CODEOWNERS
├── pyproject.toml                 uv workspace root; shared Ruff and Pyright config
├── uv.lock
├── package.json / pnpm-workspace.yaml   web only
├── Makefile                       dev, test, lint, eval, release targets (thin wrappers; logic lives in tools/)
├── .env.example                   see engineering/starter-files/.env.example
├── .github/
│   ├── workflows/                 ci.yml, deploy-staging.yml, deploy-prod.yml, nightly.yml
│   ├── pull_request_template.md
│   └── dependabot.yml
├── apps/
│   ├── web/                       Next.js; no business logic; talks only to api
│   ├── api/                       routers/, auth/, feed/, media/, admin/, onboarding/, main.py
│   ├── workflows/                 functions/ (one file per Inngest function), main.py
│   └── call-worker/               agent.py, governor/, audio/, main.py
├── packages/                      importable Python packages, namespace `forone.*`
│   ├── core/                      forone.core: settings, db, models, events, keys, media, outbox, messaging, ratelimit, audit, guard, ops.log
│   ├── adapters/                  forone.adapters: interfaces, one module per vendor, vendors.yaml, prices.yaml, tracing middleware, fake/
│   ├── pipeline/                  forone.pipeline: teacher, writer, fitter, editor, voice studio, glosses
│   ├── learner/                   forone.learner: event log, stores, briefs, pii classification
│   ├── assess/                    forone.assess: verbatim, analyst, classifier, measures, updater, claim gate
│   ├── measures/                  forone.measures: every 16.1/16.2 number as versioned SQL
│   ├── eval/                      forone.eval: suites, checks, scoring, synthetic learners
│   ├── ops/                       forone.ops: alerts loader, paging, canary, logscrub
│   └── languages/                 language packages (section 4)
│       ├── _shared/               schema for a package; validation; loader
│       └── en/                    the first target language: bibles, voices, inventory, lists, prompts, consent texts
├── ui_strings/                    learner-language UI copy (ar first), keyed; loaded by web and api
├── eval/
│   ├── suites.yaml                named suites (09 §4.2)
│   ├── thresholds.yaml            floors, ceilings, allowed regression per metric
│   ├── fixtures/                  learners/, scripts/, editor/, transcripts/, clips/, recordings/, facts/, notes/, pii_corpus.jsonl
│   └── baselines/                 the last accepted run per suite, committed
├── ops/
│   ├── alerts.yaml                every alert rule as SQL plus runbook link
│   ├── oncall.yaml
│   └── runbooks/                  R1..R12 plus handover.md, incident.md
├── infra/
│   ├── terraform/                 modules/ (network, rds, s3, kms, ecs, alb, iam, secrets) and envs/{staging,prod}
│   └── docker-compose.yml         dev services
├── tools/
│   ├── vendor-lab/                run clips and scripts through adapters; comparison tables
│   ├── call-bench/                50 scripted calls against staging
│   ├── cost-model/                assumptions.yaml and the recompute script
│   ├── eval/                      CLI front for forone.eval
│   ├── release/                   cut, approve, drain-replace, rollback
│   └── import_m0.py               Milestone 0 learner files and tags into fixtures and events
├── docs/                          ropa.md (processor register), adr/ (architecture decision records)
├── architecture/, perspectives/, milestone-0/, features/, design/, engineering/   the product and design documents (already in the repo)
```

## 3. Naming rules

- **Python packages** are namespaced `forone.<package>` and live in `packages/<package>/forone/<package>/`. Import across packages only downward: `core` imports nothing of ours; `adapters` imports `core`; `pipeline`, `learner`, `assess` import `core` and `adapters`; `measures`, `eval`, `ops` import anything; apps import packages and never each other. A Ruff `banned-api` rule and an import-linter contract enforce this.
- **Inngest functions** are files named after the function id with slashes replaced by underscores: `day/next` lives in `apps/workflows/functions/day_next.py`. The function id is the single source of truth and appears in the file's first line.
- **Events** are `snake_case` nouns past tense or noun phrases as architecture 01 §4.3 lists them (`episode.failed`, `call.turn_audio_ready`). Every event model is a Pydantic class in `forone.core.events` and nowhere else.
- **Tables** are plural snake_case; every learner-scoped table has `learner_id` as its first foreign key; migrations are Alembic revisions named `YYYYMMDD_HHMM_<slug>.py`.
- **Prompts** are files, never strings in code (section 5).
- **Adapters** are `forone/adapters/<vendor>.py`, one class per capability the vendor offers, registered in `forone/adapters/registry.py`. The vendor name in the file, the class, `vendors.yaml` and `prices.yaml` is the same lowercase token (`anthropic`, `google`, `elevenlabs`, `inworld`, `soniox`, `deepgram`, `assemblyai`, `speechace`, `openai`, `livekit`). The schema for `vendors.yaml` rejects `hume`.
- **Branches** are `<type>/<short-slug>` (`feat/`, `fix/`, `prompt/`, `infra/`, `docs/`); `main` is protected. Tags are `vYYYY.MM.DD-N`.
- **Feature flags** are `area.flag_name` (`talkback.enabled`, `pipeline.editor_model`); a flag never guards a product law.
- **Environment variables** are `UPPER_SNAKE`, prefixed `FORONE_` only for the handful that select behaviour of the image itself (`FORONE_ENV`, `FORONE_SERVICE`, `FORONE_FAKE_VENDORS`); vendor keys keep the vendor's own conventional name.

## 4. Language packages: a change from the architecture documents

The architecture documents (written 2026-10-16) name one package, `packages/package_ar_en/`, because at that time the product was Arabic-speaking learners of English. On 2026-10-23 Muath decided there is no launch country or learner group, and that target languages open one by one through the five-check gate in concept v2 §8. The code must therefore treat the target language and the learner's own language as two separate axes from day one, even though the pilot is English only.

- `packages/languages/<target>/` holds everything a model sees about the **target language**: host and producer bibles, voice ids per vendor, structure inventory, word lists, ban list, the prompts (section 5), crisis keywords and resources, and the gate evidence file `gate.yaml` that records the five checks and their dates. `en` is the only package in the beta.
- `ui_strings/<learner_language>.yaml` holds what the **learner reads in their own language**: Salma's UI copy, consent texts, the privacy notice, the three message kinds. `ar` ships first. Consent texts and the privacy notice keep their version numbers inside this file because counsel edits them.
- Nothing in `apps/` or `packages/` other than the loader may contain a language code literal. A unit test greps for `"en"`, `"ar"` string literals outside `packages/languages/` and `ui_strings/` and fails on a hit.

This is the one place the handbook knowingly departs from architecture 01. Record it as ADR-0001 in `docs/adr/` when the repo is scaffolded.

## 5. Where generated prompts live

Every prompt, rubric, rule table and threshold a model sees is a **file in the language package**, versioned in `packages/languages/en/versions.yaml` (architecture 09 D7). The layout:

```
packages/languages/en/
├── versions.yaml              prompt_version per artifact; bumped by hand in the PR that changes the file
├── prompts/
│   ├── teacher_system.md      the teacher's system prompt; frontmatter: role, model class, cache_prefix markers
│   ├── writer_system.md
│   ├── fitter_tagging.md
│   ├── editor_rubric.md
│   ├── host_system.md
│   ├── salma_live.md
│   ├── salma_notes.md
│   ├── chat_host.md
│   ├── analyst_full.md / analyst_fast.md
│   ├── memory_keeper.md
│   ├── proof_producer.md
│   └── rater.md               pinned per four-week window; the eval-gate refuses a bump inside the window
├── bibles/                    show bible, host bibles, Salma's bible (the writers' files, Markdown)
├── rules/                     structure_rules.yaml, law_words.yaml, ban_list.yaml, crisis_keywords.yaml
├── voices/                    voices.yaml: one entry per character per vendor
└── gate.yaml                  the five-check language gate evidence
```

Rules that follow from this:

1. A prompt file has a Markdown body and a YAML frontmatter with `role`, `model_class` (`opus`, `sonnet`, `haiku`, `gemini-flash`), `cache_prefix_ends_at` (a marker string; everything above it is the cached prefix and must not contain per-learner text), and `inputs` (the named slots the pipeline fills). The loader fails at import time if a slot in the body is not declared.
2. **Per-learner text is never written into a prompt file.** It enters through the slots, wrapped by `forone.core.guard.listener_said()` (architecture 07 D10).
3. Prompt text assembled at runtime (the brief, the call brief, the notes selection) is built by code in `forone.pipeline` or `forone.assess` from the file plus the learner's rows. The assembled text is stored in the learner's own rows (`pipeline_steps.prompt_ref`, `calls.brief_ref`) in the home region, never in a shared store, and goes to Langfuse only for learners with `data_use = true`.
4. **The Milestone 0 prompts** in `/milestone-0/05-prompts.md` are the seed. Week 1 of the build moves each one into its file under `prompts/` with version `1.0.0` and a frontmatter note `origin: milestone-0/05-prompts.md §x`. They are not edited in place in the kit; the kit stays as the historical record.
5. A change to any file under `prompts/`, `rules/` or `versions.yaml` triggers the eval gate (handbook 04 and 05) and requires a reviewer who is not the author (handbook 08).
6. The admin UI has no prompt editor. Pipeline D17 forbids it and this handbook keeps it forbidden.

## 6. What does not go in the repository

Secrets of any kind (handbook 03 and 07); learner data, including de-identified fixtures that are not covered by the Milestone 0 consent (handbook 09); audio files larger than the 30 consented clips (fixtures over 5 MB live in the `forone-fixtures` S3 bucket and are fetched by `make fixtures`); build outputs; the architecture pages' HTML is kept because it is a document, but regenerated HTML must be committed with the Markdown that produced it.

## 7. Scaffolding order (build week 1, day 1)

1. `uv init --workspace` at the root; `packages/core` first with `Settings`, the logger and the database session; a hello-world `api` with `/healthz`.
2. `infra/docker-compose.yml` from architecture 01 §4.9; `make dev` brings it up.
3. `packages/adapters` with the `Protocol` interfaces, the tracing middleware, `vendors.yaml`, `prices.yaml`, and the `fake/` recorded-fixture adapters (handbook 02 §5).
4. `packages/languages/en` with the Milestone 0 prompts moved in (section 5).
5. `.github/workflows/ci.yml` from `engineering/starter-files/ci.yml`, green on the empty tree before any feature lands.
6. `infra/terraform` with the staging environment; the first `deploy-staging.yml` run.

A repository where CI is green on day one stays green; one where CI arrives in week 3 never does.
