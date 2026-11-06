# 02. Local development

Part of the For one engineering handbook. Written 2026-11-06 against architecture 01 §4.7 and §4.9, 08 §4.7, 09 §4.2 and 07 §4.9. The goal of this page: a new engineer runs a full day of the product on a laptop in under an hour, for free, without a single real learner's data.

## 1. Prerequisites

| Tool | Version | Why |
|---|---|---|
| Python | 3.12 (managed by `uv`) | the three Python services |
| `uv` | latest | workspace, lockfile, virtualenvs |
| Node | 22 LTS, `pnpm` 9 | `web` |
| Docker Desktop or Colima | current | dev services (section 3) |
| `ffmpeg` | 6 or later | audio mixing and the fixture adapters |
| AWS CLI v2 | current | staging access only; never needed for local work |
| `terraform` | 1.9 or later | only if you touch `infra/` |
| `gh` | current | pull requests, release approvals |

Apple Silicon is the assumed laptop. The spaCy model and the turn-detector weights download on first `make dev` (about 600 MB) into `.cache/forone/`, which is git-ignored.

## 2. First run

```
git clone git@github.com:Muath-8/for-one.git && cd for-one
cp .env.example .env            # fill nothing yet; fake vendors are the default
make dev                        # compose up, migrations, seeds, four services
open http://localhost:3000      # web
open http://localhost:8288      # Inngest dev UI
open http://localhost:8025      # Mailpit (every email the system sends)
open http://localhost:9001      # MinIO console (every object the system stores)
```

`make dev` runs, in order: `docker compose up -d`, `uv sync`, `alembic upgrade head`, `forone seed` (section 4), then `api` on 8000, `workflows` on 8001, `call-worker` in dev-dispatch mode and `web` on 3000 under one process manager (`overmind` or `honcho`; the Makefile picks whichever is installed). `make dev-stop` stops everything; `make dev-reset` drops the database and MinIO buckets and seeds again.

The first successful run ends with three synthetic learners on the Today screen, one of whom has an episode ready to play that was produced entirely from recorded fixtures. If that is not what you see, the setup is wrong and nothing else is worth doing until it is right.

## 3. Dev services (docker compose)

| Service | Image | Port | Stands in for |
|---|---|---|---|
| `postgres` | `pgvector/pgvector:pg16` | 5432 | RDS Postgres 16 with pgvector |
| `minio` | `minio/minio` | 9000, 9001 | S3 (three buckets created by the seed) |
| `inngest` | `inngest/inngest` (`inngest dev`) | 8288 | Inngest Cloud |
| `livekit` | `livekit/livekit-server --dev` | 7880, 7881, 7882/udp | LiveKit Cloud |
| `mailpit` | `axllent/mailpit` | 8025, 1025 | Resend |

No Redis, no Kafka, no Elasticsearch: the architecture keeps rate limits, outbox, alerts and measures in Postgres on purpose, so dev has nothing else to run.

SSE-C with a per-learner key works against MinIO unchanged. KMS does not exist locally: `forone.core.keys` uses a **local KMS stub** when `FORONE_ENV=dev` that wraps DEKs with a key from `.env` (`DEV_KMS_MASTER_KEY`). The stub is a separate module, `forone/core/keys_dev.py`, and the import is guarded so it cannot load outside `dev`. A unit test asserts that.

## 4. Seeds

`forone seed` is idempotent and creates:

- The language package `en` loaded into `package_versions`, voices mapped to the **fake** voice vendor, consent texts from `ui_strings/ar.yaml`.
- Three synthetic learners (`synth-L01` to `synth-L03`) built from the Milestone 0 learner-file template, with different levels (A2+, B1, B1+), different interests and planted error patterns, each with a `learner_schedule` row that drops at "five minutes from now" so you can watch the daily loop run.
- One staff account per role (`owner@dev.local`, `engineer@dev.local`, `reviewer@dev.local`, `tagger@dev.local`, `ops@dev.local`); the OTP for any dev account is printed to the console and to Mailpit.
- Twelve invite codes, one sample request, a `price_book` loaded from `prices.yaml`, `vendor_config` with `spend_mode = normal`, and feature flags at their defaults.
- A seven-day backfill of `measure_points` from the synthetic learners' fake sessions so `/admin/measures` is not empty.

Seeds never contain a real person. The fifteen Milestone 0 learner files are **not** seeds; they are eval fixtures (handbook 05) under consent and live in `eval/fixtures/learners/` with tokenized names, and they are loaded only by `tools/eval`, never by `forone seed`.

## 5. Mock providers: the fake vendors

The single most important dev habit: **nobody runs real vendors from a laptop by default.** `FORONE_FAKE_VENDORS=1` is set in `.env.example` and swaps every adapter in `forone.adapters` for a recorded-fixture adapter from `forone/adapters/fake/`. The real adapters are selected only when the variable is unset and the vendor key is present.

How the fakes work:

| Capability | Fake behaviour | Fixture source |
|---|---|---|
| `TextModel`, `BatchTextModel` | Returns the recorded completion for a hash of (role, prompt_version, input slots); on a miss, returns a deterministic template completion that satisfies the schema (a valid script of the right length with the words from the brief) and logs `fake_miss` | `eval/fixtures/cassettes/text/<role>/<hash>.json` |
| `SpeechSynth`, `StreamingSpeechSynth` | Returns a pre-rendered clip per character from the fixture set, time-stretched to the character count, with sentence timings synthesized from word count; the voice is recognizably a placeholder so nobody mistakes it for the real host | `eval/fixtures/cassettes/tts/<character>.ogg` |
| `StreamingRecognizer` | Plays back a scripted learner turn list for the synthetic learner (the caller profile from handbook 05 §6) with realistic partials and end-of-turn timing | `eval/fixtures/learners/<id>.caller.json` |
| `VerbatimRecognizer` | Returns the hand-written verbatim text for that turn, including the planted errors | same |
| `Pronunciation` | Returns a fixed score with jitter seeded by turn id | code |
| `Aligner` | Word timings from character count at 830 characters a minute | code |
| `Embeddings` | A 1536-dim hash embedding, cosine-stable for identical text | code |
| LiveKit | The real dev server; the fake worker still joins a room so the call screen is exercised | compose |
| Resend, web push | Mailpit; push logged to console | compose |

Every fake call still goes through the **tracing middleware** and writes a `vendor_calls` row priced from `price_book`, with `vendor = 'fake:<real vendor>'`. The cost dashboard therefore works in dev and shows what the session *would* have cost. This is deliberate: an engineer sees the price of a prompt change before it ever runs for real.

**Recording a cassette.** When a fixture is missing or stale (a prompt version changed), run the step once against the real vendor with `make record ROLE=writer LEARNER=synth-L02`. This sets `FORONE_FAKE_VENDORS=record`, calls the real adapter, writes the cassette, and prints the cost. Cassettes are committed. Record only with synthetic learners; a cassette recorded from any real learner's brief is a data-handling violation (handbook 09).

**Running real vendors locally** is allowed for vendor work (a new adapter, a voice test) with these limits, enforced by the middleware when `FORONE_ENV=dev`: `SPEND_CAP_USD_PER_DAY=20` per developer key, `pricing: standard` only (no batch from a laptop), and a console warning on every real call. Each engineer has their own vendor keys with their own caps (handbook 07); the production keys are never on a laptop.

## 6. Environment variables

The complete list with owner, scope and dev default. The owner is who holds the real value; "engineer" means any engineer can mint one for themselves. `.env.example` (in `engineering/starter-files/`) mirrors this table and is the file to update when a variable is added; CI fails if `Settings` declares a field that is not in `.env.example`.

| Variable | Used by | Dev default | Owner of the real value |
|---|---|---|---|
| `FORONE_ENV` | all | `dev` | infra (per environment) |
| `FORONE_SERVICE` | python image | set by the process manager | infra |
| `FORONE_FAKE_VENDORS` | adapters | `1` | engineer; always unset in staging and prod |
| `HOME_REGION` | infra, S3, KMS | `local` | Muath (pending counsel, architecture 01 §10 #1) |
| `CALL_WORKER_REGION` | call-worker placement | `local` | infra |
| `DATABASE_URL` | api, workflows | compose postgres | infra (Secrets Manager) |
| `DATABASE_URL_READONLY` | admin measures pages | compose postgres, `forone_readonly` | infra |
| `S3_ENDPOINT_URL` | all | `http://localhost:9000` | unset outside dev |
| `S3_BUCKET_MEDIA`, `S3_BUCKET_VOICE`, `S3_BUCKET_EXPORTS` | api, workflows, call-worker | `forone-media-dev` etc. | infra |
| `KMS_KEY_ID`, `MEDIA_SERVICE_KMS_KEY_ID` | api, workflows | unset (stub) | infra |
| `DEV_KMS_MASTER_KEY` | keys_dev only | generated by `make dev` | engineer; dev only |
| `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `INNGEST_BASE_URL` | api, workflows | dev server values | infra (Inngest Cloud env) |
| `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` | api, call-worker | `ws://localhost:7880`, `devkey`, `secret` | infra (LiveKit Cloud project) |
| `INTERNAL_JWT_SIGNING_KEY` | api, call-worker | generated | infra |
| `VENDOR_CONFIG_PATH` | adapters | `packages/adapters/vendors.yaml` | repo |
| `ANTHROPIC_API_KEY` | workflows, call-worker | empty | Muath opens the org; engineer keys per person with caps |
| `GOOGLE_API_KEY` | workflows | empty | same |
| `ELEVENLABS_API_KEY`, `INWORLD_API_KEY` | workflows, call-worker | empty | same |
| `SONIOX_API_KEY`, `DEEPGRAM_API_KEY`, `ASSEMBLYAI_API_KEY` | call-worker, workflows | empty | same |
| `SPEECHACE_API_KEY` | workflows | empty | same |
| `OPENAI_API_KEY` | workflows (embeddings only) | empty | same |
| `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST` | all python | empty (tracing to Postgres only) | infra; EU host |
| `SENTRY_DSN` | all | empty | infra |
| `RESEND_API_KEY`, `EMAIL_FROM` | api, workflows (messaging only) | Mailpit, `show@dev.local` | infra |
| `VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY`, `VAPID_SUBJECT` | api, workflows (messaging only) | generated by `make dev` | infra |
| `TURNSTILE_SECRET`, `RATE_LIMIT_SALT` | api | test keys from Cloudflare docs, random salt | infra |
| `PAYMENTS_PROVIDER`, `PAYMENTS_SECRET`, `PAYMENTS_WEBHOOK_SECRET` | api | `stripe`, test keys | Muath (processor decision 2026-11-16) |
| `APPLE_CLIENT_ID`, `APPLE_TEAM_ID`, `APPLE_KEY_ID`, `APPLE_PRIVATE_KEY` | api | empty (Apple sign-in disabled in dev) | Muath (Apple Developer Program) |
| `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET` | api | empty | Muath (Google Cloud project) |
| `SESSION_SECRET`, `COOKIE_DOMAIN` | api | generated, `localhost` | infra |
| `RESEARCH_PSEUDONYM_SECRET` | workflows (anonymize) | generated | infra; rotated never (rotation breaks pseudonym stability) |
| `SPEND_CAP_USD_PER_DAY`, `SPEND_CAP_SAMPLE_USD_PER_DAY`, `SPEND_CAP_PILOT_USD_PER_DAY`, `SESSION_COST_ALERT_USD`, `ONBOARDING_STARTS_PER_DAY` | adapters, api | `20`, `5`, `5`, `1.00`, `20` | Muath sets policy; infra sets values |
| `ADMIN_IP_ALLOWLIST` | api | empty (allow all in dev) | infra |
| `BETTERSTACK_TOKEN`, `SLACK_OPS_WEBHOOK` | ops | empty (page to console) | infra |
| `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_LIVEKIT_URL`, `NEXT_PUBLIC_VAPID_PUBLIC_KEY`, `NEXT_PUBLIC_TURNSTILE_SITE_KEY` | web | localhost values | infra (Vercel) |

`Settings` in `forone.core.settings` is the only reader of `os.environ`. Any `os.environ[...]` elsewhere fails Ruff.

## 7. Everyday commands

| Command | Does |
|---|---|
| `make test` | unit tests for every package with fake vendors, under a minute |
| `make test-int` | integration tests against compose (RLS walk, migrations up and down, Inngest payload test) |
| `make lint` | Ruff, Pyright, import-linter, eslint, tsc, the package validator |
| `make eval SUITE=writer` | run one offline suite locally (costs money if cassettes miss; prints the estimate first and asks) |
| `make record ROLE=... LEARNER=synth-...` | record a cassette against the real vendor |
| `make day LEARNER=synth-L02` | fire `day/next` for one learner now and tail the Inngest run |
| `make call LEARNER=synth-L02` | start a call with the scripted caller against the local worker |
| `make migrate NAME=add_x` | new Alembic revision; `make migrate-check` asserts it is additive |
| `make fixtures` | pull large fixtures from the fixtures bucket (needs staging AWS access) |
| `make costs` | print yesterday's dev cost per session from `vendor_calls` |

## 8. Working on `web` alone

`pnpm dev` in `apps/web` with `NEXT_PUBLIC_API_URL` pointing at `https://staging.forone.app` is allowed for pure UI work and needs a staging staff account (handbook 03 §6). It is never pointed at prod.

## 9. Things that are different on purpose

- Dev uses `pricing: standard` everywhere; batch exists only in staging and prod. A dev run therefore over-estimates cost by about the batch saving; `make costs` prints both numbers.
- Dev's drop window is "five minutes from now", not 05:30 Riyadh; `learner_schedule` is seeded that way and `day/next` honours it.
- The call worker in dev answers in under a second because the fake host is a lookup. Latency work is done on staging with `tools/call-bench`, never on a laptop.
- Emails are never sent; Mailpit shows them. Pushes are logged. There is no way to reach a real inbox from dev, by construction (`forone.core.messaging` refuses a non-Mailpit host when `FORONE_ENV=dev`).
