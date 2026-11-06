# System topology, services and infrastructure

Domain 1 of 9 of the For one technical architecture. Written 2026-10-16, revised 2026-10-17 after design review, and revised again 2026-11-06 against the 2026-10-23 decisions (decisions.md), the second review pass and [10-decision-records.md](10-decision-records.md) (the ADRs cited below as ADR-NN). First written against PRD-v2 (Implementation PRD v3.0, 2026-10-10), concept-v2 sections 7 to 10, decisions.md, the AI-architecture and business-launch lenses, the Milestone 0 production kit, and the eight sibling architecture documents (02 to 09). "PRD x.y" means PRD-v2 part x.y. Tags: [DECISION] decided here; [ASSUMPTION] assumed because the spec is silent; [OPEN for Muath] only the owner can settle.

The document answers one question: what runs where, so that a team of one to two engineers plus Muath can ship every P0 item between 2026-11-18 and 2026-12-22 and then grow the same system from 15 learners to 10,000 without a rewrite.

What changed in this revision, in one paragraph: the 2026-10-17 revision applied the two design reviews (metadata-only tracing, the scene-1 gate, the waitlist and invite tables, the 15-minute rule on every learner-voice object, the `day/next` lead-time rule, the `call-worker` drain, the corrected cost arithmetic and the two-engineer build plan), and this pass verified each of those findings is in place and applied the cross-domain rulings of 10-decision-records: there is no launch country, so the learner row carries `native_language`, `target_language`, `residence_country` and `tz`, the language package splits into `packages/languages/<target>/` and `packages/native/<lang>/`, the home region defaults to `eu-central-1` with `me-central-1` as the alternative, and operations run round the clock with a release window computed from `learner_schedule` (ADR-02, 08, 16, 20); three USD plans set `plan.episodes_per_day`, episodes 2 and 3 are made on request through `POST /v1/episodes/next` as `daily_extra` (ADR-04, 05); Salma's notes, the notes door and `notes.ready` are gone and the after-session pass is one function (ADR-06); every date moves 16 days to the build of 2026-11-18 to 12-22 and the beta from 2026-12-23 (ADR-07); produced show audio moves to SSE-KMS under the environment key so it can be served by presigned URLs while learner voice stays SSE-C (ADR-12); `vendor_calls` rows get their own transaction, the DEK cache is 60 s and versioned, the Langfuse `user_id` is a `research_pseudonyms` row, and `forone_admin` serves the admin pages (ADR-13, 17, 18, 09); the payment model is a merchant-of-record processor with the processor still open (ADR-21); staging stays up through the beta and the fixed-infrastructure figure becomes about $1,000 to $1,300 a month (ADR-16).

---

## 1. Summary and the decisions in one table

The system is four deployable services and eight managed services. Everything that is not live runs as a durable Inngest function; everything live runs in one LiveKit Agents worker; everything stateful lives in one Postgres database and three S3 buckets in one home region. Every vendor is behind a thin adapter, chosen by a config file, with two voice vendors wired from day one.

| # | Decision | Chosen | Reason in one line | Rejected |
|---|---|---|---|---|
| 1 | Backend language | **Python 3.12** (FastAPI, Inngest Python SDK, LiveKit Agents) | The assessment domain needs spaCy, ERRANT-style rules and wordfreq; the call needs the LiveKit reference SDK with Anthropic, Soniox and turn-detector plugins; the M0 prompts move into Python modules unchanged | TypeScript everywhere (no NLP libraries, LiveKit Node plugins lag); two backend languages (team too small) |
| 2 | Web app | **Next.js 15 (App Router, TypeScript)** on Vercel, installable PWA, no business logic | Boring, documented, SSR for the landing page served per `Accept-Language` with `dir` and `lang` from the native package (ADR-02), PWA tooling (Serwist), one-person shippable; all logic stays in the API | Vite SPA (no SSR landing), React Native (PRD 1.4: native after the beta) |
| 3 | Services | `web`, `api`, `workflows`, `call-worker` | Four deployables is the smallest number that separates the three runtime shapes: request/response, long durable steps, long-lived real-time process | One monolith (Inngest steps and LiveKit workers cannot share a process shape); microservices per role (eleven architects, two engineers) |
| 4 | Durable workflow engine | **Inngest Cloud (EU)**, Python SDK, served from `workflows` | PRD 14.3 default; managed; `sleep_until`, `wait_for_event`, `cancel`, debounce and idempotency map one-to-one onto the daily loop | Temporal Cloud (more operations; a rewrite of the shells if adopted later, section 8); Celery/Redis (no durable timers or waits) |
| 5 | Live call | **LiveKit Cloud** SFU plus our own `call-worker` on ECS Fargate | PRD 14.3 default; managed media, multilingual turn detector, dispatch API | Self-hosted LiveKit (operations), Pipecat (English-only turn model), speech-to-speech models (no verbatim transcript, no shared voice) |
| 6 | Database | **Amazon RDS for PostgreSQL 16** with pgvector, one instance, one database, **Multi-AZ from the first prod deploy** | PRD 14.3; one place for the event log, the stores, the episodes and the schedule; row-level isolation by `learner_id`; Multi-AZ costs about $120 a month more than one lost morning of drops for 50 paying learners | Supabase/Neon (auth and storage would pull PII into another processor; no pgaudit and no `me-central-1` option if counsel chooses it), Aurora Serverless (cost floor, no benefit at beta scale), DynamoDB (the model is relational); single-AZ until 2027-01-26 (section 10 #4 prices it if Muath prefers it) |
| 7 | Object storage and keys | **S3**, three buckets; **learner-voice kinds under SSE-C with a per-learner data key (DEK)** wrapped by one KMS key, **produced show kinds under SSE-KMS with the environment key** and served by 10-minute presigned URLs (`media_objects.encryption in ('sse_c_learner','sse_kms_env')`, ADR-12); **the call worker receives only a per-call key derived from the DEK** | Per-learner key deletion deletes the voice (PRD 12.6) at $1/month total instead of $1/learner/month; S3 does Range reads natively; SSE-C can never be served by a presigned URL, a CDN or `<audio src>`, so locking show audio behind `api` bandwidth was an accident of the first draft; the most exposed service never holds the key that protects every recording the learner ever made | KMS key per learner (cost), app-side encryption (no Range support without chunking code), everything SSE-C (the 2026-10-17 revision), everything SSE-KMS (loses "key deletion deletes the voice"), handing the raw DEK to the worker (the first draft) |
| 8 | Home region | **AWS `eu-central-1` (Frankfurt) by default** for RDS, S3, KMS, Fargate; Vercel `fra1`; Inngest and Langfuse in their EU regions holding pointers and metadata only; **`me-central-1` (UAE) is the alternative**, a one-day config move (`HOME_REGION`) as late as the Terraform apply in build week 1; the final choice is [OPEN for Muath, with counsel] (ADR-08; 10-decision-records §10 item 1) | With no launch country the cohort is worldwide: EU and UK learners' data in the UAE is a transfer without an adequacy decision, while the same data in Frankfurt needs only the AWS DPA; the US vendor transfers are the same in every option; latency does not decide it because no database sits on the call's turn path (3.6) | `me-central-1` as the default (the first draft, chosen for one country); GCP `me-central2` Dammam (only if counsel requires in-country data at rest for one regime; 5 to 8 engineer-days, not a config change); a region per learner (two of everything for a two-engineer team) |
| 9 | Hosting of services | `web` on Vercel; `api`, `workflows`, `call-worker` as containers on **ECS Fargate** behind one ALB with WAF; `/internal/*` reachable only from the VPC | No Kubernetes; the three Python services share one image and one deploy path; Fargate autoscales the call worker on CPU with scale-in protection while calls run | Vercel-only (no long-lived call process, step timeouts), Fly.io/Render (no VPC-only listener for `/internal/*`, no `me-central-1` option if counsel chooses it), EKS (operations) |
| 10 | Vendor adapters | One Python package `forone.adapters` with one interface per capability, selected by `vendors.yaml` plus a `vendor_config` table for same-day failover; the writer/editor vendor-pair rule enforced at selection time | PRD 14.3 "a swap is configuration"; the table lets an on-call person fail over without a deploy; PRD 6.1 and 14.3 require the editor to be from a different vendor than the writer in every configuration, including failover | Hard-coded clients per role; an agent framework (PRD 14.3 forbids) |
| 11 | Scheduling the daily loop | One Inngest run per learner per active day (`day/next`) that waits for the pick, falls back at the cutoff, escalates to on-demand pricing at drop minus 90 min, drops at the drop time, and publishes late (without a push) if the episode arrives after the drop; minimum lead time 7 h, otherwise standard pricing from the start | Per-learner local time with no cron tables; an inactive day starts no run, which is exactly PRD 3.6 rule 2 | A global cron that scans all learners every minute (drift, double-sends, no per-learner wait) |
| 12 | Auth | Email one-time code, Apple, Google via **Authlib + our own OTP** in the API; sessions as HttpOnly cookies on `.forone.app`; staff sign in through the same OTP path against `staff_accounts` (07 §4.13) | Accounts and PII stay in our Postgres in the home region (PRD 12.6); the admin surface names a person, not a shared password | Clerk/Auth0 (learner PII in a US processor, per-MAU cost); basic auth plus IP allowlist for `/admin` (the first draft; no MFA, no individual identity, and the on-call's phone IP changes) |
| 13 | CI/CD | GitHub Actions; Vercel Git integration for `web`; Docker image to ECR and ECS rolling deploy for `api` and `workflows`; a drain-then-replace deploy for `call-worker`; Alembic migrations as a deploy job | One pipeline a single engineer can read end to end; a call is never cut by a deploy | ArgoCD/Flux, separate build systems per service |
| 14 | Environments | `dev` (docker compose), `staging` (one small copy of prod in the same account, **up from build week 2 through the beta**, ADR-16), `prod` | Staging is where the 50 scripted calls, the canaries, the `eval-gate` runs and the M0 end-to-end run happen, and with learners in every timezone there is no quiet window in which to stop it; about $260 a month, carried into section 6 and 10-decision-records §10 item 9 | Preview environments per PR for the backend (cost and time); stopping staging between test windows (the 2026-10-17 revision; saved about $180 a month and cost a day of stand-up before every test) |
| 15 | Tracing data | Langfuse Cloud EU receives **metadata only** by default (ids, model and prompt versions, token counts, cost, latency, a hash of the prompt); prompt and completion text stay in the learner's own rows in the home region with the span id as pointer; text goes to Langfuse only for learners with `data_use = true`, after `anonymize()`; `user_id` is the research pseudonym from `research_pseudonyms`, never the learner id; 30-day retention (this decision now binds every domain, ADR-09) | PRD 1.3 #8 and 12.5.5: learner text may leave the system for "checking and improving the teacher" only with the opt-in; debugging reads the text from Postgres by span id under RLS | Full prompts and completions for every learner in Langfuse (the first draft; a hard-constraint breach); self-hosting Langfuse (operations) |
| 16 | Allowance and extra episodes | `plan.episodes_per_day` (1, 2 or 3 from `plans.yaml`: `one_a_day` $19.99, `two_a_day` $29.99, `three_a_day` $44.99) new episodes per learner-local day, enforced in `api`; episode 1 is the drop made by `day/next` and the batch pipeline; episodes 2 and 3 are made when the learner asks (`POST /v1/episodes/next`, a button after the current episode ends, never autoplay) through the on-demand path as `episode_kind = daily_extra`; `day/next` inserts the day's rows in state `planned` so the nightly teacher run plans all of them (ADR-04, ADR-05) | Typical use is 50 to 60% of the allowance, so pre-producing everything would spend about a third of the voice line on episodes nobody asks for; the on-demand path already meets 30 s | Pre-producing the full allowance; a "next episode" feed (law 11); SAR founding year and a yearly plan (PRD-v2 1.4) |
| 17 | Operations clock | No protected hour and no timezone-fixed job: every rule is relative to each learner's `drop_at`; `tools/release` computes the deploy window from `learner_schedule` (deploy only when under 2% of learners have a drop in the next 45 min, `call-worker` only when idle) and the check is binding; hourly crons over learner-local days that closed (ADR-16) | Learners anywhere means drops at every hour; a Riyadh-centred window would cut someone's morning | A Riyadh-centred rota and release window (the first two drafts) |

---

## 2. Requirements this domain implements

| Requirement | PRD | What it binds here |
|---|---|---|
| Invite-only access from the waitlist; invites in batches of about 50 a week from 2026-12-23 (weekly on the beta's weekday, `cohort_key = invite_date`, ADR-19); each invite carries the waitlist answers into onboarding | 1.4 Access, 2.1.5, 2.1.6, 19.3 | `waitlist` and `invites` tables (4.2); `POST /v1/onboarding/start` requires an unredeemed invite code; `/admin/invites` sends a batch; the answers are copied into the `pre_account` learner's intake facts so Salma does not ask them again |
| Installable web app plus a private podcast feed per learner, web push, Screen Wake Lock, Media Session | 1.4, 3.3, 5.1 | `web` is a PWA; `api` renders the feed (with directory-exclusion tags) and serves media with Range support; VAPID push from `forone.core.messaging` in `api` and `workflows` |
| Sample episode streamed within 30 s, cost under $0.05, one per device/phone/email per 24 h; the learner's to keep and forward | 2.1, 15 | The pipeline's sample path in `episode/produce`, started by `sample.requested {sample_id}`; `sample_requests` enforces the limits and holds the share token; sample audio lives under a service key in `forone-media/samples/` and is served at `GET /s/{share_token}.mp3` for 30 days (3.6, 4.2) |
| First sound under 60 s, pilot under 45 s, call 60 to 90 s, account after the call; Talk or Type at A2 | 2.2, 15 | Onboarding runs anonymously under a `pre_account` learner row with a 24 h lifetime and `voice_storage = false` semantics; A3 runs as a LiveKit call on `call-worker` or as a typed exchange through `api` (`POST /v1/onboarding/{id}/messages`); the pipeline supports `mode: pilot` on on-demand pricing |
| `plan.episodes_per_day` new episodes per active day (ADR-04): the first by the drop, with the cutoff at drop minus 6 h and batch with on-demand fallback at drop minus 90 min; episodes 2 and 3 on request (ADR-05); one swap; return episode after 5 days; gap note once | 3.1, 3.2, 3.6 as amended by decisions.md §2, 3.8 | `day/next`, `episode/produce`, `gap/note` functions; the allowance (`episodes_today < plan.episodes_per_day`) enforced in `api` on `POST /v1/episodes/next`; return detection on app open or feed-link exchange only, never on a feed poll |
| Exactly three outbound message kinds | 3.10 | `forone.core.messaging` is the only module that holds the Resend client and the VAPID keys; it exposes exactly three senders (`drop_notification`, `gap_note`, `transactional`) with a closed enum of transactional kinds; a lint and a unit test fail the build on any other caller or kind. Two kinds the PRD's table lacks (`retention_warning` from 12.5.9 and `invite` from 2.1.6) are added as transactional and flagged in section 10 #10 for a PRD amendment |
| Session and door state model; one open session; close on next publish; the doors are listen, shadow, read, call, chat, round two and the small door (no notes door, ADR-06) | 4, decisions.md §3 | `sessions`, `doors` tables; a session closes when the learner first opens the next `pilot`, `daily`, `swap` or `return` episode, or at that episode's drop time at the latest; `proof` and `finale` episodes never close a session (3.4) |
| Durable pipeline steps with timeouts and retries; fallback episode; page a human after 3 fallbacks in 7 days; no audio plays before the gate passes on it | 6.1, 6.3, 14.3 | Inngest step config; `episode.failed` and `pipeline.human_page` events; on streaming kinds the model checks run on scene 1 before `episode.streaming_started` (3.6) |
| Live roles never write to the stores; only after-session roles write; the event log is append-only | 8.1, 14.2 | `call-worker` appends to `events` only through `api`; `api` and `workflows` append through `forone.core.events.append()`; nothing updates an event (the verbatim result is a second event, `call_turn_verbatim`, 04 D2); store writes happen only in `workflows`, except learner-authored edits applied synchronously by `api` (04 D5) |
| Append-only event log with model, prompt versions and cost on every event; idempotent ingestion after an offline replay | 8.2 | `POST /v1/events` batch contract (4.2); tracing hook in every adapter |
| Eleven beta roles as pipeline steps (teacher, writer, fitter, editor, voice studio, host, producer, analyst, memory keeper, proof producer, recording rater); LiveKit, Inngest, Postgres, encrypted object storage, tracing; adapters with two voice vendors | 14.1, 14.3 | Sections 3 and 4; the rater and the proof producer map to `proof/make` and the finale step of `season/fanout` in 4.3 |
| The language gate and the vendor tests before build week 1; 50 scripted calls inside the build's first two weeks | 14.4, 10.14, concept-v2 §8, ADR-03, ADR-07 | `vendor-lab gate --target en` (`forone.langgate`) runs the five checks on the pilot's clips and scripts during Milestone 0 (recognizer by 2026-11-10, voice by 11-17, `vendors.yaml` committed by 11-17); a minimal `call-worker` in build week 2 carries the 50 calls by 2026-12-01 and `tools/call-bench` reruns them in week 4 (section 7) |
| Every latency budget | 15 | Section 3.6, one row per budget, with the measurement point stated |
| Audio deleted within 15 min when storage is off, for every learner-voice object; all audio within 24 h after revocation; export within 1 h; deletion live 24 h, backups 30 d; 90-day unpaid-trial retention; the one kept then-and-now recording | 5.4.11, 10.9.2, 12.5, 15 | `audio/expire` on every ephemeral `media_objects` insert, `call/verbatim-turn` per-turn deletion, `learner/purge-audio`, `learner/export`, `learner/delete` (including the processors), `retention/daily`; `media_objects.kept_explicitly`; RDS backup retention 30 days |
| Consent as provable data | 2.2 A9, 12.4, 12.5 | `consents` (owned by 04, driven by 07's `consent_change` events) is read by `POST /v1/calls`, `audio/expire`, `learner/purge-audio` and the tracing middleware |
| Encryption at rest and in transit; per-learner audio keys; row-level isolation; tokenized, resettable feed URLs excluded from directories | 12.6 | SSE-C with the per-learner DEK for learner voice and SSE-KMS under the environment key for produced show audio (ADR-12); `learner_id` on every table and Postgres RLS with `SET LOCAL`; `feed_tokens`; `<itunes:block>yes</itunes:block>` and `<googleplay:block>yes</googleplay:block>` in every feed |
| Crisis protocol activations logged | 7.9.4 | `crisis.activated` event and `crisis_log` (owned by 07 D9); the worker's step-out is recorded through `/internal/events` and the event |
| Hosting region pending counsel's review for a worldwide cohort (EU and UK GDPR, Saudi PDPL, a generic baseline, ADR-20); `residence_country` asked at A9, never inferred | 12.6, 18 #3, ADR-08, ADR-20 | `HOME_REGION` config with `eu-central-1` as the default; `learners.residence_country`; section 10 #1 |
| Cost traced per role, vendor, learner from the first learner; a defined cost-per-session metric | 14.5, 16.1, 19.2 | Adapter middleware emits one `vendor_calls` row per call (table owned by the cost domain); section 6 defines what the 16.1 number includes |
| Twelve laws, in particular law 11 (no autoplay, no feed; one, two or three new episodes a day by plan) and law 12 (claims only through the gate) | 1.2, concept-v2 §5 law 11 | No endpoint creates an episode on learner request except swap, return and `POST /v1/episodes/next` inside the allowance (a learner action after the current episode ends, never autoplay, ADR-05); the proof producer's input comes only from the claim gate's output table |
| Abuse controls on public, cost-bearing endpoints | 2.1.3, 14.5 stop line | `forone.core.ratelimit` (07): per-device and per-contact 24 h limits, an IP-prefix window, a Turnstile challenge on the sample and waitlist forms, a per-kind daily spend cap for `sample` and `pilot` separate from the global cap, a global daily cap on onboarding starts |

---
## 3. Architecture

### 3.1 Context diagram (described)

Draw one box in the middle labelled **For one platform**. Around it:

- **Learner** (phone, Safari or Chrome, earphones). Arrows into the platform: opens the web app (HTTPS), subscribes to the private feed from a podcast app (HTTPS RSS plus audio), joins a call (WebRTC to LiveKit Cloud), receives web push and email. The learner may live anywhere: the row carries `native_language`, `target_language`, `residence_country` and `tz` (ADR-02), and every prompt loader, brief compiler and TTS request reads the pair from it. Arrow out: nothing is pushed except the three message kinds of PRD 3.10.
- **Visitor** (no account). Arrows: the sample page, the share page `forone.app/s/{share_token}`, the waitlist form, the invite link `/i/{code}`.
- **Muath and the ops person** (laptop and phone). Arrows: the `/admin` pages in `api` (staff sign-in, 07 §4.13), the Inngest dashboard, Langfuse, Sentry, the ops Slack channel, GitHub.
- **Human reviewer** (PRD 6.8; an outside contractor and therefore a processor, 07 §4.9). Arrow: reads sampled episodes from `/admin/review` under the `reviewer` role, which shows the script, audio and editor verdict and never the learner's name, email, life facts or notebook.
- **Managed vendors** (all outbound HTTPS from the platform): Anthropic (teacher, writer, host, Salma, chat, analyst, memory keeper, proof producer, rater), Google Gemini (editor; embeddings; TTS candidate), ElevenLabs and Inworld (voice vendors; whichever two win the blind test), Soniox and Deepgram (streaming recognition candidates), AssemblyAI or ElevenLabs Scribe (verbatim), Speechace or Microsoft (pronunciation), LiveKit Cloud (media), Inngest Cloud (workflow state: ids and timestamps), Langfuse Cloud EU (trace metadata under the research pseudonym; anonymized text only for opted-in learners), Resend (email), the payment processor (a merchant-of-record processor recommended, Paddle, with Stripe plus Stripe Tax as the fallback; OPEN, ADR-21), Apple and Google (sign-in), Sentry (scrubbed errors). The complete processor register with what each sees, where, and for how long is 07 §4.9; this document adds no vendor that is not in it.
- **Podcast apps** (Apple Podcasts and others). Arrow: fetch the tokenized RSS and the audio enclosures; the platform never pushes to them. A fetch is logged for operations and for the PRD 12.3 hours-heard rule; it never makes a day active and never triggers an episode.

### 3.2 Container diagram (described)

Inside the platform box, draw four service boxes and the managed stores.

```
[web]  Next.js on Vercel (fra1)                    static + SSR, PWA, LiveKit client, player
   |  HTTPS JSON, cookies on .forone.app
[api]  FastAPI on ECS Fargate (HOME_REGION)        auth, invites, sessions/doors, events, feed, media, push,
   |                                               messaging, payments webhooks, admin, Inngest event sender
   |----> [Postgres RDS, Multi-AZ]  learners, waitlist, invites, schedule, consents, events, stores, episodes,
   |                      sessions, media_objects, feed_items, subscriptions, vendor_config, outbox, sample_requests
   |----> [S3 x3]         forone-media (show kinds SSE-KMS env key, presigned; samples too), forone-voice (SSE-C per learner), forone-exports
   |----> [KMS]           one CMK that wraps each learner's DEK
   |----> [Inngest Cloud] events in (ids, timestamps, enums only)
[workflows]  FastAPI serving Inngest functions on ECS Fargate
   |  reads/writes Postgres and S3; calls every vendor adapter (batch and standard pricing); sends push and email
   |  <---- Inngest Cloud invokes steps over HTTPS
[call-worker]  LiveKit Agents (Python) on ECS Fargate, autoscaled with scale-in protection while calls run
   |  <----> LiveKit Cloud (WebRTC media, dispatch)
   |  -----> streaming STT, host LLM, call TTS, Salma TTS (adapters as LiveKit plugins)
   |  -----> api: POST /internal/events (call_turn, talkback, hold_floor, silence, crisis), PUT turn audio to S3
   |         (VPC-only listener rule; per-call JWT minted at dispatch)
[Langfuse EU]  one span per model call from workflows and call-worker: metadata by default, text only with data_use
[Sentry]       scrubbed errors from all four services
```

Trust boundaries: `web` holds no secrets; `call-worker` holds vendor keys and, per call, one derived call key `HKDF(DEK, "call:" + call_id)` plus one short-lived JWT, handed to it in the brief response and discarded at call end (no zeroization claim, ADR-18); `workflows` and `api` hold everything. The `events` table is append-only: `api` appends learner and worker events, `workflows` appends after-session events (`call_turn_verbatim`, `claim_shown`, analyst outputs); both go through `forone.core.events.append()`; `call-worker` never holds a database connection. Stores are written by `workflows`, with the one exception of learner-authored edits (fact cards, "working on", notebook) which `api` applies synchronously (04 D5). `/internal/*` routes are served by the same `api` tasks but an ALB listener rule forwards them only from the VPC CIDR; from the internet they return 404. `HOME_REGION` defaults to `eu-central-1` with `me-central-1` as the alternative (ADR-08); everything in the diagram except Vercel, Inngest, Langfuse and LiveKit sits in it.

### 3.3 Service boundaries

| Service | Shape | Owns | Must not do |
|---|---|---|---|
| `web` | Next.js, Vercel | Landing, sample and share pages, waitlist and invite screens, onboarding A1 to A10 (Talk and Type), Today/Show/Notebook, player, call screen, Controls, checkout redirect, PWA manifest and service worker | Hold any vendor key; compute anything about the learner; call vendors directly |
| `api` | FastAPI, Fargate, 2 tasks min across 2 AZs | Auth and sessions; invites and the waitlist; the REST API for the app; the allowance by plan and `POST /v1/episodes/next` (ADR-04, 05); event ingestion (`POST /v1/events`, `POST /internal/events`); the typed onboarding exchange (Salma text turns, 3.6); feed rendering; media: presigned URLs for show kinds and Range streaming for learner voice and the feed (ADR-12); the three senders via `forone.core.messaging`; payment webhooks and the `subscriptions` state machine (07 D12); sample and onboarding limits; `/admin` under `staff_accounts`; sending Inngest events (with write-behind outbox) | Run any model call longer than 10 s synchronously (the typed Salma turn is one streamed Sonnet-class call under 5 s and is the only synchronous model call in `api`); write to the nine stores except through 04 D5 |
| `workflows` | FastAPI serving the Inngest Python SDK, Fargate, 1 task min, autoscaled on ALB `RequestCountPerTarget` and CPU | Every Inngest function: `day/next`, `episode/produce`, `session/after-pass`, `call/verbatim-turn`, proof, season, retention, export, deletion, voice-note reply, vendor health, outbox relay, crisis record; push and email sends through `forone.core.messaging` (it holds the VAPID and Resend keys for that reason) | Accept any request not signed by Inngest; serve learner traffic |
| `call-worker` | LiveKit Agents worker, Fargate, 1 task min, autoscaled on CPU and active jobs, scale-in protected while `active_jobs > 0`; region `CALL_WORKER_REGION` (3.6) | The live call (onboarding A3 and A7, main, round two, small-door replies when live) and talkback; per-turn audio capture and upload; emitting call events through `api`; the crisis step-out | Read the learner model (it gets one compiled host brief at dispatch); write stores; decide anything about assessment; hold the learner DEK |
| Payments | Adapter inside `api` plus the processor's hosted checkout | Checkout session creation for the three USD plans, webhooks, `payment_events`, `subscriptions` (`plan`, `founding_locked`, `founding_seq` 1 to 100), tax and invoices from the merchant-of-record processor (07 D12, ADR-21) | Store card data (the processor's hosted page does); compute tax (the processor remits it) |
| Admin | Eight pages inside `api` (`sqladmin` on the `forone_admin` role, ADR-17; staff OTP sign-in with roles `owner`, `engineer`, `reviewer`, IP allowlist as an optional second factor, 07 §4.13) plus the Inngest and Langfuse dashboards | Learner list and state, episode pipeline status and fallbacks, failed runs, vendor health and failover switch, human review queue, crisis log, invites, billing | Be a product; nothing here is shown to a learner |

### 3.4 Data flow for one day (the daily loop as events)

1. Learner uses today's session. `web` sends `play`, `huh`, `tap` and the rest in batches to `POST /v1/events` with client-minted ids (4.2); `api` appends to `events` and, when the day first qualifies as active (half an episode played, a call started, or small door used, PRD 3.6), sends Inngest event `day.became_active {learner_id, local_date, schedule_version}` once per `(learner_id, local_date)`, and only for learners in status `trial` or `paid` (PRD 12.5.9: new episodes stop for `trial_ended`). On the onboarding day, `api` sends it at A9 once the schedule is saved (the day became active at A7, but `learner_schedule` does not exist until A9).
2. Inngest starts `day/next` for that learner and date (idempotent on `learner_id-local_date-schedule_version`). It computes `drop_at` with the rule below, checks whether a pick or an episode for that date already exists (a replayed or late event), inserts the day's extra rows (`kind = daily_extra`, `slot` 2 and 3 up to `plan.episodes_per_day`) in state `planned` so the nightly teacher run plans every episode of the day (ADR-05), and otherwise waits for `idea.chosen` until `drop_at - 6h`.
   [DECISION] **The drop rule.** The episode produced from active day N drops at day N+1's drop time ("Tomorrow at 7:40", PRD 2.2 A10, 3.1.4), with three exceptions keyed to `lead = drop_at - now()`:
   - If day N's own drop time is still at least 2 h ahead when day N becomes active and no episode exists for day N (the learner played yesterday's unplayed episode at 06:00 with a 07:40 drop), `drop_at` is day N's drop time, on standard pricing, so the learner is not made to wait 25 h for a new episode. Rejected: the pure calendar rule (a 25 h gap after an early-morning session is the one place it hurts).
   - If `lead < 7 h` (a session ending at 00:30 for a 06:00 drop), the pick wait is capped at 30 min instead of `drop_at - 6h`, and `episode/produce` runs on standard pricing from the start; the batch cut lines are never reached. The learner's own pick, usually made at the end of the session, is still honored.
   - If `lead < 2 h`, `drop_at` moves to the following day's drop time (PRD 3.6.2 tolerates one waiting episode); the push text is unchanged.
   The wait timeout is clamped at zero; a `day.became_active` replayed after `drop_at - 6h` sends `learner.cutoff_reached` at once, and one replayed after `drop_at` publishes immediately on `episode.ready` without a push.
3. Call ends: `call-worker` sends `call.ended` through `api`; `session/after-pass` runs (assessment domain) as one function with the 10-minute budget: verbatim turns were already transcribed during the call, the analyst's first stage runs inside it, and it ends with `session.after_pass.completed`. There is no notes stage and nothing is sent to the learner afterwards (ADR-06; the teacher's echo plan in the next host brief is the only correction channel).
4. Learner picks an idea at the end of chat (or tells Salma one, or long-press remix). `api` inserts the `episodes` row for `(learner_id, local_date + 1 or the exception above, kind = daily)` in state `requested` (the unique key makes a double pick a no-op), records `idea_chosen` in the event log and sends `idea.chosen {learner_id, local_date, idea_id, episode_id, source}`. That event starts the pipeline domain's `episode/produce`, idempotent on `episode_id`; the pipeline waits for `session.after_pass.completed` itself (15-minute timeout, then the last good plan, PRD 9.8), runs the teacher as its first step, and computes its own batch cut lines from `drop_at`. [DECISION] A pick that arrives after the cutoff is recorded (`source: late`) and ignored for the episode already in production unless that episode has not reached `written`; then `api` sends it as `working_on.changed`-style re-plan (`idea.chosen` with the same `episode_id`) and the pipeline restarts from the brief. Salma's line in the app for the ignored case: "Tomorrow's is already in the studio; this one is first on the list for the day after."
5. `day/next` only watches: if no `idea.chosen` arrives by the cutoff it inserts the `episodes` row itself and sends `learner.cutoff_reached {learner_id, plan_id, episode_id, drop_at}`; the pipeline uses the top-ranked idea (PRD 3.1 rule 5).
6. `episode/produce` (pipeline domain) runs brief, write, fit, edit, voice, re-listen, glosses, publish, switching from Batch to standard pricing at `drop_at - 90min` (PRD 3.2). Its publish step writes `episodes.state = ready`, upserts `feed_items` with `publish_at = drop_at` (owned by 02 §4.x; `(learner_id, episode_id, publish_at, published_at, title, duration_s, audio_ref, notes_html, guid)`), and sends `episode.ready`. The app shows the episode the moment it is ready (PRD 3.3.1). It does **not** touch sessions. The teacher step writes one plan with 1 to 3 episode briefs, each with its own targets, so the `planned` extra rows start at the writer when the learner asks for them.
7. `day/next` waits for `episode.ready`, sleeps until `drop_at`, then publishes the feed item (`feed_items.published_at`), sends the one web push to the learner's installed devices (`push_subscriptions`, 06) and sends `drop.published`. If the episode is not ready at `drop_at` it sends `pipeline.human_page`, sends no push, and keeps waiting for `episode.ready` until the next cutoff (`drop_at + 18h`); a late episode is published to the feed when it arrives, still without a push, and appears in the app the moment it is ready. [DECISION] Session close belongs to `api`, not the pipeline: the open session closes when the learner first opens the next `pilot`, `daily`, `swap` or `return` episode (PRD 4 rules 7 and 8), and at the latest at that episode's drop, which `day/next`'s publish step enforces by calling `sessions.close_previous(learner_id, episode_id)`. The new `sessions` row is created in state `ready` by the same call. `proof` and `finale` episodes attach to the open session (or to none) and never close one (PRD 11.1.2: the proof "sits above today's episode").
8. Episodes 2 and 3 of the day (ADR-05): after the drop episode has been heard, Today shows one "next one" button; `POST /v1/episodes/next` checks `episodes_today < plan.episodes_per_day` and the learner's status, moves the next `planned` row to `requested`, and sends `learner.extra_requested {learner_id, local_date, episode_id, slot}`, which starts `episode/produce` on the on-demand path from the writer (the brief is already in the plan), scene 1 first, under 30 s, on standard pricing. Never autoplay, no feed of extras; the feed carries the drop episode plus any extra the learner has played. For learners whose last 7 days show 5 or more extras, the nightly run pre-produces episode 2 (`prewrite_extra`, 02) and `POST /v1/episodes/next` then only publishes it. Unused `planned` rows are closed at the next `day/next` and cost nothing.
9. There is no separate nightly teacher cron for active learners: the teacher step inside the nightly `episode/produce` run covers the weekly mix, arcs, seasons, tomorrow's ideas and the day plan for up to three episodes. Inactive days start no run and cost nothing. The only time-based fan-outs are `season/fanout` (finale on or after day 28, P1) and `proof/fanout` (the weekly proof day), both hourly over learner-local days (ADR-16) and both restricted to `trial` and `paid` learners.

### 3.5 Who talks to whom (interfaces)

| From | To | Protocol | Notes |
|---|---|---|---|
| `web` | `api` | HTTPS JSON, cookie auth, `/v1/...` | OpenAPI generated client; every response carries `X-Forone-LM-Version` (06 D11) for cache keys |
| Visitor | `api` | `POST /v1/sample`, `GET /v1/sample/{id}`, `GET /s/{share_token}.mp3`, `POST /v1/waitlist`, `GET /i/{code}` | Turnstile token required on the two forms; `forone.core.ratelimit` on every route |
| `web` | LiveKit Cloud | WebRTC | Token minted by `api` `POST /v1/calls` (or `POST /v1/onboarding/start` for A3), 10-minute TTL, room name `call-{callId}` |
| Podcast app | `api` | HTTPS `GET /f/{feedToken}.xml`, `HEAD`/`GET /f/{feedToken}/{episodeId}.mp3` | Token is 32 bytes base64url; the XML carries `<itunes:block>yes</itunes:block>` and `<googleplay:block>yes</googleplay:block>` (PRD 12.6: excluded from directories); the `.mp3` route stays proxied by `api` with Range passthrough even though show audio is SSE-KMS (podcast apps cache enclosure URLs, so a presigned URL would expire in their cache; ADR-12) and logs one `feed_fetches` row (06) per enclosure fetch (used by the 12.3 hours-heard rule once the learner later uses that episode's call, chat or small door); neither route sends any Inngest event |
| `api` | Inngest Cloud | HTTPS `inngest.send()` | Payload = ids, timestamps, enums and short codes only; a CI test fails on any event model field named `name`, `email`, `text`, `topic`, `quote`, `transcript`, `audio` or longer than 200 characters. Write-behind `outbox` on failure, relayed by a 30 s cron in `workflows` |
| Inngest Cloud | `workflows` | HTTPS signed requests to `/api/inngest` | Signing key verified; nothing else routes here |
| `workflows` | `api` | none | `workflows` talks to Postgres and S3 directly through the shared `forone.core` package, and sends push and email through `forone.core.messaging`, the same module `api` uses |
| LiveKit Cloud | `call-worker` | Agent dispatch with `metadata = {callId, jwt}` | Worker fetches the brief from `api` `GET /internal/calls/{callId}/brief` with the per-call JWT (5-minute TTL, audience `call-worker`, subject `callId`), so the worker never holds a DB connection or a static secret that unwraps keys |
| `call-worker` | `api` | HTTPS `POST /internal/events`, `POST /internal/calls/{id}/turns` | Reachable only from the VPC CIDR (ALB listener rule); the per-call JWT in `Authorization`; events are the same batch shape as `POST /v1/events` with `source = 'worker'` |
| `call-worker` | S3 | `PUT` turn audio with SSE-C headers | The per-call key `HKDF(DEK, "call:" + call_id)` is delivered in the brief response, held in memory for the call only, and recorded in `media_objects.key_derivation = 'call:{call_id}'` so reads re-derive it from the DEK |
| `api`, `workflows`, `call-worker` | Langfuse | HTTPS SDK, async, fire-and-forget | Span = `{trace_id, span_id, role, vendor, model, prompt_version, learner_model_version, episode_id|call_id, input_tokens, output_tokens, cached_tokens, cost_usd, latency_ms, prompt_sha256}`; `user_id` is the research pseudonym from `research_pseudonyms(learner_id, pseudonym)` (a random row, deleted with the learner, so the secret behind it can rotate; ADR-09), never the learner id, so `learner/delete` can delete by it; prompt and completion text are written to `model_io` (4.2) in Postgres with the span id and go to Langfuse only when `consents.data_use` is true, after 07's `anonymize()`; no audio ever; retention 30 days |
| `web` | `api` | `GET /v1/episodes/{id}/media` | For show kinds (`sse_kms_env`) the response is a 302 to a 10-minute presigned S3 URL (ADR-12); for learner-voice kinds (`sse_c_learner`: the tape, kept recordings) `api` streams with Range under the DEK; the service worker caches the bytes either way |

### 3.6 The request path for each latency budget (PRD 15)

| Budget | Path | Where the time goes | How it fits |
|---|---|---|---|
| First open to first sound (Salma) under 60 s | `web` A1 to A2 (static, cached at the edge) → `POST /v1/onboarding/start {invite_code, tz, native_language, target_language, age_attested, mode}` validates the invite (the native language comes from the landing page's `Accept-Language` choice, the target from the invite; `residence_country` is asked at A9, ADR-20), creates a `pre_account` learner (with the waitlist answers as intake facts) and, for `mode: talk`, a LiveKit room → `call-worker` joins with the Salma persona → Salma's first line is a pre-rendered audio clip in the learner's native package (`packages/native/<lang>/`, ADR-02). For `mode: type` (A2 "Type", or mic permission denied) the same intake runs as a text exchange: `POST /v1/onboarding/{id}/messages` streams Salma's reply (Sonnet-class, cached persona, under 5 s), the first two lines are static text, and the two English turns are the same scripted turns 4 and 7 | Page load 1 to 3 s; mic permission (user); room connect 1 to 2 s; first clip plays at once | The first two Salma lines are static audio from the package, not synthesized; the live pipeline warms behind them. The typed path has no first-sound budget but keeps the 5-minute first-English-sentence target as a typed sentence. Week 3 serves A3 on the minimal worker stood up in week 2 (section 7) |
| First spoken target-language sentence under 5 min | A3 is a Salma call with a 3-minute cap, two target-language lines scripted in the persona | Learner's own pace | The two target-language turns are fixed in the persona prompt at turns 4 and 7; the worker enforces the 8-turn cap |
| Sample episode playable under 30 s | `POST /v1/sample` (Turnstile, device and contact limits, IP window, `sample` spend cap) → `sample_requests` row with the three answers and a `share_token` → `sample.requested {sample_id, device_key}` → the pipeline's sample path inside `episode/produce` (standard pricing, Sonnet writer, code checks plus **the editor model's law scan, check 10, on a Haiku-class model over the 250-word script**, about 2 to 4 s and under $0.005) → scene 1 TTS → `episode.streaming_started` → client polls `GET /v1/sample/{id}` every 1 s and starts on scene 1 while the rest renders | Writer 8 to 15 s; law scan 2 to 4 s; TTS scene 1 3 to 5 s; Inngest step hops (Inngest EU to `eu-central-1`) 0.2 to 0.8 s per step, about 1.5 to 3.5 s over the path (0.3 to 1 s per step if `me-central-1` is chosen); poll up to 1 s | **30 s median, 45 s p95** is what this design delivers on 2026-12-23 (the pipeline document's measured target is 25 to 40 s); the PRD says "under 30 s" with no percentile. [OPEN for Muath] section 10 #9 accepts the p95 or cuts the sample to a 60-second script and sentence-level first TTS. The law scan stays a model check because the sample is the one surface strangers forward (PRD 6.3 lists check 10 among the model checks; rejected: the code word list of the first draft). Sample audio is written under a service key (SSE-KMS) to `forone-media/samples/{sample_id}/`, holds no learner data beyond a first name and a topic, and is served at `GET /s/{share_token}.mp3` without login for 30 days, then deleted by `retention/daily` |
| Pilot playback under 45 s after A3 | `onboarding.intake_completed {learner_id, intake_facts_ref, name_clip_ref}` fired by `api` at the end of A3 starts `episode/produce` in its on-demand path; A5 casting plays meanwhile | Writer 8 to 15 s on a Sonnet-class model with the intake as the only input; **editor checks 3, 5 and 10 on scene 1 before scene 1 plays** (Haiku-class, 2 to 4 s); TTS scene 1 3 to 5 s; step hops 2 to 4 s | Pilot skips the teacher (a rule-built brief from the intake) and runs one fitter pass only; the remaining scenes are checked and voiced while scene 1 plays (A5 covers 40 to 90 s, PRD 2.2) |
| Dropped episode start under 2 s | `web` Today screen prefetches `episode.m4a` (or the first 512 KB when the service worker cannot cache) through `GET /v1/episodes/{id}/media` when the screen loads, which answers with a 10-minute presigned S3 URL for show kinds (ADR-12); play is a local buffer start | Cold: one request to `api` (about 50 ms) plus one Range request straight to S3 (about 100 to 250 ms for a learner within the region's continent; up to 400 ms from further away) | Prefetch plus the service worker caching the episode after first play (06 D3). Show audio is SSE-KMS under the environment key, so S3 serves it directly and `api` carries only learner voice and the feed; CloudFront in front of the show kinds is a later lever (section 6), not a beta item |
| On-demand episode (swap, return, next one) under 30 s | `api` sends `learner.swap_requested {learner_id, episode_id}` (after checking the one-swap rule), `learner.extra_requested {learner_id, local_date, episode_id, slot}` (after checking `episodes_today < plan.episodes_per_day`; the brief comes from the nightly plan so the run starts at the writer, ADR-05) or `learner.return_detected {learner_id, days_away}` (**on app open or a feed-link exchange only**: the first authenticated request of the day, or `/call/{episodeId}?k=` and `/show/{episodeId}?k=` from the feed notes, when no session event exists in 5 or more days; idempotent on `learner_id + local_date`; never on an XML or enclosure fetch, because podcast apps poll on their own schedule and an inactive learner must cost nothing, PRD 3.8.3 and 3.6.2); `episode/produce` on-demand path, scene 1 first, `episode.streaming_started` | Writer 10 to 20 s for a 6-minute script; **model checks 3, 4, 5, 7 and 10 on scene 1** (Haiku-class, 2 to 4 s); TTS scene 1 3 to 5 s; step hops 2 to 4 s | **Nothing plays before the gate has passed on it.** Scene 1 streams only after its checks pass; the full-script checks (1 to 11) run while scene 1 plays; a fail on scenes 2+ is repaired in place (one recheck) or, on a second fail, the whole fallback episode is produced and the player is told to restart from its scene 1 with Salma's one-line notice. A splice of a fallback from scene 2 onward is never made (PRD 1.2 law 4, 6.3 check 9). Consequence stated for the feed: a feed-only listener never becomes active (PRD 12.3 counting rule) and so never receives a new episode until they open the app or tap a feed link; the feed notes say so in one line |
| Call connect under 3 s | `POST /v1/calls` (mints token and the per-call JWT, writes `calls` row, derives the call key, dispatches the agent with `callId`) → `web` joins the room → worker accepts the job, fetches the brief (one request, under 100 ms), opens STT and TTS streams | Room join 0.5 to 1.5 s; worker job accept under 500 ms with a warm pool | Minimum 1 warm worker task per environment; worker pre-opens vendor websockets at job start; the first host line is synthesized while the learner's mic connects; the LiveKit turn-detector and Silero VAD models are baked into the image at build time (4.8) so an autoscaled task is ready in under 60 s |
| Host reply median under 1.5 s, p95 under 2.5 s | learner audio → LiveKit edge → worker → streaming STT (final on end-of-turn) → host LLM (Sonnet-class, cached brief, streaming) → call TTS (streaming) → LiveKit → learner | **Clock starts at the end-of-turn decision** (03 §4.15 `reply_latency_ms`, adopted as the PRD 15 gate; `silence_to_sound_ms` from the last speech frame is reported beside it and includes the 1.0 to 2.5 s adaptive silence, which is pedagogy, not latency). STT finalization 200 to 400 ms; LLM first token 300 to 600 ms with prompt cache; TTS first byte 100 to 300 ms; **vendor round trips 3 × 20 to 100 ms = 60 to 300 ms from `eu-central-1`** to EU or US-east endpoints (3 × 120 to 180 ms = 400 to 550 ms if the worker ran in `me-central-1`); LiveKit edge to the learner 30 to 80 ms wherever they are (LiveKit Cloud's global edge [ASSUMPTION, confirmed in build week 2]) | Summed honestly the median is 0.8 to 1.4 s from Frankfurt and 1.1 to 1.6 s from the UAE, with little headroom either way. [DECISION] `call-worker` runs in the region closest to the chosen STT, LLM and TTS endpoints (`CALL_WORKER_REGION`, default `eu-central-1`, candidate `us-east-1`; ADR-08 says the worker runs where the vendors are fastest); it holds no data at rest, uploads turn audio to the home-region S3 (cross-region when the two differ, about 50 KB per turn), and the build-week-2 50-call test runs both placements so the placement is chosen by 2026-12-01 (the vendor pair itself is chosen by the language gate by 2026-11-17, ADR-03). Counsel's note on in-transit processing in a second AWS region goes with section 10 #1. Sentence-by-sentence TTS; brief in the cached prefix; no DB on the turn path |
| Talkback answer under 2 s | hold S → data message → worker routes the next audio chunk to the recognizer configured for `[native, target]` (`talkback_stt.languages` per call, ADR-02) → Salma text (Sonnet-class, cached persona plus produced-word history) → Salma TTS → learner's ear | Same chain as a host turn but with a shorter prompt | Word-or-hint lookup is a dict in the brief (produced words), no DB |
| Word sheet under 300 ms | `web` reads the gloss bundle shipped with the episode (`glosses.json`, fetched once with the transcript) | Local | Glosses are precomputed in `episode/produce` step 7; nothing is fetched on tap except the audio slice, which is also local |
| Chat opener under 30 s | door open or `call.ended` with the app in foreground → `chat/open` step with the precomputed opener from the episode package | Under 1 s if precomputed; 5 to 10 s if the call summary must be folded in | The opener text is written in `episode/produce`; after a call, one Sonnet-class call adds the call summary |
| After-session pass and teacher update within 10 min | `session/after-pass` (one function, ADR-06; the analyst's first stage runs inside it) → `session.after_pass.completed` → the teacher step of `episode/produce`, which was waiting for it | The last turn's verbatim 5 to 15 s (`call/verbatim-turn` gives the last turn of a finished call priority over queued turns of running calls, 4.3); analyst, classifier, measures, updater, memory keeper 1 to 3 min; teacher 1 to 2 min on standard pricing when the drop is near, batch otherwise | The pass runs on standard pricing (10 min is too tight for Batch); the teacher's pricing follows the pipeline's cut lines; the Notes-under-90-s budget of PRD 15 no longer exists (decisions.md §3) |
| Tomorrow's episode ready before the drop; fallback to on-demand at drop minus 90 min | `day/next` and `episode/produce` as in 3.4 | Batch API jobs usually finish in minutes, at worst 24 h | Every step reads `deadline`; `submit_batch` polls every 5 min and abandons the batch at the deadline, re-running on standard pricing |
| Audio deleted within 15 min when storage is off | **Every** `media_objects` insert of a learner-voice kind (`call_turn, call_full, recording, voice_note, say_it_once, shadow, clip`) with `ephemeral = true` sets `expires_at = created_at + 15 min` and starts `audio/expire` for that object (debounced per call); `call/verbatim-turn` deletes each turn's audio the moment that turn's verbatim succeeds (PRD 5.4.11); the then-and-now recording follows the same rule unless `kept_explicitly` (PRD 12.5.2); `retention/daily` is the audit, not the mechanism; an S3 lifecycle on `.../ephemeral/` at 1 day is the backstop of last resort | n/a | Three independent paths plus a lifecycle rule; 07's `privacy/verify` checks the result daily |
| All audio deleted within 24 h of revocation | `learner.consent_changed {voice_storage: false}` → `learner/purge-audio` lists every `media_objects` row of a learner-voice kind and deletes it; the DEK stays until account deletion because produced show audio is still needed; text needs no key | n/a | Verified by `retention/daily` and 07's `privacy/verify` |
| Live voice failure falls back to voice notes | `web` detects no room connection within 3 s or two pipeline errors → shows "Weak signal" → records with MediaRecorder → `POST /v1/calls/{id}/voicenotes` → `call/voice-note-reply` | 20 to 40 s per exchange | The call thread stores both modes; the session is never lost |
| Voice vendor outage: second vendor within the same day's production | `vendor/health` marks a vendor degraded after 5 failures in 10 min and **pages**; the pipeline's per-render understudy switch handles single segments automatically; **the whole-vendor switch for `episode_tts` and `call_tts` is a one-click manual action on `/admin/vendors`** (at beta scale five failures can be one bad batch, and a voice switch forces the on-air announcement of PRD 7.1.3); the pipeline emits `voice.vendor_failover` and adds the one-line on-air announcement | n/a | Both voice vendors have accounts, voices mapped per host and accent, and are exercised weekly by a canary episode; automatic failover stays on for `streaming_stt`, `verbatim_stt` and `editor` |

### 3.7 Media layout: segments in storage, one file for the player

[DECISION] Every produced audio asset is stored as an ordered list of segments plus one stitched file. An episode is 2 to 4 scenes plus cold open and throw; each scene is one segment, synthesized as its own step, so (a) on-demand episodes stream from scene 1 while later segments render, (b) the audio re-listen can re-synthesize one line without touching the rest, (c) a TTS vendor failover mid-episode changes one segment's vendor, not the episode. The feed and the archive use the stitched file, made after the last segment passes re-listen. Word timestamps are stored per segment and offset into a single `timings.json` for the player. This is a storage and pipeline contract (02's `AudioManifest`), not a player contract: the player uses one `<audio>` element on the stitched `episode.m4a` for every ready episode and a two-element scene handoff only while an on-demand episode is still streaming (06 D3; the first draft's per-segment player everywhere was rejected by the client domain because gapless handoff is unreliable on iOS and breaks lock-screen position). [DECISION] If the week-3 iOS test shows seam gaps over 300 ms on the streaming kinds, the streaming kinds move to an HLS event playlist served by `api` (AAC segments, native in Safari's `<audio>`, hls.js on Chrome); the segment storage is already the right input for it.

---
## 4. Detailed design

### 4.1 Monorepo

```
forone/
  apps/
    web/                 Next.js 15, TypeScript, Vercel
    api/                 FastAPI app: routers, auth, invites, feed, media, admin, typed onboarding
    workflows/           FastAPI app serving Inngest functions
    call-worker/         LiveKit Agents worker (Python)
  packages/
    core/                forone.core: settings, db (SQLAlchemy 2 + Alembic), models, event schemas (Pydantic), events.append,
                         keys (DEK with the 60 s versioned cache, per-call HKDF), media, outbox, messaging (the three senders), ratelimit, audit,
                         guard (law words, humanity, progress claims and the correction guard, 07), plans (plans.yaml loader)
    adapters/            forone.adapters: interfaces + one module per vendor + vendors.yaml loader + tracing middleware
    pipeline/            forone.pipeline: teacher, writer, fitter, editor, voice studio, glosses (episode domain)
    learner/             forone.learner: event log, nine stores, compiled briefs (data domain)
    assess/              forone.assess: verbatim, analyst, classifier, measures, updater, claim gate (assessment domain)
    languages/<target>/  target-language package (ADR-02): episode and call voices, recognizers and thresholds, lexicon, structure inventory,
                         calibration set, law words and correction phrases, crisis keywords, host prompts, ban list, gate.yaml; `languages/en` for the pilot
    native/<lang>/       native-language package (ADR-02): interface strings with `dir`, consent texts and notice, gloss language, Salma's voice
                         and lines, crisis clips and resources per ISO country; `native/ar` for the pilot, `native/en` the universal fallback
  tools/
    vendor-lab/          CLI: `forone.langgate` runs concept-v2 §8's five checks per target language (ADR-03); evidence in langgate/<target>/<date>/
    call-bench/          CLI: 50 scripted calls against staging, prints latency percentiles (03 §4.15)
    m0_import.py         Milestone 0 learner files into events (04)
  infra/
    terraform/           VPC, NAT, RDS (Multi-AZ), S3, KMS, ECR, ECS services, ALB + WAF, IAM, Secrets Manager (one module per env)
    docker-compose.yml   dev: postgres+pgvector, minio, inngest dev server, livekit-server --dev, mailpit
  .github/workflows/     ci.yml, deploy-staging.yml, deploy-prod.yml
```

Tooling: `uv` workspace, Ruff, Pyright, pytest; `pnpm` for `web`. One Docker image `forone-python` with three entrypoints (`api`, `workflows`, `call-worker`) selected by `FORONE_SERVICE`. The image bakes in ffmpeg, the spaCy model of each open target language (English for the pilot), the LiveKit multilingual turn-detector weights and the Silero VAD weights at build time (about 1.6 GB [ASSUMPTION]; pulled from ECR in the same region in 20 to 40 s, which is inside the 60 s cold-start allowance for an autoscaled `call-worker` task).

### 4.2 Schemas this domain owns

The event log and the nine stores are the data domain's (04); `feed_items`, `episode_artifacts` and the pipeline tables are 02's; `consents`, `recordings`, `claims`, `word_uses` are 04's and 05's; `research_pseudonyms` is 04's with 07's deletion rule (ADR-09) [ASSUMPTION]; `crisis_log`, `audit_log`, `payment_events`, `subscriptions`, `staff_accounts`, `rate_limits` are 07's; `push_subscriptions`, `feed_fetches`, `accounts`, `otp_codes` are 06's; `vendor_calls`, `learner_spend_daily` and `session_costs` are 08's. The schemas below are the topology's own tables, plus three that reviews found missing and no sibling owns (`waitlist`, `invites`, `model_io`). `plans.yaml` (ADR-04) is a checked-in file in `forone.core.plans`, not a table: `{one_a_day: {price_usd: 19.99, episodes_per_day: 1}, two_a_day: {price_usd: 29.99, episodes_per_day: 2, recommended: true, trial: true}, three_a_day: {price_usd: 44.99, episodes_per_day: 3}}`.

**Row-level security, decided once.** [DECISION] Every table with `learner_id` has RLS policies on `current_setting('forone.learner_id', true)`, set with `SET LOCAL` inside the transaction by a SQLAlchemy `begin` hook (never session-level `SET`, which leaks across a pooled connection). Roles are 04's: `forone_app` (api; RLS enforced), `forone_workflows` (crons and fan-outs: `proof/fanout`, `season/fanout`, `retention/daily`, `vendor/health`, `outbox/relay`; `BYPASSRLS`), `forone_purge` (inside `learner/delete` only), `forone_admin` (the `/admin` pages: aggregate reads across learners, writes only to the admin tables, every content read written to `audit_log`; ADR-17), `forone_human` (psql sessions and Muath's SQL; the only role under pgaudit, so the human-SQL audit is not buried under dashboard reads), `forone_readonly` (read replicas and the weekly report). The per-learner functions in `workflows` (`episode/produce`, `session/after-pass`, `day/next`) run as `forone_workflows` but set `forone.learner_id` anyway, so a cross-learner query in them is a bug the CI test catches. 07's CI test walks `information_schema` for tables lacking policies. Rejected: deferring RLS to P1 with a repository lint (the roles and the test are one day of work and the sibling domains already build on them).

```sql
-- learners: identity and lifecycle. Auth tables (accounts, otp_codes, auth_sessions) are 06's.
create table learners (
  id              uuid primary key default gen_random_uuid(),
  status          text not null check (status in ('pre_account','trial','paid','trial_ended','deleting','deleted')),
  display_name    text,
  email           citext unique,
  birth_date      date,                      -- null until A9; under-18 refused at write time (07 D8)
  age_attested_at timestamptz,               -- A1 checkbox
  tz              text not null,             -- IANA, from the device at onboarding start; no default (ADR-02: no launch country)
  native_language text not null,             -- BCP 47 primary tag, selects packages/native/<lang>/ (ADR-02)
  target_language text not null,             -- selects packages/languages/<target>/; 'en' is the only target open at the beta (ADR-03)
  residence_country char(2),                 -- ISO 3166-1, asked at A9 with a country picker, never from IP (ADR-20); null until A9
  plan            text not null default 'two_a_day' check (plan in ('one_a_day','two_a_day','three_a_day')),  -- plans.yaml; the trial runs on two_a_day (ADR-04)
  invite_id       uuid references invites(id),
  created_at      timestamptz not null default now(),
  trial_started_at timestamptz,              -- set at A9; the 7-day trial (PRD 2.2 A9)
  trial_ends_at   timestamptz,               -- trial_started_at + 7 days; the day-6 email is trial_ends_at - 1 day
  deletion_requested_at timestamptz
);
-- The Langfuse user_id is a row in research_pseudonyms(learner_id, pseudonym) (ADR-09; 04's DDL), created at A9 and deleted with the learner.
-- Lifecycle of pre_account: created at POST /v1/onboarding/start; voice_storage is treated as false (every A3/A7 object is
-- ephemeral and expires in 15 min) except the name clip (kind 'clip', kept until A9 decides, then re-flagged from consents);
-- promoted to 'trial' at A9; deleted with its key by 07's pre_account_sweep 24 h after created_at if still pre_account.

-- waitlist: PRD 2.1.5. The answers are copied into the pre_account learner's intake facts at onboarding start.
create table waitlist (
  id              uuid primary key default gen_random_uuid(),
  name            text not null,
  contact_kind    text not null check (contact_kind in ('whatsapp','email')),
  contact         text not null,             -- the address or number; needed to send the invite
  contact_hash    text not null,             -- sha256(normalized contact + RATE_LIMIT_SALT); unique per person
  native_language text,                      -- from the landing page's language choice (ADR-02)
  target_language text not null default 'en',
  why_learning    text check (why_learning in ('job','studies','travel','other')),  -- was why_english; the target is a field now
  self_rating     smallint check (self_rating between 1 and 3),
  country         char(2),                   -- ISO 3166-1, self-declared; was city
  sample_request_id uuid references sample_requests(id),
  created_at      timestamptz not null default now(),
  unique (contact_hash)
);

-- invites: PRD 2.1.6, batches of about 50 a week from 2026-12-23 (ADR-07; sent_at::date is the cohort_key, ADR-19); minted from /admin/invites.
create table invites (
  id              uuid primary key default gen_random_uuid(),
  code            text not null unique,      -- 16 chars base32, the /i/{code} link
  waitlist_id     uuid not null references waitlist(id),
  batch_no        integer not null,
  sent_at         timestamptz,
  sent_via        text check (sent_via in ('email','whatsapp_manual')),  -- WhatsApp sending is manual in the beta (section 10 #8)
  expires_at      timestamptz not null,      -- sent_at + 14 days
  redeemed_at     timestamptz,
  learner_id      uuid references learners(id)
);
create index on invites (batch_no);

-- learner_schedule: the anchor and the rhythm (PRD 3.9), versioned so a running day/next is cancelled and restarted.
create table learner_schedule (
  learner_id      uuid primary key references learners(id) on delete cascade,
  drop_time_local time not null,             -- e.g. 07:40
  backup_time_local time,
  anchor_text     text,                      -- "on the 7:40 bus"
  rhythm_days     smallint check (rhythm_days between 3 and 6),
  spare_days      smallint default 2,
  proof_weekday   smallint,                  -- 0..6, null until known (PRD 11.1); proof/fanout uses onboarding weekday + 7 days until then
  onboarded_weekday smallint not null,
  expects_drop    boolean not null default false,  -- set by day/next when the previous local day was active; read by 09's episode_not_ready_before_drop (ADR-19)
  version         integer not null default 1,
  updated_at      timestamptz not null default now()
);

-- learner_keys: envelope-encrypted per-learner data key (DEK). Deleting the row crypto-shreds all SSE-C objects.
create table learner_keys (
  learner_id      uuid primary key references learners(id) on delete cascade,
  dek_wrapped     bytea not null,            -- KMS Encrypt(32 random bytes) under the env CMK
  kms_key_id      text not null,
  key_version     integer not null default 1,   -- bumped by destroy(); part of the cache key (ADR-18)
  created_at      timestamptz not null default now(),
  destroyed_at    timestamptz                -- set first; row deleted by learner/delete after objects are gone
);
-- Per-call keys: call_key = HKDF-SHA256(ikm = DEK, info = 'call:' || call_id, length 32). Derived by api at dispatch,
-- handed to call-worker in the brief, recorded on each object as key_derivation; api re-derives it for reads.
-- keys.get_dek (ADR-18): api and workflows cache the unwrapped DEK for 60 s keyed by (learner_id, key_version); never for
-- admin_break_glass or export; one audit_log row per (learner_id, purpose, actor) per cache window with a uses count;
-- destroy() sets destroyed_at and bumps key_version so every process misses on its next read. No zeroization claim is made.

-- episodes: one row per produced episode (daily, daily_extra, pilot, sample, swap, return, proof, finale). The lifecycle column is `state` (ADR-19).
create table episodes (
  id              uuid primary key default gen_random_uuid(),
  learner_id      uuid references learners(id),          -- null only for kind = 'sample'
  sample_request_id uuid references sample_requests(id),  -- set only for kind = 'sample'
  kind            text not null check (kind in ('pilot','daily','daily_extra','swap','return','sample','proof','finale')),  -- daily_extra: episodes 2 and 3 of the day (ADR-05)
  slot         smallint not null default 1 check (slot between 1 and 3),  -- 1 = the drop episode; 2 and 3 = daily_extra
  state           text not null check (state in ('planned','requested','briefed','written','fitted','edited','voiced','checked','ready','published','fallback','failed','superseded')),
                                             -- planned: inserted by day/next for the day's allowance, brief written by the nightly teacher run; superseded: a planned extra the learner never asked for
  local_date      date not null,             -- the learner's day this episode is for (the request date for samples)
  idea_id         uuid,                      -- the chosen idea (teacher domain table)
  brief_ref       text,
  package_ref     text,                      -- s3 key of the written package json
  pricing         text not null default 'batch' check (pricing in ('batch','on_demand')),
  deadline_at     timestamptz,
  drop_at         timestamptz,
  ready_at        timestamptz,
  published_at    timestamptz,
  fallback_reason text,
  model_versions  jsonb not null default '{}',
  prompt_versions jsonb not null default '{}',
  cost_usd        numeric(8,4) not null default 0,       -- rolled up from vendor_calls by the cost domain
  inngest_run_id  text,
  created_at      timestamptz not null default now(),
  check ((kind = 'sample') = (learner_id is null)),
  check ((kind = 'sample') = (sample_request_id is not null)),
  unique (learner_id, local_date, kind, slot)   -- the production idempotency key; api or day/next inserts in state 'requested' (or 'planned' for extras)
);
create index on episodes (learner_id, state);

-- sessions and doors: PRD Part 4.
create table sessions (
  id              uuid primary key default gen_random_uuid(),
  learner_id      uuid not null references learners(id),
  episode_id      uuid not null references episodes(id),
  state           text not null check (state in ('ready','open','done','closed')),
  opened_at       timestamptz, done_at timestamptz, closed_at timestamptz,
  active_day_marked boolean not null default false,
  swap_used       boolean not null default false,
  created_at      timestamptz not null default now()
);
-- one open session per learner; only pilot, daily, swap and return episodes get a session row (proof and finale attach to the open one)
create unique index one_open_session on sessions (learner_id) where state in ('ready','open','done');

create table doors (
  session_id      uuid not null references sessions(id) on delete cascade,
  door            text not null check (door in ('listen','shadow','read','call','chat','round_two','small_door')),  -- no notes door (ADR-06)
  state           text not null default 'not_started' check (state in ('not_started','in_progress','done','skipped')),
  position        jsonb,
  updated_at      timestamptz not null default now(),
  primary key (session_id, door)
);

-- media_objects: every S3 object, so deletion, export and the 15-minute rule are table scans, not bucket listings.
create table media_objects (
  id              uuid primary key default gen_random_uuid(),
  learner_id      uuid references learners(id),          -- null only for sample audio and canary renders
  bucket          text not null check (bucket in ('media','voice','exports')),
  key             text not null,
  kind            text not null,             -- episode_segment, episode_full, read_aloud, recap, feed_tag, proof, sample,
                                             -- call_turn, call_full, recording_retell, recording_opinion, recording_repeat,
                                             -- voice_note, say_it_once, shadow, clip, export
  episode_id      uuid references episodes(id),
  call_id         uuid,
  recording_id    uuid,                      -- 05's recordings row for the three then-and-now parts
  segment_index   smallint,
  duration_ms     integer,
  bytes           bigint,
  content_type    text not null default 'audio/mpeg',
  encryption      text not null check (encryption in ('sse_c_learner','sse_kms_env')),  -- set by kind (ADR-12): learner-voice kinds sse_c_learner; show kinds sse_kms_env
  key_derivation  text,                      -- sse_c_learner only: null = the learner DEK itself; 'call:{call_id}' = per-call HKDF key
  ephemeral       boolean not null default false,   -- true when voice storage is off: must be gone within 15 min of creation
  kept_explicitly boolean not null default false,   -- the one then-and-now recording the learner chose to keep (PRD 12.5.2)
  expires_at      timestamptz,               -- created_at + 15 min when ephemeral; share expiry for samples (30 days)
  deleted_at      timestamptz,
  created_at      timestamptz not null default now(),
  unique (bucket, key),
  check (encryption = 'sse_kms_env' or learner_id is not null)
);
create index on media_objects (ephemeral, expires_at) where deleted_at is null;
-- learner-voice kinds (sse_c_learner; the set every deletion rule uses):
--   call_turn, call_full, recording_retell, recording_opinion, recording_repeat, voice_note, say_it_once, shadow, clip
-- show kinds (sse_kms_env under MEDIA_ENV_KMS_KEY_ID; served by 10-minute presigned URLs from api; deleted by prefix in learner/delete, 04's purge order):
--   episode_segment, episode_full, episode_feed, read_aloud, recap, feed_tag, proof, sample, export

-- feed_tokens: the private podcast feed (PRD 12.6). Reset = insert a new row, revoke the old.
create table feed_tokens (
  token           text primary key,          -- 32 random bytes, base64url
  learner_id      uuid not null references learners(id) on delete cascade,
  created_at      timestamptz not null default now(),
  revoked_at      timestamptz
);
create index on feed_tokens (learner_id) where revoked_at is null;

-- model_io: prompt and completion text per model call, in the home region, pointed at by the Langfuse span (decision 15).
create table model_io (
  span_id         text primary key,
  learner_id      uuid references learners(id),          -- null for samples and canaries
  role            text not null,
  episode_id      uuid, call_id uuid,
  prompt_sha256   text not null,
  prompt          text not null,
  completion      text not null,
  created_at      timestamptz not null default now()
) partition by range (created_at);           -- monthly partitions; dropped after 90 days (debugging window)

-- vendor_config: runtime overrides on top of vendors.yaml. Read with a 60 s cache by every service.
create table vendor_config (
  role            text primary key,          -- episode_tts, call_tts, streaming_stt, ... (section 4.5)
  vendor          text not null,
  model           text,
  reason          text,
  set_by          text not null,
  set_at          timestamptz not null default now()
);

-- vendor_health: written by vendor/health; drives automatic failover for recognizers and the editor, paging for voices.
create table vendor_health (
  vendor          text not null,
  capability      text not null,
  window_start    timestamptz not null,
  failures        integer not null default 0,
  successes       integer not null default 0,
  degraded        boolean not null default false,
  primary key (vendor, capability, window_start)
);

-- outbox: write-behind for Inngest events when inngest.send() fails.
create table outbox (
  id              bigserial primary key,
  event_name      text not null,
  payload         jsonb not null,
  idempotency_key text,
  created_at      timestamptz not null default now(),
  sent_at         timestamptz,
  attempts        integer not null default 0,
  last_error      text
);

-- sample_requests: PRD 2.1 limits and the three answers (so the Inngest event carries only the id).
create table sample_requests (
  id              uuid primary key default gen_random_uuid(),
  device_hash     text not null,             -- sha256 of the first-party device cookie + RATE_LIMIT_SALT
  contact_hash    text,                      -- sha256 of normalized email or phone, when given
  ip_prefix_hash  text not null,             -- sha256 of the /24 (or /48) + salt, for the IP window
  name            text not null,
  topic           text not null,
  job             text,
  answers_audio_ref text,                    -- when answered by voice; deleted with the sample
  share_token     text not null unique,      -- 22 chars base64url; GET /s/{share_token}.mp3, no login
  expires_at      timestamptz not null,      -- created_at + 30 days; audio and row deleted by retention/daily
  episode_id      uuid references episodes(id),
  created_at      timestamptz not null default now()
);
create index on sample_requests (device_hash, created_at);
create index on sample_requests (contact_hash, created_at);
create index on sample_requests (ip_prefix_hash, created_at);

-- calls: one row per live call, typed onboarding exchange or voice-note thread (shared with the live-call domain).
create table calls (
  id              uuid primary key default gen_random_uuid(),
  learner_id      uuid not null references learners(id),
  session_id      uuid references sessions(id),
  kind            text not null check (kind in ('onboarding','first','main','round_two','small_door','then_and_now')),
  mode            text not null default 'live' check (mode in ('live','voice_notes','typed')),
  room_name       text,
  brief_ref       text,
  worker_region   text,                      -- CALL_WORKER_REGION at dispatch
  started_at      timestamptz, ended_at timestamptz,
  end_reason      text,                      -- natural_close, learner_ended, timeout_8m, pipeline_error, crisis, policy, drained
  vendors         jsonb not null default '{}',
  created_at      timestamptz not null default now()
);
```

Billing state is 07 D12's (`subscriptions {learner_id, plan: one_a_day|two_a_day|three_a_day, state: trialing|active|past_due|canceled|expired, founding_locked, founding_seq, current_period_end, customer_ref}` and `payment_events`; ADR-04, ADR-21); this document only requires that `learners.status` and `learners.plan` are derived from it in the same transaction (the allowance reads `learners.plan`) and that `retention/daily` runs 07's `billing/reconcile` [P1]. The 48 h grace in section 5 is the `past_due` state during the processor's retry window.

**The `events` contract (`POST /v1/events`, `POST /internal/events`).** [DECISION] A batch of up to 50 items `{client_event_id (UUIDv7), type, door, occurred_at, payload}`, body at most 64 KB; `events` has `unique (learner_id, client_event_id)`; the response is `{accepted, duplicates, rejected: [{client_event_id, reason}]}` (04 flow A, 06 D11). `occurred_at` is the client's clock, `received_at` the server's; ordering is by `(occurred_at, seq)` with a skew guard of 24 h (the PWA replays its IndexedDB queue for up to 24 h after an outage). `day.became_active` is derived server-side from the deduplicated rows, so a replay never double-counts a play or starts a second `day/next`. The `events` table (data domain) is partitioned by month on `occurred_at`; this domain requires that partitions exist 3 months ahead (a `retention/daily` step creates them) and that `events` carries `inngest_run_id` and `vendor_call_id` columns for tracing.

### 4.3 Inngest: functions, triggers, crons, fan-outs

Rule that binds every function: **Inngest sees pointers, never content.** Event payloads and step return values carry ids, timestamps, enums and short codes; names, emails, transcripts, scripts, briefs and audio stay in Postgres and S3 and are looked up inside the step. A CI test (07) fails the build if any event model has a field named `name`, `email`, `text`, `topic`, `quote`, `transcript` or `audio`, or any string field without a `max_length` of 200 or less. This keeps learner content out of Inngest's EU storage and keeps step outputs under its size limits.

Event catalogue (names are canonical across the nine documents; payloads are Pydantic models in `forone.core.events`; every event used by a function below is listed here):

```python
# forone/core/events.py (complete catalogue for this domain's functions)
from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel, Field
from uuid import UUID

Short = Field(max_length=200)

# --- daily loop (sender: api unless noted) ---
class DayBecameActive(BaseModel):          # "day.became_active"; sent once per (learner, local_date), status in (trial, paid); at A9 on the onboarding day
    learner_id: UUID; local_date: date; schedule_version: int
class IdeaChosen(BaseModel):               # "idea.chosen"; api inserts the episodes row first and passes its id
    learner_id: UUID; local_date: date; idea_id: UUID; episode_id: UUID; source: Literal["pick","tell_salma","remix","cutoff","late"]
class LearnerCutoffReached(BaseModel):     # "learner.cutoff_reached"; sender: workflows (day/next), which inserted the episodes row
    learner_id: UUID; plan_id: UUID | None; episode_id: UUID; drop_at: datetime
class LearnerSwapRequested(BaseModel):     # "learner.swap_requested"; after the one-swap check; episode_id is the new row
    learner_id: UUID; replaced_episode_id: UUID; episode_id: UUID
class LearnerExtraRequested(BaseModel):     # "learner.extra_requested"; POST /v1/episodes/next after the allowance check; the planned row moved to requested (ADR-05)
    learner_id: UUID; local_date: date; episode_id: UUID; slot: int
class LearnerReturnDetected(BaseModel):    # "learner.return_detected"; app open or feed-link exchange only, never a feed fetch; idempotent per local_date
    learner_id: UUID; local_date: date; days_away: int; episode_id: UUID
class OnboardingIntakeCompleted(BaseModel):# "onboarding.intake_completed"; end of A3 (talk or type); episode_id is the pilot row
    learner_id: UUID; intake_facts_ref: str = Short; name_clip_ref: str | None = Short; episode_id: UUID
class SampleRequested(BaseModel):          # "sample.requested"; the answers stay in sample_requests
    sample_id: UUID; episode_id: UUID; device_key: str = Short
class WorkingOnChanged(BaseModel):         # "working_on.changed"; veto or addition in the notebook; same-day re-plan
    learner_id: UUID
class LearnerScheduleChanged(BaseModel):   # "learner.schedule_changed"; cancels day/next; api then re-sends day.became_active with the new version
    learner_id: UUID; schedule_version: int; local_date: date

# --- pipeline (sender: workflows, episode/produce) ---
class EpisodeReady(BaseModel):             # "episode.ready"
    learner_id: UUID | None; episode_id: UUID; episode_kind: str = Short; drop_at: datetime | None; artifact_ids: list[UUID]; fallback: bool = False
class EpisodeStreamingStarted(BaseModel):  # "episode.streaming_started"; api mints the URL from the media object id (02 aligned to this)
    episode_id: UUID; first_segment_media_object_id: UUID
class EpisodeFallbackShipped(BaseModel):   # "episode.fallback_shipped"
    learner_id: UUID; episode_id: UUID; fallback_of: UUID
class EpisodeFailed(BaseModel):            # "episode.failed"
    learner_id: UUID | None; episode_id: UUID; step: str = Short; reason: str = Short
class IdeasReady(BaseModel):               # "ideas.ready"; the Today screen reads the ideas table by plan_id
    learner_id: UUID; plan_id: UUID
class PipelineHumanPage(BaseModel):        # "pipeline.human_page"; consumed by the ops domain
    learner_id: UUID | None; reason: str = Short; count_7d: int | None = None
class DropPublished(BaseModel):            # "drop.published"; sender: day/next
    learner_id: UUID; episode_id: UUID; notified: bool

# --- session, call, chat, recording (sender: api unless noted) ---
class SessionStarted(BaseModel):           # "session.started"; cancels gap/note
    learner_id: UUID; session_id: UUID
class CallEnded(BaseModel):                # "call.ended"; from call-worker via api
    learner_id: UUID; call_id: UUID; session_id: UUID | None; kind: str = Short; end_reason: str = Short; voice_storage: bool
class CallTurnAudioReady(BaseModel):       # "call.turn_audio_ready"; per learner turn; is_last marks the final turn of a finished call
    learner_id: UUID; call_id: UUID; turn_index: int; media_object_id: UUID; is_last: bool = False
class VerbatimTurnCompleted(BaseModel):    # "verbatim.turn_completed"; sender: workflows (call/verbatim-turn)
    learner_id: UUID; call_id: UUID; turn_index: int; low_confidence: bool
class VoiceNoteReceived(BaseModel):        # "voicenote.received"
    learner_id: UUID; call_id: UUID; media_object_id: UUID
class ChatClosed(BaseModel):               # "chat.closed"; at message 5 or the learner's last message
    learner_id: UUID; session_id: UUID; chat_id: UUID
class RecordingCompleted(BaseModel):       # "recording.completed"; all three then-and-now uploads are in (05)
    learner_id: UUID; recording_id: UUID; season_number: int; form: str = Short
# (the first drafts' NotesReady event is removed: there is no notes stage, ADR-06)
class SessionAfterPassCompleted(BaseModel):# "session.after_pass.completed"; sender: workflows
    learner_id: UUID; session_id: UUID; learner_model_version: int
class CrisisActivated(BaseModel):          # "crisis.activated"; sender: api (from the worker or chat) or workflows (analyst); 07 D9
    learner_id: UUID; source: str = Short; surface: str = Short; call_id: UUID | None; session_id: UUID | None; event_id: UUID

# --- audio and consent ---
class MediaObjectCreated(BaseModel):       # "media.object_created"; sender: api (worker uploads, voice notes, say-it-once, shadow, recordings)
    learner_id: UUID; media_object_id: UUID; kind: str = Short; ephemeral: bool; call_id: UUID | None
class LearnerConsentChanged(BaseModel):    # "learner.consent_changed"; mirrors 07's consent_change event
    learner_id: UUID; voice_storage: bool | None; data_use: bool | None; text_shown_version: str = Short
class GapArmed(BaseModel):                 # "gap.armed"; when the learner opts in or edits the gap, and after each session
    learner_id: UUID; gap_days: int; armed_at: datetime

# --- account ---
class LearnerDeletionRequested(BaseModel): # "learner.deletion_requested"
    learner_id: UUID
class LearnerExportRequested(BaseModel):   # "learner.export_requested"; the email is read from learners at send time
    learner_id: UUID
class ProofRequested(BaseModel):           # "proof.requested"; sender: proof/fanout
    learner_id: UUID; week_start: date
class SeasonBoundary(BaseModel):           # "season.boundary"; sender: season/fanout
    learner_id: UUID; season_number: int

# --- vendors ---
class VendorDegraded(BaseModel):           # "vendor.degraded"; sender: vendor/health
    vendor: str = Short; capability: str = Short; auto_switched: bool
class VoiceVendorFailover(BaseModel):      # "voice.vendor_failover"; sender: episode/produce or /admin/vendors; drives the on-air line
    from_vendor: str = Short; to_vendor: str = Short; at: datetime
```

Function table. "Owner" names the architecture domain that writes the step bodies; this domain owns the function shells, triggers and limits.

| Function id | Trigger | Config | Steps (summary) | Owner of step bodies |
|---|---|---|---|---|
| `day/next` | `day.became_active` | idempotency `learner_id-local_date-schedule_version`; `cancel` on `learner.schedule_changed` (match learner) and `learner.deletion_requested`; concurrency 1 per learner | compute `drop_at` by the 3.4 rule; read `episodes` for that date (a cancelled-and-restarted run or a replay skips the waits already satisfied); insert the `planned` extra rows up to `plan.episodes_per_day` and set `learner_schedule.expects_drop` (ADR-05, ADR-19); `wait_for_event idea.chosen` until the cutoff (clamped at zero); on timeout insert the `episodes` row and send `learner.cutoff_reached`; `wait_for_event episode.ready` until `drop_at`; `sleep_until drop_at`; close the previous session and create the new one; publish feed item; push; `drop.published`; if not ready at `drop_at`: `pipeline.human_page`, keep waiting until `drop_at + 18h`, publish late without a push | this domain |
| `episode/produce` | `idea.chosen`, `learner.cutoff_reached`, `learner.swap_requested`, `learner.extra_requested`, `learner.return_detected`, `onboarding.intake_completed`, `sample.requested`, `working_on.changed` | idempotency `episode_id` (every trigger carries it; the row exists in state `requested` before the event is sent); concurrency 1 per learner (a swap cancels a running daily), 150 global in beta (inside the Inngest plan's concurrency cap, verified in week 1); on-demand kinds prioritized via the priority expression; `cancel` on `learner.schedule_changed` is **not** set: the function re-reads `episodes.drop_at` (updated by `api` on a schedule change) before each cut-line decision | teacher (one day plan with 1 to 3 episode briefs; skipped for `daily_extra`, which starts at the writer from its planned brief, ADR-05) → write → fit (≤ 2 loops) → variety → edit (+ 1 repair; check 10 widened to "nothing reads as a correction or a lesson", ADR-06) → voice (fan-out per segment; scene 1 gated by checks 3, 4, 5, 7, 10 before `episode.streaming_started` on streaming kinds) → mix → align → relisten → glosses → publish; fallback episode on second editor fail; `episode.failed` and `pipeline.human_page` when unrecoverable | episode domain (the function and its steps); this domain (the shell config above) |
| `session/after-pass` | `call.ended`, `chat.closed`, `voicenote.received`, `recording.completed` | concurrency 1 per learner; one function with the 10-minute budget (ADR-06: the 90-second notes stage is gone) | finish the last verbatim; analyst (first stage inside the pass), classifier, measures, `word_uses` and `structure_observations` rows (04's tables, written here), updater, memory keeper, the echo plan for the next host brief; `session.after_pass.completed`; 07's `research/anonymize` step when `consents.data_use` | assessment domain |
| `call/verbatim-turn` | `call.turn_audio_ready` | concurrency 20 global in the beta (vendor contract; scaled in 4.10); priority expression `event.data.is_last ? 100 : 0` so the last turn of a finished call jumps the queue; retries 2; secondary verbatim vendor when the queue age exceeds 30 s | verbatim transcription of one turn → **append** `call_turn_verbatim` through `events.append()` (04 D2; nothing updates an event) → `verbatim.turn_completed`; **if voice storage is off, delete that turn's audio now** (PRD 5.4.11) | assessment domain |
| `call/voice-note-reply` | `voicenote.received` | concurrency 1 per call | verbatim STT → host reply text from the brief → call TTS → append to call thread | live-call domain |
| `audio/expire` | `media.object_created {ephemeral: true}` | idempotency `media_object_id`; retries 5 | `sleep_until expires_at` (created + 15 min); if the object is not yet deleted (the verbatim path usually got there first), delete it; mark the call's evidence low-confidence if its verbatim is not done (PRD 5.4.11); write 07's `privacy_audit_runs` row. Covers call turns, the full recording, voice notes, say-it-once, shadow lines and the three then-and-now parts unless `kept_explicitly` | this domain |
| `learner/purge-audio` | `learner.consent_changed {voice_storage: false}`, `call.ended {voice_storage: false}` (07: a flip during a call) | retries 5; concurrency 1 per learner | delete every learner-voice `media_objects` row; verify within 24 h; report to `retention/daily` and `privacy/verify` | this domain |
| `gap/note` | `gap.armed` | `cancel` on `session.started` (match learner); idempotency `learner_id-armed_at`; status guard `trial`, `paid` | `sleep_until armed_at + gap_days`; `messaging.gap_note(learner_id)` sends email and push once; mark sent | this domain |
| `proof/fanout` | cron `0 * * * *` | single run; role `forone_workflows` | select `trial` and `paid` learners whose local proof time (proof weekday at drop time, or onboarding weekday + 7 days until `proof_weekday` is known, PRD 11.1.1) falls in the past hour; send `proof.requested` | this domain |
| `proof/make` | `proof.requested` | concurrency 1 per learner | read passed claims (claim gate output), proof producer scripts, voice (segments), publish above Today and to the feed without closing the session | assessment and episode domains |
| `season/fanout` | cron `0 * * * *` | single run; P1; `trial` and `paid` only; learner-local day boundaries that passed in the last hour (ADR-16) | learners whose season day 28 closed in that hour → `season.boundary`; the pipeline plans the finale (rater and proof producer steps) and the next season's opening (PRD 9.1 #5, 11.2) | this domain |
| `retention/daily` | cron `15 * * * *` | single run; role `forone_workflows`; per learner-local midnight that passed in the last hour (ADR-16; the name stays, the clock is the learner's) | `trial_ended` 90-day warnings (`messaging.transactional(kind='retention_warning')`) and deletions; verify revoked learners have no audio; delete expired samples (audio, `sample_requests` row, `answers_audio_ref`); drop `model_io` partitions older than 90 days; create `events` partitions 3 months ahead; report `media_objects` with `expires_at` past (should be empty); 07's `billing/reconcile` [P1] | this domain |
| `learner/export` | `learner.export_requested` | retries 3 | assemble JSON (stores), transcripts, kept audio (decrypted and re-encrypted under a one-time zip password), 07's consent and access files into `forone-exports`; look up the email; `messaging.transactional(kind='export_ready')` with a 7-day link within 1 h | data domain (content), this domain (shell) |
| `learner/delete` | `learner.deletion_requested` | retries 5; `cancel` none | revoke sessions, feed tokens and push subscriptions at once; cancel running functions for the learner; delete S3 objects by `media_objects`; **delete the learner's traces in Langfuse by pseudonym (08 §4.3.4; it does not hold up the "deleted" email, ADR-09), scrub the Sentry user, delete the Resend contact and suppression entries, delete LiveKit room metadata if any persists (LiveKit Cloud keeps none by our settings [ASSUMPTION, verified in build week 1])**; delete show kinds by prefix (`sse_kms_env`, ADR-12); delete rows including `research_pseudonyms` (role `forone_purge`); set `learner_keys.destroyed_at`, bump `key_version` so every cached DEK misses (ADR-18), then delete the row; mark `deleted` within 24 h; write 07's `deletion_ledger`; log for the 30-day backup window | this domain |
| `crisis/activate` | `crisis.activated` | retries 5 | insert `crisis_log`, quarantine the event, page ops with ids only (07 D9) | security domain |
| `vendor/health` | cron `*/5 * * * *` | single run | roll `vendor_health` windows; if failures ≥ 5 and success rate < 50% in 10 min: for `streaming_stt`, `verbatim_stt`, `editor` set `vendor_config` to the secondary (honoring the writer/editor pair rule) and send `vendor.degraded {auto_switched: true}`; for `episode_tts`, `call_tts`, `salma_tts` send `vendor.degraded {auto_switched: false}` and page (manual one-click switch on `/admin/vendors`) | this domain |
| `cost/reconcile-spend` | cron `45 * * * *` | single run (08) | compare `vendor_calls` with the worker's S3 spool and the vendors' usage endpoints for the last hour; insert missing rows; re-upsert `learner_spend_daily` (ADR-13) | cost domain |
| `outbox/relay` | cron `* * * * *` | single run | send unsent outbox rows (batches of 100), backoff on error | this domain |

The `day/next` shell, as it will be written:

```python
# apps/workflows/functions/day_next.py
import inngest
from datetime import timedelta
from forone.core import schedule, episodes, sessions, feed, messaging, ideas, ops
from forone.core.time import now, iso, clamp_timeout

@client.create_function(
    fn_id="day/next",
    trigger=inngest.TriggerEvent(event="day.became_active"),
    idempotency="event.data.learner_id + '-' + event.data.local_date + '-' + string(event.data.schedule_version)",
    cancel=[
        inngest.Cancel(event="learner.schedule_changed", if_exp="event.data.learner_id == async.data.learner_id"),
        inngest.Cancel(event="learner.deletion_requested", if_exp="event.data.learner_id == async.data.learner_id"),
    ],
    concurrency=[inngest.Concurrency(limit=1, key="event.data.learner_id")],
    retries=3,
)
async def day_next(ctx: inngest.Context, step: inngest.Step) -> None:
    lid, local_date = ctx.event.data["learner_id"], ctx.event.data["local_date"]
    plan = await step.run("compute-drop", lambda: schedule.plan_next_drop(lid, local_date))
    # plan = {drop_at, drop_date, pricing: "batch"|"on_demand", pick_wait_until}   (the 3.4 rule: lead >= 7 h batch; 2..7 h on-demand with a 30 min pick wait; < 2 h next day)
    drop_at = plan["drop_at"]

    await step.run("plan-extras", lambda: episodes.plan_extras(lid, plan["drop_date"]))                # planned rows for slot 2..episodes_per_day (ADR-05); sets learner_schedule.expects_drop
    existing = await step.run("existing", lambda: episodes.daily_for(lid, plan["drop_date"]))   # a restarted run skips what is already done
    if existing is None:                                                                                  # no pick yet for that date
        pick = await step.wait_for_event("wait-pick", event="idea.chosen",
                                         if_exp=f"async.data.learner_id == '{lid}'",
                                         timeout=clamp_timeout(plan["pick_wait_until"] - now()))            # never negative
        if pick is None:                                                                                  # PRD 3.1 rule 5
            ep = await step.run("cutoff-row", lambda: episodes.insert_requested(lid, plan["drop_date"], "daily", drop_at, plan["pricing"]))
            await step.send_event("cutoff", inngest.Event(name="learner.cutoff_reached",
                                  data={"learner_id": lid, "plan_id": ep["plan_id"], "episode_id": ep["id"], "drop_at": iso(drop_at)}))

    ready = await step.run("already-ready", lambda: episodes.ready_daily_for(lid, plan["drop_date"]))
    if ready is None:
        ev = await step.wait_for_event("wait-ready", event="episode.ready",
                                       if_exp=f"async.data.learner_id == '{lid}' && async.data.episode_kind == 'daily'",
                                       timeout=clamp_timeout(drop_at - now()))
        ready = ev.data if ev else None
    await step.sleep_until("until-drop", drop_at)
    late = False
    if ready is None:                                                                                     # Today keeps yesterday's episode; no push (PRD 3.6)
        await step.send_event("page", inngest.Event(name="pipeline.human_page",
                              data={"learner_id": lid, "reason": "episode not ready at drop time"}))
        ev = await step.wait_for_event("wait-ready-late", event="episode.ready",
                                       if_exp=f"async.data.learner_id == '{lid}' && async.data.episode_kind == 'daily'",
                                       timeout=timedelta(hours=18))
        if ev is None:
            return
        ready, late = ev.data, True
    ep_id = ready["episode_id"]
    await step.run("sessions", lambda: sessions.close_previous_and_create(lid, ep_id))                   # PRD 4 rules 7 and 8, latest point
    await step.run("publish-feed", lambda: feed.publish(lid, ep_id))                                      # sets feed_items.published_at
    notified = False if late else await step.run("push", lambda: messaging.drop_notification(lid, ep_id)) # title and length only (PRD 3.3)
    await step.send_event("published", inngest.Event(name="drop.published", data={"learner_id": lid, "episode_id": ep_id, "notified": notified}))
```

Schedule changes: `api` updates `learner_schedule` (version + 1), updates `episodes.drop_at` and `deadline_at` for any `requested`-to-`voiced` daily episode of that learner, sends `learner.schedule_changed` (which cancels the running `day/next`) and then sends `day.became_active` with the new `schedule_version` for the same `local_date`; the new run's `existing` and `already-ready` steps skip whatever is already done. Deadline handling inside `episode/produce` is the pipeline domain's (batch cut lines at `drop_at - 4h` for the teacher and `drop_at - 2h30` for the writer, the PRD's switch at `drop_at - 90min`, re-read from `episodes.drop_at` at each decision); this domain only requires that every batch step polls with `step.sleep` rather than holding a connection, so `workflows` tasks stay small.

### 4.4 The call path (topology only; the live-call domain owns the pipeline)

1. `POST /v1/calls {sessionId, kind}` in `api`: checks the door rules (PRD 4) and `learners.status`, writes `calls` (with `worker_region` and the learner's `[native_language, target_language]` for the recognizer and the voices, ADR-02), compiles nothing (the host brief was compiled in `episode/produce` and stored at `brief_ref`), derives the per-call key `HKDF(DEK, "call:" + call_id)`, mints a per-call JWT (5-minute TTL, audience `call-worker`, subject `call_id`), creates a LiveKit room `call-{callId}` with agent dispatch metadata `{callId, jwt}`, returns a participant token (10-minute TTL) and the room URL. Onboarding A3 and A7 use the same path from `POST /v1/onboarding/start` and `POST /v1/onboarding/{id}/first-call`.
2. `call-worker` receives the dispatch, calls `GET /internal/calls/{callId}/brief` with the JWT and gets: the one-page host brief (or the Salma onboarding persona for A3), the Salma talkback brief (produced-word history as a dict), the vendor selection for this call from `vendor_config`, **the per-call key (32 bytes, in memory only, zeroized at call end; never the learner DEK)**, `voiceStorage` (false for `pre_account`), the anxiety flag and pause profile, and the crisis clip references.
3. The worker runs the LiveKit `AgentSession`: VAD, multilingual turn detector, STT plugin (Soniox or Deepgram), LLM plugin (Anthropic, cached brief), TTS plugin (the call voice from `vendors.yaml`). The S-button sends a data-channel message that flips the worker into talkback mode for that press.
4. Per learner turn, the worker writes the turn's audio (Opus, 24 kHz) to `forone-voice/{ephemeral/}learners/{lid}/calls/{callId}/turn-{n}.ogg (04 D15: `ephemeral/` is the bucket-level prefix)` with SSE-C under the call key, posts `call_turn` (streaming text, timings) to `/internal/events`, and posts `call.turn_audio_ready` (`api` inserts the `media_objects` row and emits `media.object_created`), which starts verbatim transcription while the call continues. The final turn carries `is_last: true`.
5. At the end: `call.ended` with `end_reason`; if voice storage is on, the worker also uploads the full mixed recording (`call_full`). A crisis step-out posts `crisis` to `/internal/events`; `api` emits `crisis.activated`.
6. Capacity: one Fargate task (2 vCPU, 4 GB) runs about 8 concurrent calls [ASSUMPTION, measured in the build-week-2 50-call test and the week-4 load test]; autoscaling target 60% CPU, minimum 1 task per environment, maximum 40 in the beta (about 320 concurrent calls).
7. [DECISION] **Deploys and scale-in never cut a call.** A call lasts up to 8 min and ECS Fargate's `stopTimeout` maximum is 120 s, so: (a) every `call-worker` task sets ECS task scale-in protection while `active_jobs > 0` (the worker calls the ECS agent endpoint on job start and job end); (b) a deploy starts the new task set, puts the old tasks into LiveKit Agents drain mode (stop accepting jobs; `SIGTERM` handled by the SDK's drain hook) and stops each old task only when idle or after 10 min; `tools/release` runs this loop; (c) there is no fixed deploy window, because learners drop and call at every hour (ADR-16): `tools/release` computes the window from `learner_schedule` and refuses a deploy when more than 2% of learners have a drop in the next 45 minutes (an override needs a reason row), and the `call-worker` step proceeds only when the old tasks are idle; (d) a task that must stop with a call running ends it with `end_reason = drained` and the client falls to voice notes, which is the "deploy during a call" row in section 5. The same drain applies to `workflows` only in the trivial sense that Inngest retries an interrupted step.

### 4.5 Vendor adapter layer

Capabilities and their interfaces live in `forone.adapters`. The live path uses LiveKit plugins for STT, LLM and TTS; the same `vendors.yaml` selects them, so a swap is one line in both paths.

```python
# packages/adapters/forone/adapters/interfaces.py
from dataclasses import dataclass
from typing import AsyncIterator, Literal, Protocol, Sequence

@dataclass(frozen=True)
class CallMeta:            # attached to every adapter call; the tracing middleware writes vendor_calls (own transaction, ADR-13) and the Langfuse span from it
    learner_id: str | None; role: str; episode_id: str | None; call_id: str | None; learner_model_version: int | None
    data_use: bool = False # from consents; True lets the middleware send scrubbed prompt and completion text to Langfuse

@dataclass(frozen=True)
class TextResult:
    text: str; input_tokens: int; output_tokens: int; cached_tokens: int; model: str; vendor: str; cost_usd: float; request_id: str

class TextModel(Protocol):
    async def complete(self, *, system: str, messages: Sequence[dict], schema: dict | None, max_tokens: int,
                       temperature: float, cache_prefix: str | None, meta: CallMeta) -> TextResult: ...
    async def stream(self, *, system: str, messages: Sequence[dict], meta: CallMeta) -> AsyncIterator[str]: ...

class BatchTextModel(Protocol):
    async def submit(self, *, requests: Sequence[dict], meta: CallMeta) -> str: ...            # returns batch id
    async def poll(self, batch_id: str) -> Literal["running", "done", "failed"]: ...
    async def results(self, batch_id: str) -> Sequence[TextResult]: ...
    async def cancel(self, batch_id: str) -> None: ...

@dataclass(frozen=True)
class SynthResult:
    audio: bytes; content_type: str; duration_ms: int; word_timings: list[tuple[str, int, int]] | None
    chars: int; vendor: str; voice_id: str; cost_usd: float

class SpeechSynth(Protocol):               # batch: episodes, read-aloud, recap, proof
    async def synthesize_dialogue(self, *, lines: Sequence[tuple[str, str]], voices: dict[str, str], accent: str,
                                  rate: float, tags: bool, meta: CallMeta) -> SynthResult: ...
    def supports_timestamps(self) -> bool: ...

class StreamingSpeechSynth(Protocol):      # live: the host and Salma on the call (also the LiveKit TTS plugin's config)
    def livekit_plugin(self, *, voice_id: str, rate: float): ...

class StreamingRecognizer(Protocol):       # live: host turns and native-language talkback (languages = [native, target] per call, ADR-02)
    def livekit_plugin(self, *, languages: Sequence[str], code_switch: bool): ...

@dataclass(frozen=True)
class VerbatimResult:
    words: list[dict]   # {text, start_ms, end_ms, confidence}
    text: str; vendor: str; cost_usd: float; disfluencies_kept: bool

class VerbatimRecognizer(Protocol):        # after: verbatim with fillers, false starts, confidences
    async def transcribe(self, *, audio: bytes, content_type: str, language: str, meta: CallMeta) -> VerbatimResult: ...

class Pronunciation(Protocol):             # known sentences only
    async def score(self, *, audio: bytes, reference_text: str, meta: CallMeta) -> dict: ...

class Aligner(Protocol):                   # forced alignment when the TTS vendor gives no timestamps
    async def align(self, *, audio: bytes, transcript: str, meta: CallMeta) -> list[tuple[str, int, int]]: ...

class Embeddings(Protocol):
    async def embed(self, *, texts: Sequence[str], meta: CallMeta) -> list[list[float]]: ...

# forone.core.messaging: the PRD 3.10 guard. The only module that imports the Resend client or reads the VAPID keys.
TransactionalKind = Literal["signin_code","receipt","trial_ending","payment_failed","export_ready","account_deleted",
                            "retention_warning",   # PRD 12.5.9 "one email warning"; not in 3.10's table (section 10 #10)
                            "invite"]              # PRD 2.1.6; not in 3.10's table (section 10 #10)
class Messaging(Protocol):
    async def drop_notification(self, learner_id: str, episode_id: str) -> bool: ...     # web push to installed devices only (push_subscriptions)
    async def gap_note(self, learner_id: str) -> None: ...                               # email + push, once, opt-in
    async def transactional(self, *, learner_id: str | None, to: str | None, kind: TransactionalKind, data: dict) -> str: ...
# A Ruff rule (banned-api) forbids `resend` and `pywebpush` imports outside forone.core.messaging; a unit test asserts the enum has 8 members.

class Payments(Protocol):
    async def create_checkout(self, *, learner_id: str, plan: Literal["one_a_day","two_a_day","three_a_day"], return_url: str) -> str: ...  # ADR-04; the MoR processor adds tax at checkout (ADR-21)
    async def handle_webhook(self, *, headers: dict, body: bytes) -> list[dict]: ...  # normalized subscription events
    async def refund(self, *, subscription_ref: str, amount: int, reason: str) -> str: ...
    async def reconcile(self, *, since: str) -> list[dict]: ...
```

Selection and failover:

```yaml
# packages/adapters/vendors.yaml  (checked in; vendor_config rows override at runtime)
rules:
  editor_vendor_must_differ_from_writer: true      # PRD 6.1.4, 14.3; checked in adapters.for_role at selection time, in every failover state
  call_tts_same_vendor_as_episode_tts: preferred    # PRD 14.3; see note under episode_tts
roles:
  teacher:        {vendor: anthropic, model: claude-opus-5.5,   pricing: batch,    fallback: {vendor: anthropic, model: claude-sonnet-5.5}}
  writer:         {vendor: anthropic, model: claude-sonnet-5.5, pricing: batch,    fallback: {vendor: google, model: gemini-3.8-flash}}
  fitter:         {vendor: anthropic, model: claude-haiku-5.5,  pricing: standard}
  editor:         {vendor: google,    model: gemini-3.8-flash,  pricing: standard, fallback: {vendor: anthropic, model: claude-opus-5.5, flag: same_vendor_edit}}
  # Pair rule: when the writer is on its fallback (google), the editor is forced to its fallback (anthropic), and vice versa,
  # so writer.vendor != editor.vendor holds whenever two vendors are up. When only Anthropic is up the editor runs on
  # claude-opus-5.5 (at least as strong as the writer, never code checks only) and every episode is flagged same_vendor_edit
  # for review (ADR-11; the first draft's Haiku fallback is rejected). If both vendors are down there is no editor and the
  # pipeline waits (fallback episode at the cut line). Both single-vendor-down states are [ASSUMPTION] degraded modes with
  # the human-review sample doubled for the day.
  host:           {vendor: anthropic, model: claude-sonnet-5.5, pricing: standard, fallback: {vendor: google, model: gemini-3.8-flash}}
  salma_text:     {vendor: anthropic, model: claude-sonnet-5.5, pricing: standard}
  chat_host:      {vendor: anthropic, model: claude-sonnet-5.5, pricing: standard}
  analyst:        {vendor: anthropic, model: claude-haiku-5.5,  pricing: standard}
  memory_keeper:  {vendor: anthropic, model: claude-haiku-5.5,  pricing: standard}
  proof_producer: {vendor: anthropic, model: claude-sonnet-5.5, pricing: batch}
  rater:          {vendor: anthropic, model: claude-sonnet-5.5, pricing: standard, pinned_until: 2027-02-16}   # PRD 10.11: pinned per window; 05 sets the first window to 2026-12-23 to 2027-02-16 so no cohort's first finale crosses a boundary (05 4.15)
  # Roles that depend on the target language are keyed by it (ADR-03); the values come from languages/<target>/gate.yaml.
  episode_tts:    {en: {vendor: VOICE_WINNER, secondary: VOICE_RUNNER_UP}}  # filled from the language gate's blind test by 2026-11-17
  call_tts:       {en: {vendor: VOICE_WINNER, secondary: VOICE_RUNNER_UP}}
  # The blind test rates each vendor's episode voice and call voice as a pair. A vendor with no streaming low-latency voice
  # (Gemini 3.8 Flash TTS is one of the three candidates and has none) is eligible for episode_tts only with a declared
  # accent-matched call_tts from the runner-up, and that mismatch is announced on air once (PRD 7.1.3) and asked about in
  # the day-7 check-in, as Milestone 0 already does with ElevenLabs Agents.
  salma_tts:      {ar: {vendor: SALMA_WINNER, secondary: SALMA_RUNNER_UP}, en: {vendor: VOICE_WINNER}}   # per native package (ADR-02); the Arabic voice from the 7.3 test
  streaming_stt:  {en: {vendor: soniox,  secondary: deepgram}}              # gate check 2 (ADR-03); languages = [native, target] per call
  verbatim_stt:   {en: {vendor: assemblyai, secondary: elevenlabs_scribe}}  # gate check 2
  pronunciation:  {en: {vendor: speechace, secondary: microsoft}}
  aligner:        {vendor: elevenlabs_alignment, secondary: whisperx_local}
  embeddings:     {vendor: google, model: gemini-embedding-001}            # [DECISION] no new processor: Google already sees every script as the editor
voices:                                                                     # per package: languages/<target>/voices.yaml and native/<lang>/salma.yaml
  karim: {british: {elevenlabs: "...", inworld: "...", google: "..."}, american: {...}}
  mona:  {...}
  salma: {ar: {gulf: {...}, neutral: {...}}, en: {...}}
```

Swap mechanics: `adapters.for_role("episode_tts")` reads `vendors.yaml`, then `vendor_config` (cached 60 s), applies the `rules`, and returns the adapter plus the voice map for the host and accent. A failover is `UPDATE vendor_config` from `/admin/vendors` (voices, always manual) or by `vendor/health` (recognizers and the editor). Every adapter call passes through one middleware that times it, computes cost from a price table in the package (`prices.yaml`, dated; the 2027-01-01 Gemini doubling is a second dated row and lands in beta week 2), writes a `vendor_calls` row (cost domain) **in its own short transaction the moment the vendor responds**, idempotent on `(inngest_run_id, step, attempt)` or `(call_id, turn_index, capability)`, with the same statement upserting `learner_spend_daily` (ADR-13: a cost row inside the caller's transaction is lost on exactly the retry the spend guard exists to catch); in `call-worker` the row is first appended to an S3 spool per turn and flushed from there, and `cost/reconcile-spend` (4.3) fills any gap hourly. The middleware also writes `model_io` for text roles and emits the Langfuse span under decision 15 (`meta.data_use` decides whether anonymized text is attached). Both voice vendors are exercised weekly by a canary episode for a synthetic learner so a cold secondary is never discovered during an outage. Vendor concurrency and rate limits are requested during Milestone 0 with the gate (08 §4.9): 50 streaming STT sessions, 50 call TTS streams, 20 parallel verbatim jobs, the Anthropic batch tier.

### 4.6 The web app

- Next.js 15 App Router, React 19, Tailwind; `html dir` and `lang` come from the learner's native package (`native/ar` renders `dir="rtl" lang="ar"`, `native/en` renders `ltr`; the landing page is served per `Accept-Language` with English as the default, ADR-02); every content block renders with `dir="auto"` so target-language bubbles and native-language text each set their own direction (PRD 1.4).
- PWA: `@serwist/next` service worker; precaches the shell; runtime-caches `episode.m4a` and `timings.json` after first play; web app manifest with `display: standalone`. Web push via the Push API with VAPID (iOS 16.4+ requires the installed app, which A10 asks for); subscriptions are stored in `push_subscriptions` (06) and the drop push goes only to them (PRD 3.3.2).
- Player (06 D3): one `<audio>` element on the stitched `episode.m4a` for every ready episode; a two-element scene handoff only while an on-demand episode is still streaming; Media Session API handlers map previous-track to "replay last sentence" and next-track to "mark" (PRD 5.1); speed 0.75, 0.85, 1.0 only; no control above 1.0 exists in the code.
- Onboarding: A2 offers Talk or Type; Type (and a denied microphone) runs A3 as a text exchange against `api`; A7 then runs as a live call if the mic is available, else as the chat door's typed first exchange.
- Call screen: `livekit-client`, Screen Wake Lock, hold-to-talk pad and the S button as data-channel messages; captions from the worker's transcription events over the data channel.
- The "next one" control (ADR-05): one button after the current episode ends, shown only while `episodes_today < plan.episodes_per_day`, calling `POST /v1/episodes/next`; never autoplay, no list of upcoming episodes; the Show tab lists all of the day's episodes once made. The plan picker on day 7 and "about $1 a day" are 06's (ADR-04).
- No business logic: door rules, the allowance, the swap count and consent flags are enforced by `api` and merely reflected by the UI. The UI law checklist (PRD 1.2) is a lint rule: no component named or styled as a progress bar, chart, percentage, level or streak exists in `apps/web`.
- Hosting: Vercel Pro, functions region `fra1` (follows `HOME_REGION`; `dxb1` if `me-central-1` is chosen, ADR-08), Git integration, preview deploys against staging `api`.

### 4.7 Environments, configuration and secrets

| | dev | staging | prod |
|---|---|---|---|
| Postgres | docker `postgres:16` + pgvector | RDS db.t4g.medium, single AZ, 7-day backups; up from build week 2 through the beta (ADR-16) | RDS db.t4g.large **Multi-AZ** (beta) → db.r6g.xlarge at 10k, 30-day backups, PITR; RPO under 5 min, RTO 2 min on failover, 30 min on restore; a restore drill in week 5 |
| S3 | MinIO | `forone-{media,voice,exports}-staging` | `forone-{media,voice,exports}-prod`, versioning off (deletion must be real), lifecycle rules |
| Inngest | `inngest dev` container | Inngest Cloud env `staging` | Inngest Cloud env `prod` (EU) |
| LiveKit | `livekit-server --dev` | LiveKit Cloud project `forone-staging` | LiveKit Cloud project `forone-prod` |
| Vendors | real keys, `pricing: standard`, spend cap $20/day | real keys, spend cap $50/day | real keys; daily cap Σ over learners of `episodes_per_day × $1.00` (ADR-15), per-learner soft guard 2.5 × `episodes_per_day` × budget and hard guard 4 ×; per-kind caps `sample` $20/day, `pilot` $60/day |
| `web` | `next dev` | Vercel preview + `staging.forone.app` | `app.forone.app` |
| Email | Mailpit | Resend test domain | Resend `forone.app` |

Configuration is twelve-factor: a `Settings` Pydantic model in `forone.core.settings` reads environment variables; the same names are used in Vercel, ECS task definitions and docker compose.

| Key | Example | Used by |
|---|---|---|
| `FORONE_ENV` | `prod` | all |
| `FORONE_SERVICE` | `api`, `workflows`, `call-worker` | Python image entrypoint |
| `HOME_REGION` | `eu-central-1` (default; `me-central-1` the alternative, ADR-08) | infra, S3 and KMS clients |
| `CALL_WORKER_REGION` | `eu-central-1` or `us-east-1` (3.6) | call-worker task placement |
| `DATABASE_URL` | `postgresql+psycopg://...` (role per service: `forone_app`, `forone_workflows`) | api, workflows |
| `S3_BUCKET_MEDIA`, `S3_BUCKET_VOICE`, `S3_BUCKET_EXPORTS` | | api, workflows, call-worker |
| `KMS_KEY_ID`, `MEDIA_ENV_KMS_KEY_ID` | the learner CMK (wraps DEKs); the environment key for `sse_kms_env` show kinds, samples and canaries (ADR-12) | api, workflows |
| `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY`, `INNGEST_BASE_URL` | | api (send), workflows (serve) |
| `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` | | api (tokens, dispatch), call-worker |
| `INTERNAL_JWT_SIGNING_KEY` | per-call JWTs (replaces the static service token) | api (mint and verify) |
| `VENDOR_CONFIG_PATH` | `vendors.yaml` | adapters |
| `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `ELEVENLABS_API_KEY`, `INWORLD_API_KEY`, `SONIOX_API_KEY`, `DEEPGRAM_API_KEY`, `ASSEMBLYAI_API_KEY`, `SPEECHACE_API_KEY` | | workflows, call-worker |
| `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST` | EU host | all Python |
| `SENTRY_DSN` | | all |
| `RESEND_API_KEY`, `EMAIL_FROM` | `show@forone.app` (Salma signs the body; the sender is the show) | api, workflows (messaging only) |
| `VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY`, `VAPID_SUBJECT` | | api, workflows (messaging only) |
| `TURNSTILE_SECRET`, `RATE_LIMIT_SALT` | | api |
| `PAYMENTS_PROVIDER`, `PAYMENTS_SECRET`, `PAYMENTS_WEBHOOK_SECRET` | `paddle` (recommended, merchant of record) or `stripe` (ADR-21; OPEN) | api |
| `APPLE_CLIENT_ID`, `APPLE_TEAM_ID`, `APPLE_KEY_ID`, `APPLE_PRIVATE_KEY`, `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET` | | api |
| `SESSION_SECRET`, `COOKIE_DOMAIN` | `.forone.app` | api |
| `SPEND_CAP_FLOOR_USD_PER_DAY`, `SPEND_CAP_SAMPLE_USD_PER_DAY`, `SPEND_CAP_PILOT_USD_PER_DAY`, `SESSION_BUDGET_USD`, `ONBOARDING_STARTS_PER_DAY` | `50`, `20`, `60`, `1.00`, `120`; the daily cap is `max(floor, Σ episodes_per_day × SESSION_BUDGET_USD)` and the per-learner guards are 2.5 × and 4 × `episodes_per_day` × budget (ADR-15) | adapters middleware, api |
| `ADMIN_IP_ALLOWLIST` | optional second factor for `/admin` (07 §4.13) | api |
| `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_LIVEKIT_URL`, `NEXT_PUBLIC_VAPID_PUBLIC_KEY`, `NEXT_PUBLIC_TURNSTILE_SITE_KEY` | | web |

Secrets live in AWS Secrets Manager and are injected into task definitions; Vercel holds only the `NEXT_PUBLIC_*` keys. No secret is in the repo, the image or a `.env` file outside `dev`.

### 4.8 CI/CD

```yaml
# .github/workflows/ci.yml (on every PR and on main)
jobs:
  python:  uv sync → ruff (incl. the messaging banned-api rule) → pyright → pytest (unit; integration against docker-compose postgres + minio + inngest dev;
           the RLS policy walk; the Inngest payload PII test; the messaging enum test)
  web:     pnpm install → tsc → eslint (includes the law-furniture rule) → next build
  package: validate packages/languages/* (bibles, voices mapped for both vendors, inventory, law words, ban list schema, gate.yaml) and
           packages/native/* (strings with dir, consent texts and notice, Salma lines, crisis clips and resources per country); eval-gate path map per package
  image:   docker build forone-python (ffmpeg, spaCy model, turn-detector and Silero weights baked in) → push to ECR tagged with the git sha (main only)
# deploy-staging.yml: on push to main → alembic upgrade head (one-off ECS task) → ecs update-service api, workflows (rolling, min healthy 100%)
#                     → tools/release drain-replace call-worker → smoke test (POST /v1/sample on staging; one scripted call)
# deploy-prod.yml: on tag v* → manual approval → tools/release window check (binding: refused when > 2% of learners have a drop in the
#                  next 45 min, any hour; override needs a reason row; ADR-16) → same steps against prod, call-worker only when idle (4.4 #7)
#                  → canary episode and canary call on the synthetic learner → notify ops
```

Migrations are additive-only during the beta (no destructive change without a two-step deploy). Rollback is `ecs update-service` to the previous task definition; the database rolls forward only. `web` deploys on Vercel from the same commit; API changes are backward compatible for one release because the installed PWA may run an older build for a day.

### 4.9 Dev environment

```yaml
# infra/docker-compose.yml
services:
  postgres: {image: pgvector/pgvector:pg16, ports: ["5432:5432"], environment: {POSTGRES_PASSWORD: dev}}
  minio:    {image: minio/minio, command: server /data --console-address ":9001", ports: ["9000:9000","9001:9001"]}
  inngest:  {image: inngest/inngest, command: inngest dev -u http://host.docker.internal:8001/api/inngest, ports: ["8288:8288"]}
  livekit:  {image: livekit/livekit-server, command: --dev --bind 0.0.0.0, ports: ["7880:7880","7881:7881","7882:7882/udp"]}
  mailpit:  {image: axllent/mailpit, ports: ["8025:8025","1025:1025"]}
```

`make dev` starts compose, runs migrations, seeds the `languages/en`, `native/ar` and `native/en` packages and three synthetic learners (one per native package, `tz` spread across three continents) from the Milestone 0 learner files, and starts `api` (8000), `workflows` (8001), `call-worker` (dev dispatch) and `web` (3000). A full `episode/produce` run against real vendors costs under $0.70 and takes 3 to 6 minutes locally; `FORONE_FAKE_VENDORS=1` swaps every adapter for a recorded-fixture adapter so tests run free and offline.

### 4.10 Scaling from 15 to 10,000

| Dimension | 15 learners (2026-12-23) | 250 learners (2027-01-26) | 10,000 learners (scale target) | What changes |
|---|---|---|---|---|
| Episodes per day | about 15 (10 drops plus extras at about half the allowance, ADR-05) | about 220 | about 9,000 (60% active; 6,000 drops plus on-demand extras) | Nothing in code; `episode/produce` global concurrency from 150 to 600; TTS vendor concurrency contract; Anthropic batch tier |
| Generation window | spread | spread | about 25 pipelines starting per minute in a timezone band's 22:00 to 02:00, 150 to 300 concurrent when the cohort concentrates; smoother for a worldwide cohort | `workflows` autoscales 1 → 8 tasks on ALB `RequestCountPerTarget` and CPU (Inngest Cloud publishes no queue-depth metric to CloudWatch; the function concurrency limits are the real throttle), fixed 2 tasks during the busiest generation hours (computed from `learner_schedule`, not a wall-clock window) from 250 learners on; RDS connections through RDS Proxy from 250 learners on |
| Concurrent calls at peak | 2 | 15 | 200 to 400 | `call-worker` 1 → 40 tasks (about 8 calls each); LiveKit Cloud scales itself; STT and TTS concurrency contracts are the real ceiling and are negotiated before public launch |
| Verbatim turns at peak | 50 per hour | 400 per hour | about 10,000 per hour in a concentrated cohort's two-hour morning peak (25 turns × 400 calls) | `call/verbatim-turn` concurrency 20 → a contract of 100 to 200 parallel jobs negotiated before public launch; `is_last` priority lets the after-session pass start as soon as a call ends; the secondary verbatim vendor takes overflow when queue age exceeds 30 s; the row did not exist in the first draft |
| Events per day | 2,000 | 30,000 | 1.2 million (about 1 KB each) | Monthly partitions; nothing is detached in the beta (04 D15); compacting cold partitions to Parquet in S3 is a post-beta option |
| Media storage | 1 GB | 20 GB | 20 TB per year of produced audio at 6 MB per episode plus kept voice | Lifecycle: produced audio kept while the account exists (archive promise), so this is the one cost that accumulates; priced in section 6 |
| Media egress | negligible | 30 GB/month, mostly straight from S3 | 2 to 3 TB/month: show kinds from S3 by presigned URL, learner voice and the feed through `api` | Show audio is served by presigned URLs from day one (ADR-12), so `api` carries only learner voice and the podcast feed; a dedicated `media` service on Fargate (same code, separate scaling) for the feed route at about 1,000 learners; CloudFront in front of the `sse_kms_env` prefixes when egress passes about $100 a month; the drop-minute burst (Apple Podcasts sends HEAD plus a full download per subscriber at publish, through `api`) is in the week-4 load test |
| Inngest executions | 20k/month | 300k/month | about 15 million steps/month | Plan tier; if the price curve is wrong at 2,000 learners, the same functions run unchanged on self-hosted Inngest (the named exit); Temporal would be a rewrite of the shells (about two weeks) with the step bodies reused |
| Postgres | db.t4g.large Multi-AZ | db.t4g.large Multi-AZ | db.r6g.xlarge, 500 GB, Multi-AZ, one read replica for admin and analytics | Stores read by the teacher are per-learner rows; no cross-learner query is on a hot path |
| Regions | one (`HOME_REGION`, plus `CALL_WORKER_REGION` if the latency test chooses it) | one | one, plus LiveKit's global edge | Multi-region is not needed at 10,000 learners anywhere: one home region plus the vendor transfers that every option shares is the honest minimum (ADR-08); a second home region would be needed only for a residency rule that forbids the first |

Time-zone concentration is the load shape to size for: with no launch country (ADR-02) a worldwide cohort spreads the nightly generation and the morning calls around the clock, but an invite batch, a market or a referral wave can still put most learners in one band, so the fan-out configuration above is sized for 6,000 learners generating within the same four hours and calling within the same two morning hours, not for a global average. The operational consequence is ADR-16's: there is no quiet hour anywhere in the day.

---

## 5. Failure modes, fallbacks and degraded modes

| Failure | Blast radius | Detection | Degrades to | Recovery |
|---|---|---|---|---|
| Vercel outage | App unreachable; feed still works (served by `api`); calls cannot start (no client) | Better Stack uptime on `app.forone.app` | Learners listen through their podcast app; the drop push still fires | Nothing to do; `web` is stateless |
| `api` down (ECS) | App, feed, media, event ingestion, call start all fail; `workflows` continues producing | ALB health checks, Sentry, uptime | The PWA queues events in IndexedDB for up to 24 h and replays them with client ids (no double counts); calls in progress continue (the worker buffers events for 10 min then writes them to S3 as a spool file ingested later) | ECS replaces tasks; minimum 2 tasks across 2 AZs |
| Postgres down | Everything stateful | RDS events, Sentry | Read-only is not possible; calls in progress continue to the end from the in-memory brief and spool their events | Multi-AZ failover in prod (60 to 120 s, decision 6); PITR for corruption; restore drill in week 5 (RTO 30 min) |
| Deploy or scale-in during a call | The calls on the stopping task | `end_reason = drained` count (should be zero) | Drain mode: the old task takes no new jobs and is stopped only when idle or after 10 min; scale-in protection while `active_jobs > 0`; if a task must stop anyway the client falls to voice notes in the same thread (PRD 5.4.10) | The release window is computed from `learner_schedule` (4.4 #7, ADR-16); the row is reported in the 06:00 UTC digest |
| Inngest Cloud down | No new pipelines, timers or waits; nothing lost | Inngest status, `outbox` growth alert | `api` keeps writing to `outbox`; the Today screen shows yesterday's episode; once Inngest returns a human can re-send `idea.chosen` for a learner from `/admin` | `outbox/relay` drains; running functions resume from the last step |
| LiveKit Cloud down or room connect fails in 3 s | Live calls | Client timer, worker job failures | Voice-note fallback in the same call thread (PRD 5.4.10); talkback becomes text in the fallback; A3 falls to the typed path | Automatic when LiveKit returns; no session lost |
| Primary voice vendor down | Episode and call audio | `vendor/health` (5 failures in 10 min) pages; the pipeline's per-render understudy switch handles single segments | On-call flips `episode_tts` and `call_tts` to the secondary on `/admin/vendors` (one click, no deploy); `voice.vendor_failover` makes the next episode say so in one line (PRD 7.1.3) | Manual switch back after a canary passes, inside the release window |
| Streaming STT vendor down | Live calls | Worker errors | Secondary recognizer (Deepgram) by `vendor_config`, automatic; code-switch talkback quality may drop, logged per call in `calls.vendors` | Same |
| Verbatim recognizer down or queue age over 30 s | The after-session pass, assessment | `call/verbatim-turn` retries exhaust; queue age metric | Secondary verbatim vendor; if both fail within 15 min and voice storage is off, audio is deleted and the call's evidence is marked low confidence with no claims (PRD 5.4.11) | Re-run of the after-session pass is possible only when audio was kept |
| Anthropic API down | Teacher, writer, host, Salma, chat, analyst | Adapter middleware error rate | Host and writer fall back to Gemini Flash; **the editor flips to its Anthropic fallback at the same time** so writer and editor stay on different vendors (pair rule, 4.5), which fails too while Anthropic is down: then there is no editor (never code checks only, ADR-11), the pipeline waits, and the fallback episode ships at the cut line; the teacher falls back to the rule-built brief (PRD 9.8); analyst and memory keeper wait (the 10-minute budget becomes best-effort and is reported) | Automatic per call via `fallback` in `vendors.yaml`; the human-review sample is doubled for the day [ASSUMPTION degraded mode] |
| Editor (Gemini) down | Pipeline gate | Step failures | The editor runs on `claude-opus-5.5` (standard pricing, about $0.05 more on a fallback day, 08), at least as strong as the writer it now shares a vendor with; every episode of the day is flagged `same_vendor_edit` for review and the human-review sample is doubled [ASSUMPTION degraded mode; PRD 6.1.4 has no third text vendor; ADR-11 rejects a Haiku fallback] | Automatic |
| Batch job not done by drop minus 90 min | One episode's cost | Deadline check in step | Standard pricing for remaining steps (PRD 3.2) | Automatic; cost domain reports the share of escalations |
| Episode fails the editor twice | One learner's day | `episode.failed`, `episodes.state = fallback` | Fallback episode (PRD 6.3); on a streaming kind, the player restarts from the fallback's scene 1 with Salma's line, never a splice; 3 fallbacks in 7 days for one learner page a human | Prompt or package fix |
| Episode not ready at drop time at all | One learner's day | `day/next` sends `pipeline.human_page`; 09 pages P2 per learner with dedupe and P1 `drops_late_systemic` at 3 or more learners or 5% in an hour (ADR-16) | No notification; Today keeps the last episode (law 11 says nothing is owed); the episode is published to the feed when it arrives, without a push; the next active day starts a new run | Human runs `episode/produce` from `/admin` with `on_demand` |
| Spend runaway (loop, retry storm) | Money | The daily cap Σ `episodes_per_day × $1.00` and the per-kind caps in the adapter middleware; the per-learner soft guard (2.5 × `episodes_per_day` × budget) and hard guard (4 ×), ADR-15; `vendor_calls` rows written in their own transaction so a retry storm is counted (ADR-13) | Middleware refuses new vendor calls over the cap and pages; live calls are exempt from the cap mid-call; a tripped `sample` or `pilot` cap stops only that kind, so a bot flood never halts production for real learners; automatic spend modes may only change what no learner hears (force batch, cap rewrites, skip canaries, pause on-demand extras under the cap) and never a model (ADR-14) | Human raises the cap or fixes the bug; a model downgrade is a feature flag a person flips after `eval-gate` passes |
| Bot flood on `/v1/sample`, `/v1/waitlist`, `/v1/onboarding/start`, OTP | Money, OTP abuse | WAF rate rule (2,000 requests per 5 min per IP), `ratelimit` refusals, Turnstile failures | Turnstile on the forms; device, contact and IP-prefix windows; `ONBOARDING_STARTS_PER_DAY` global cap; the invite gate on onboarding | Raise or lower the windows from Secrets Manager; no deploy |
| KMS unavailable | New DEK unwraps | Errors | The 60 s DEK cache (ADR-18) covers only calls and reads already in flight; new calls fall to voice notes (whose upload needs no unwrap: `api` encrypts on the next successful unwrap) and show audio keeps playing because `sse_kms_env` objects are served by S3 with the environment key | AWS recovery |
| Learner's DEK destroyed by mistake | That learner's voice recordings are gone (show audio is under the environment key and survives, ADR-12) | Only by audit | Transcripts, the notebook and the learner model survive (text is not under the DEK); Salma states plainly that recordings were lost | Backups cannot restore it by design; the `/admin` destroy action needs two people; `destroy()` bumps `key_version` so no cached copy outlives it (ADR-18) |
| Langfuse unreachable | Debug traces | SDK queue errors | Spans dropped (fire-and-forget); `vendor_calls` and `model_io` are unaffected, so nothing is lost that the home region holds | None needed |
| Podcast app does not accept private feeds (Part 18 #11) | Feed route for that app | Beta observation | The app's own player and web push remain | Document which apps work in A10 instructions |
| Payment processor webhook delay | Trial-to-paid state | Webhook age alert | `past_due` keeps access for the processor's retry window (about 48 h); no episode is withheld for a webhook delay | `billing/reconcile` in `retention/daily` [P1] |

Degraded-mode principle, written into `api`: **a learner never sees an error page for a generation problem.** Every failure in the production path resolves to one of three visible states: today's episode, yesterday's episode still waiting, or Salma's one plain sentence.

---

## 6. Cost and performance against the budgets

The PRD's $0.66 estimate (PRD 14.5) is model and voice cost; it books $0.03 for "proof share and hosting". Infrastructure here is a fixed monthly cost plus small variable costs. Figures are list prices for `eu-central-1` checked 2026-11-06 (within about 5% of `me-central-1`, so the alternative region changes nothing below) and are estimates, not measurements; the cost domain replaces them with measured numbers from the first learner. With three plans (ADR-04) a session is still one episode heard plus its doors; a learner-day on `two_a_day` or `three_a_day` is 1 + extras sessions, and 08 prints the margin by plan from the measured extras (ADR-15).

[DECISION] **What the PRD 16.1 "cost per session" number includes.** It is AI and voice cost plus **variable** infrastructure per session (LiveKit minutes, S3 requests and egress, KMS requests, Inngest steps), all measurable per session from `vendor_calls` and metered rows. **Fixed** infrastructure (the table below) is reported as its own line beside it, at the month's actual learner count and amortized at the planned 250-learner run-rate (5,000 sessions a month). The 19.2 exit criterion "a measured cost per session" is the first number; "a costed path to $0.35 or less" must show both. The cost domain (08) prints it this way already. Rejected: folding fixed infra into the 16.1 number (at 15 learners it would read $3 a session and trip the $1.00 stop line on a research cost the business lens already budgeted); leaving infra out of the exit criterion entirely (the $0.35 target must absorb it at scale).

| Item | Beta prod (15 to 250 learners) | At 10,000 learners | Notes |
|---|---|---|---|
| Vercel Pro | $20/month | $20 to $150/month | Bandwidth is small because audio does not pass through Vercel |
| RDS Postgres | about $250/month (db.t4g.large **Multi-AZ**, 100 GB gp3) | about $900/month (r6g.xlarge Multi-AZ, replica, 500 GB) | Single-AZ would be about $130; the difference is section 10 #4's question |
| ECS Fargate | about $220/month (api 2 × 1 vCPU/2 GB, workflows 1 × 1 vCPU/2 GB, call-worker 1 × 2 vCPU/4 GB, always on; about $0.047 per vCPU-hour and $0.0051 per GB-hour in `eu-central-1`, $0.0496 and $0.0054 in `me-central-1`) | about $2,500/month (autoscaled averages: api 4, workflows 4, call-worker 12 of 2 vCPU/4 GB) | Call-worker hours are the variable part; the first draft's $120 undercounted |
| NAT gateway | about $40/month ($0.045 per hour plus $0.045 per GB of vendor traffic) | about $150/month | Private subnets need it to reach vendors; S3 and Secrets Manager go through VPC endpoints, not the NAT |
| ALB and WAF | about $35/month | about $150/month | WAF rate rule and managed rule set (07) |
| CloudWatch logs and metrics | about $20/month | about $200/month | Three services plus pgaudit (07) |
| Secrets Manager | $12/month (30 secrets) | $15/month | |
| S3 storage and requests | $5/month | about $300/month by the end of year one (6,000 episodes/day × 6 MB × 365 ≈ 13 TB/year, growing) | The archive promise (PRD 4 rule 6) is the one unbounded store; see open item 7 |
| S3 egress (show kinds by presigned URL, learner voice and the feed through `api`) | $3/month | about $250/month (2.5 TB) | ADR-12 moves most of it from Fargate bandwidth to plain S3 egress; CloudFront is the lever when it passes about $100 a month |
| KMS | $2/month | $10/month | One CMK, envelope per learner |
| LiveKit Cloud | $50/month (Ship plan) | about $3,000/month at 6,000 calls/day × 7 min × 2 participants | Variable; counted inside the PRD's $0.16 call line, not in hosting |
| Inngest Cloud | $0 to $75/month | $500 to $1,500/month [ASSUMPTION on tier pricing; verify in week 1 with the concurrency cap] | Self-hosted Inngest if above $0.01 per session |
| Langfuse Cloud EU | $0 to $59/month | about $500/month | Metadata-only spans are small; sampling at scale per 08 §4.3.4 |
| Sentry, Better Stack, Resend, domains | about $60/month | about $400/month | |
| **Prod fixed total** | **about $700 to $850/month** | **about $8,000 to $10,000/month including LiveKit; about $5,500 to $7,000 excluding it** | |
| Staging | about $260 to $300/month running (t4g.medium, three small tasks, NAT, ALB, its Inngest and LiveKit environments); up from build week 2 through the beta (ADR-16); stopping it between test windows would save about $180 a month and is rejected (decision 14) | n/a | The canaries, `eval-gate`, the 50-call reruns and the release smoke test need it at any hour |
| **All environments** | **about $1,000 to $1,300/month** with staging up (prod $700 to $850, staging $260 to $300, plus the shared Sentry, Better Stack and domain lines); the 2026-10-17 figure of $800 to $1,100 assumed staging mostly stopped | | Carried into 10-decision-records §10 item 9 (section 10 #4 here) |
| **Fixed infra per session** | prod only: about $2.30 to $2.80 at 15 learners (300 sessions a month); $0.35 to $0.43 at 100 (2,000 sessions); **$0.14 to $0.17 at 250** (5,000 sessions; the run-rate figure printed beside the 16.1 number). All environments: $3.30 to $4.30 at 15; $0.50 to $0.65 at 100; $0.20 to $0.26 at 250 | **about $0.03 to $0.035 excluding LiveKit minutes** (which sit in the call line); $0.04 to $0.05 including them | At scale the hosting share lands on the PRD's $0.03 hosting line only with the levers below; in the beta the fixed cost is the price of research, as the business lens says ("100 beta learners cost about $2,000 a month") |

Levers for the scale-infra share of the $0.35 target, in order: (1) CloudFront in front of the `sse_kms_env` prefixes (ADR-12 already allows it; about $150 of the $250 egress) and the dedicated `media` service for the feed route (most of `api`'s growth); (2) self-hosted Inngest above $0.01 per session (about $1,000 a month at 10,000 learners); (3) Fargate Savings Plans for the always-on floor (about 20% of the Fargate line); (4) Langfuse sampling per 08. Together they bring the hosting share to about $0.025.

Performance levers this domain provides toward the $0.35 scale target: batch pricing by default with deadline escalation (saves about half of the teacher and writer lines); prompt caching of bibles, briefs and the package's fixed prompt prefixes (the adapter sets `cache_prefix` on every role); segment-level re-synthesis instead of whole-episode retries; one voice vendor for episode and call where the pair allows it, so a cheaper vendor swap applies to both; the per-day spend cap and the $1.00-per-session alert enforce the stop line (PRD 1.4) in code.

Latency: every budget in section 3.6 is met by design in the common path except the streamed on-demand budgets (sample, swap, return and the "next one" episode), which this design delivers at 30 s median and 45 s p95 (section 10 #9); the two that depend on vendors (host reply and the 10-minute after-session pass) are measured in staging by `tools/call-bench` (50 scripted calls, PRD 14.4) in build week 2 on the minimal worker, again in week 4 on the full pipeline, and by the first 20 real calls in week 5. The per-session break-even at full use is 08's and 10-decision-records §10 item 4's: $0.57 / $0.42 / $0.42 for the three plans, against a post-doubling floor of $0.39 to $0.43.

---

## 7. Build plan for 2026-11-18 to 2026-12-22

Team assumption: two engineers (E1 backend, pipeline shells and infrastructure; E2 web and call) plus Muath on prompts, the two packages, the language gate and counsel. The first draft's plan was not feasible as written (eight production adapters, full Terraform and the whole web app on a single week each, and A3 calls served by a worker built a week after onboarding shipped); this plan is a critical path with the cuts named. Every date is ADR-07's: build weeks W1 2026-11-18 to 11-24, W2 11-25 to 12-01, W3 12-02 to 12-08, W4 12-09 to 12-15, W5 12-16 to 12-22; exit 12-22; beta from 12-23; freeze 2026-12-21 12:00 to 12-24 12:00 UTC and 2026-12-31 to 2027-01-02; gate review 2027-01-26. If there is one engineer, the last row applies.

The critical path is the call: A3 and A7 are LiveKit calls (PRD 2.2), the 50 scripted calls are due inside the build's first two weeks (PRD 14.4), and the vendor pair must be chosen before the onboarding screens are wired to it. Two things changed since the 2026-10-17 plan. First, the vendor tests are the language gate (ADR-03) and run during Milestone 0, before build week 1, so `vendors.yaml` is committed on 2026-11-17 and week 1 no longer spends an engineer on throwaway scripts; the adapters for the winners can start on day one. Second, the plans, the on-demand extras, the two packages, the regimes and the round-the-clock operations (ADR-02, 04, 05, 16, 20) add the cross-domain items 10-decision-records §7 places in each week; they are marked (ADR-NN) below. The **minimal `call-worker`** (reference STT, LLM and TTS plugins, the static Salma onboarding persona and a static host brief, no talkback, no governor, no brief fetch) is still stood up in week 2, carries the 50 calls and the A3/A7 onboarding calls in week 3, and grows into the full call pipeline in week 4.

| Week | Dates | E1 ships | E2 ships | Muath | Test with pilot data |
|---|---|---|---|---|---|
| 0 (Milestone 0, in parallel) | 2026-11-01 to 11-17 | Terraform written for `HOME_REGION = eu-central-1` with the region as one variable (ADR-08), not applied; the monorepo skeleton and CI if time allows | `vendor-lab gate --target en` (`forone.langgate`, ADR-03): the 30 pilot clips through Soniox, Deepgram, AssemblyAI and ElevenLabs Scribe with the hand tags (check 2, by 11-10); the two-host script and the Salma script rendered on Gemini TTS, Inworld and ElevenLabs for the blind playlists, rating episode voice and call voice as a pair (check 1, by 11-17); a LiveKit Agents quickstart with the reference plugins for the latency check (check 4); quota and concurrency requests sent (4.5) | Raters recruited (5 native speakers of English, 5 learners of it from anywhere); the M0 consent addendum naming the recognizer and voice vendors accepted before any clip leaves (by 11-01; 10-decision-records §10 item 13); counsel's answers on region, consents and crisis lines by 11-17 (§10 item 1 and 2); Apple Developer Program and Google OAuth verification started (section 10 #6) | `languages/en/gate.yaml` records the pass with the winners; `vendors.yaml` committed by 2026-11-17 |
| 1 | 2026-11-18 to 11-24 | Monorepo, CI, docker compose; `forone.core` settings, DB, migrations, the tables in 4.2 with `learners.{native_language,target_language,residence_country,plan,tz}` (ADR-02), `media_objects.encryption` and the two bucket policies (ADR-12), `episodes.state` with `planned` and `daily_extra` (ADR-05), `learner_schedule.expects_drop` (ADR-19), plus 04's `events` (append-only, `call_turn_verbatim`) and `word_uses` DDL, 06's `push_subscriptions`; the `events` contract; the roles `forone_app`, `forone_workflows`, `forone_purge`, `forone_admin`, `forone_human` (ADR-17); `keys.get_dek` with the 60 s versioned cache (ADR-18); Terraform applied for staging in `HOME_REGION` (VPC with NAT and endpoints, RDS, S3, KMS, ECR, ECS, ALB with WAF, Secrets Manager; about two days, with the console fallback of the one-engineer row); `api` skeleton; Inngest hello function; Sentry; logging and paging skeleton (09); Langfuse wiring under decision 15 with `model_io` and `research_pseudonyms` (ADR-09) | `forone.adapters` interfaces and the tracing middleware with the own-transaction `vendor_calls` write and the worker S3 spool (ADR-13); **adapters for the gate's winners only** (Anthropic standard and batch, Google including embeddings (ADR-10), the winning and runner-up voice vendors, the winning and secondary recognizers, the winning and secondary verbatim vendors); the two package directories with `languages/en`, `native/ar` and `native/en` skeletons and the CI package validation (ADR-02); the LiveKit Agents quickstart from week 0 moved into `apps/call-worker` | Prompts from M0 moved into `languages/en` with versions; Salma's lines into `native/ar`; consent texts and notice per native language drafted with counsel | Every test render is a priced row from the first day of the build |
| 2 | 2026-11-25 to 12-01 | `vendors.yaml` loaded with the editor fallback on Opus flagged `same_vendor_edit` (ADR-11); `episode/produce` shell handed to the pipeline domain with the teacher's multi-episode day plan and the `daily_extra` kind (ADR-05); segment media layout, SSE-C write and Range read for learner voice, presigned URLs for show kinds, `media_objects`, per-call HKDF keys; `day/next` with the 3.4 rule and the `planned` extra rows; `outbox` and relay; `forone.core.messaging` and `ratelimit`; `eval-gate` with the per-package path map (09); staging deploy pipeline; **staging stays up from here through the beta (ADR-16)**; synthetic learners seeded from M0 learner files, one per native package; canary episode | **Minimal `call-worker` on staging** with drain mode and scale-in protection from the start; `tools/call-bench`; **the 50 scripted calls by 2026-12-01 in both worker placements** (`eu-central-1` and `us-east-1`; PRD 14.4 #3; `reply_latency_ms` and `silence_to_sound_ms`); `web` shell: PWA, `dir` and `lang` from the native package, email-code auth and sessions, the event queue, the player against hand-built timings (06 week 2) | Worker placement chosen on the latency results; processor decision prepared for 12-02 (10-decision-records §10 item 3) | The end-to-end pipeline produces episodes for the three synthetic learners on staging by 2026-12-01; M0 scripts set the similarity threshold (Part 18 #10) in the editor step on the Google embeddings |
| 3 | 2026-12-02 to 12-08 | `waitlist`, `invites`, `/admin/invites` on `forone_admin`, the invite gate; onboarding API: `POST /v1/onboarding/start` (talk on the minimal worker, type through `api`), intake facts, `onboarding.intake_completed`, the pilot on-demand path with the scene-1 gate; A9 with the country question and the consent per native language (ADR-20); `plans.yaml`, the allowance by plan, `POST /v1/episodes/next` and `learner.extra_requested` (ADR-04, 05); swap and return paths; feed route, tokens, directory tags, `feed_fetches`; `POST /v1/sample`, `sample_requests`, share route, Turnstile, per-kind caps; `Payments` against the chosen processor's test mode (decision by 12-02; Paddle recommended) with 07's `subscriptions`, the three plans and the founding lock (ADR-21); consents wiring (07 flow A); staff sign-in and admin pages 1 to 3 (learners, episodes, failed runs) | Onboarding screens A1 to A10 (Talk and Type) with the country picker at A9, casting, Today and Notebook routes, the player (06 D3) with the iOS seam test that decides the HLS fallback, the "next one" control after the episode ends (ADR-05), word sheet from the gloss bundle, push subscription and the A10 setup card; A3 and A7 wired to the minimal worker | Waitlist answers collected since M0 loaded into `waitlist`; the day-7 survey answer on "podcast app or WhatsApp" decides how prominent the feed card is in A10; processor and entity decided (12-02) | Staging onboarding end to end on real phones in two native languages; invite redemption; the pilot plays under 45 s after A3; a `two_a_day` learner gets episode 2 under 30 s |
| 4 | 2026-12-09 to 12-15 | `call/verbatim-turn` (append `call_turn_verbatim`, per-turn deletion, `is_last` priority); `audio/expire` on `media.object_created`; `learner/purge-audio`; chat routes and `chat.closed` with the correction guard on the chat path (ADR-06); `/admin/vendors` and `vendor/health`; the crisis record path (`crisis.activated`, with 07) with resources per ISO country and clips per pair (ADR-20); the per-plan cost guard and the daily cap formula (ADR-15); drop-minute load test of the feed route; `call-worker` autoscaling | **The full call pipeline** on the minimal worker's skeleton: chosen STT with `talkback_stt.languages = [native, target]` per learner (ADR-02), host LLM with cached brief fetched per call, call TTS, Salma talkback, hold-to-talk, adaptive patience from the pause profile, the correction guard on every host and Salma line (ADR-06), per-turn audio upload and `call.turn_audio_ready`, the crisis step-out, voice-note fallback end to end; `call-bench` 50-call rerun on the full English stack (10-decision-records §7) | Host and Salma prompts versioned in the packages; the Haiku-host comparison read (§10 item 6) | M0 call transcripts and Muath's hand tags are the fixture set for `call/verbatim-turn` and the analyst's first stage, so the after-session pass can be exercised in week 4 although the full function lands in week 5 |
| 5 | 2026-12-16 to 12-22 | `session/after-pass` as one function wired to the assessment domain's steps (ADR-06); `gap/note`, `proof/fanout`, `retention/daily` and `season/fanout` as hourly learner-local jobs, `measures/hourly` and `privacy/verify` hourly, `drops_late_systemic`, the binding release window in `tools/release` (ADR-16); `learner/export`, `learner/delete` with the processor deletions; `cost/reconcile-spend`; "Margin by plan" fed from `vendor_calls` and `learners.plan` (ADR-15, 08); prod stood up from the same Terraform (Multi-AZ) in `HOME_REGION`; the restore drill; runbooks; on-call rota; measured cost per session with the fixed-infra line beside it | Controls; the then-and-now recording screen and `recording.completed` (the first "then", P0); crisis resources route per country; sample landing page live per `Accept-Language`; the Show tab listing all of the day's episodes if time allows (see slips); the end-to-end run with the Milestone 0 learners on prod | The 15 M0 learners re-onboard through A1 to A10 under the beta consent (§10 item 13); their M0 recordings serve as the "then" baseline where they consented; the exit document with the measured cost and the costed path to $0.35 | Cost per session measured on real sessions for the 2026-12-22 exit criterion; freeze from 2026-12-21 12:00 UTC to 12-24 12:00 UTC |
| P0 items at risk of slipping into the first beta week (2026-12-23 to 12-29) | | The Show tab (archive list; episodes remain reachable from Today's "yesterday" and the feed), admin pages 4 to 8 (SQL under `forone_human` and the Inngest dashboard cover them), Sign in with Apple (depends on Apple's approval, section 10 #6), the IndexedDB offline queue beyond simple retry (events are lost only during an `api` outage), `/admin/invites` as a page (the first batch can be minted by a script), `prewrite_extra` (every extra is made on request until it lands). [OPEN for Muath] section 10 #5: accept these as week-6 items or cut elsewhere | | | |
| P1, during the beta | 2026-12-23 to 2027-01-26 | Round-two call kind; dial-in experiment (a SIP trunk into LiveKit, 8 kHz audio flagged `low_confidence`); `media` service split for the feed route; RDS Proxy; `billing/reconcile`; the offline test suite harness (`FORONE_FAKE_VENDORS` recordings plus a simulated caller); the finale (first finales 2027-01-19); HLS for streaming kinds if the week-3 test demanded it; the voice plan for the 2027-01-01 Gemini doubling in the first release after 2027-01-02 (freeze 12-31 to 01-02) | | | |
| Cuts if there is one engineer | | Drop Sign in with Apple until the beta [OPEN for Muath: it is an untagged P0 account method in PRD 1.4]; serve learner voice and the feed from `api` only (already the beta design; show kinds are presigned either way); no autoscaling (fixed 2 `call-worker` tasks, about 16 concurrent calls, enough for 50 learners spread across timezones); no admin pages beyond staff sign-in and the review queue (SQL as `forone_human` and the Inngest dashboard); Terraform replaced by a documented console setup for staging and prod, Multi-AZ kept; the typed A3 path stays (it is cheaper than the call); the voice-note fallback stays; `prewrite_extra`, the dial-in experiment and the HLS fallback move to later; the Show tab and `proof/fanout` beyond the simple proof move to the beta; `native/en` only for the interface if the Arabic strings are not ready (Arabic-speaking learners still get Salma in Arabic from the package's clips) | | | |

What is too much for this team and is cut or deferred here: a separate admin app (use `sqladmin` pages and the vendors' dashboards); multi-region; self-hosted anything (LiveKit, Inngest, Langfuse); CloudFront for media (a lever above about $100 a month of egress, section 6); an API gateway; a message bus (Inngest events and Postgres are enough); native apps (PRD 19.3 and 10-decision-records §10 item 8 decide when); a third native package before the beta cohort asks for it; a GCP migration unless counsel requires in-country data at rest for one regime (section 10 #1).

---

## 8. Alternatives rejected

| Alternative | Why rejected |
|---|---|
| TypeScript as the one backend language | No ERRANT-style classifier, lemmatizer or MTLD library of the quality the assessment domain needs; LiveKit Agents' Node SDK lacked the Anthropic and Soniox plugins at writing time; the M0 prompts and the hand-tagging tools are already Python-shaped |
| Python everywhere including a server-rendered web app (HTMX) | A PWA with a word-synced player, a WebRTC call screen and RTL text needs a real client framework; Next.js is the smallest boring one |
| Temporal Cloud instead of Inngest | Equivalent model as a choice (PRD 14.3), not as a migration: workers polling task queues, deterministic workflow code, signals instead of `wait_for_event` expressions; more concepts for a two-person team; Inngest's HTTP-invoked steps run inside the FastAPI app with no worker fleet. Self-hosted Inngest is the named exit; Temporal would be a rewrite of the shells (about two weeks) with the step bodies reused |
| Celery, BullMQ, SQS plus cron | No durable `wait_for_event`, `sleep_until` or `cancel`; the daily loop would need hand-written state tables and a scanner, which is where double-sends and drift come from |
| Vercel-only (serverless API plus Inngest steps on Vercel functions) | The call worker must be a long-lived process; TTS and batch-polling steps exceed function limits; audio streaming through Vercel functions is billed bandwidth |
| Kubernetes (EKS) | Operations load; Fargate gives the same containers with no cluster to run |
| Supabase or Neon Postgres | Supabase's auth and storage would pull PII into another processor; neither offers pgaudit or the `me-central-1` alternative counsel may choose; RDS is the boring equivalent in the home region |
| Single-AZ RDS in the beta | Saves about $120 a month; with learners in every timezone a host failure at any hour is somebody's morning of drops, and a restore measured in tens of minutes may fall on a one-engineer rota's night; the failure table in section 5 depends on failover |
| KMS key per learner | $1 per learner per month, which is 15% of the scale-target session budget; envelope DEKs give the same crypto-shred property |
| Handing the learner DEK to `call-worker` | The most exposed service (vendor keys, third-party plugins, autoscaled to 40 tasks) would hold the key that protects every recording the learner ever made; a per-call HKDF key costs one line and reads re-derive it |
| A static `INTERNAL_SERVICE_TOKEN` for `/internal/*` | One leaked secret would unwrap keys from the internet; a per-call JWT plus a VPC-only listener rule cost the same to build |
| App-side AES-GCM for audio | Range requests need chunked encryption code; S3 SSE-C gives Range for free |
| CloudFront in front of media in the beta | Learner voice is SSE-C and can never be cached; show kinds are SSE-KMS and could be (ADR-12), but at 15 to 250 learners presigned S3 URLs cost nothing extra and CloudFront is a $100-a-month lever for later (section 6) |
| Full prompts and completions in Langfuse for every learner | Breaks PRD 1.3 #8 and 12.5.5 (learner text to a processor for "checking and improving the teacher" without the opt-in); metadata spans plus `model_io` in the home region give the same debugging with one join |
| Sending the sample's three answers and the export email inside Inngest events | Content in Inngest Cloud EU contradicts the pointer rule and the residency description given to counsel; `sample_requests` already holds the answers |
| Playing scene 1 while the editor's model checks still run on it | An unconfirmed life fact, an unsourced world fact or a law breach could play; a splice of a fallback from scene 2 breaks law 4; a Haiku-class pass over one scene costs 2 to 4 s, inside the budget |
| Triggering the return episode on a feed fetch | Podcast apps poll hourly whether or not the learner plays; the inactive learner would become the most expensive one (PRD 3.8.3 says "plays the feed", 3.6.2 says no episode after an inactive day) |
| Automatic voice-vendor failover | Five failures in ten minutes at beta scale can be one bad batch; an automatic switch changes how the hosts sound and forces the on-air announcement on a transient; manual one-click switch with a page is the right size |
| Per-segment `<audio>` elements everywhere | Gapless handoff is unreliable on iOS and breaks lock-screen position (06 D3); one element on the stitched file for ready episodes, handoff only while streaming |
| OpenAI embeddings | A fifth text processor receiving every script for one cosine check; Gemini embeddings add nothing to the register |
| Speech-to-speech models for the call | No verbatim transcript, voice list fixed, per-turn control limited (AI-architecture lens table); PRD 14.3 chose the pipeline |
| Pipecat | Its turn model is English-only; LiveKit's multilingual model covers the learner's native language for talkback |
| Clerk or Auth0 | PII in a US processor; per-MAU pricing; email one-time codes are 200 lines with Authlib for the social providers |
| Basic auth plus IP allowlist for `/admin` | No MFA, one shared secret, no individual identity in the audit log, and the on-call's phone IP changes; 07 §4.13's staff OTP sign-in replaces it |
| Firebase or Supabase for push and auth | Same residency argument; web push with VAPID is a library call |
| Pre-producing the whole allowance (2 or 3 episodes) in the nightly batch | Typical use is 50 to 60% of the allowance, so about a third of the voice line would go to episodes nobody asks for; episodes 2 and 3 are made on request through the on-demand path, with `prewrite_extra` only for learners who used 5 or more extras in 7 days (ADR-05). The 2026-10-17 revision's "two episodes per night (likely pick plus runner-up)" is rejected for the same reason |
| A "next episode" feed or autoplay | Law 11 (concept-v2 §5): one, two or three new episodes a day, each with a clear ending, no autoplay and no feed; the "next one" button is a learner action after the ending |
| Keeping Salma's notes behind a flag | A flag never changes a law (09 D8); decisions.md §3 removes the notes, the polish card and the margin note, and the correction guard would need a hole (ADR-06) |
| A Riyadh-centred release window and on-call rota | Learners anywhere means drops at every hour; the window is computed from `learner_schedule` and the rota question goes to Muath (ADR-16; 10-decision-records §10 item 7) |
| A Haiku-class editor when Gemini is down | The editor must be at least as strong as the writer when it shares the writer's vendor; Opus flagged `same_vendor_edit` (ADR-11) |
| SAR prices, a founding year, a yearly plan, Mada first | decisions.md §2: three monthly USD plans, a founding price lock for the first 100 payers, a merchant-of-record processor because tax falls due in many countries (ADR-04, ADR-21) |
| One package per language pair (`package_ar_en`) | n × m packages; the native side needs strings and a voice, the target side needs a gate, and they change at different rates (ADR-02) |
| A global per-minute cron scanning all learners for drops | Drift, double-sends after a crash, no per-learner wait for the pick; one durable run per learner per day is simpler to reason about |
| Deferring RLS to P1 with a repository lint | The roles and policies are one day of work, 04 and 07 already build on them, and `SET LOCAL` removes the pooled-connection leak |
| Microservices per AI role | Eleven roles are eleven Inngest steps or functions in one image; the boundary that matters is live versus durable, not role versus role |

---

## 9. Assumptions about other domains

Each is an [ASSUMPTION] the integrator should check against that domain's document; where the sibling document was read, the names here were aligned to it and the remaining differences are stated.

1. **Episode generation pipeline (02).** `episode/produce` is triggered by `idea.chosen`, `learner.cutoff_reached`, `learner.swap_requested`, `learner.extra_requested` (ADR-05: the `daily_extra` kind, starting at the writer from the nightly plan's brief; `prewrite_extra` for heavy users), `learner.return_detected`, `onboarding.intake_completed`, `sample.requested` and `working_on.changed`, **every trigger carrying `episode_id`** (the row is inserted in state `requested` by `api` or `day/next` before the event; 02's trigger payloads need the field added); it runs the teacher as its first step; it emits `episode.ready` (with `artifact_ids`, a list of media object ids, not a dict), `episode.streaming_started {episode_id, first_segment_media_object_id}` (02 has `first_segment_url`; the id wins and `api` mints the URL, so no S3 URL crosses Inngest), `episode.failed`, `episode.fallback_shipped`, `pipeline.human_page`, `voice.vendor_failover`, `ideas.ready {learner_id, plan_id}` (without the ideas' text), `episode.cost_recorded`; it writes `feed_items` (its table) and `episodes.state` (ADR-19 settled the name; `status` is gone); its teacher step writes one day plan with 1 to 3 episode briefs so the day's language load stays within 2 to 4 words and 1 structure per episode; its prompts load from `packages/languages/<target>/` and its gloss cache key carries `native_lang` (ADR-02); its editor check 10 is widened to "nothing reads as a correction or a lesson" and its fallback editor is Opus flagged `same_vendor_edit` (ADR-06, 11); its similarity check runs on Google embeddings (ADR-10); it runs the model checks 3, 4, 5, 7 and 10 on scene 1 before `episode.streaming_started` on streaming kinds and the law scan on a Haiku-class model for the sample; it never closes a session; it writes show kinds as `sse_kms_env` (ADR-12). It adopts the segment layout (3.7) with its `AudioManifest`. Of the two conflicts the 2026-10-17 revision listed, (a) the backend language is settled as Python, and (b) the CDN assumption is now half met: show audio is served straight from S3 by presigned URL, prefetch and service-worker caching meet the 2 s budget, and CloudFront is a later lever.
2. **Live call and voice stack (03).** The worker uploads each learner turn's audio as it completes under the per-call key and emits `call.turn_audio_ready` with `is_last` on the final turn; the host brief is compiled by the pipeline at episode time and stored at `brief_ref`, with the Salma talkback dict included; the worker emits `call_turn`, `talkback`, `hold_floor`, `silence` and `crisis` through `POST /internal/events` with the per-call JWT; one Fargate task handles about 8 concurrent calls; the S button and hold-to-talk are data-channel messages; captions are delivered over the data channel; `reply_latency_ms` (03 §4.15) is the PRD 15 gate; the worker implements drain mode and scale-in protection (4.4 #7) and deploys at any hour the computed window allows (ADR-16); the latency check of the language gate runs during Milestone 0 on the quickstart, the 50-call test runs in build week 2 on the minimal worker and `call-bench` reruns it in week 4 on the full English stack (ADR-03, ADR-07, 10-decision-records §7); Salma's talkback and persona come from `packages/native/<lang>/` and `talkback_stt.languages = [native, target]` per call (ADR-02); the correction guard runs on every host and Salma line and the host brief's `recasts` field (the teacher's echo plan) is the only correction channel (ADR-06); the Salma onboarding persona runs on the same worker for A3 and A7.
3. **Learner model, event log and data platform (04).** Owns the `events` table (monthly partitions, `inngest_run_id` and `vendor_call_id` columns, `unique (learner_id, client_event_id)`), the nine stores, `consents`, `research_pseudonyms` (ADR-09), `word_uses` (ADR-19; written by 05), compiled briefs, the Postgres roles (`forone_app`, `forone_workflows`, `forone_purge`, `forone_admin`, `forone_human`, `forone_readonly`; ADR-17) and the learner-model version counter; `learners.{native_language,target_language,residence_country,plan,tz}` are the columns 04's learner row carries (ADR-02, 04, 20); the verbatim result is a second event `call_turn_verbatim` appended by `workflows` through `events.append()` (04 D2, ADR-19), accepted here; learner-authored edits applied synchronously by `api` (04 D5) are the one exception to "stores are written in `workflows`", accepted here; export content is assembled by its code inside the `learner/export` shell.
4. **Assessment engine and claim gate (05).** Owns the step bodies of `session/after-pass` (one function with the 10-minute budget; no notes stage and no notes event, ADR-06) and `call/verbatim-turn`; writes `word_uses` and `structure_observations` (ADR-19) and the echo plan for the next host brief; the claim gate writes passed claims to a table that is the only input of `proof/make` (`proofs.sessions_in_week` is computed, not stored, ADR-19); `recordings` holds the three then-and-now parts and the `kept` choice that this document mirrors as `media_objects.kept_explicitly`; the recognizer confidence threshold lives in the language package; the rating model is pinned through `vendors.yaml` `pinned_until: 2027-01-19` (the first 4-week window from 2026-12-23, ADR-07).
5. **Client app, podcast feed and delivery (06).** `web` is logic-free; `dir` and `lang` come from the native package and the landing page is served per `Accept-Language` (ADR-02); the "next one" control and the plan picker on day 7 are its screens (ADR-04, 05); the feed XML and the feed's enclosures are served by `api` with the token and deep-link scheme in 3.5 plus the directory-exclusion tags, while the app's show audio comes from presigned URLs (its §4.4.4 case 2, ADR-12); the notes door and the margin chip are gone (ADR-06); `push_subscriptions`, `feed_fetches`, `accounts`, `otp_codes`, `auth_sessions`, `handoff_tokens` are its tables; `waitlist` and `invites` are defined here (06 lists them as additions; one DDL must win, this one is offered); the share page is `forone.app/s/{share_token}` and the audio route `GET /s/{share_token}.mp3` (06 D16 uses `sampleId`; the unguessable token wins, since the sample id is also the poll handle); `learner.return_detected` is sent on app open or feed-link exchange only (06 D6, accepted here); the player is one element on the stitched file (06 D3, accepted here); web push payloads carry title and length only; the PWA queues events offline for 24 h with client ids; `POST /v1/onboarding/start` carries `{invite_code, tz, native_language, target_language, age_attested, mode}` and A9 asks `residence_country` with a country picker (ADR-20).
6. **Security, privacy, consent and compliance (07).** Accepts envelope DEKs with S3 SSE-C for learner-voice kinds and SSE-KMS under the environment key for produced show kinds served by presigned URLs (ADR-12 amends its D1 and D3), the per-call HKDF key with the 60 s versioned DEK cache and its audit rows (ADR-18), Postgres RLS by `learner_id`, and `forone_admin` for the admin pages with pgaudit only on `forone_human` (ADR-17); its §4.9 is a regime table (EU and UK GDPR, Saudi PDPL, a generic baseline) with crisis resources per ISO country in `packages/native/<lang>/crisis/resources.yaml` (ADR-20); its `guard.check_output` item 6 is the correction guard with `guard/correction_words.yaml` per language (ADR-06); defines the consent-event semantics (`consent_change` with `text_shown_version`) that drive `audio/expire` and `learner/purge-audio`; owns `crisis_log`, `audit_log`, `staff_accounts`, `rate_limits`, `payment_events`, `subscriptions`, `pre_account_sweep`, `privacy/verify` and the processor register (§4.9), which lists every vendor in 3.1 including the human reviewer and excludes OpenAI; approves Inngest Cloud EU (ids and timestamps), Langfuse Cloud EU (metadata under the research pseudonym; anonymized text only for opted-in learners, 30-day retention, ADR-09), LiveKit Cloud, Resend and Sentry as processors or names replacements; its payments design is the merchant-of-record model with the processor open (D12, ADR-21).
7. **Cost model, vendor strategy and tracing (08).** Owns `vendor_calls` (written in its own transaction, idempotent, with the worker spool and `cost/reconcile-spend` hourly, ADR-13), `learner_spend_daily`, `session_costs` (a table filled by `cost/rollup`, with `plan`), `prices.yaml` (with dated rows for the 2027-01-01 Gemini change, beta week 2), the Langfuse conventions (ADR-09: `user_id` is the pseudonym, text only with `data_use`), the per-plan guards and the daily cap formula (ADR-15), the spend modes that change only what no learner hears (ADR-14), the weekly cost report with "Margin by plan", `plan_mix`, `blended_margin` and the fixed-infra line beside the 16.1 number, and the quota requests; the adapter middleware defined here is the single emission point and also writes `model_io`.
8. **Evaluation, observability and operations (09).** Owns Sentry, Better Stack, the ops Slack channel, runbooks, the release window computed from `learner_schedule` and the on-call rota for a worldwide cohort (ADR-16); `measures/hourly` and `privacy/verify` run hourly over learner-local days that closed, the digest at 06:00 UTC and the weekly report Mondays 06:00 UTC; `episode_not_ready_before_drop` reads `learner_schedule.expects_drop` and is P2 per learner, `drops_late_systemic` is P1; `explicit_corrections_per_100_turns` (ceiling 0) counts the correction guard's hits (ADR-06); `cohort_key = invite_date` (ADR-19); the paging hooks here (`ops.page`) call its interface; `tools/release` implements the `call-worker` drain-replace deploy and the binding window check; the offline test suite reuses `FORONE_FAKE_VENDORS` fixtures and `tools/call-bench`; its `recognizers`, `voices-blind` and `calls_50` suites are the language gate's regression form (ADR-03).
9. **Payments (07 D12, ADR-21).** The `Payments` interface in 4.5 (with `refund` and `reconcile`) is unchanged by the merchant-of-record model: the processor issues the invoice and remits tax in every country, the webhook model is the same; three USD plans, cards, Apple Pay and Google Pay worldwide, Mada and other regional methods later; the processor decision on 2026-12-02 (Paddle recommended, about 5%; Stripe with Stripe Tax the fallback, about 3% plus registrations) selects the implementation; `learners.status` and `learners.plan` follow `subscriptions` in the same transaction; a founding price lock (`founding_locked`), not a founding plan.

---

## 10. Open for Muath

The shared register of everything only Muath can settle is 10-decision-records §10 (ADR-22); the items below that overlap with it are one line each and point there. The others are specific to this document and stay in full.

1. **Home region and counsel's view on storing learner voice (counsel, by 2026-11-17).** ADR-08 makes `eu-central-1` the default and keeps `me-central-1` as a one-day config move as late as the Terraform apply in build week 1; `call-worker` may run in a second region for latency and holds nothing at rest. The GCP in-country option is 5 to 8 engineer-days plus a retest and would displace most of week 3's web app, so it is built only if counsel requires in-country data at rest for one regime; see 10-decision-records §10 item 1.
2. **Processors to approve.** This document's part of the register (Inngest Cloud EU, Langfuse Cloud EU under ADR-09, LiveKit Cloud, Resend, Sentry, the human reviewer, the AI, voice and recognition vendors in 3.1; Claude through Bedrock ruled out for the beta) is listed in 07 §4.9; see 10-decision-records §10 item 14.
3. **Payment processor and legal entity (by 2026-12-02).** Merchant of record recommended (Paddle); the adapter is built against the chosen processor's test mode in week 3; see 10-decision-records §10 item 3.
4. **Fixed infrastructure budget: about $1,000 to $1,300 a month** with staging up through the beta (prod alone $700 to $850; Multi-AZ RDS is about $120 of it over single-AZ and this document makes it the baseline, decision 6); see 10-decision-records §10 item 9.
5. **Second engineer, and the week-6 slips (decide by 2026-11-18).** The plan in section 7 assumes two engineers and still names P0 items likely to land in the first beta week (2026-12-23 to 12-29): the Show tab, admin pages 4 to 8, Sign in with Apple, the deeper offline queue, the invites page, `prewrite_extra`. Decide whether there are two engineers, and accept the slips or name what else is cut; 10-decision-records §10 item 10 points here for the list.
6. **Apple Developer Program ($99/year) and Google Cloud OAuth verification** are needed for Sign in with Apple and Google sign-in on the web (PRD 1.4). Both take days to approve; start by 2026-11-10 during Milestone 0 (or by 2026-11-25 at the latest) or ship week 3 with email codes only. If there is one engineer, Sign in with Apple is cut until the beta (an untagged P0 method in PRD 1.4, so this is yours to cut).
7. **Archive growth.** The archive promise keeps every produced episode while the account exists (PRD 4 rule 6, 12.2), which is the one unbounded storage line (about 13 TB per year at 10,000 learners on one episode a day, up to half again with the extras of ADR-05). Confirm that this is intended, or allow produced audio older than one season to be re-synthesized on demand from the stored script.
8. **Invites over WhatsApp.** The waitlist collects WhatsApp numbers (PRD 2.1.5) but the product's channels are email and web push (PRD 3.10). In the beta, WhatsApp invites are sent by hand from the `/admin/invites` list (`sent_via = whatsapp_manual`, about 50 a week on the beta's weekday from 2026-12-23, an hour of Muath's time); the WhatsApp Business API (Meta approval, a provider such as Twilio) is a later decision. Confirm, or make invites email-only.
9. **Streamed on-demand budgets: 30 s median, 45 s p95.** PRD 15 says "under 30 s" for the sample, swap and return with no percentile, and ADR-05 adds the "next one" episode to the same path; this design delivers 30 s median and 45 s p95 on 2026-12-23 (writer, the scene-1 gate, TTS and the Inngest step hops from the EU). Accept the p95, or cut the sample to a 60-second script with sentence-level first TTS (about 22 s median, 32 s p95, a weaker sample).
10. **PRD 3.10 amendment.** Two emails the PRD requires elsewhere are not in its three-kinds table: the 90-day deletion warning (12.5.9) and the invite (2.1.6). They are built as transactional kinds (`retention_warning`, `invite`). Per PRD 18's closing rule this is escalated here rather than built silently; confirm the amendment (the PRD-v3 thread carries it, 10-decision-records §5).
11. **Consents for Milestone 0 data.** The vendor-test addendum before any clip leaves (by 2026-11-01, now part of the language gate) and whether the pilot consent covers re-onboarding the 15 learners in build week 5 and keeping de-identified fixtures; see 10-decision-records §10 item 13.
12. **On-call for a worldwide cohort.** There is no quiet hour (ADR-16); the one-engineer rota answers overnight P1s with the product's fallbacks and a human at the next working hour unless a second responder is funded; Better Stack's on-call plan is about $30 a month; see 10-decision-records §10 item 7.
13. **Domain and sending identity.** `forone.app` is a placeholder in this document; email comes from a show address with Salma signing the body. Confirm the brand domain so DNS, VAPID subject and cookie domain can be set in build week 1 (2026-11-18).

---

## 11. Revision log (2026-11-06)

The two reviews of this document were applied on 2026-10-17; this pass verified every finding is in place and found none missing, so the review bullets below record the verification and the few places where an ADR has since moved the fix.

- conformance blocker "Langfuse receives every learner's text" → verified in place (decision 15, `model_io`, `learner/delete` processor steps); ADR-09 moves `user_id` from `learners.langfuse_pseudonym` to a `research_pseudonyms` row (§3.5, §4.2, §4.3, §9.3).
- conformance major "audio plays before the gate" → verified (§3.6 scene-1 gate, §4.3 `episode/produce`, §8).
- conformance major "waitlist and invites missing" → verified (§2, §4.2); the waitlist row loses `why_english` and `city` for `why_learning`, `country`, `native_language`, `target_language` (ADR-02).
- conformance major "infra per session arithmetic" → verified (§6 decision); the all-environments figure re-done for staging up (ADR-16).
- conformance major "A3 on a worker built in week 4" → verified (minimal worker in build week 2, §7); the vendor tests themselves now run as the language gate during Milestone 0 (ADR-03, ADR-07).
- conformance major "return episode on a feed poll" → verified (§3.4, §3.6, §4.3, §8).
- conformance major "15-minute rule only for call audio" → verified (§3.6, §4.3 `audio/expire`, `media_objects.kept_explicitly`).
- conformance major "sample needs a learner and a DEK" → verified (§4.2 nullable `learner_id`, `share_token`; samples under the environment key, now `sse_kms_env`, ADR-12).
- conformance minor "nine roles" → verified (§2, eleven roles). minor "3.10 guard" → verified (`forone.core.messaging`). minor "event catalogue incomplete" → verified; `notes.ready` is now removed by ADR-06 and `learner.extra_requested` added by ADR-05. minor "PII in Inngest payloads" → verified (CI test in §3.5, §4.3). minor "day/next untreated cases" → verified (§3.4 drop rule). minor "cancel without restart" → verified (§4.3). minor "proof_weekday null, trial_ended guard" → verified. minor "call_tts same vendor, OpenAI embeddings" → verified (ADR-10 confirms Google). minor "editor fallback collision" → verified; the fallback model changes from Haiku to Opus flagged `same_vendor_edit` (ADR-11, §4.5, §5). minor "task count, Apple cut, Multi-AZ" → verified (§7, decision 6). minor "proof closes the session" → verified (§3.4 step 7). minor "verbatim concurrency" → verified (§4.10). minor "RLS bypass role, directory tags" → verified; the roles gain `forone_admin` and `forone_human` (ADR-17). minor "missing email kinds" → verified (§4.5, §10 #10). minor "M0 consent for vendor tests" → verified (§10 #11, now pointing to the register).
- skeptic blocker "five-week plan infeasible" → verified (two-engineer plan, §7); §7 re-dated and extended with the cross-domain items (ADR-07).
- skeptic blocker "schedule math without lead time" → verified (§3.4 drop rule, `clamp_timeout`, `episodes` unique key; the key now includes `slot`, ADR-05).
- skeptic major "deploy kills calls" → verified (drain and scale-in protection, §4.4 #7); the Riyadh deploy windows the review proposed are replaced by the computed release window (ADR-16 wins; §4.4 #7 (c), §4.8, §5).
- skeptic major "latency arithmetic" → verified (§3.6 measurement point); the vendor RTT term is re-done from `eu-central-1` (ADR-08).
- skeptic major "sample budget overstated" → verified (§3.6, §6, §10 #9).
- skeptic major "PII in events", "feed fetch trigger", "events append-only", "per-call key", "player contract", "Multi-AZ consistency", "cost table omissions", "session close by the pipeline", "pre_account lifecycle", "abuse on the sample endpoint" → all verified in place (§3.2, §3.4, §3.5, §3.6, §3.7, §4.2, §4.3, §4.7, §5, §6, §8).
- skeptic major "region ruling after week 1" → superseded: ADR-08 makes `eu-central-1` the default, the GCP note stays in §10 #1 and the register holds the open question.
- skeptic minor "workflows autoscaling signal", "automatic voice failover", "OpenAI embeddings", "missing schema and events", "events contract", "RLS leak", "Temporal portability", "admin basic auth" → verified. minor "api as the only media origin forever" → superseded by ADR-12: show kinds are SSE-KMS and presigned from day one (§1 decision 7, §3.5, §3.6, §4.2, §4.10, §6, §8).
- ADR-01 → front matter re-dated and sourced; "What changed" paragraph describes this revision.
- ADR-02 → `learners.{native_language,target_language,residence_country,tz}` with no `Asia/Riyadh` default (§4.2); `packages/languages/<target>/` and `packages/native/<lang>/` replace `package_ar_en` (§4.1, §4.8, §4.9); landing page per `Accept-Language`, `dir` and `lang` from the native package (§1 decision 2, §4.6); recognizer languages `[native, target]`, Salma's clips and voice per native package, spaCy model per target (§3.6, §4.1, §4.4, §4.5); the one-country load-shape paragraph rewritten (§4.10); waitlist fields (§4.2); §8 row.
- ADR-03 → `vendor-lab` is `forone.langgate`; target-dependent `vendors.yaml` roles keyed by language; the gate runs during Milestone 0 and `vendors.yaml` is committed by 2026-11-17 (§2, §4.1, §4.5, §7 week 0).
- ADR-04 → `plans.yaml`, `learners.plan`, the allowance in `api`, `subscriptions.plan` values and `founding_locked`, `Payments.create_checkout` plan literal (§1 decision 16, §2, §3.3, §4.2, §4.5).
- ADR-05 → `daily_extra` kind, `slot`, `planned` and `superseded` states, `day/next` inserts the planned rows, `POST /v1/episodes/next`, `learner.extra_requested`, the "next one" control, `prewrite_extra`, episode counts in §4.10 (§1, §2, §3.4 steps 2, 6 and 8, §3.6, §4.2, §4.3, §4.6, §8).
- ADR-06 → the "Salma's notes under 90 s" row removed from §3.6; the after-pass is one function (§3.4, §3.6, §4.3, §9.4); `notes.ready` and `NotesReady` removed from the catalogue; `note_shown` removed from §3.2; the notes door removed from `doors` (§4.2); the correction guard named in `forone.core.guard` and in the week-4 call and chat paths (§4.1, §7); editor check 10 widened (§4.3); the 90 s budget references in §4.10, §5 and §6 rewritten.
- ADR-07 → every date moved 16 days: §1, §2, §3.6, §4.2, §4.5 (`pinned_until: 2027-02-16`, 05's cohort-aligned first window), §4.10 column headers, §7 heading and rows, §9, §10; freezes stated in §7.
- ADR-08 → `HOME_REGION` default `eu-central-1`, `me-central-1` the alternative, `CALL_WORKER_REGION` default `eu-central-1` candidate `us-east-1`, Vercel `fra1` (§1 decision 8, §3.2, §3.6, §4.6, §4.7, §6 prices, §10 #1); the final choice stays open.
- ADR-09 → `research_pseudonyms` replaces `learners.langfuse_pseudonym`; `anonymize()`; Langfuse deletion does not hold up the "deleted" email (§1 decision 15, §3.5, §4.2, §4.3, §9.3, §9.6).
- ADR-10, ADR-11 → Google embeddings confirmed; the editor fallback is `claude-opus-5.5` flagged `same_vendor_edit` (§4.5, §5, §8).
- ADR-12 → `media_objects.encryption in ('sse_c_learner','sse_kms_env')`; show kinds under `MEDIA_ENV_KMS_KEY_ID`, served by 10-minute presigned URLs from `GET /v1/episodes/{id}/media`; the feed enclosure stays proxied; `learner/delete` deletes show kinds by prefix (§1 decision 7, §2, §3.2, §3.3, §3.5, §3.6, §4.2, §4.3, §4.7, §4.10, §6, §8, §9.1, §9.5, §9.6).
- ADR-13 → `vendor_calls` written in its own transaction, idempotency keys, `learner_spend_daily` upsert, the worker S3 spool, `cost/reconcile-spend` hourly (§4.3, §4.5, §5).
- ADR-14, ADR-15 → spend modes change only what no learner hears; the daily cap Σ `episodes_per_day × $1.00`, soft and hard per-learner guards by plan; `SPEND_CAP_FLOOR_USD_PER_DAY` and `SESSION_BUDGET_USD` replace the fixed cap keys (§4.7, §5, §6).
- ADR-16 → no Riyadh windows anywhere: the release window computed from `learner_schedule` (§1 decision 17, §4.4 #7, §4.8, §5); `retention/daily`, `season/fanout` and `proof/fanout` hourly over learner-local days (§3.4, §4.3); `drops_late_systemic` (§5); staging up from build week 2 (§1 decision 14, §4.7, §6, §7); the fixed-infra figure becomes $1,000 to $1,300 a month (§6, §10 #4); on-call points to the register (§10 #12).
- ADR-17 → `forone_admin` for the admin pages, `forone_human` for psql under pgaudit (§3.3, §4.2, §7, §9.3, §9.6).
- ADR-18 → `keys.get_dek` 60 s cache keyed by `(learner_id, key_version)`, `learner_keys.key_version`, `destroy()` bumps it, audit rows per cache window, the 10-minute cache and the zeroization claim dropped (§4.1, §4.2, §4.3, §5).
- ADR-19 → `episodes.state` confirmed and the `status` conflict closed (§9.1); `learner_schedule.expects_drop` added (§4.2, §4.3, §9.8); `word_uses` and `structure_observations` named as 04's tables written by the pass (§4.2, §4.3); `cohort_key = invite_date` (§2, §4.2); `proofs.sessions_in_week` computed (§9.4); `tools/call-bench` was already the name.
- ADR-20 → `learners.residence_country` asked at A9; regimes instead of PDPL-only; crisis resources per ISO country in the native package (§2, §3.6, §4.1, §4.2, §7, §9.6).
- ADR-21 → merchant-of-record model, Paddle recommended, Stripe with Stripe Tax the fallback, processor open until 2026-12-02; `PAYMENTS_PROVIDER` values; Mada later (§3.1, §3.3, §4.5, §4.7, §8, §9.9, §10 #3).
- ADR-22 → §10 items 1, 2, 3, 4, 11 and 12 reduced to one line each pointing at 10-decision-records §10 items 1, 14, 3, 9, 13 and 7; items 5 to 10 and 13 stay in full. No §10 item was removed outright: ADR-21 settled the payment model but the processor stays open, and ADR-08 settled the default region but the final choice stays open.
- Not applied, deliberately: the skeptic's proposed Riyadh-time deploy windows (ADR-16 forbids any timezone-fixed window; the computed window replaces them) and the conformance review's suggestion to keep a Haiku-class editor as the Gemini fallback (ADR-11 requires an editor at least as strong as the writer when the vendor is shared). Everything else in both reviews is in place.
