# 07. Vendor accounts and cost controls

Part of the For one engineering handbook. Written 2026-11-06 against architecture 08 (D4, D5, D10, D11, §4.5, §4.8, §4.9, §10), 01 §4.7 and 07 §4.9. Nothing on this page is a secret; the keys themselves live only in AWS Secrets Manager (handbook 03 §4).

## 1. Accounts Muath must open himself

These accounts carry a contract, a card, or the legal identity of the company. An engineer cannot open them, and each should be opened under a company email (`ops@<domain>` or a Google Workspace group), with two-factor on, and the engineer added as a member rather than given the owner's password. The "by" dates are the first day the account is needed in the build plan.

| # | Account | Why | Plan to pick | By | Monthly cost to expect |
|---|---|---|---|---|---|
| 1 | **AWS** (new account under an AWS Organization, home region per counsel) | RDS, S3, KMS, Fargate, Secrets Manager, CloudWatch, WAF | pay as you go; enable Cost Explorer and a budget alert at $1,200 | before build week 1 | $700 to $1,100 |
| 2 | **GitHub** organization (move `for-one` into it, or keep under `Muath-8` with the engineers as collaborators) | the repository, Actions, environments with approval, branch protection | Team plan (needed for required reviewers on private repos; the repo is public today) | week 1 | $4 per seat |
| 3 | **Vercel** | `web` hosting, previews, `dxb1` edge | Pro | week 1 | $20 per seat |
| 4 | **Anthropic Console** (organization, with a workspace per environment: `dev`, `staging`, `prod`) | teacher, writer, fitter, host, Salma, analyst, memory keeper, proof, rater | API with prepaid balance; request the usage tier for 1M tokens a minute on Sonnet and 200K on Opus; Batch API enabled; zero-data-retention request (open for Muath, architecture 07 §4.9) | week 1 | about $1,500 prepaid for December at 100 learners |
| 5 | **Google Cloud** project with the Gemini API (paid tier) | editor; TTS candidate; also hosts the OAuth consent screen for Google sign-in | paid tier with billing on the project (the Milestone 0 lesson); request a TTS requests-per-minute raise if Gemini wins | week 1 | tens of dollars; more if Gemini voices win |
| 6 | **ElevenLabs** | voice finalist; alignment | pay as you go until the blind test; a paid tier only if it wins at a negotiated rate at or below $25 per million characters (architecture 08 D5) | week 1 | $0 to $330 |
| 7 | **Inworld** | voice finalist | pay as you go; paid tier if it wins | week 1 | $0 to $100 |
| 8 | **Soniox** | streaming recognizer finalist, talkback | pay as you go; ask for 50 concurrent streams | week 1 | usage |
| 9 | **Deepgram** | streaming recognizer finalist and hot secondary | pay as you go; ask for 50 concurrent streams | week 1 | usage |
| 10 | **AssemblyAI** | verbatim recognizer finalist | pay as you go; 50 concurrent batch jobs | week 1 | usage |
| 11 | **Speechace** | pronunciation scoring | developer plan | week 2 | plan price |
| 12 | **OpenAI** | embeddings only (script similarity; never learner text) | pay as you go, $20 hard limit | week 2 | under $5 |
| 13 | **LiveKit Cloud** | the call media layer; projects `forone-staging` and `forone-prod`; Egress disabled | Ship | week 2 | $50 plus minutes |
| 14 | **Inngest Cloud** (EU) | durable workflows; envs `staging` and `prod` | free, then Pro when steps exceed the free tier | week 1 | $0 to $75 |
| 15 | **Langfuse Cloud** (EU region project) | model traces; 30-day retention; data-use opt-in rule | Core | week 1 | up to $59 |
| 16 | **Sentry** (EU data residency) | errors | Team | week 1 | about $26 |
| 17 | **Better Stack** | uptime, heartbeats, on-call paging with phone calls | the on-call plan (open for Muath) | week 4 | about $30 |
| 18 | **Resend** | the three message kinds; sending domain verified; open and click tracking **off** | Pro once over the free tier | week 3 | $0 to $20 |
| 19 | **Cloudflare** | DNS for the brand domain; Turnstile on the sample and waitlist forms; proxy off for `api.` | free | week 1 | $0 |
| 20 | **Domain registrar** | the brand domain (still open, architecture 01 §10 #13) | | week 1 | yearly |
| 21 | **Apple Developer Program** | Sign in with Apple on the web | $99 a year; takes days to approve; start by 2026-11-09 or ship week 3 with email codes only | 2026-11-09 | $99 a year |
| 22 | **Google OAuth verification** (on the Google Cloud project above) | Google sign-in on the web | brand verification takes days | 2026-11-09 | $0 |
| 23 | **Payment processor** (Stripe if the entity allows; else Tap, Moyasar or HyperPay for Mada) | subscriptions, hosted checkout, VAT invoices | decision due 2026-11-16 (PRD 18 #2); Stripe test mode is the week-3 scaffold | 2026-11-16 | fees |
| 24 | **Slack** workspace with `#forone-ops` and `#forone-deploys` | alerts, deploys, on-call, the staging lock | free | week 1 | $0 |
| 25 | **Microsoft Azure** Speech resource (EU or home region) | secondary pronunciation scorer; optional until Speechace fails a test | pay as you go | later | $0 |

Not to open: **Hume** (voice APIs shut 2026-11-13; CI rejects any `hume` dependency). Not carried from Milestone 0 as processors: Google Drive, Google Forms, WhatsApp, ElevenLabs Agents, claude.ai Projects.

Each account is a row in the processor register `docs/ropa.md` (architecture 07 §4.9) with its DPA status, and CI refuses to let code call a vendor whose row is not `dpa: signed` or `dpa: clickwrap-accepted`. Opening the account is Muath's job; filling the register row and the retention switch (section 3) is the engineer's, the same day.

## 2. Keys

- **One key per environment per vendor**, named `forone-prod`, `forone-staging`, created in the vendor console by Muath or the infra engineer, pasted once into AWS Secrets Manager, and never seen again. Vendors that support workspaces or projects get one per environment so usage and spend separate cleanly in their billing.
- **One key per engineer per vendor for laptop work**, named `dev-<name>`, created under the same org with the vendor's own spend limit where the vendor offers one (Anthropic workspace limits, OpenAI hard limit, Google budget alert), and otherwise bounded by the middleware's `SPEND_CAP_USD_PER_DAY=20` when `FORONE_ENV=dev`.
- **CI eval keys** (`forone-ci-eval`) are a third set with their own cap, read by the eval-gate from the secret `forone/ci/eval`, and never the prod keys.
- Rotation quarterly and on suspicion; `gitleaks` on every PR; a leaked key is rotated the same day whether or not it reached `main`.
- Nobody pastes a key into Slack, a PR, a ticket, a Notion page or a chat with an AI assistant. A key pasted anywhere is a leaked key.

## 3. Vendor-side settings that must be set by hand

Listed in `infra/MANUAL.md` with value, who, when; the privacy verify job checks the ones with an API.

| Vendor | Setting | Value |
|---|---|---|
| Anthropic | data retention | zero-data-retention requested; training off is the API default |
| Google Gemini | paid tier | on (paid-tier prompts not used to improve products) |
| ElevenLabs, Inworld | content retention / history | off; voice ids owned by us; no cloning from learner audio |
| Soniox, Deepgram | audio retention | off, confirmed in writing |
| AssemblyAI | retention after transcription | minimum; this vendor sees the most learner voice, negotiate hardest |
| LiveKit | Egress | disabled at project level |
| Inngest | run history | 30 days |
| Langfuse | retention | 30 days; deletion API wired into `learner/delete` |
| Resend | open and click tracking | off; log retention minimum |
| Sentry | data residency; server-side scrubbing | EU; scrub `text`, `quote`, `transcript` |
| Vercel | log retention | minimum |
| AWS | CloudTrail, Config, GuardDuty | on; budget alert; MFA on every console user; no access keys |

## 4. Spend caps and the guard

The middleware in `forone.adapters` prices every call from `price_book` and enforces, per environment:

| Control | dev | staging | prod |
|---|---|---|---|
| `SPEND_CAP_USD_PER_DAY` | 20 per engineer key | 50 | `max(50, learners × 1.50)` from launch, recomputed daily |
| `SPEND_CAP_SAMPLE_USD_PER_DAY` | 5 | 20 | 20 |
| `SPEND_CAP_PILOT_USD_PER_DAY` | 5 | 60 | 60 |
| `SESSION_COST_ALERT_USD` | 1.00 | 1.00 | 1.00 |
| Per-learner cost guard (architecture 07 D11) | off | soft $2.50, hard $5.00 | soft $2.50, hard $5.00 (pauses on-demand generation, never playback) |
| Kind ceilings | sample $0.05, pilot $0.40, swap $0.60 | same | same |

**Spend modes** (architecture 08 §4.5.2): `normal`, `conserve` at 80% of the daily cap (teacher to Sonnet batch, rewrites capped, batch TTS forced, canaries skipped, host to Haiku), `halt` at 100% (queued episodes finish, no new on-demand generation except return episodes, calls never cut, claims and notes never degraded). `halt` is for a runaway, not for budgeting; if it fires on a normal day the cap is wrong and is raised.

**The stop line** ($1.00 trailing 7-day mean, or 20% of sessions over it) pages Muath and the on-call, opens a 48-hour window for a costed plan recorded in `cost_reports`, and repeats daily until a plan exists. It never stops service; stopping the beta is Muath's decision (architecture 08 §4.5.3, open item #7 in 09).

**Vendor-side caps** are set too, as the backstop for a middleware bug: Anthropic workspace spend limits per environment, OpenAI hard limit, Google budget alerts at $50 and $200, AWS budget at $1,200, ElevenLabs and Inworld tier ceilings. The middleware's cap is lower than every vendor cap so ours fires first.

## 5. Fallbacks

`vendors.yaml` (architecture 08 §4.7) names, per role, the primary, the ordered fallback chain, the degrade path and the pricing escalation. Two rules the middleware enforces regardless of the file: a `pinned_until` role (the rater) refuses any fallback or override while pinned; the writer and editor may not resolve to the same vendor without a `note`, and then the episode is tagged for human review.

Same-day failover without a deploy: `vendor_config` rows override the file, flipped on `/admin/vendors` by `owner` or `engineer`, audited. The on-call flips to the understudy during an outage; flipping **back** happens only after a passing canary, in the release window, with the on-air announcement (PRD 7.1).

Two voice vendors are wired from day one; a paid tier is bought only for the blind-test winner, and the runner-up stays on pay-as-you-go with a weekly canary that keeps the account live (architecture 08 D10).

## 6. The vendor risk calendar, as engineering tasks

| Date | Event | Task | Owner |
|---|---|---|---|
| 2026-11-08 | recognizer test deadline | `vendor-lab stt` run complete; Muath's truth file by 2026-11-04 | engineer, Muath |
| 2026-11-13 | Hume shuts down; voice decision due | CI check in place; `vendors.yaml` committed with winners; paid tier for the winner | engineer, Muath |
| 2026-11-16 | payment processor decision | fee row in `prices.yaml`; adapter swap if not Stripe (three days) | Muath, engineer |
| 2026-11-20 | ElevenLabs negotiated-rate deadline if it won | contract or the runner-up becomes primary | Muath |
| 2026-12-07 | beta starts | daily cap recomputed from learner count; reconciliation job live | engineer |
| 2026-12-28 | weekly report prints next week's prices | first sight of the January jump | automatic |
| 2026-12-31 | rater pin window ends | re-pin for the next four weeks; calibration re-run | engineer |
| 2027-01-01 | Gemini prices double | second dated rows already in `prices.yaml`; vendor swap or negotiated rate per Muath's December decision | Muath |
| 2027-01-10 | beta gate review | cost gate evidence is the report of 2027-01-11 | Muath |
| every 120 days | price staleness | `price_stale` alarm; re-check every row against the vendor's price page | on-call |

## 7. Monthly reconciliation

`cost/reconcile` compares `vendor_calls` sums for the month with each vendor's invoice: Anthropic through its usage and cost admin API, the rest by CSV upload on `/admin/costs`. A variance over 5% for any vendor raises an alarm and is the first item at the next Tuesday ops review. The usual causes: a `prices.yaml` row that is wrong, a vendor billing a unit we do not count (connection minutes, concurrency reservations), or a key used outside the middleware. All three are bugs.
