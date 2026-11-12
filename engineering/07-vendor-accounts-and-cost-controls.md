# 07. Vendor accounts and cost controls

Part of the For one engineering handbook. Written 2026-11-06 against architecture 08 (D4, D5, D10, D11, §4.5, §4.8, §4.9, §10), 01 §4.7 and 07 §4.9. Revised 2026-11-12 for ADR-24 (every processor approved, Paddle as merchant of record) and ADR-25 (no dates; web only, so no Apple or Google developer accounts; the agent builds under Muath). Nothing on this page is a secret; the keys themselves live only in AWS Secrets Manager (handbook 03 §4).

## 1. Accounts Muath opens

These accounts carry a contract, a card, or the legal identity of the company, so only Muath opens them (register A1, A5, A6). Each is opened under a company email (`ops@<domain>` once the domain exists), with two-factor on. The coding agent never holds an account login; it gets scoped API keys through Secrets Manager (section 2). "Needed before" is the first point in the release plan's dependency order where the account is used; each vendor's standard DPA is accepted when the account is opened.

| # | Account | Why | Plan to pick | Needed before | Monthly cost to expect |
|---|---|---|---|---|---|
| 1 | **AWS** (new account under an AWS Organization, home region `eu-central-1`) | RDS, S3, KMS, Fargate, Secrets Manager, CloudWatch, WAF | pay as you go; enable Cost Explorer and a budget alert at $1,200 | phase 1 (Terraform for staging) | $700 to $1,100 |
| 2 | **GitHub** (the repository, under `Muath-8` or an organization) | the repository, Actions, environments with approval, branch protection | Team plan if the repository is private (required reviewers on private repos) | phase 1 | $4 per seat |
| 3 | **Vercel** | `web` hosting, previews, `fra1` edge | Pro | phase 1 | $20 per seat |
| 4 | **Anthropic Console** (organization, with a workspace per environment: `dev`, `staging`, `prod`) | teacher, writer, fitter, host, Salma, analyst, memory keeper, proof, rater | API with prepaid balance; request the usage tier for 1M tokens a minute on Sonnet and 200K on Opus; Batch API enabled; request zero data retention (ADR-24.17) | phase 1 | $2,500 prepaid for the first month after launch (ADR-24.13) |
| 5 | **Google Cloud** project with the Gemini API (paid tier) | editor; embeddings for script similarity (ADR-10); TTS candidate | paid tier with billing on the project; request a TTS requests-per-minute raise if Gemini wins | phase 1 | tens of dollars; more if Gemini voices win |
| 6 | **ElevenLabs** | voice finalist; alignment | pay as you go until the blind test; a paid tier only if it wins, at a negotiated rate (target $12 to $15 per million characters, ADR-24.6, register A9) | phase 1 (vendor tests) | $0 to $330 |
| 7 | **Inworld** | voice finalist | pay as you go; paid tier if it wins | phase 1 (vendor tests) | $0 to $100 |
| 8 | **Soniox** | streaming recognizer finalist; the word button's own-language recognizer | pay as you go; ask for 50 concurrent streams | phase 1 (vendor tests) | usage |
| 9 | **Deepgram** | streaming recognizer finalist and hot secondary | pay as you go; ask for 50 concurrent streams | phase 1 (vendor tests) | usage |
| 10 | **AssemblyAI** | verbatim recognizer finalist | pay as you go; 50 concurrent batch jobs | phase 1 (vendor tests) | usage |
| 11 | **Speechace** | pronunciation scoring | developer plan | phase 4 (the full call) | plan price |
| 12 | **LiveKit Cloud** | the call media layer; projects `forone-staging` and `forone-prod`; Egress disabled | Ship | phase 2 | $50 plus minutes |
| 13 | **Inngest Cloud** (EU) | durable workflows; envs `staging` and `prod` | free, then Pro when steps exceed the free tier | phase 1 | $0 to $75 |
| 14 | **Langfuse Cloud** (EU region project) | model traces; 30-day retention; data-use opt-in rule | Core | phase 1 | up to $59 |
| 15 | **Sentry** (EU data residency) | errors | Team | phase 1 | about $26 |
| 16 | **Better Stack** | uptime, heartbeats, phone escalation to Muath (ADR-24.12) | the plan with phone calls | production (phase 6) | about $30 |
| 17 | **Resend** | the three message kinds and the transactional emails, including the sign-in code; sending domain verified; open and click tracking **off** | Pro once over the free tier | the domain exists (A6) | $0 to $20 |
| 18 | **Cloudflare** | DNS for the domain; Turnstile on the sample form; proxy off for `api.` | free | the domain exists (A6) | $0 |
| 19 | **Domain registrar** | the domain (`APP_DOMAIN`, ADR-25.8) | | email sending and the first public deploy | yearly |
| 20 | **Paddle**, merchant of record (ADR-24.4); Stripe with Stripe Tax only if Paddle declines the account | subscriptions, hosted checkout (cards, Apple Pay, Google Pay, PayPal), tax, invoices, refunds and the EU withdrawal right | the sandbox for building; the live account under the company (A5) before checkout is built against the live API | phase 5 (plans and checkout) | fees |
| 21 | **Slack** workspace with `#forone-ops` and `#forone-deploys` | alerts, deploys, release proposals, the staging lock | free | phase 1 | $0 |
| 22 | **Microsoft Azure** Speech resource (EU or home region) | secondary pronunciation scorer; optional until Speechace fails a test | pay as you go | only if needed | $0 |

Not to open: **Hume** (voice APIs shut 2026-11-13; CI rejects any `hume` dependency); **OpenAI** (embeddings use Google's model, ADR-10); **Apple Developer Program** and **Google OAuth** (email one-time code is the only sign-in, ADR-25.4; Apple Pay and Google Pay come through Paddle's hosted checkout with no developer account).

Each account is a row in the processor register `legal/05-ropa.md` (architecture 07 §4.9) with its DPA status, and CI refuses to let code call a vendor whose row is not `dpa: signed` or `dpa: clickwrap-accepted`. Opening the account is Muath's job; the agent fills the register row and documents the retention switch (section 3) in the same PR that adds the adapter.

## 2. Keys

- **One key per environment per vendor**, named `forone-prod`, `forone-staging`, created in the vendor console by Muath, pasted once into AWS Secrets Manager, and never seen again. Vendors that support workspaces or projects get one per environment so usage and spend separate cleanly in their billing.
- **One development key per vendor for the agent**, named `dev-agent`, created by Muath under the same org with the vendor's own spend limit where the vendor offers one (Anthropic workspace limits, Google budget alert), and otherwise bounded by the middleware's `SPEND_CAP_USD_PER_DAY=20` when `FORONE_ENV=dev`. It is used only for vendor stories; everything else runs on the fakes.
- **CI eval keys** (`forone-ci-eval`) are a third set with their own cap, read by the eval-gate from the secret `forone/ci/eval`, and never the prod keys.
- The agent never sees a staging or prod key; the services read them from Secrets Manager through their task roles.
- Rotation quarterly and on suspicion; `gitleaks` on every PR; a leaked key is rotated by Muath the same day whether or not it reached `main`.
- No key is ever pasted into Slack, a PR, an issue, a prompt, a log or a chat with any assistant, including the coding agent's own session. A key pasted anywhere is a leaked key.

## 3. Vendor-side settings that must be set by hand

Listed in `infra/MANUAL.md` with value, who, when; the privacy verify job checks the ones with an API.

| Vendor | Setting | Value |
|---|---|---|
| Anthropic | data retention | zero-data-retention requested; training off is the API default |
| Google Gemini | paid tier | on (paid-tier prompts not used to improve products) |
| ElevenLabs, Inworld | content retention / history | off; voice ids owned by us; no cloning from learner audio |
| Soniox, Deepgram | audio retention | off, confirmed in writing |
| AssemblyAI | retention after transcription | minimum; this vendor sees the most learner voice |
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
| `SPEND_CAP_USD_PER_DAY` | 20 for the agent's key | 50 | `max(50, Σ plan.episodes_per_day × 1.00)` over learners in a trial or subscription, recomputed daily from launch (architecture 08 §4.5.1, ADR-15) |
| `SPEND_CAP_SAMPLE_USD_PER_DAY` | 5 | 20 | 20 |
| `SPEND_CAP_FIRST_USD_PER_DAY` (the onboarding's first episode) | 5 | 60 | 60 |
| `SESSION_COST_ALERT_USD` | 1.00 | 1.00 | 1.00 |
| Per-learner cost guard (architecture 07 D11) | off | soft $2.50, hard $5.00 | soft $2.50, hard $5.00 (pauses on-demand generation, never playback) |
| Kind ceilings | sample $0.05, first episode $0.40, swap $0.60 | same | same |

**Spend modes** (architecture 08 §4.5.2): `normal`; `conserve` at 80% of the daily cap (batch TTS forced, rewrites capped at one round, canaries and the nightly smoke skipped, the anonymizer deferred, pre-writes skipped); `halt` at 100% (queued drop episodes finish, no new on-demand generation except return episodes, extras and swaps paused for the rest of the UTC day, calls never cut, claims never degraded). An automatic mode changes only what no learner hears (ADR-14): it never swaps a model. The Haiku host and the Sonnet teacher are feature flags Muath flips after `eval-gate` passes. `halt` is for a runaway, not for budgeting; if it fires on a normal day the cap is wrong and is raised.

**The stop line** ($1.00 trailing 7-day mean, or 20% of sessions over it) notifies Muath, opens a 48-hour window for a costed plan recorded in `cost_reports`, and repeats daily until a plan exists. The agent drafts the plan from section 6.3 of architecture 08 when asked; Muath records it. It never stops service; stopping the product is Muath's decision (architecture 08 §4.5.3). The daily cap formula and the 48-hour window are policy as written here (ADR-24.23).

**Vendor-side caps** are set too, as the backstop for a middleware bug: Anthropic workspace spend limits per environment, Google budget alerts at $50 and $200, AWS budget at $1,200, ElevenLabs and Inworld tier ceilings. The middleware's cap is lower than every vendor cap so ours fires first.

## 5. Fallbacks

`vendors.yaml` (architecture 08 §4.7) names, per role, the primary, the ordered fallback chain, the degrade path and the pricing escalation. Two rules the middleware enforces regardless of the file: a `pinned_until` role (the rater) refuses any fallback or override while pinned; the writer and editor may not resolve to the same vendor without a `note`, and then the episode is tagged for the AI review pass.

Same-day failover without a deploy: `vendor_config` rows override the file, flipped on `/admin/vendors` by Muath, or by the agent through `ops.yml` with Muath's approval, audited. The automatic health check flips recognizers and the editor to their understudies during an outage; flipping **back** happens only after a passing canary, in the release window, with the on-air announcement for a voice (PRD 7.1).

Two voice vendors are wired from the start; a paid tier is bought only for the blind-test winner, and the runner-up stays on pay-as-you-go with a weekly canary that keeps the account live (architecture 08 D10).

## 6. Outside facts that change costs

The only dated items on this page are facts about the outside world (ADR-25.1).

| Date or interval | Event | Task |
|---|---|---|
| 2026-11-13 | Hume's voice APIs shut down | CI rejects any `hume` dependency |
| 2027-01-01 | Gemini 3.8 prices double | the second dated rows are in `prices.yaml`; the voice blind test is judged on post-doubling prices (ADR-24.6) |
| 2027-01-06 | OpenAI TTS deprecation | not used; listed so nobody adds it |
| every 120 days | price staleness | `price_stale` alarm; the agent re-checks every row against the vendor's price page and opens a PR |

## 7. Monthly reconciliation

`cost/reconcile` compares `vendor_calls` sums for the month with each vendor's invoice: Anthropic through its usage and cost admin API, the rest by CSV upload on `/admin/costs`. A variance over 5% for any vendor raises an alarm and is the first item in the next weekly review. The usual causes: a `prices.yaml` row that is wrong, a vendor billing a unit we do not count (connection minutes, concurrency reservations), or a key used outside the middleware. All three are bugs, and each becomes a story.
