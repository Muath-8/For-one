# Cost model, vendor strategy and tracing

Domain 08 of the For one technical architecture. Written 2026-10-17 against PRD-v2 (Implementation PRD v3.0, 2026-10-10), and revised 2026-11-06 against the 2026-10-23 decisions (decisions.md), the second review pass (the conformance and skeptic reviews in `_review-findings.md`) and 10-decision-records.md. "PRD x.y" means PRD-v2 part x.y; where decisions.md or 10-decision-records change a part, the decision is cited instead (ADR-01). Tags: [DECISION] ruled here; [ASSUMPTION] assumed because the sources are silent; [OPEN for Muath] only the owner can settle. Implements PRD-v2 1.4 (AI cost line), 14.3 (stack, adapters, two voice vendors, price events), 14.4 (vendor tests, now the language gate's checks, ADR-03), 14.5 (cost per session), 10.14 (recognizer test), 16.1 (cost gate) and 16.2 (heavy-use outliers), and decisions.md §2 (the cost model sets the price: three monthly USD plans and the margin by plan). It reuses the names the topology (01), pipeline (02), call (03), data (04), assessment (05) and client (06) documents already introduced; where two of them named the same thing differently, this document rules, because cost tracing is this domain's.

**What changed in this revision, in one paragraph.** The document now prices three plans (`one_a_day` $19.99, `two_a_day` $29.99, `three_a_day` $44.99, ADR-04) instead of one daily session: `plan` is on every roll-up, section 6.5 computes cost per learner-day and the margin by plan, the weekly report gains "Margin by plan" with `plan_mix` and `blended_margin`, the daily cap and the per-learner guards scale with `plan.episodes_per_day` (ADR-15), and the volume table is sized for 2 to 3 episodes a day. The unit table re-adopts 02 §6 (writer 9k output, alignment always with Gemini, the pre-write and idea-refresh lines, 1-hour cache writes at 2x input), which moves the beta session from $0.64 to $0.67 a session to $0.67 to $0.70 before levers. Salma's after-call notes, the polish line and the chat margin note are gone (ADR-06); what remains is `salma_explain` on demand. `vendor_calls` is written in its own transaction with the `learner_spend_daily` upsert and an S3 spool in the worker (ADR-13); spend modes no longer downgrade models (ADR-14); Langfuse receives metadata and the research pseudonym unless the learner opted into data use (ADR-09); the editor fallback is Opus and embeddings are Google's (ADR-10, 11); the vendor tests are `vendor-lab gate --target <lang>` with raters and clips per target language (ADR-03); every date follows ADR-07 and every job runs in UTC (ADR-16). Section 11 is the revision log.

Every price in this document is a list price with its date. Anthropic prices are from the API reference cached 2026-10-06 as 02 §6 restates them; every other vendor's price is from the lens documents' vendor-page reads of 2026-10-09 unless marked [ASSUMPTION]. None is a measurement. The first measurement replaces them on 2026-12-22 (PRD-v2 19.2 exit criterion, re-dated by ADR-07).

---

## 1. Summary and the decisions in one table

The cost model sets the price (decisions.md §2): three monthly USD plans of one, two or three new episodes a day, with the rule that no plan may lose money on a learner who uses every episode at the planning cost of $0.35 a session. The beta cannot meet the $0.60 budget by accident, and the $0.30 to $0.35 scale target cannot be met at list prices after 2027-01-01. The arithmetic in section 6 says: with 02 §6's unit table the recommended beta stack lands at $0.61 to $0.70 a session before levers depending on which voice vendor wins the blind test (Gemini with batch TTS at the bottom, Inworld at the top, ElevenLabs at list price at $1.21 and out), and $0.56 to $0.61 after the configuration levers of section 6.3. The Gemini price doubling on 2027-01-01, now in beta week 2, adds $0.18 to a Gemini-voiced session and $0.015 to any session (the editor), which is why the voice vendor decision due 2026-11-17 is the single most important cost decision in the beta. The floor stack reaches $0.36 to $0.39 before the doubling and $0.43 to $0.45 after it (10-decision-records §10 item 4 quotes $0.39 to $0.43 from the first draft's unit table; 02 §6's writer output and side lines add $0.02 to $0.03). That post-doubling floor is above the $0.42 break-even of the `two_a_day` and `three_a_day` plans on a learner who uses every episode (section 6.5): either the price points or the floor stack must move, and the levers that close the gap (a negotiated voice rate, on-tap rendering, shorter calls, or $34.99 for `two_a_day`) are 10-decision-records §10 items 4 and 5 [OPEN for Muath].

Cost is traced the way the topology already specified: one middleware in `forone.adapters` writes one `vendor_calls` row and one Langfuse observation per vendor call, priced from a dated `price_book`, and upserts the per-learner spend counter in the same statement (ADR-13). This document owns those tables, the price file, the Langfuse conventions, the roll-ups, the weekly report with its margin section, the alarms and the spend guard. Nothing about cost is shown to a learner (PRD-v2 law 1 and 16.2: "a warning light, never a goal").

| # | Decision | Chosen | Reason in one line | Rejected |
|---|---|---|---|---|
| D1 | Single source of cost truth | `vendor_calls` table in Postgres, one row per vendor call, written by the adapter middleware in its own short transaction the moment the vendor responds, idempotent on `(inngest_run_id, step, attempt)` or `(call_id, turn_index, capability)`, with `learner_spend_daily` (07) upserted in the same statement; `pipeline_steps.cost_usd` (02) and `episodes.cost_usd`, `calls.metrics.cost_usd`, `events.cost_usd` (04) are denormalized sums of it [DECISION, PRD-v2 14.5, ADR-13] | One table answers "per role, per vendor, per learner, per plan, per session" with one `GROUP BY`; roll-ups can be rebuilt from it; a row outside the caller's transaction survives the retry the spend guard exists to catch | Cost only in `events` (sample episodes, canaries and vendor tests have no learner); cost only in Langfuse (a processor, sampled at scale, outside our region); the row inside the caller's transaction (the first draft: lost on every rollback) |
| D2 | Price source | `packages/adapters/prices.yaml`, checked in, dated rows with `valid_from`, loaded into the `price_book` table by migration; the middleware prices from the table, never from the YAML at runtime [DECISION] | 01 named the file and 02 named the table; both are right: the file is reviewed in a pull request, the table is joinable in SQL | Prices hard-coded in adapters; prices fetched from vendor APIs (none publish a machine-readable price list) |
| D3 | Tracing tool and what it receives | Langfuse Cloud EU, one trace per unit of work, 100% of traces in the beta; `user_id` is the research pseudonym (`research_pseudonyms`, 04), never the learner id; by default an observation carries ids, versions, usage, cost, latency and a prompt hash only; prompt and completion text are sent only when `consents.data_use` is true at call time and after `anonymize()`; retention 30 days; debugging reads prompts from the home region (02's `pipeline_steps` artifacts; the call brief and turns in `events`) [DECISION, 01 D15, ADR-09] | Three documents had three rules for one processor; the strictest is the one 01 already designed, and the pipeline keeps every prompt as an artifact anyway | OpenTelemetry to Grafana only (no prompt views); Helicone-style proxy (a hop in the live path); self-hosted Langfuse (operations for a two-person team; kept as the fallback if the processor is refused); full text with the learner id for every learner (this document's first draft) |
| D4 | Budget enforcement in code | A `cost_guard` with three spend modes (`normal`, `conserve`, `halt`) switched by daily spend; automatic modes change only what no learner hears (force batch, cap rewrites, skip canaries and the nightly smoke, defer anonymization) and may pause on-demand extras under the daily cap; model downgrades (Haiku host, Sonnet teacher) are feature flags a person flips after `eval-gate` passes (09 D8); the stop line ($1.00) opens a 48-hour plan window as a P3 ticket, it does not stop service [DECISION, PRD-v2 1.4, 16.1, ADR-14] | PRD-v2 says "over $1.00 with no costed plan" is the stop signal; the plan is a human decision, and so is any quality change | Hard per-learner cut-off (breaks law 4 and the trust contract: a learner would lose a session for our budgeting); automatic model downgrades on a busy day (the first draft's `conserve`: the product working would have degraded itself) |
| D5 | Beta voice rule | The blind test picks the cheapest vendor that passes (PRD-v2 14.5); ElevenLabs can win only at a negotiated rate at or below $25 per million characters [DECISION] | At $80 per million characters the voice line alone is $0.66 and the session is over the stop line | ElevenLabs at list price (quality is not in doubt; the price is) |
| D6 | Text model tiering, beta | Exactly the PRD classes: Opus 5.5 teacher (batch), Sonnet 5.5 writer (batch), host, Salma when asked (`salma_explain`), chat, proof; Haiku 5.5 fitter, analyst, memory keeper, talkback resolver; Gemini 3.8 Flash editor with `claude-opus-5-5` as its fallback (ADR-11); Google embeddings (ADR-10) [DECISION, PRD-v2 14.3] | The text lines sum to about $0.22 of the session; the levers are elsewhere until measured | Haiku host from day one (a quality decision the 50-call test must make, section 6.3); Haiku as the fallback editor (weaker than the writer it checks) |
| D7 | Batch everywhere nobody waits | Teacher and writer on the Message Batches API with 02's cut lines from build week 2; batch TTS where the vendor offers it from P1; after-session roles and the on-demand `daily_extra` episodes (ADR-05) stay standard [DECISION, PRD-v2 3.2, 14.5] | Batch halves the two biggest text lines ($0.13 saved); TTS batch saves $0.07 only on Gemini and its turnaround is unverified | Batch for the analyst and memory keeper (saves under $0.002 and delays the after-session pass) |
| D8 | Prompt caching contract | Every role has a `cache_prefix` (package prompt, bible, brief) and the middleware records `cache_read_input_tokens` and `cache_creation_input_tokens` with the TTL used (1-hour for the batch pipeline, 02 D5; 5-minute inside a call); an alarm fires when a role's cache hit rate falls under a floor set from the build week 2 baseline (85% until then) over 24 hours [DECISION] | A silent cache invalidator costs about $0.03 a session on the host alone and shows nowhere else; a 1-hour write costs 2x input and must be priced as such | Trusting the prompt layout without measuring it; pricing every cache write at the 5-minute rate (the first draft, 37.5% low for the pipeline) |
| D9 | Vendor tests as code, per target language | `vendor-lab gate --target <lang>` (01, ADR-03) runs the 14.4 and 10.14 tests as the language gate's checks 1, 2 and 4 through the adapter package and writes scoring sheets as CSV under `langgate/<target>/<date>/`; raters are 5 native speakers of the target plus 5 learners of it from anywhere; the decision rules are in this document, section 4.6; English is the pilot target and the only one whose gate must pass before the beta [DECISION, PRD-v2 14.4, 10.14, ADR-03] | The winners drop into `packages/languages/<target>/vendors.yaml` with no new code; the sheets are the evidence Muath signs; one harness per language instead of one-off scripts per pair | Listening in vendor playgrounds (different voices, no timestamps, no cost rows); a test parameterized by one learner nationality (the first draft) |
| D10 | Two voice vendors wired, one contract first | Both blind-test finalists are implemented during the gate run (2026-11-01 to 11-17, before build week 1; pipeline D9); a paid tier is bought only for the winner, the runner-up stays on pay-as-you-go until the first failover proves it [DECISION, PRD-v2 14.3] | Two minimum commitments for a product with 100 learners is waste; pay-as-you-go keeps the understudy warm | Two enterprise contracts (year two, at 10,000 learners) |
| D11 | Reconciliation, three clocks | Hourly: `learner_spend_daily` against `vendor_calls` (ADR-13). Once, before `vendors.yaml` is committed: 10 minutes of audio rendered and 30 minutes transcribed on every finalist, `vendor_calls` sums compared with each vendor's usage dashboard the same day, rows marked `verified: <date>`. Monthly: `vendor_calls` sums against each vendor's billing (Anthropic through the Usage and Cost Admin API; others by CSV upload), alert above 5% variance [DECISION] | Without it, a wrong row in `prices.yaml` goes unnoticed for a quarter, and about $0.10 of the session rests on rows nobody has checked against a bill before the voice decision | Trusting the price file; the first bill check four weeks after the decision it should inform |
| D12 | What the learner sees | Nothing. No cost, no "heavy user" message, no throttle text; the allowance (`plan.episodes_per_day`, ADR-04) is the only learner-facing limit and it is a product rule, not a cost rule [DECISION, law 1, 11] | Cost is ours to manage | Any cost-driven message to a learner |
| D13 | Price-setting and the margin by plan | The cost model prices a learner-day as session cost × episodes used plus the on-demand premium on episodes 2 and 3 (about $0.05 each, ADR-05); section 6.5 prints the decisions.md margin table from `assumptions.yaml` and, from the beta, from measured data; the weekly report's "Margin by plan" section carries net price (list less the processor's measured fee and tax), measured episodes used, cost per learner-month, margin, break-even cost per session at full use, `plan_mix` and `blended_margin` [DECISION, decisions.md §2, ADR-15] | decisions.md made the cost model the thing that sets the price; the public-launch gate reads the blended margin (concept-v2 §9) | Pricing one daily session and leaving the plan arithmetic to a spreadsheet (the first draft) |
| D14 | Per-plan guards and the daily cap | Per learner and learner-local day: soft guard 2.5 × `episodes_per_day` × $0.60, hard guard 4 × `episodes_per_day` × $0.60 (07's `costguard.check`); environment cap `SPEND_CAP_USD_PER_DAY = max($50, Σ over active learners of plan.episodes_per_day × $1.00)` over the UTC day [DECISION, ADR-15] | Every per-day limit in the first drafts assumed one episode a day and was 50 to 200% low for the upper plans | Fixed $2.50 / $5.00 guards and learners × $1.50 |

---

## 2. Requirements this domain implements

| PRD-v2 part | Requirement | Where in this document |
|---|---|---|
| 1.4 | Budget about $0.60 per session in the beta; scale target $0.30 to $0.35; stop line $1.00 with no plan; cost tracing on every model, voice and recognition call from the first learner | 4.1 to 4.4 (tracing), 4.5 (alarms), 6 (model) |
| 14.1 | Cost tracing is code, not AI | 3, 4 |
| 14.3 | Stack defaults; thin adapters; two voice vendors wired from the start; Gemini 3.8 doubling 2027-01-01; Hume shutdown 2026-11-13; Langfuse logging every call with cost and learner-model version (under 01 D15 and ADR-09: metadata unless the learner opted in) | 4.2 (price book), 4.7 (adapters and fallback), 4.8 (risk calendar), 4.3 (Langfuse) |
| 14.4 | Voice blind test (10 raters: 5 native speakers of the target language, 5 learners of it; ADR-03 generalizes the PRD's nationality-specific raters), the 30-clip recognizer test per target language, 50 scripted calls | 4.6 (procedures and scoring sheets, as the language gate's checks) |
| 14.5 | Cost per session = teacher share, writing, fitting, editing, all audio, call and round two, re-transcription, Salma when asked, chat, after-session pass, the weekly proof per learner-week; traced per role, per vendor, per learner, per plan; reported weekly; next to heavy-use outliers (the notes line is removed by decisions.md §3, ADR-06) | 4.4 (roll-ups and the weekly report), 6 (the itemized model) |
| decisions.md §2 | Three monthly USD plans; the cost model sets the price; no plan loses money on a full-use learner at $0.35 a session; margins by plan at typical and full use; blended margin above about 50% at the public-launch gate (concept-v2 §9) | 6.5 (cost per learner-day, margin by plan), 4.4.2 section 9 of the report |
| 10.14 | 30 real-learner clips through each streaming and batch recognizer; error survival, filler retention, hallucinations near pauses, code-switch handling; winner per role and the confidence threshold | 4.6.3 |
| 15 | Voice vendor outage: second vendor within the same day's production | 4.7 (fallback order), 5 |
| 16.1 | Gate: cost per session under $0.60; stop and rethink over $1.00 with no plan | 4.5 |
| 16.2 | Minutes per day: heavy-use outliers flagged, a warning light never a goal | 4.4.3 |
| 19.2 | Build week 1: cost tracing; exit on 2026-12-22: measured cost per session and a costed path to $0.35 or less | 7, 6.4 |
| 2.1 | Sample episode cost ceiling $0.05 | 4.5 (per-kind ceilings) |
| 12.5, 12.6 | Data rules for a processor holding learner text (Langfuse); deletion | 4.3.4 |
| Laws 1, 11; trust 2 | No cost-driven surface or message to the learner | D12 |

Laws that bind the design directly: law 1 (no numbers that fill or target; cost dashboards are internal only), law 11 (the allowance of one, two or three new episodes a day is the only cap; cost never shortens a learner's day), trust promise 2 (no cost-driven re-engagement or throttling messages).

---

## 3. Architecture

### 3.1 Components

| Component | Kind | Owner | Job |
|---|---|---|---|
| `forone.adapters.tracing` | Python module (middleware) | this domain | Wraps every adapter call: times it, extracts units, prices them from `price_book`, writes `vendor_calls`, emits the Langfuse observation, enforces the spend guard |
| `forone.adapters.prices` | Python module plus `prices.yaml` | this domain | Loads the price file into `price_book`; `price_for(vendor, model, unit, pricing_mode, at)` |
| `price_book` | Postgres table | this domain | Dated unit prices |
| `vendor_calls` | Postgres table (monthly partitions) | this domain | One row per vendor call |
| `learner_spend_daily` | Postgres table (07 owns the DDL; this domain's middleware upserts it) | 07 and this domain | The hot-path per-learner, per-plan spend counter the guard reads; upserted in the same statement as the `vendor_calls` insert (ADR-13) |
| `session_costs`, `learner_costs_daily`, `role_vendor_costs_daily` | Postgres tables, filled by `cost/rollup` | this domain | Roll-ups per session, per learner-day, per role-vendor-day, every one carrying `plan` |
| `cost_guard` | One row in `vendor_config` (`key='spend_mode'`) plus the `cost/alarms` function; the per-learner guard is 07's `costguard.check` with this domain's thresholds | this domain | Spend modes, per-plan guards and alarms |
| `cost/rollup`, `cost/alarms`, `cost/reconcile-spend`, `cost/weekly-report`, `cost/reconcile-monthly` | Inngest functions in `workflows` | this domain | Roll-ups every 15 minutes; alarms every 15 minutes; `learner_spend_daily` reconciled against `vendor_calls` hourly; report Mondays 06:00 UTC; invoice reconciliation on the 2nd of each month at 06:00 UTC (ADR-16: fixed UTC times, nothing in a learner's timezone) |
| `vendor-lab` | CLI in the monorepo (01), with the `gate --target <lang>` command (ADR-03) | this domain with the call and pipeline domains | Runs the 14.4 and 10.14 tests per target language through the adapter package, writes scoring sheets under `langgate/<target>/<date>/` |
| `/admin/cost` | One `sqladmin` page in `api` (01's admin pages, on `forone_admin`, ADR-17) | this domain | Last 7 days by role, vendor, learner, plan; outliers; spend mode; price book version; margin by plan |
| Langfuse Cloud EU | Managed | this domain owns conventions; the security domain approves the processor | Traces with ids, versions, usage, cost, latency and learner-model version; prompt and completion text only for `data_use` learners after `anonymize()` (ADR-09) |
| Anthropic Usage and Cost Admin API | Vendor API | this domain | Monthly reconciliation for the Anthropic lines |

### 3.2 Data flow, described as a diagram

Draw four lanes left to right: **callers**, **adapter layer**, **cost stores**, **consumers**.

1. Callers: `workflows` (teacher, writer, fitter, editor, voice studio, re-listen, analyst, memory keeper, Salma when asked, proof producer, rater), `call-worker` (streaming STT, host LLM, call TTS, talkback resolver, Salma TTS), `api` (sample episode trigger, gloss misses, `POST /v1/episodes/next` for `daily_extra` episodes, ADR-05). Each caller constructs a `CallMeta` (01's dataclass) carrying `learner_id`, `plan`, `role`, `episode_id`, `episode_kind`, `call_id`, `session_id`, `learner_model_version`, `prompt_version`, `inngest_run_id`.
2. Adapter layer: `adapters.for_role(role)` returns the adapter chosen by `vendors.yaml` and overridden by `vendor_config`. Every public method is wrapped by `tracing.traced`. The wrapper starts a timer and a Langfuse observation, calls `costguard.check` (07) with the projected cost, calls the vendor, reads the usage the adapter returns (`UnitUsage`), prices it with `price_for`, and writes one `vendor_calls` row **in its own short autocommit transaction the moment the vendor responds, never inside the caller's transaction** (ADR-13). The insert is idempotent on `(inngest_run_id, step, attempt)` for pipeline and after-session calls and on `(call_id, turn_index, capability)` for call turns, so an Inngest retry that re-runs a step after a timeout, a validation failure or a crashed task finds the money already counted; the same statement upserts `learner_spend_daily` (`insert ... on conflict (learner_id, local_date) do update set cost_usd = cost_usd + excluded.cost_usd`), so the guard counter and the ledger cannot diverge. On vendor error it writes the row with `outcome='error'` and the fallback adapter's call writes a second row with `fallback_from_vendor` set. In `call-worker` the rows are written off the audio thread: each turn's rows are appended to an S3 spool object per call (`spool/calls/{call_id}.ndjson` in the bucket 01 already uses for event spooling) before the 5-second buffered flush to Postgres, so a task that dies mid-call loses nothing; `cost/rollup` ingests any spool object whose rows are not in `vendor_calls`.
3. Cost stores: `vendor_calls` (raw), then `cost/rollup` every 15 minutes into `session_costs` (keyed by `session_id`, with `cost_by_role` jsonb and `plan`), `learner_costs_daily`, `role_vendor_costs_daily`; `cost/reconcile-spend` hourly recomputes `learner_spend_daily` for the learner-local days still open from `vendor_calls` and alerts on a drift above $0.05. The pipeline's publisher reads `session_costs` for `episodes.cost_usd` and emits `episode.cost_recorded` (02); the call worker reads its own buffered sum into `calls.metrics.cost_usd` (03). `events.vendor_call_id` (04) points back to the row for model-produced events.
4. Consumers: `cost/alarms` (reads the roll-ups, `learner_spend_daily` and `vendor_calls` for the last 15 minutes), `cost/weekly-report` (reads the roll-ups and `subscriptions.plan`, writes a Markdown report to the ops channel and `/admin/cost`), `cost/reconcile-monthly` (reads `vendor_calls` and the vendors' billing), Langfuse (receives the same observation with metadata; prompt and completion text only for `data_use` learners after `anonymize()`; never audio).

A fifth element sits above the lanes: `price_book`, read by the adapter layer and written only by migrations from `prices.yaml`.

### 3.3 Where the cost of one session comes from

One session (an episode with its call) on the recommended stack produces about 60 `vendor_calls` rows: 1 teacher (the nightly plan for all of the day's 1 to 3 episodes, ADR-05), 1 writer, 1 to 3 rewrites, 2 fitter, 1 to 2 editor, 1 embedding, 4 to 6 TTS jobs (scenes, article, recap), 1 alignment (always with Gemini TTS), 1 re-listen ASR, 0 to 10 gloss misses, about 25 host turns (each a `text` row), 1 streaming STT row per stream (2), 25 call TTS rows, 0 to 3 talkback rows, about 25 verbatim rows (per turn, 05), 1 pronunciation, 2 analyst, 1 memory keeper, 0 to 1 `salma_explain` (only when the learner asks), 3 to 5 chat host. All carry `session_id`, so `session_costs` is one aggregate. A `daily_extra` episode (the learner's "next one") produces the same rows minus the teacher's (its brief is in the nightly plan) with the writer at standard pricing; a learner-day is the sum of its 1 to 3 sessions (section 6.5).

### 3.4 Interfaces this domain exposes

```python
# packages/adapters/forone/adapters/tracing.py (public surface)
from forone.adapters.interfaces import CallMeta

class UnitUsage(TypedDict, total=False):
    input_tokens: int; cache_read_tokens: int; cache_write_tokens: int; output_tokens: int
    chars: int; audio_seconds: float; utterances: int; requests: int

def traced(capability: str):
    """Decorator for every adapter method. The adapter returns (result, UnitUsage, vendor_request_id)."""

async def record_external(meta: CallMeta, *, vendor: str, capability: str, units: UnitUsage,
                          cost_usd: float | None = None, outcome: str = "ok") -> str:
    """For costs that are not adapter calls but belong to a session: LiveKit participant minutes,
    media egress. Returns vendor_calls.id."""

def spend_mode() -> Literal["normal", "conserve", "halt"]:
    """Cached 60 s from vendor_config. Callers that can save money without changing what a learner hears read it (section 4.5)."""

def learner_guard_usd(plan: str) -> tuple[Decimal, Decimal]:
    """(soft, hard) per learner-local day: 2.5 and 4 x plan.episodes_per_day x cost.session_budget_usd (ADR-15); read by 07's costguard.check."""

def price_for(vendor: str, model: str, unit: str, pricing_mode: str, at: datetime) -> Decimal: ...
```

```sql
-- what other domains read
select cost_usd, cost_by_role, plan from session_costs where session_id = $1;
select learner_id, plan, day, cost_usd, episodes, sessions, minutes_heard, minutes_spoken from learner_costs_daily where day >= $1;
```

---

## 4. Detailed design

### 4.1 `vendor_calls`

```sql
create table vendor_calls (
  id                    uuid primary key default gen_random_uuid(),
  occurred_at           timestamptz not null default now(),
  env                   text not null,                        -- dev | staging | prod
  service               text not null,                        -- api | workflows | call-worker | vendor-lab
  learner_id            uuid,                                  -- null for sample, canary, vendor tests
  plan                  text,                                  -- subscriptions.plan at call time: one_a_day | two_a_day | three_a_day | trial (ADR-04)
  session_id            uuid,
  episode_id            uuid,
  call_id               uuid,
  inngest_run_id        text,
  step                  text,                                  -- pipeline or after-pass step name; with inngest_run_id and attempt the idempotency key (ADR-13)
  attempt               int,
  turn_index                int,                                   -- call turns: with call_id and capability the idempotency key
  langfuse_trace_id     text,
  role                  text not null,                        -- vendors.yaml role: teacher, writer, host, episode_tts ...
  capability            text not null,                        -- text | batch_text | tts | tts_stream | stt_stream | stt_verbatim | pronunciation | align | embed | media | external
  vendor                text not null,
  model                 text,                                  -- model id, voice id, or recognizer model
  pricing_mode          text not null,                        -- standard | batch | on_demand
  prompt_version        text,
  learner_model_version int,
  units                 jsonb not null,                        -- UnitUsage
  cost_usd              numeric(10,6) not null,
  price_book_ids        int[] not null,                        -- the rows used to price this call
  latency_ms            int,
  outcome               text not null,                        -- ok | error | timeout | cancelled | fallback_used
  error_code            text,
  fallback_from_vendor  text,
  vendor_request_id     text,
  episode_kind          text                                   -- daily | daily_extra | swap | return | pilot | sample | fallback | rehearsal | finale | proof | canary (ADR-19)
) partition by range (occurred_at);
-- monthly partitions created by retention/daily (01), same as events
create unique index on vendor_calls (inngest_run_id, step, attempt) where inngest_run_id is not null;   -- ADR-13 idempotency
create unique index on vendor_calls (call_id, turn_index, capability) where call_id is not null and turn_index is not null;
create index on vendor_calls (session_id) where session_id is not null;
create index on vendor_calls (learner_id, occurred_at);
create index on vendor_calls (role, vendor, occurred_at);
create index on vendor_calls (occurred_at) where outcome <> 'ok';
```

Rules:
- Row-level security by `learner_id` as in 04, with a `forone_cost` role allowed to read across learners for roll-ups and reports (the only cross-learner read path besides the gloss cache and opt-in research set; the security domain approves it).
- `units` is the raw usage the vendor reported, never derived. Where a vendor reports nothing (streaming TTS by the second), the adapter counts the unit itself and sets `units.estimated = true`.
- The insert runs in its own short transaction and never in the caller's (ADR-13); a duplicate on either unique index is an `on conflict do nothing`, so a retried step is counted once. The same statement upserts `learner_spend_daily(learner_id, local_date, plan, cost_usd, calls)` (07's table) when `learner_id` is set.
- Deletion: `learner/delete` (04) aggregates a learner's rows into `learner_costs_daily` with `learner_id = null, deleted_learner_bucket = true` before deleting them, so totals survive.
- Retention: raw rows 13 months (one year of comparisons plus one), roll-ups forever.

### 4.2 `prices.yaml` and `price_book`

```yaml
# packages/adapters/prices.yaml  (every row: who, what, unit, price, dated; the file is the pull-request surface)
version: 2026-11-06
# every row may carry `verified: <date>` once D11's one-off check has compared it with the vendor's dashboard; estimate.py
# refuses to print a stack whose chosen roles use a row that is neither verified nor from a vendor price page read (`source`).
rows:
  # Anthropic, API reference cached 2026-10-06, as 02 section 6 restates it. Cache write: 5-minute TTL = 1.25x input (cache_write_tokens,
  # used inside a call); 1-hour TTL = 2x input (cache_write_1h_tokens, used by the batch pipeline, 02 D5). Batch = 50% of every token.
  - {vendor: anthropic, model: claude-opus-5-5,   unit: input_tokens,          usd_per_million: 4.00,  valid_from: 2026-10-06, source: anthropic-pricing}
  - {vendor: anthropic, model: claude-opus-5-5,   unit: output_tokens,         usd_per_million: 20.00, valid_from: 2026-10-06}
  - {vendor: anthropic, model: claude-opus-5-5,   unit: cache_read_tokens,     usd_per_million: 0.20,  valid_from: 2026-10-06}
  - {vendor: anthropic, model: claude-opus-5-5,   unit: cache_write_tokens,    usd_per_million: 5.00,  valid_from: 2026-10-06, note: "5-minute TTL"}
  - {vendor: anthropic, model: claude-opus-5-5,   unit: cache_write_1h_tokens, usd_per_million: 8.00,  valid_from: 2026-10-06, note: "1-hour TTL, 2x input (02 section 6)"}
  - {vendor: anthropic, model: claude-sonnet-5-5, unit: input_tokens,          usd_per_million: 2.00,  valid_from: 2026-10-06}
  - {vendor: anthropic, model: claude-sonnet-5-5, unit: output_tokens,         usd_per_million: 10.00, valid_from: 2026-10-06}
  - {vendor: anthropic, model: claude-sonnet-5-5, unit: cache_read_tokens,     usd_per_million: 0.20,  valid_from: 2026-10-06}
  - {vendor: anthropic, model: claude-sonnet-5-5, unit: cache_write_tokens,    usd_per_million: 2.50,  valid_from: 2026-10-06, note: "5-minute TTL"}
  - {vendor: anthropic, model: claude-sonnet-5-5, unit: cache_write_1h_tokens, usd_per_million: 4.00,  valid_from: 2026-10-06, note: "1-hour TTL, 2x input (02 section 6)"}
  - {vendor: anthropic, model: claude-haiku-5-5,  unit: input_tokens,          usd_per_million: 0.10,  valid_from: 2026-10-06, note: "prompts up to 100K tokens; 0.50 above"}
  - {vendor: anthropic, model: claude-haiku-5-5,  unit: output_tokens,         usd_per_million: 0.50,  valid_from: 2026-10-06}
  - {vendor: anthropic, model: claude-haiku-5-5,  unit: cache_read_tokens,     usd_per_million: 0.01,  valid_from: 2026-10-06, assumption: "0.1x input; verify"}
  - {vendor: anthropic, model: claude-haiku-5-5,  unit: cache_write_tokens,    usd_per_million: 0.125, valid_from: 2026-10-06, note: "5-minute TTL"}
  - {vendor: anthropic, model: claude-haiku-5-5,  unit: cache_write_1h_tokens, usd_per_million: 0.20,  valid_from: 2026-10-06, assumption: "2x input by the same rule as Opus and Sonnet; verify"}
  - {vendor: anthropic, model: "*", pricing_mode: batch, multiplier: 0.5, valid_from: 2026-10-06}
  # Google, Gemini API pricing page 2026-10-09; several prices double 2027-01-01 (second dated row)
  - {vendor: google, model: gemini-3.8-flash, unit: input_tokens,  usd_per_million: 0.75, valid_from: 2026-10-09}
  - {vendor: google, model: gemini-3.8-flash, unit: output_tokens, usd_per_million: 3.75, valid_from: 2026-10-09}
  - {vendor: google, model: gemini-3.8-flash, unit: input_tokens,  usd_per_million: 1.50, valid_from: 2027-01-01}
  - {vendor: google, model: gemini-3.8-flash, unit: output_tokens, usd_per_million: 7.50, valid_from: 2027-01-01}
  - {vendor: google, model: gemini-3.8-flash-tts, unit: audio_tokens, usd_per_million: 9.00,  valid_from: 2026-10-09, note: "25 audio tokens per second = 1,500 per minute"}
  - {vendor: google, model: gemini-3.8-flash-tts, unit: audio_tokens, usd_per_million: 18.00, valid_from: 2027-01-01}
  - {vendor: google, model: "*-tts", pricing_mode: batch, multiplier: 0.5, valid_from: 2026-10-09}
  - {vendor: google, model: gemini-3.8-flash-lite-tts, unit: audio_minutes, usd_per_unit: 0.00875, valid_from: 2026-10-09, assumption: "lens: about $0.07 per 8-minute episode; verify the token rate and whether it doubles"}
  # Voice vendors (vendor pages 2026-10-09)
  - {vendor: inworld,    model: tts-2,        unit: chars, usd_per_million: 25.00, valid_from: 2026-10-09}
  - {vendor: inworld,    model: tts-2-flash,  unit: chars, usd_per_million: 15.00, valid_from: 2026-10-09}
  - {vendor: elevenlabs, model: v4,           unit: chars, usd_per_million: 80.00, valid_from: 2026-10-12, note: "list after the promotion that ended 2026-10-12"}
  - {vendor: elevenlabs, model: v4-turbo,     unit: chars, usd_per_million: 40.00, valid_from: 2026-10-12}
  - {vendor: elevenlabs, model: flash-v2.5,   unit: chars, usd_per_million: 40.00, valid_from: 2026-10-09}
  - {vendor: elevenlabs, model: forced-alignment, unit: audio_minutes, usd_per_unit: 0.0037, valid_from: 2026-10-09, note: "about $0.026 per 7-minute episode"}
  - {vendor: cartesia,   model: sonic-3.6,    unit: chars, usd_per_million: 45.00, valid_from: 2026-10-09, assumption: "mid of the $37 to $50 range"}
  # Recognition (vendor pages 2026-10-09)
  - {vendor: soniox,     model: stt-rt-v5,              unit: audio_minutes, usd_per_unit: 0.0020, valid_from: 2026-10-09}
  - {vendor: deepgram,   model: nova-3-multilingual,    unit: audio_minutes, usd_per_unit: 0.0058, valid_from: 2026-10-09, note: "promotional; may end"}
  - {vendor: assemblyai, model: universal-3.6-realtime, unit: audio_minutes, usd_per_unit: 0.0075, valid_from: 2026-10-09}
  - {vendor: assemblyai, model: universal-3.6-batch,    unit: audio_minutes, usd_per_unit: 0.0040, valid_from: 2026-10-09, assumption: "batch verbatim; lens range $0.002 to $0.017; verify"}
  - {vendor: elevenlabs_scribe, model: scribe-v2,       unit: audio_minutes, usd_per_unit: 0.0067, valid_from: 2026-10-09, assumption: "verify"}
  - {vendor: speechace,  model: pronunciation,          unit: utterances,    usd_per_unit: 0.0080, valid_from: 2026-10-09, note: "per 15-second utterance"}
  - {vendor: microsoft,  model: pronunciation,          unit: audio_minutes, usd_per_unit: 0.0170, valid_from: 2026-10-09, assumption: "about $1 per hour, unverified"}
  # Other
  - {vendor: google,  model: gemini-embedding, unit: input_tokens, usd_per_million: null, valid_from: 2026-11-06, assumption: "ADR-10 moves embeddings to Google under the existing processor row; no lens read the list price; 02 section 6 budgets under $0.001 a call (1.5k tokens); the row is filled from the price page in the gate run and is `unpriced` until then"}
  - {vendor: livekit, model: cloud-ship, unit: participant_minutes, usd_per_unit: 0.0010, valid_from: 2026-10-16, assumption: "01 flags this rate for verification"}
  - {vendor: aws,     model: s3-egress,  unit: gigabytes, usd_per_unit: 0.09, valid_from: 2026-10-16}
  # Payments (ADR-21; outside the AI cost, read by the margin section of the weekly report; the real fee row replaces these on the processor decision of 2026-12-02)
  - {vendor: payments, model: paddle-mor,      unit: revenue_share, multiplier: 0.05, valid_from: 2026-11-06, assumption: "about 5% plus a per-transaction fee, tax included in the merchant-of-record price"}
  - {vendor: payments, model: stripe-plus-tax, unit: revenue_share, multiplier: 0.03, valid_from: 2026-11-06, assumption: "about 3% plus tax registrations we would carry; the decisions.md planning figure of 15% to tax and fees stands until the fee row is real"}
```

```sql
create table price_book (
  id serial primary key, vendor text not null, model text not null, unit text not null,
  pricing_mode text not null default 'standard', usd_per_unit numeric(14,9) not null,
  multiplier numeric(6,4), valid_from date not null, valid_to date, source text, note text,
  file_version text not null, unique (vendor, model, unit, pricing_mode, valid_from));
```

`price_for` picks the row with the greatest `valid_from <= at` and applies the vendor's `pricing_mode` multiplier row when the call's mode is `batch`. The adapter reports which cache TTL a write used (`UnitUsage.cache_write_ttl` in `{5m, 1h}`) and the middleware prices `cache_write_tokens` or `cache_write_1h_tokens` accordingly; the pipeline's pooled prefixes (02 D5) are 1-hour writes, the host's in-call prefix is a 5-minute write. A call priced with a row older than 120 days raises a `price_stale` warning in the weekly report; a call with no matching row is priced at zero, written with `outcome='ok'` and `error_code='unpriced'`, and counted in the alarms (section 4.5) so a new model never silently costs nothing.

Verification (D11, skeptic review): rows marked `assumption` carry about $0.10 of the $0.67 to $0.70 session. During the gate run and before `vendors.yaml` is committed (by 2026-11-17), `vendor-lab verify-prices` renders 10 minutes of audio and transcribes 30 minutes on every finalist and compares the `vendor_calls` sums with each vendor's usage dashboard the same day; a row within 2% is marked `verified: <date>`, otherwise the row is corrected in the same pull request. `estimate.py` refuses to print a stack whose chosen roles use an unverified `assumption` row, so the exit document's measured number cannot rest on a guess.

The 2027-01-01 doubling is represented exactly as 01 and 02 asked: a second dated row. The weekly reports of 2026-12-21 and 2026-12-28 carry a "what this week would have cost at next week's prices" column so the jump, which lands in beta week 2 (ADR-07), is seen before it happens.

### 4.3 Langfuse conventions

**4.3.1 Trace identity.** One trace per unit of work, named and keyed so a trace can be found from any id in Postgres:

| Unit of work | Trace name | `trace_id` | `session_id` | `user_id` |
|---|---|---|---|---|
| Episode production (any kind, including `daily_extra`) | `episode` | `episode_id` | `session_id` | the research pseudonym (`research_pseudonyms.pseudonym`, 04; ADR-09) |
| Live call | `call` | `call_id` | `session_id` | the pseudonym |
| After-session pass | `after_pass` | `uuid5(NAMESPACE_FORONE, f"{session_id}:after")` (a hash input the SDK accepts without normalization; skeptic minor) | `session_id` | the pseudonym |
| Onboarding (A3 to A8) | `onboarding` | the pre-account session id (06) | same | a pre-account pseudonym, re-keyed to the learner's pseudonym at A9 |
| Weekly proof | `proof` | `proof_id` | null | the pseudonym |
| Sample episode | `sample` | `sample_id` | null | null (anonymous) |
| Canary, vendor-lab | `canary`, `vendor_lab` | run id | null | null |

Observations are named `{role}.{capability}` (`host.text`, `episode_tts.tts`, `verbatim_stt.stt_verbatim`). LLM calls are Langfuse generations with `usage` and `cost` set from the same numbers as `vendor_calls` (so the two never disagree), plus `metadata`: `learner_model_version`, `prompt_version`, `vendors_yaml_sha`, `price_book_ids`, `pricing_mode`, `episode_kind`, `plan`, `spend_mode`, `prompt_sha256`, `data_use` (whether text was sent). Tags: `env`, `role`, `vendor`, `pricing_mode`, `target_language`.

**4.3.2 What is logged.** 01 D15 as revised on 2026-10-17 stands for every domain (ADR-09). By default an observation carries ids, versions, usage, cost, latency and the prompt hash; no prompt, completion, TTS input text, STT output or pronunciation reference leaves the home region. For a learner whose `consents.data_use` is true at call time, the middleware attaches the prompt and completion (text roles), the TTS input text and voice id (never audio), the STT output text (never audio) and the pronunciation reference sentence and score object, each passed through `anonymize()` (04) first. Debugging a bad episode for any other learner reads the prompt from the artifacts the pipeline stores in the home region: 02 keeps every prompt and completion as a `pipeline_steps` artifact, and the call brief and turns are in `events`; the Langfuse trace gives the ids to find them.

**4.3.3 Scrubbing.** Before emission the middleware runs `forone.learner.pii.scrub_for_processor` (04) over metadata and over any field classified as identity: email, phone, birth date, payment ids never leave. Text sent for `data_use` learners has already been through `anonymize()`, which replaces the learner's name and the people in their life with the pseudonym table's placeholders; the display name the host brief carries never reaches the processor.

**4.3.4 Sampling and deletion.** Beta: 100% of traces. Scale (10,000 learners, about 600,000 observations a day at the upper plans' usage): 20% of `episode` and `call` traces, 100% of `after_pass`, `proof`, `onboarding` and anything whose role is `analyst`, `memory_keeper`, `rater` or `proof_producer` (these feed claims; PRD-v2 10.10 "openable" evidence must be debuggable). Sampling is by trace, decided once at trace start from the trace id, which is always a UUID (the after-pass id is derived with `uuid5`, 4.3.1), so a sampled episode is complete. Retention 30 days (01 D15). Deletion: `learner/delete` (04) calls Langfuse's deletion by the pseudonym; this domain owns the adapter `langfuse_admin.delete_user(pseudonym)` and the daily retry until `deletion_ledger.verified_empty` (04). Because the processor holds only the pseudonym and anonymized text, the "deleted" email does not wait on this call (ADR-09 closes 04 §10's question). [ASSUMPTION] Langfuse Cloud exposes per-user deletion through its API in the plan we buy; verified during the gate run with a test user, and if it does not, the fallback is self-hosting (section 8).

**4.3.5 Cost of Langfuse itself.** Beta: Core plan, $0 to $59 a month (01). At 10,000 learners with the sampling above: about 150,000 observations a day, metadata-only spans being small, inside a Pro or Team plan at a few hundred dollars a month; the 01 estimate of $500 a month stands.

### 4.4 Roll-ups, the weekly report and outliers

**4.4.1 Roll-up tables.**

```sql
create table session_costs (
  session_id uuid primary key, learner_id uuid not null, plan text not null, episode_id uuid, local_date date not null,
  episode_kind text not null, cost_usd numeric(10,6) not null,        -- episode_kind daily_extra marks episodes 2 and 3 (ADR-05)
  cost_by_role jsonb not null,            -- {"teacher":0.0812,"writer":0.0540,...}
  cost_by_vendor jsonb not null,
  cost_by_line jsonb not null,            -- the PRD 14.5 lines as revised, section 6.1 mapping
  pricing_escalated bool not null default false,   -- batch cancelled at a cut line (02)
  fallback_used bool not null default false,
  minutes_heard numeric(6,2), minutes_spoken numeric(6,2),
  updated_at timestamptz not null default now());

create table learner_costs_daily (
  learner_id uuid, day date, plan text not null, cost_usd numeric(10,6) not null,
  episodes int not null,                  -- new episodes used that learner-local day (1 to plan.episodes_per_day)
  sessions int not null, calls int not null, swaps int not null, minutes_heard numeric(6,2), minutes_spoken numeric(6,2),
  deleted_learner_bucket bool not null default false, primary key (learner_id, day));
-- learner_spend_daily (07) is the hot-path twin of this table, upserted by the middleware and reconciled hourly (ADR-13); this one is the reporting roll-up.

create table role_vendor_costs_daily (
  day date, role text, vendor text, pricing_mode text, calls int, errors int, cost_usd numeric(12,6),
  units jsonb, cache_hit_rate numeric(5,4), p95_latency_ms int, primary key (day, role, vendor, pricing_mode));
```

`cost/rollup` runs every 15 minutes (Inngest cron), takes `vendor_calls` rows with `occurred_at > last_watermark` plus any worker spool object not yet ingested, and upserts the three tables. `plan` is the learner's `subscriptions.plan` at the time of the call (a trial learner is on `two_a_day`, ADR-04). A session's cost is final 24 hours after the session closes (late verbatim rows arrive after the call); `session_costs.updated_at` says when it last moved. The weekly proof is reported as its own **per-learner-week** line (`learner_costs_daily.cost_usd` on the proof's day, role `proof_producer`): with two and three episodes a day a learner has 7 to 21 sessions in a week, so a per-session share means nothing across plans. Only the per-session gate (PRD-v2 16.1) divides it, by the learner's measured `proofs.sessions_in_week` (computed, ADR-19), into `cost_by_line.proof_share`; PRD-v2 14.5's "a quarter of the weekly proof" is the `one_a_day` case at four sessions.

The PRD lines, as revised by decisions.md §3 (the notes line is gone), are computed from roles by this mapping, which is also what the report prints:

| PRD-v2 14.5 line | Roles summed |
|---|---|
| Teacher | `teacher` |
| Writer | `writer` (including rewrites) |
| Fitter, glosses, editor | `fitter`, `gloss`, `editor`, `embeddings` |
| Voice studio | `episode_tts`, `aligner`, `relisten_stt`, media mix |
| Call (main and round two) | `streaming_stt`, `talkback_stt`, `host`, `call_tts`, `talkback_resolver`, `salma_live`, `salma_tts` (in-call), `livekit`, worker compute |
| Re-transcription and pronunciation | `verbatim_stt`, `pronunciation` |
| Salma (when asked) and chat | `salma_explain` (Sonnet, on demand: the rare explanation when the learner asks), `chat_host`. The notes, polish-card and margin-note roles of the first draft are removed (decisions.md §3, ADR-06); the PRD-v2 14.5 "notes" line is revised by the PRD-v3 thread |
| Analyst and memory keeper | `analyst`, `memory_keeper`, `rater` (amortized), conversation-chunk `embeddings` |
| Proof (per learner-week) and hosting | `proof_producer`, proof `salma_tts` (the weekly proof voice), `s3_egress` (presigned S3 for show audio, ADR-12), feed encode |
| On-demand premium (`daily_extra`) | the difference between a `daily_extra` episode's writer at standard pricing and the batch writer, about $0.05 (ADR-05); printed per learner-day, not per session |

Onboarding (Salma A3, pilot, first call) and the sample episode are not sessions. They are rolled into `learner_costs_daily` on the day they happen and reported as **acquisition cost per learner** on a separate line (about $0.45 at list prices: Salma and first call $0.10 from 03, pilot about $0.30 at standard pricing from 02, sample $0.04 from 02 §6). They are deliberately not divided into the per-session number, so the per-session gate (PRD-v2 16.1) measures the steady state.

**4.4.2 The weekly report.** `cost/weekly-report` runs Mondays 06:00 UTC (ADR-16: learners are in every timezone, so reports run at a fixed UTC time and session rows carry each learner's `local_date`) for the previous Monday-to-Sunday UTC week, writes Markdown to the ops channel (through the evaluation domain's `ops.notify`) and stores it at `cost_reports(week, body, csv)` for `/admin/cost`. Sections, in order, each a table:

1. **Headline:** sessions, mean cost per session, median, p90, against $0.60 and $1.00; the same four numbers for the previous week; the share of sessions over $1.00.
2. **By PRD line** (the lines of the mapping above plus acquisition, the proof per learner-week and fixed infrastructure as its own line, 01 §6): mean per session this week, last week, the estimate (section 6.1) and the delta.
3. **By role and vendor:** calls, errors, cost, units, cache hit rate, p95 latency, share of calls on batch, share escalated at a cut line.
4. **By episode kind:** daily, daily_extra, swap, return, pilot, fallback: count and mean cost.
5. **Heavy-use outliers** (4.4.3) with the per-plan guard trips.
6. **Vendor health:** failovers this week (`voice.vendor_failover`, STT secondary use), unpriced calls, stale and unverified prices, Langfuse sampling rate, `spool_recovered` rows, and **peak concurrency** (calls in the busiest hour, computed from `learner_schedule` for the coming week and from `calls` for the past one; the concurrency bought must be the measured peak plus 50%).
7. **Next week's prices:** from 2026-12-21, the headline recomputed with every `price_book` row whose `valid_from` is within 30 days (the 2027-01-01 doubling shows here on 12-21 and 12-28, before it lands in beta week 2).
8. **Reconciliation status** (hourly drift of `learner_spend_daily`, the one-off verification, and the monthly invoice check, 4.4.4).
9. **Margin by plan** (decisions.md §2, ADR-15): one row per plan with net price (list less the processor's measured fee and tax from the `vendor: payments` row; 15% until the row is real), learners on the plan, measured episodes used per learner-month (as a share of the allowance), measured cost per learner-month, margin at measured use, margin at full use, and the break-even cost per session at full use ($0.57 / $0.42 / $0.42 at a 15% deduction); then the `plan_mix` line (share of paying learners per plan) and the `blended_margin` line (net revenue less measured cost over all paying learners), which is the number the public-launch gate reads (concept-v2 §9: above about 50%). Both are also 09's measures of the same name and lines in the Tuesday review.

The query behind section 2, so Muath can run it by hand:

```sql
select line, round(avg((cost_by_line->>line)::numeric), 4) as mean_usd, count(*) as sessions
from session_costs, jsonb_object_keys(cost_by_line) as line
where local_date between $1 and $2 and episode_kind in ('daily','daily_extra','swap','return','fallback')
group by line order by mean_usd desc;
```

And the query behind section 9 (net price per plan from `plans.yaml` and the fee row, cost from the roll-up):

```sql
with m as (select plan, count(distinct learner_id) learners, sum(cost_usd) cost, sum(episodes) episodes
           from learner_costs_daily where day between $1 and $2 and not deleted_learner_bucket group by plan)
select plan, learners, round(cost / learners, 2) as cost_per_learner_period,
       round(1 - cost / (learners * net_price_for(plan, $1, $2)), 3) as margin_measured,
       round(episodes::numeric / (learners * episodes_per_day(plan) * ($2 - $1 + 1)), 3) as allowance_used
from m order by plan;
```

**4.4.3 Heavy-use outliers (PRD-v2 16.2).** A learner is flagged in the report when, over the trailing 7 days, any of: `cost_usd` above 3 times the median of learners on the same plan, minutes heard above 3 times that median, or any learner-local day above the plan's soft guard (2.5 × `episodes_per_day` × $0.60: $1.50, $3.00, $4.50; ADR-15). The flag goes to the report and to `/admin/cost` only. It triggers no message, no throttle and no change in the learner's allowance (law 11: what is already made can be heard as often as wanted; re-listens cost egress only, about $0.001 each). The one action it can lead to is a human reading the trace to check for a bug (a loop in the chat, a swap storm), because a heavy user in this product is a success, not a problem. The hard guard (4 × `episodes_per_day` × $0.60: $2.40, $4.80, $7.20) is a loop defence, not an outlier rule: it is 07's `costguard.check` returning `hard`, which pauses that learner's on-demand extras (swap, `daily_extra`, round two, chat replies) until the next `drop_at` with Salma's plain allowance sentence, never the drop, a call in progress, or the after-session evidence, and raises 09's `cost_runaway` (P1).

**4.4.4 Reconciliation.** Three clocks (D11). Hourly, `cost/reconcile-spend` recomputes `learner_spend_daily` from `vendor_calls` for every learner-local day still open and corrects any row that drifted (a spool ingested late, a row written after the counter); drift above $0.05 on any learner is a `notify`. Once, before `vendors.yaml` is committed: `vendor-lab verify-prices` (4.2). Monthly, `cost/reconcile-monthly` on the 2nd at 06:00 UTC: pulls the Anthropic Usage and Cost report for the organization through the Admin API (an admin key, `ANTHROPIC_ADMIN_API_KEY`, read-only, stored in Secrets Manager) and compares it to `sum(cost_usd) where vendor='anthropic'` by model; for Google, ElevenLabs, Inworld, Soniox, Deepgram, AssemblyAI, Speechace and LiveKit, reads a CSV Muath uploads at `/admin/cost/invoices` (vendor, period, usd) within 10 days of each invoice; for the payment processor, reads the fee and tax totals the same way into the `vendor: payments` row the margin section uses. Writes `vendor_invoices(vendor, period, invoiced_usd, traced_usd, variance_pct)`; variance above 5% raises a `cost.alarm_raised{kind: reconciliation}`. [ASSUMPTION] the Admin API's cost report groups by model and workspace, which is enough; per-key grouping is not needed because the beta runs one workspace per environment. Automating the other vendors' invoices is P1 or later; nine CSV uploads a month is cheaper than nine scrapers.

### 4.5 Alarms, the spend guard and the stop line

**4.5.1 Alarm catalog.** `cost/alarms` runs every 15 minutes; each alarm is an event `cost.alarm_raised {kind, severity, value, threshold, learner_id?, role?, vendor?}` consumed by the evaluation domain's paging (`ops.page` for `page`, `ops.notify` for `notify`). Every alarm is idempotent per (kind, subject, day).

| Kind | Condition | Severity | Config key (default) |
|---|---|---|---|
| `session_over_alert` | A `session_costs.cost_usd` crosses the alert line | notify | `SESSION_COST_ALERT_USD` (1.00, from 01) |
| `session_over_budget_trend` | Trailing 7-day mean per daily session above budget | notify (weekly repeat) | `cost.session_budget_usd` (0.60) |
| `session_warn_trend` | Trailing 7-day mean above the warning line | page (once a week) | `cost.session_warn_usd` (0.80) |
| `stop_line` | Trailing 7-day mean above the stop line, or 20% of sessions above it | P3 ticket plus notify to Muath (09's `cost_stop_line`); opens a 48-hour plan window (4.5.3); never a page, because a plan is not an outage | `cost.stop_line_usd` (1.00) |
| `daily_spend_80` | Environment spend in the UTC day above 80% of the daily cap | notify; `spend_mode` → `conserve` | `SPEND_CAP_USD_PER_DAY = max(50, Σ over learners with an active subscription or trial of plan.episodes_per_day × 1.00)`, recomputed daily from 2026-12-23 (ADR-15); the cap day is the UTC day |
| `daily_spend_100` | Spend above the cap | page (09's `cost_runaway`, P1); `spend_mode` → `halt` for new on-demand generation only | same |
| `kind_ceiling` | A sample episode over $0.05, a pilot over $0.40, a swap over $0.60 | notify | `cost.kind_ceilings` |
| `cache_hit_low` | A text role's `cache_read_tokens / (cache_read + input + cache_write)` under 85% over 24 h, at least 50 calls | notify | `cost.cache_hit_floor` (0.85) |
| `unpriced` | Any `error_code='unpriced'` row | notify | |
| `price_stale` | A price row older than 120 days used | notify (weekly) | |
| `escalation_rate` | More than 20% of daily episodes escalated from batch at a cut line in a day | notify | `cost.escalation_rate_max` (0.20) |
| `vendor_error_rate` | A vendor's error rate above 5% over 10 minutes (shared with `vendor/health`, 01) | page | |
| `learner_spend_soft` | A learner's local day above 2.5 × `episodes_per_day` × budget (07's `costguard.check` → `soft`) | notify (report only) | `cost.learner_soft_multiple` (2.5) × `plan.episodes_per_day` × `cost.session_budget_usd` |
| `learner_spend_hard` | A learner's local day above 4 × `episodes_per_day` × budget (`costguard.check` → `hard`; a loop, not a heavy user) | page (09's `cost_runaway`, P1); that learner's on-demand extras pause until the next `drop_at` (4.4.3) | `cost.learner_hard_multiple` (4) |
| `reconciliation` | Monthly variance above 5% | notify | `reconcile.variance_alert_pct` (5) |

**4.5.2 Spend modes.** `spend_mode` lives in `vendor_config` (`key='spend_mode'`), read by callers through `tracing.spend_mode()` (cached 60 seconds), set by `cost/alarms` and by hand from `/admin/vendors`. It returns to `normal` at 00:00 UTC, the start of the next cap day (with a worldwide cohort there is no other "next day"; ADR-16), unless an alarm holds it.

The rule (ADR-14, 09 D8): an automatic mode may change only what no learner hears. Model downgrades (`host.model=haiku`, `teacher.model=sonnet`) are feature flags in 09's flag table that a person flips after `eval-gate` passes on the comparison suite; `cost/alarms` can never flip them. The first draft's `conserve`, which swapped the teacher and the host for every learner when a busy day crossed 80% of the cap, is rejected: a busy day is the product working, and a quality change is a human decision (D6, 6.3 lever 6).

| Mode | Pipeline (02) | Call (03) | After-session (05) | Client-visible effect |
|---|---|---|---|---|
| `normal` | as designed | as designed | as designed | none |
| `conserve` | batch TTS forced where available (02 `voice.batch.enabled`); writer rewrites capped at 1 round (the fitter's own repair still runs); canary episodes and the nightly smoke (09) skipped; the research anonymizer run deferred to the next day; `prewrite_extra` and `prewrite_rank2` pre-writes skipped (the on-demand path still serves them); swap, return and `daily_extra` episodes still made | unchanged (no model change, no feature withheld) | unchanged (claims and evidence are never degraded for cost) | none, by construction |
| `halt` | tomorrow's drop episodes already queued finish; no new on-demand generation except return episodes (a returning learner must get a show, PRD-v2 3.8); `daily_extra` requests and swaps paused for the rest of the UTC day; the sample endpoint returns the cached sample with a plain "try again tomorrow" page (06 owns the copy) | calls continue (a learner mid-day is never cut off) | unchanged | a swap or "next one" request shows Salma's one plain allowance sentence (the ADR-04 wording of PRD-v2 3.6 #6: "That's all the new episodes for today...") and nothing else |

`halt` is for a runaway (a bug generating in a loop), not for budgeting; in five weeks of beta it should never fire. If it fires on a normal day, the cap is wrong and is raised. Pausing extras under the cap is the one learner-visible thing an automatic mode may do, and the ADR allows it because the allowance sentence already exists for the same case.

**4.5.3 The stop line (PRD-v2 1.4, 16.1).** The stop line is a rule about plans, not about service. When `stop_line` fires, Muath and the engineer get the ticket and the notification with the week's section-2 and section-9 tables attached. Within 48 hours Muath records a plan in `cost_reports` (`plan_text`, `plan_by`) naming which levers of section 6.3 are pulled and the expected per-session effect; the next weekly report prints the plan and the measured effect. If no plan is recorded within 48 hours, the alarm repeats daily. This is the "no costed plan to reduce it" condition made operational; the decision to stop and rethink stays with Muath, as PRD-v2 16.1 says.

### 4.6 Vendor tests as the language gate's checks (PRD-v2 14.4, 10.14; ADR-03)

The three tests are checks 1 (voices), 2 (learner speech to text) and 4 (the call) of concept-v2 §8's language gate, run per **target language** by `vendor-lab gate --target <lang>` (`forone.langgate`). They use the adapter package (so every render and transcription is also a `vendor_calls` row tagged `service='vendor-lab'`) and write CSV scoring sheets under `langgate/<target>/<date>/`. The decision rules are code (`vendor-lab decide`) so the winner is reproducible from the sheets. A target opens when its gate run passes; `packages/languages/<target>/gate.yaml` records the pass with the date and the winners, and the target-dependent roles of `vendors.yaml` (`episode_tts`, `call_tts`, `streaming_stt`, `verbatim_stt`, `pronunciation`) are keyed by target language in `packages/languages/<target>/vendors.yaml`. English is the pilot target and the only one whose gate must pass before the beta; its run uses the Milestone 0 pilot's clips and scripts between 2026-11-01 and 11-17, in parallel with Milestone 0 (ADR-07). Muath signs the result by committing `vendors.yaml` with the winners by 2026-11-17, before build week 1. Nothing in the procedure names a learner nationality: raters are 5 native speakers of the target plus 5 learners of it from anywhere, and the clips are real learners of the target whatever their own language.

The one place D9's "through the production adapters" bends: the gate for English runs before build week 1, so its renders go through the adapter package's first cut (vendor SDK, `usage_of`, the price lookup) rather than the finished middleware; the rows it writes are repriced by `cost/rollup --reprice` once the middleware lands, which is why `units` is raw.

**4.6.1 Voice blind test (14.4 #1; gate check 1), 2026-11-01 to 11-17.**

Materials: the Milestone 0 two-host sample script (05-prompts.md, 10 lines, about 650 characters) extended to 90 seconds with four more lines in the same register, in both accents of the target where the package defines two; three candidate voices per host per accent per vendor from the target package's voice pools (PRD-v2 7.1), rendered with the same speech rate (1.0) and no style tags. Salma's voice is not part of this test: it is one voice per **native** language, chosen when `packages/native/<lang>/` is built, by the same forced-choice form run with 5 native speakers of that language (for `native/ar` the question of a Gulf or a neutral educated voice is that package's question, not a beta-wide one).

```
vendor-lab gate --target en --checks voices --from m0/
vendor-lab tts render --script languages/en/tests/two-host-90s.{british,american}.txt \
    --vendors gemini,inworld,elevenlabs --voices-from languages/en/voices.yaml --rate 1.0 --out langgate/en/2026-11-05/tts/
vendor-lab tts sheet  --from langgate/en/2026-11-05/tts/ --raters 10 --design latin-square   # prints 10 playlists and the blank sheet
vendor-lab native voice --lang ar --script native/ar/tests/salma-20s.txt --vendors gemini,inworld,elevenlabs --out native/ar/voice-test/2026-11-05/   # the Salma choice, per native package
```

Technical gate, run first, automatic (a vendor that fails any row is excluded before anyone listens):

| Check | Gate | Why |
|---|---|---|
| Two-speaker or per-line rendering of a full scene | works | pipeline 4.8 |
| Word timestamps returned, or alignment cost booked | either | 02 D10 |
| Rate control between 0.85 and 1.0 | vendor or `atempo` | PRD-v2 5.1 |
| Render p95 for a 90-second scene | under 20 s | on-demand kinds, 02 4.13 |
| Streaming TTFB p95 (call voice) | under 300 ms | 03 D8 `tts_stream_tfb_gate_ms` |
| Concurrent streams on the tier we would buy | at least 20 at the first cohort; recomputed weekly from `learner_schedule` (4.9) | beta peak modelled at 15 concurrent calls for a one-timezone cohort; a worldwide cohort spreads it |
| Name respelling or phoneme tag accepted | one of them | 02 name pronunciation |
| Batch endpoint | noted, not gated | lever 6.3 #3 |
| Cost per 10 minutes of episode audio at list | printed | D5 |

Listening protocol: 10 raters (5 learners of the target language from anywhere, drawn from the Milestone 0 pool and the waitlist but not from the beta cohort, and 5 native speakers of the target, paid), each hears every vendor's rendering of one accent (the target's accents split evenly across raters) in a Latin-square order with vendor names hidden, on earphones, on a phone. Per rendering they answer: naturalness 1 to 5; "would you listen to this on your commute?" yes or no; for native raters, accent authenticity 1 to 5; one free-text line. Then one forced pairwise choice between each pair of vendors (3 pairs).

Scoring sheet columns (`tts-sheet.csv`): `target, rater_id, rater_group(learner|native), rater_native_language, accent, vendor_blind_code, voice_candidate, naturalness_1_5, commute_yes_no, accent_1_5, pairwise_wins, free_text`. `vendor-lab decide tts` computes per vendor: mean naturalness (both groups), commute-yes share, mean accent (native group), pairwise win rate, list cost per 10 minutes.

Decision rule (D5, PRD-v2 14.5 "the cheapest voice that passes"): a vendor passes if commute-yes is at least 60% and its mean naturalness is within 0.3 of the best vendor's. Among passing vendors the cheapest at list price wins; the next cheapest passing vendor is the runner-up and provides the understudy voices (02 D9); if only one passes, the runner-up is the best non-passing vendor and the on-air announcement text for a failover is written to say the voice is temporary. If ElevenLabs is the only passing vendor, the win is conditional on a negotiated rate at or below $25 per million characters by 2026-11-24 (one week after the decision) [OPEN for Muath, 10-decision-records §10 item 5]; until then Gemini (the cheapest) is configured as primary and ElevenLabs as runner-up. Salma's voice per native language is chosen by the forced choice (majority of 5 native speakers) when that native package is built; for `native/ar`, ties go to a neutral educated voice because it ages better across regions (PRD-v2 19.4).

**4.6.2 Call latency (14.4 #3; gate check 4).** Owned by the call domain's `tools/call-bench` (03; ADR-19 names it the one load and latency tool). This domain adds two columns to its report, read from `vendor_calls`: cost per call by line, and the cache hit rate of the host role across the 50 calls (gate: at least 90%, since every turn after the first should read the cached brief). A run whose host cache hit rate is under 90% fails the cost gate even if latency passes, because the $0.034 host input line in 03's estimate assumes it. The 50 calls run on staging during the gate (English, by 11-17) and again in build week 4 on the full stack, when the Haiku-host comparison (lever 6) runs inside them.

**4.6.3 The recognizer test (10.14; gate check 2), during Milestone 0 (deadline 2026-11-10).**

Materials from Milestone 0 (PRD-v2 19.1 #7): 30 clips of real learners of the target language, 20 to 90 seconds each, with consent (10-decision-records §10 item 13), chosen to cover at least 10 clips with mid-clause pauses over 1.5 s, at least 8 with code-switching into the learner's own language (whatever it is; the pilot's learners are Arabic speakers, so the English run's clips switch into Arabic), at least 5 with fillers and restarts, and the rest ordinary turns. Ground truth per clip, hand-made by Muath or a native reader of the learner's language: a verbatim human transcript (fillers kept), the list of learner errors with their exact span (from the Milestone 0 tags), the filler spans, the own-language spans.

```
vendor-lab gate --target en --checks recognizers --clips m0/clips/ --truth m0/truth.jsonl \
    --streaming soniox,deepgram,assemblyai --batch assemblyai,elevenlabs_scribe \
    --out langgate/en/2026-11-06/stt/
vendor-lab stt decide --from langgate/en/2026-11-06/stt/
```

Per clip and vendor the runner records (`stt-sheet.csv`): `clip_id, vendor, mode(streaming|batch), wer_vs_human, errors_total, errors_survived, errors_corrected_silently, fillers_total, fillers_kept, hallucinated_phrases, hallucinated_near_pause, code_switch_words_total, code_switch_words_correct_language, word_timings(bool), confidences(bool), streaming_final_latency_ms, cost_usd`. "Survived" means the learner's error appears verbatim in the transcript; "corrected silently" means the transcript shows the correct form where the learner was wrong (the failure mode the voice lens warned about). Hallucination near a pause is a phrase in the transcript with no counterpart in the human transcript, inside or right after a pause over 1.5 s.

Decision rules:
- **Batch verbatim winner:** highest mean error survival rate among vendors with filler retention at least 80% and at most 1 hallucinated phrase per 30 clips; ties broken by cost. Minimum to be usable at all: error survival at least 85%; if no vendor reaches it, the assessment domain's confidence filter must be stricter and the claim gate stays on first-ever events and words owned until a second test (PRD-v2 10.10 already allows this).
- **Streaming winner:** lowest WER with code-switch words in the correct language at least 80% and final-after-end-of-speech p95 under 400 ms (03's STT budget); ties by cost. The talkback stream (`talkback_stt`) can use a different vendor from the host stream if code-switch handling differs; its language hint is set per call from the learner row, `languages: [learner.native_language, learner.target_language]` (ADR-02).
- **Confidence threshold** (PRD-v2 10.2 #4, Part 18 #10): on the batch winner, sort every tagged error by the recognizer's mean word confidence over its span and find the lowest threshold at which the precision of "a transcribed deviation is a real learner error" reaches 0.8; written to `packages/languages/<target>/recognizer.yaml` (`languages/en/recognizer.yaml` for the pilot) as `confidence_threshold` with the test date. The streaming winner's threshold is computed the same way but used only for planning signals.
- The recognizer error by first language (PRD-v2 10.14 last sentence) starts here: the clips' WER by vendor and by the learner's `native_language` is the day-one baseline the evaluation domain tracks; a second target language re-runs the whole check with its own clips.

### 4.7 Adapter interfaces and the fallback order

The interfaces are the topology's (01, 4.5: `TextModel`, `BatchTextModel`, `SpeechSynth`, `StreamingSpeechSynth`, `StreamingRecognizer`, `VerbatimRecognizer`, `Pronunciation`, `Aligner`, `Embeddings`) and the pipeline's `TtsAdapter` capabilities (02, 4.8). This domain adds what the middleware needs from every adapter and the fallback semantics in `vendors.yaml`.

```python
# packages/adapters/forone/adapters/base.py
class Adapter(Protocol):
    vendor: str
    capability: str
    def usage_of(self, raw_response) -> UnitUsage: ...          # the vendor's own counts; never estimated when the vendor reports
    def price_model_id(self) -> str: ...                         # the price_book.model this adapter bills under
    async def health(self) -> HealthResult: ...                  # ok, p95_ms, concurrency_remaining if the vendor reports it
    def is_retryable(self, exc: Exception) -> bool: ...          # 429, 5xx, timeouts: yes; 4xx validation: no

@dataclass(frozen=True)
class FallbackStep:
    vendor: str; model: str | None; pricing_mode: str; note: str | None   # note is logged, e.g. "breaks second-vendor rule"

# vendors.yaml semantics (additions to 01 and 03):
#   fallback: a list of FallbackStep tried in order after `retries` retryable failures on the primary;
#   `degrade: <name>` names the code path when every step fails (owned by the calling domain);
#   `pricing_escalation: [batch, standard]` for batch roles (02's cut lines drive it, the middleware records it).
```

The middleware's retry policy is the same for every capability: up to `retries` (default 2) on retryable errors with exponential backoff capped at the role's `timeout_ms`, then the fallback chain, each step with 1 retry; every attempt is a `vendor_calls` row (`outcome='error'` or `'fallback_used'`); the live path uses `retries: 0` and goes straight to the chain, because a retry costs latency.

```yaml
# packages/adapters/vendors.yaml (this domain's view of every role's chain; models as 01 and 03 spell them).
# Roles whose winner depends on the target language (episode_tts, call_tts, streaming_stt, talkback_stt, verbatim_stt, relisten_stt,
# pronunciation) resolve their VOICE_*, STREAM_* and VERBATIM_* placeholders from packages/languages/<target>/vendors.yaml (ADR-03);
# SALMA_* resolve from packages/native/<lang>/voice.yaml (ADR-02). The learner row supplies both languages per call.
roles:
  teacher:          {vendor: anthropic, model: claude-opus-5-5,   pricing: batch, pricing_escalation: [batch, standard],
                     fallback: [{vendor: anthropic, model: claude-sonnet-5-5, pricing: standard}], degrade: rule_based_brief}        # PRD 9.8
  writer:           {vendor: anthropic, model: claude-sonnet-5-5, pricing: batch, pricing_escalation: [batch, standard],
                     fallback: [{vendor: google, model: gemini-3.8-flash, pricing: standard, note: "editor must switch to anthropic"}], degrade: fallback_episode}   # PRD 6.3
  fitter:           {vendor: anthropic, model: claude-haiku-5-5, fallback: [{vendor: google, model: gemini-3.8-flash}], degrade: code_only_coverage}
  gloss:            {vendor: anthropic, model: claude-haiku-5-5, fallback: [{vendor: google, model: gemini-3.8-flash}], degrade: ship_without_gloss_mark_miss}
  editor:           {vendor: google, model: gemini-3.8-flash, fallback: [{vendor: anthropic, model: claude-opus-5-5, pricing: standard, note: "same_vendor_edit: breaks the second-vendor rule; review item"}], degrade: never}   # ADR-11: the fallback editor must be at least as strong as the writer; code checks alone are not an editor
  embeddings:       {vendor: google, model: gemini-embedding, fallback: [], degrade: skip_similarity_check_review_item}   # ADR-10: no OpenAI processor
  episode_tts:      {vendor: VOICE_WINNER, fallback: [{vendor: VOICE_RUNNER_UP, note: "understudy voice; on-air announcement"}], degrade: wait_and_retry_until_t_switch_then_yesterday_stays}
  aligner:          {vendor: elevenlabs_alignment, fallback: [{vendor: whisperx_local}], degrade: sentence_level_timings}
  relisten_stt:     {vendor: VERBATIM_WINNER, fallback: [{vendor: VERBATIM_RUNNER_UP}], degrade: ship_unchecked_mark_review}
  host:             {vendor: anthropic, model: claude-sonnet-5-5, retries: 0,
                     fallback: [{vendor: anthropic, model: claude-haiku-5-5}, {vendor: google, model: gemini-3.8-flash}], degrade: voice_notes}   # PRD 5.4.10
  call_tts:         {vendor: VOICE_WINNER, retries: 0, fallback: [{vendor: VOICE_RUNNER_UP, note: "understudy"}], degrade: voice_notes}
  salma_tts:        {vendor: SALMA_WINNER, fallback: [{vendor: SALMA_RUNNER_UP}], degrade: text_bubble_only}
  streaming_stt:    {vendor: STREAM_WINNER, retries: 0, fallback: [{vendor: STREAM_RUNNER_UP}], degrade: voice_notes}
  talkback_stt:     {vendor: STREAM_WINNER, languages: [learner.native_language, learner.target_language], code_switch: true, fallback: [{vendor: STREAM_RUNNER_UP}], degrade: talkback_unavailable_bubble}   # set per call from the learner row (ADR-02)
  talkback_resolver:{vendor: anthropic, model: claude-haiku-5-5, retries: 0, fallback: [], degrade: cache_only}
  salma_live:       {vendor: anthropic, model: claude-sonnet-5-5, retries: 0, fallback: [{vendor: anthropic, model: claude-haiku-5-5}], degrade: typed_intake}
  verbatim_stt:     {vendor: VERBATIM_WINNER, fallback: [{vendor: VERBATIM_RUNNER_UP}], degrade: low_confidence_no_claims}   # PRD 5.4.11
  pronunciation:    {vendor: speechace, fallback: [{vendor: microsoft}], degrade: score_null}
  analyst:          {vendor: anthropic, model: claude-haiku-5-5, fallback: [{vendor: google, model: gemini-3.8-flash}], degrade: claims_withheld_retry_later}
  memory_keeper:    {vendor: anthropic, model: claude-haiku-5-5, fallback: [{vendor: google, model: gemini-3.8-flash}], degrade: retry_next_pass}
  salma_explain:    {vendor: anthropic, model: claude-sonnet-5-5, fallback: [{vendor: anthropic, model: claude-haiku-5-5}], degrade: explanation_unavailable_bubble}   # on demand only (ADR-06); replaces the first draft's salma_text notes role
  chat_host:        {vendor: anthropic, model: claude-sonnet-5-5, fallback: [{vendor: anthropic, model: claude-haiku-5-5}], degrade: opener_only_then_quiet}
  proof_producer:   {vendor: anthropic, model: claude-sonnet-5-5, pricing: batch, fallback: [{vendor: anthropic, model: claude-sonnet-5-5, pricing: standard}], degrade: slow_week_template}
  rater:            {vendor: anthropic, model: claude-sonnet-5-5, pinned_until: 2027-02-16, fallback: [], degrade: code_metrics_only}   # PRD 10.11; 05 4.15 sets the first window 2026-12-23 to 2027-02-16
```

Three rules the middleware enforces regardless of the file: a `pinned_until` role refuses any fallback or `vendor_config` override while pinned (05); the writer and editor may not resolve to the same vendor in one run unless the row carries a `note` (PRD-v2 6.1), in which case the middleware tags the episode `review_items(kind='same_vendor_edit')` for the human reviewer (the Opus fallback day costs about $0.05 more a session, section 5); and a `model` override of `host` or `teacher` is accepted only from 09's feature-flag table with a `flipped_by` person and a passing `eval-gate` run id, never from `cost/alarms` (ADR-14).

### 4.8 Vendor risk calendar

| Date | Event | Exposure | Action and owner |
|---|---|---|---|
| 2026-10-12 | ElevenLabs v4 launch promotion ended | List price $80 per million characters applies to any ElevenLabs render | `prices.yaml` carries the list price; D5 rule |
| 2026-11-01 | English language gate run starts (ADR-03), in parallel with Milestone 0 | The vendor-test consent addendum must be in place before any clip leaves (10-decision-records §10 item 13) | `vendor-lab gate --target en` on the pilot's clips and scripts |
| 2026-11-10 | 10.14 recognizer test deadline (during Milestone 0, ADR-07) | Verbatim and streaming winners unknown until then | `vendor-lab gate --checks recognizers`; Muath's truth file by 2026-11-06 |
| 2026-11-13 | Hume shuts its voice APIs | None if nothing imports Hume | CI check: no `hume` dependency in the lockfile; `vendors.yaml` schema rejects `vendor: hume` |
| 2026-11-17 | Voice vendor decision (14.4) due; `vendors.yaml` committed before build week 1 | The $0.18 voice line and the $0.03 to $0.08 call voice line | `vendors.yaml` committed with winners; paid tier bought for the winner only (D10); `verify-prices` run the same day (D11) |
| 2026-11-17 | Google shuts older Cloud speech models | None (Gemini 3.8 Flash TTS is not among them) [ASSUMPTION; verify during the gate run] | Check in `vendor-lab tts` against the deprecations page |
| 2026-11-24 | ElevenLabs negotiated-rate deadline if it won the blind test | Whether ElevenLabs can be primary | [OPEN for Muath, 10-decision-records §10 item 5] |
| 2026-12-02 | Payment processor decision (ADR-21; start of build week 3) | Processor fees (Paddle as merchant of record about 5% with tax handled; Stripe with Stripe Tax about 3% plus registrations) are outside the AI cost but in the margin section | The real fee row replaces the `vendor: payments` assumption rows in `prices.yaml`; the margin section reads it |
| 2026-12-21 | Weekly report prints next-week prices for the first time; freeze starts 12:00 UTC (to 12-24 12:00 UTC) | First sight of the 2027-01-01 jump | Report section 7 |
| 2026-12-23 | Beta starts, first cohort; daily spend cap recomputed from the plan mix | Cap too low halts; too high hides a loop | `SPEND_CAP_USD_PER_DAY = max(50, Σ plan.episodes_per_day × 1.00)` over active learners (ADR-15) |
| 2026-12-28 | Weekly report prints next-week prices again | The jump is four days away | Report section 7 |
| 2026-12-31 | Second freeze 12-31 to 2027-01-02 | No vendor change during the freeze | None |
| 2027-02-16 | First rater window ends (05 4.15) | Re-pin for the next 4-week window (PRD-v2 10.11) | Assessment domain updates `pinned_until`; calibration set re-run |
| 2027-01-01 | Gemini 3.8 prices double (Flash text, Flash TTS; Live), in beta week 2 | Editor +$0.015 a session; a Gemini-voiced session +$0.17 (episode voice +$0.135, call voice +$0.032) | Second dated rows already in `prices.yaml`; the costed path (6.4) treats post-doubling prices as the base case; the January voice plan (6.1 note 3) is executed in the first release after 2027-01-02 |
| 2027-01-06 | OpenAI deprecates its text-to-speech models | None (no OpenAI processor after ADR-10) | Note only |
| 2027-01-26 | Beta gate review | Cost gate: under $0.60; stop over $1.00 with no plan; blended margin against the public-launch gate | Report of 2027-01-25 is the gate evidence |
| Open-ended | Deepgram's promotional rate ends; Inworld pricing is young; Anthropic Haiku 5.5 tier above 100K-token prompts | Streaming STT, voice, and any prompt that grows past 100K tokens (the teacher brief must stay under it) | `price_stale` alarm after 120 days; `cache_hit_low` and a per-role input-token p95 in the report |

### 4.9 Contracts and quotas at 100 and 10,000 learners

Volumes assume the plans of ADR-04 at concept-v2 §8's typical usage (60%, 50% and 45% of the allowance) and a 50/50/0 mix of `one_a_day` and `two_a_day` learners: about 24 sessions a learner a month on average, so **about 2,400 to 3,000 sessions a month at 100 learners** (3,000 if everyone is on `two_a_day`) and **240,000 to 300,000 at 10,000**; the full-use upper bound (everyone on `three_a_day` using every episode) is 9,000 and 900,000, and every quota below must be checked against the measured plan mix in the weekly report rather than this assumption. Each session is one 6:30 call, a 6-minute episode plus 2.5 minutes of read-aloud and 1.5 of recap (10 minutes of produced audio), and 7 minutes of learner audio re-transcribed. Peak concurrency: the first draft assumed anchors clustering in one timezone so that 15% of the day's calls fell in one hour; a worldwide cohort spreads them, so the peak is **computed weekly from `learner_schedule`** (calls expected per UTC hour next week) and printed in the report's vendor section, and the concurrency bought is the measured peak plus 50%. The table keeps 15% as the planning figure until the first cohort exists.

| Vendor | Unit | 100 learners (about 3,000 sessions/month) | 10,000 learners (about 300,000 sessions/month) | What to ask for |
|---|---|---|---|---|
| Anthropic | Tokens a day (all roles, cached reads included) | about 25M | about 2.5B; batch about 40% of it | Beta: usage tier with 1M-token-a-minute Sonnet limits (self-serve); a prepaid balance of about $2,500 for the beta's first month at the upper plans' usage (10-decision-records §10 item 9). Scale: a committed-spend agreement, higher Batch API queue limits, and a workspace per environment; about $75,000 a month of text at the floor stack |
| Voice vendor (winner) | Characters a month (episodes, read-aloud, recap, proof, call host turns) | about 30M | about 3B | Beta: the paid API tier that gives 20 concurrent streams (ElevenLabs Business or Inworld paid; Gemini paid tier with a TTS requests-per-minute quota raise). Scale: enterprise contract with a per-million-character rate; the voice line is the biggest negotiable line |
| Voice vendor (runner-up) | Same, only on failover and canaries | under 1M | about 75M (canaries plus failover days) | Pay-as-you-go; one weekly canary keeps the account live |
| Streaming STT | Concurrent streams at peak; minutes a month | 15 concurrent planning figure, recomputed from `learner_schedule`; about 24,000 min (two streams per call) | about 900 concurrent at the one-timezone figure, fewer spread worldwide; 2.4M min | Beta: a concurrency raise to 50 during the gate run (03). Scale: contract with concurrency sized to the measured peak plus 50% |
| Verbatim STT | Minutes a month | 21,000 (calls) + 30,000 (re-listen) | 5.1M | Scale: volume pricing below $0.003 a minute |
| Pronunciation | Utterances a month | 3,000 to 9,000 | 300,000 to 900,000 | Speechace plan sized to utterances; Microsoft as the secondary needs an Azure Speech resource in the home region (`HOME_REGION`, default `eu-central-1`, ADR-08) |
| LiveKit Cloud | Participant minutes a month | about 42,000 | about 4.2M | Beta: Ship plan. Scale: enterprise; the per-minute rate is the largest infrastructure line (01) |
| Langfuse | Observations a day | about 6,000 (metadata-only spans) | about 150,000 after sampling | Beta: Core. Scale: Pro or Team, or self-host |
| Inngest | Steps a day | about 7,500 | about 750,000 | Beta: free or Pro. Scale: verify tier pricing; 01 names the switch rule (above $0.01 a session) |
| Alignment (always with Gemini TTS; Inworld only if its timestamps fail) | Minutes a month | 30,000 | 3M | Scale: a self-hosted aligner on one GPU task is cheaper than $0.0037 a minute above about 300,000 minutes a month (P1 or later) |
| Payment processor | Subscriptions billed a month | 100 to 120 | 10,000 to 12,000 | Outside this document except the fee row; a merchant of record also remits the tax (ADR-21) |

Quotas to request during the gate run and build week 1 (so no test or canary is throttled): Anthropic rate tier for 1M tokens a minute on Sonnet and 200K on Opus and the Batch API enabled; the voice finalists' 20-stream concurrency; Soniox and Deepgram 50 concurrent streams; AssemblyAI 50 concurrent batch jobs; Speechace a developer plan; LiveKit Ship.

---

## 5. Failure modes, fallbacks and degraded modes

| Failure | Detection | Automatic response | What the learner notices | What this domain records |
|---|---|---|---|---|
| Vendor rejects or times out (any role) | middleware retry exhaustion | fallback chain (4.7), then the calling domain's `degrade` path | nothing, or the degraded surface that domain specifies | rows with `outcome='error'` then `'fallback_used'`; `vendor_error_rate` alarm at 5% |
| Both voice vendors down at production time | `episode_tts` chain exhausted | retry every 5 minutes until `t_switch` (02); then the pipeline marks the run failed and yesterday's episode stays (PRD-v2 3.6 #2 behaviour reused); `pipeline.human_page` | no new episode today; no notification | `escalation_rate` and `vendor_error_rate` alarms |
| Batch not back by a cut line | 02's poll loop | cancel and run standard; `pricing_escalated=true` | nothing | `escalation_rate` alarm if above 20% of the day; the saving lost is printed in the report |
| A price row missing for a new model or voice | `unpriced` rows | priced at zero, alarm | nothing | report line until `prices.yaml` is fixed and `cost/rollup --reprice --since` is run (re-prices rows from `units`, the reason `units` is raw) |
| Prompt cache silently broken (timestamp in a prefix, tool list reordered) | `cache_hit_low` | alarm with the role and the first hour it fell | nothing | the cost of the breakage computed as (expected cache reads × (input price − cache price)) |
| Spend loop (a bug re-running a step) | `learner_spend_hard` for one learner; `daily_spend_80` then `_100` for the environment | the learner's extras pause until the next drop; `conserve` then `halt`; `cost_runaway` page | at most: no swap or "next one" today, with the allowance sentence | spend mode changes as `cost.spend_mode_changed`; the idempotent insert means the retried step is counted once, not per attempt |
| A step's transaction rolls back after the vendor was paid (Inngest retry after a timeout, a validation failure, a crashed task) | the `vendor_calls` row exists, the `pipeline_steps` row does not | nothing to do: the row was written in its own transaction before the step's write (ADR-13); the retry's row is a no-op on the idempotency key | nothing | the row's `attempt`; a `retries_paid` count in the report, the honest measure of a retry storm |
| Postgres write of `vendor_calls` fails in the live path, or the worker task dies mid-call | buffered writer error; a spool object with no matching rows | each turn's rows are already in the per-call S3 spool object (`spool/calls/{call_id}.ndjson`, written before the 5-second flush); `cost/rollup` ingests the spool and upserts `learner_spend_daily` | nothing | a `spool_recovered` count in the report |
| Editor fallback day (Gemini down; the editor runs on `claude-opus-5-5`, ADR-11) | `fallback_used` rows on `editor` | the episode is tagged `review_items(kind='same_vendor_edit')` | nothing | about $0.05 a session more that day (9k in, 1.5k out at Opus standard: $0.036 + $0.030, less the Gemini $0.015) |
| Langfuse unreachable | SDK async queue errors | observations dropped after the queue fills (the SDK is fire-and-forget); `vendor_calls` is unaffected | nothing | `langfuse_dropped` count; the trace is reconstructable from `vendor_calls` plus the artifacts the pipeline stored |
| Langfuse deletion API fails for a deleted learner | `deletion_ledger.verified_empty=false` (04) | daily retry 30 days; alert | nothing | the call is by pseudonym and the processor holds only anonymized text, so the "deleted" email does not wait for it (ADR-09 closes 04 §10's question) |
| Reconciliation variance above 5% | `cost/reconcile-monthly` | alarm; the report names the vendor and the month | nothing | `vendor_invoices` row |
| Vendor announces a price change | a person reads it | a dated row in `prices.yaml` through a pull request; the weekly report's section 7 shows the effect before it lands | nothing | |
| A new learner cohort is heavier than modelled (more talk, longer calls) | `session_over_budget_trend` | nothing automatic; the levers in 6.3 are human decisions | nothing | the report shows which line moved |

The principle, repeated from 01: no learner ever sees a cost error. The cost domain degrades the product's own spending, never the learner's day.

---

## 6. Cost and performance against the budgets

### 6.1 The itemized model, beta stack, list prices

Unit assumptions behind every line (each is an `assumptions.yaml` key so Muath can recompute; section 6.6). The generation lines are 02 §6's unit table as revised on 2026-10-17, which this document re-adopts as 02 §9.7 asked (writer 9k output, alignment always with Gemini, the pre-write and idea-refresh lines, cached and uncached columns, 1-hour cache writes at 2x input):

- Episode 6:00 min, article read-aloud 2:30, recap 1:30; 830 characters per minute of speech; 10 minutes of produced audio = 8,300 characters = 15,000 Gemini audio tokens (25 a second).
- Teacher (one nightly call that plans all of the day's 1 to 3 episodes, ADR-05): 16,000 input tokens (7,000 cache reads, 9,000 uncached), 6,000 output tokens including thinking at effort `medium`; the 1-hour cache write of the 7,000-token pooled prefix (02 D5) is amortized over about 10 learners per pool. Writer: 13,000 input (7,000 cached), 9,000 output including thinking (the package JSON alone is 5 to 7k); rewrites 1.3 rounds of 9,000 input (7,000 cached) and 1,200 output at standard pricing. Fitter, gloss misses and moderation: 8,000 in, 3,000 out on Haiku. Editor: 1.2 calls of 9,000 in, 1,500 out on Gemini Flash. Embedding: 1,500 tokens on Google's model. Alignment: always paid with Gemini TTS (10 minutes); with Inworld only if its word timestamps fail the gate.
- Pipeline side lines (02 §6): idea refresh (Sonnet, about 30% of nights, $0.003), the `prewrite_rank2` swap pre-write allowance (20% of learners × $0.07 = $0.014), batch escalations (about 4% of runs × $0.08 = $0.003). `prewrite_extra` (ADR-05) is inside the `daily_extra` arithmetic of section 6.5, not here.
- Call (03, section 6): 6:30 main call; 25 learner turns; host share 35% (1,900 characters); host cached reads 90,000 tokens, 5-minute cache writes 4,000, uncached 3,000, output 1,500; 3 talkback asks; Soniox for 7 minutes on two streams; LiveKit 2 participants × 7 minutes. `call.minutes` and `call.learner_turns` are replaced by the pilot's measured minutes of learner speech per call and turns per call when `tools/m0_import.py` runs (section 7): those two numbers move the call and verbatim lines more than any price.
- Round two [P1]: 2.5 minutes, used after 50% of sessions [ASSUMPTION].
- Verbatim: 7 minutes of learner audio; one pronunciation utterance.
- Salma when asked and chat (05 and 03; ADR-06): `salma_explain` on demand, assumed 0.3 calls a session of 3,000 in (2,000 cached), 400 out on Sonnet [ASSUMPTION]; chat host 5 messages of 4,000 in (3,000 cached), 150 out on Sonnet. No notes, polish lines or margin notes (decisions.md §3).
- Analyst and memory keeper (05): $0.0035 of Haiku plus $0.0005 of embeddings plus the rater amortized.
- Proof (05): $0.06 a learner-week, a line of its own in the report; divided here by 4 sessions a week (the `one_a_day` typical case) only to show a per-session figure; hosting (06): $0.006 egress (presigned S3 for show audio, ADR-12) and feed encode.
- Swap: 5% of sessions have a swap at standard pricing, about $0.55 each per 02 §6 [ASSUMPTION; 02 assumed 20% of learners, which is the same order].

Arithmetic (standard rate unless noted; batch = half; the batch pipeline's cache writes at the 1-hour rate):

| Line | Arithmetic | Gemini voice | Inworld voice | ElevenLabs v4 list | PRD-v2 14.5 |
|---|---|---|---|---|---|
| Teacher (Opus 5.5, batch, prefix cached) | standard: 9k × $4 + 7k × $0.20 + (7k × $8) ÷ 10 + 6k × $20 per M = $0.036 + $0.0014 + $0.0056 + $0.12 = $0.163; batch ÷ 2 (02 §6: $0.082 cached, $0.092 uncached) | $0.082 | $0.082 | $0.082 | $0.08 |
| Writer (Sonnet 5.5, batch, prefix cached) + rewrites (standard) | standard: 6k × $2 + 7k × $0.20 + (7k × $4) ÷ 10 + 9k × $10 = $0.012 + $0.0014 + $0.0028 + $0.09 = $0.106; batch ÷ 2 = $0.052 (02 §6; uncached $0.058); rewrites 1.3 × (2k × $2 + 7k × $0.20 + 1.2k × $10) = 1.3 × $0.0174 = $0.023 | $0.075 | $0.075 | $0.075 | $0.07 |
| Fitter, glosses, editor, embedding | Haiku 8k × $0.10 + 3k × $0.50 = $0.0023 plus moderation = $0.003; Gemini 1.2 × (9k × $0.75 + 1.5k × $3.75) = 1.2 × $0.0124 = $0.015; Google embedding under $0.001 | $0.018 | $0.018 | $0.018 | $0.03 |
| Voice studio: episode, read-aloud, recap | Gemini: 15,000 tokens × $9/M = $0.135 + alignment 10 min = $0.040 (always); Inworld: 8,300 × $25/M = $0.208, timestamps included [unverified until the gate; +$0.040 if they fail]; ElevenLabs: 8,300 × $80/M = $0.664; plus re-listen 10 min × $0.004 = $0.040 and mix under $0.005 for all | $0.220 (batch TTS: $0.153) | $0.253 | $0.709 | $0.18 |
| Pipeline side lines | idea refresh $0.003 + pre-write allowance $0.014 + batch escalations $0.003 | $0.020 | $0.020 | $0.020 | (not itemized) |
| Call, main | STT 7 min × $0.002 × 2 streams = $0.015 (talkback stream rounded in); host Sonnet 90k × $0.20 + 4k × $2.50 (5-minute writes) + 3k × $2 + 1.5k × $10 per M = $0.018 + $0.010 + $0.006 + $0.015 = $0.049, re-requests $0.002; call TTS 1,900 chars: Gemini 3,500 tokens × $9/M = $0.032, Inworld Flash × $15/M = $0.029, ElevenLabs Flash × $40/M = $0.076; talkback resolver $0.001; Salma TTS $0.005; LiveKit 14 min × $0.001 = $0.014; worker compute $0.004 | $0.122 | $0.119 | $0.166 | $0.16 (with round two) |
| Round two [P1], 50% uptake | about $0.05 × 0.5 | $0.025 | $0.025 | $0.025 | (in the line above) |
| Re-transcription and pronunciation | 7 min × $0.004 = $0.028; Speechace $0.008 | $0.036 | $0.036 | $0.036 | $0.03 |
| Salma (when asked) and chat | `salma_explain` 0.3 × (1k × $2 + 2k × $0.20 + 0.4k × $10 = $0.0064) = $0.002; chat 5 × (1k × $2 + 3k × $0.20 + 150 × $10) = 5 × $0.0041 = $0.021 | $0.023 | $0.023 | $0.023 | $0.04 (notes and chat; the notes part is removed) |
| Analyst and memory keeper | $0.0035 + $0.0005 + $0.001 | $0.005 | $0.005 | $0.005 | $0.04 |
| Proof (per learner-week, shown ÷ 4) and hosting | $0.06 ÷ 4 = $0.015; hosting $0.006 | $0.021 | $0.021 | $0.021 | $0.03 |
| Swap allowance | 5% × $0.55 | $0.025 | $0.025 | $0.025 | (not itemized) |
| **Per session, standard TTS** | | **$0.672** | **$0.702** | **$1.205** | **$0.66** ($0.62 without the notes line) |
| **With batch TTS where offered** (P1) | Gemini only | **$0.605** | $0.702 | $1.205 | |
| **After 2027-01-01** (Gemini text and TTS doubled, standard TTS) | editor +$0.015; Gemini voice +$0.135 episode, +$0.032 call | **$0.854** | **$0.717** | **$1.220** | |

What the table says:

1. The generation lines (teacher, writer, fitter, voice studio, side lines) sum to $0.415 on the Gemini stack, which reproduces 02 §6's "batch, prefix cached" column ($0.42) to the cent; this document's numbers are now 02's. Against the PRD's $0.66 the session is $0.01 to $0.04 over before levers: the voice studio line is $0.04 to $0.07 over the PRD's $0.18 because the PRD line was priced before read-aloud, recap and alignment were added (02 noted the same), the writer carries 9k output tokens, and the side lines are new; the analyst line is $0.035 under and the notes line is gone. The first draft's $0.638 was built from 02's first-draft units and is superseded.
2. ElevenLabs at list price cannot be the beta voice: $1.21 a session is over the stop line before any lever. At v4 Turbo ($40 per million characters) the session is $0.87; at a negotiated $25 it is $0.70, the same as Inworld. Hence D5.
3. The Gemini stack is cheapest until 2027-01-01 and the most expensive of the two viable stacks after it ($0.85 against $0.72), and the doubling now lands in beta week 2 (ADR-07), not week 4. If Gemini wins the blind test, the runner-up must be Inworld and the January plan is a vendor swap for the episode voice with the on-air announcement (PRD-v2 7.1 #3) in the first release after 2027-01-02, or a negotiated Google rate [OPEN for Muath, 10-decision-records §10 item 5].
4. Fixed infrastructure (01 §6 as revised) is on top of these numbers and printed as its own line: about $2.30 to $2.80 a session at 15 learners (300 sessions a month); $0.33 to $0.43 at 100 learners (01's $0.35 to $0.43 was on 2,000 sessions; on the plans' 2,400 to 3,000 sessions the share is a little lower, and staging kept up through the beta adds about $180 a month, ADR-16); $0.14 to $0.17 at 250 (the run-rate figure printed beside the 16.1 number); $0.03 to $0.05 at 10,000. The fixed budget is about $1,000 to $1,300 a month with staging up (01's $800 to $1,100 plus the $180; 10-decision-records §10 item 9), not the $400 to $600 the first draft was written against. At the upper plans' usage the per-session share falls faster than the learner count suggests (at 100 learners all on `three_a_day` at full use, 9,000 sessions, it is $0.11 to $0.14), which section 6.5 shows. The PRD's "hosting" sits inside its $0.03 line only at scale; in the beta the fixed cost is the research budget the business lens priced at about $2,000 a month.

### 6.2 Where the money goes and what the learner's behaviour does to it

On the Inworld stack: voice studio 36%, call and round two 21%, teacher and writer 22%, everything else 21%. The lines that move with behaviour: the call and the verbatim lines grow with learner talk (the goal: every extra minute of learner speech costs about $0.006 of STT and verbatim and nothing else); the voice studio grows with episode length (about $0.03 a minute on Inworld, $0.017 on Gemini); chat grows with messages (capped at 5 host messages, PRD-v2 5.6); swaps and round two grow with uptake; and, new with the plans, **the number of episodes a learner asks for in a day** moves the whole session cost by a factor of one to three (section 6.5), the largest behavioural lever in the product. The lines that do not move with a learner's day: teacher (one nightly call plans all of the day's episodes), editor, analyst, proof. A learner who re-listens ten times a day costs $0.01 more than one who listens once (egress), which is the design intent of law 11.

### 6.3 Levers to the $0.60 beta budget

In the order they are pulled, with the arithmetic and who decides:

| # | Lever | Saving per session | Status | Decision |
|---|---|---|---|---|
| 1 | Batch for teacher and writer with 02's cut lines | $0.13 (already in the table) | build week 2, in | pipeline D2 |
| 2 | Episode default 6 → 5.5 minutes (PRD-v2 14.5 "5 to 6 minutes by default"; dial in 9.6) | voice −8%: $0.011 Gemini, $0.017 Inworld; writer output −$0.005 | build week 2, configuration `length.default_min` | [DECISION] 5.5 as the default dial for learners with no low-energy signal; 5 when one fires; the teacher's dial moves it ±1 within 4:00 to 8:00 |
| 3 | Batch TTS (Gemini only; Inworld and ElevenLabs have no batch tier on their pages) with the same cut lines | $0.067 on Gemini | P1 (turnaround unverified, 02; tested on 20 jobs during the gate run) | pipeline |
| 4 | Cheapest voice that passes the blind test | $0 to $0.50 depending on the winner | gate run, by 2026-11-17 | D5, the test |
| 5 | Host cache hit at 90%+ verified by the 50-call test | prevents a $0.03 loss | build week 4 | D8 |
| 6 | Haiku 5.5 as the call host if the 50-call test's move-contract score holds | host text $0.049 → $0.003: $0.046 | build week 4 test; a quality decision; flipped as 09's `host.model` feature flag after `eval-gate` passes, never by `cost/alarms` (ADR-14) | [OPEN for Muath, 10-decision-records §10 item 6] with the call domain: run 25 of the 50 calls on Haiku and compare `violations`, talk share and the human read; switch only if equal |
| 7 | Round two uptake measured, not assumed | up to $0.025 | beta | none needed |
| 8 | One analyst call instead of fast plus full once the after-session pass's 10-minute budget is proven (ADR-06: the pass is one function) | $0.0005 | P1 | assessment domain |
| 9 | Re-listen ASR per line only on lines that changed after a resynthesis; never on the cached Salma feed tag or hello clips; the gloss cache shared across learners (02) | about $0.005 a session plus $0.02 on every resynthesis | build week 2 | pipeline, already designed; this domain measures it |
| 10 | Teacher effort `low` for ordinary nights, `high` on the nightly weekly-mix run and at season boundaries (Opus 5.5's effort is the only thinking control) | output 6k → 3k tokens on 4 of 5 nights: $0.024 | build week 2 configuration `roles.teacher.effort` | [DECISION] default `medium` kept in the beta; `low` is the first lever if the measured teacher line is over $0.09 |
| 11 | Pre-produce `daily_extra` only for learners whose last 7 days show 5 or more extras (`prewrite_extra`, ADR-05); everyone else on request | avoids about a third of the voice line on episodes nobody asks for: $0.07 to $0.08 per unrequested episode | build week 2, in | pipeline, ADR-05 |

Stack after levers 1, 2, 5, 9 and 11 (all in by build week 2 at no quality cost): Gemini $0.65 standard TTS, $0.58 with batch TTS; Inworld $0.68. Lever 10 (teacher `low`) takes Gemini to $0.56 with batch TTS; lever 6 (Haiku host) takes Inworld to $0.63 and with lever 10 to $0.61; the 5-minute default (lever 2 taken further) takes Inworld to about $0.59. So: the Gemini stack meets the budget before 2027-01-01 with configuration alone only if batch TTS passes its turnaround test, and with teacher `low` otherwise; the Inworld stack meets it only with the Haiku host plus teacher `low` or the 5-minute default, all of which are quality decisions for the 50-call test and the offline suite. This is the honest state of the budget on 2026-11-06, about $0.03 a session worse than the first draft said on 2026-10-17, the difference being 02 §6's writer output and side lines.

### 6.4 The path to $0.30 to $0.35 at 10,000 learners (PRD-v2 1.4, 19.2 exit criterion)

Base case: list prices after 2027-01-01 (the scale target is a 2027 number). Each row is a configuration change unless marked.

| Line | Beta (Inworld) | Floor at scale | How |
|---|---|---|---|
| Teacher | $0.082 | $0.045 | Opus 5.5 batch at effort `low` (3k output) on 4 nights in 5 ($0.052), effort `high` weekly ($0.085): (4 × 0.052 + 0.085) ÷ 5 = $0.059; minus 1,000 fewer input tokens as the brief compiler tightens and a larger cache pool: about $0.045. Sonnet 5.5 batch instead would be $0.024 (a quality decision for the offline suite, PRD-v2 6.7) |
| Writer and rewrites | $0.075 | $0.060 | recap and shadow-line text from Haiku ($0.01 saved, 02 lever 5); rewrite rounds at 1.0 on average once the fitter's known-word list is mature ($0.005); the 9k output stays (the package JSON is most of it) |
| Fitter, editor, embedding | $0.018 | $0.030 | Gemini doubles; no lever (the editor must stay on a second vendor) |
| Voice studio | $0.253 | $0.140 | 5-minute episode default plus 2.5 read-aloud plus 1.5 recap = 9 minutes = 7,500 characters; Inworld at a negotiated $15 per million (TTS-2 at the Flash price, plausible at 3B characters a month) = $0.113 + re-listen 9 min × $0.003 = $0.027; or Gemini Flash-Lite TTS batch post-doubling about $0.079 + alignment $0.033 + re-listen $0.027 = $0.139 if it passes a blind test |
| Pipeline side lines | $0.020 | $0.015 | the pre-write allowance measured against actual swap uptake; idea refresh unchanged |
| Call | $0.119 | $0.070 | Haiku host ($0.046 saved; a flag flipped after `eval-gate`, ADR-14); 5.5-minute call; Inworld Flash or Gemini call voice; LiveKit enterprise rate |
| Round two | $0.025 | $0.015 | same levers at 2.5 minutes |
| Verbatim, pronunciation | $0.036 | $0.023 | volume rate $0.0025 a minute on 6 minutes; one utterance |
| Salma (when asked) and chat | $0.023 | $0.018 | chat host kept on Sonnet (the host's voice in text matters); `salma_explain` on Sonnet; shorter cached prefixes |
| Analyst, memory keeper | $0.005 | $0.005 | none |
| Proof (÷ sessions) and hosting | $0.021 | $0.015 | the proof per learner-week spread over 7 to 14 sessions on the upper plans; show audio on presigned S3 and a CDN (ADR-12, 01 lever 1) |
| Swap allowance | $0.025 | $0.015 | measured uptake; a swap at the floor stack costs $0.30 |
| **Total, list prices post-doubling** | **$0.702** | **$0.451** | |
| with Sonnet teacher | | $0.430 | quality decision |
| with a negotiated voice rate at $12 per million characters, or Flash-Lite at the pre-doubling rate | | $0.408 | [OPEN for Muath, 10-decision-records §10 item 5]: contract |
| with read-aloud and recap rendered on first tap instead of pre-rendered | | $0.383 | [OPEN for Muath, 10-decision-records §10 item 5]: PRD-v2 3.7 says the recap is made in the same pipeline run and 6.1 pre-renders the read-aloud; rendering them on first tap (streamed) saves the audio for the 60 to 90% of sessions that never open them [ASSUMPTION on uptake]. The engineering cost, which the first draft left out: about four engineer-days across 02 (a `render_on_tap` kind on the on-demand path), 03 (the streaming TTS path exposed to the player) and 06 (the word sheet and read-aloud sync, which assume precomputed timings, need a streamed-timings mode), plus a 2 to 4 s first-sound wait on the tap and a PRD change. The cheaper middle, proposed here: pre-render the recap (90 s, always offered) and render the read-aloud on first tap only for learners whose history shows they never open it (the teacher's dial, from `events`), which keeps the PRD's default for new learners and takes about $0.015 of the $0.025 |
| with 5-minute calls and the 4:30 close | | $0.368 | PRD-v2 5.4.2 says 5 to 7 minutes target; a 5-minute default is inside it; the beta's "4+ minutes of learner speech" gate (16.1) must still be met |

Reading: at list prices after the doubling the floor stack is **$0.43 to $0.45**; the first draft and 10-decision-records §10 item 4 say $0.39 to $0.43, and the $0.02 to $0.03 difference is 02 §6's writer output and side lines, which the first draft did not carry (the technical-design thread should read $0.43 to $0.45 as the current figure). Before the doubling (the same stack on Gemini Flash TTS batch at $0.0068 a minute) it is $0.36 to $0.39, which is where the concept's "$0.25 to $0.36" range came from. **Both post-doubling floor figures are above the $0.42 break-even of the `two_a_day` and `three_a_day` plans on a learner who uses every episode** (section 6.5): at the floor, those two plans lose $0.01 to $0.03 a session on full-use learners, and either the price points or the floor stack must move. The target of $0.30 to $0.35 in 2027 therefore needs, beyond configuration, one of three things Muath must choose: a voice contract (the cheapest and least visible), a scope change to on-tap rendering (visible as a short wait, four engineer-days), or shorter calls (visible as less talking, and in tension with the speech gate); or $34.99 for `two_a_day`. The "costed path to $0.35 or less" the exit criterion asks for is this table with measured numbers in the first column by 2026-12-22 (ADR-07); the choice among the levers is 10-decision-records §10 items 4 and 5 [OPEN for Muath].

Fixed infrastructure at 10,000 learners adds $0.03 to $0.05 (01 §6 as revised), which the PRD's scale target absorbs inside its "hosting" line only if the CDN move happens; the report keeps it separate.

### 6.5 Cost per learner-day and the margin by plan (decisions.md §2, ADR-04, ADR-05, ADR-15)

The unit the plans are priced in is the learner-month, and the unit a learner spends is the learner-day: 1 to `plan.episodes_per_day` sessions, each the session of 6.1, plus the on-demand premium on episodes 2 and 3. Episode 1 is the drop (batch pipeline). Episodes 2 and 3 are `daily_extra` episodes made on request through the on-demand path (ADR-05): the teacher's brief for them is in the nightly plan, so the extra costs the same as a session minus the teacher's share, plus the writer at standard instead of batch pricing (+$0.053) and the editor and voice at standard (no batch TTS), about **+$0.05 an episode** at the beta stack; `prewrite_extra` (lever 11) removes the premium for learners who use episode 2 five days in seven.

```
cost(learner_day) = c × e + p × max(0, e − 1)        c = session cost (6.1), e = episodes used, p = on-demand premium ($0.05)
cost(learner_month) = Σ over the learner's local days
```

At the planning cost of $0.35 a session (decisions.md), the beta stack after levers ($0.60, the budget) and the post-doubling floor ($0.44, the midpoint of 6.4), with 30 days a month, 15% of list to tax and processor fees (decisions.md's figure; the `vendor: payments` row replaces it once the processor is chosen, ADR-21: Paddle as merchant of record about 5% with tax inside the price, Stripe with Stripe Tax about 3% plus the tax we would remit) and concept-v2 §8's typical use of 60%, 50% and 45% of the allowance:

| Plan | List | Net (−15%) | Episodes a month: typical / full | Cost at $0.35: typical / full | Margin at $0.35: typical / full | Margin at $0.60 (beta): typical / full | Margin at $0.44 (floor): typical / full | Break-even cost per session at full use |
|---|---|---|---|---|---|---|---|---|
| `one_a_day` | $19.99 | $16.99 | 18 / 30 | $6.30 / $10.50 | 63% / 38% | 36% / −6% | 53% / 22% | $0.57 |
| `two_a_day` (recommended, the trial plan) | $29.99 | $25.49 | 30 / 60 (30 extras) | $10.50 / $21.00 + $1.50 premium | 59% / 18% (12% with the premium) | 29% / −47% | 48% / −9% | $0.42 ($0.40 with the premium) |
| `three_a_day` | $44.99 | $38.24 | 40.5 / 90 (60 extras) | $14.18 / $31.50 + $3.00 premium | 63% / 18% (10% with the premium) | 36% / −49% | 53% / −11% | $0.42 ($0.39 with the premium) |
| **Blended, 50/50/0 mix** (`plan_mix` from `subscriptions.plan`) | | $21.24 per learner | | $8.40 at $0.35 typical | **60%** | **32%** | **50%** | |

What the table says:

1. The decisions.md margin table is reproduced (63/38, 59/18, 63/18 at $0.35) and its rule holds at the planning cost: no plan loses money on a full-use learner at $0.35. The on-demand premium, which decisions.md did not price, takes the full-use margins of the upper plans to 10 to 12% and their break-even to $0.39 to $0.40; `estimate.py --margin` prints both.
2. In the beta the rule does not hold, as decisions.md's caveat says: at $0.60 a full-use `two_a_day` learner costs $37.50 a month against $25.49 net, a loss of about $12 a month per such learner (about $15 on `three_a_day`); with typical use at about half the allowance the blended margin is about 32%, positive but under the public-launch gate's "above about 50%" (concept-v2 §9). At most about 50 beta learners are on the upper plans, so the exposure is a few hundred dollars a month, which is the research budget.
3. At the post-doubling floor of $0.43 to $0.45 the `two_a_day` and `three_a_day` plans still lose money on full-use learners ($0.01 to $0.03 a session, $0.60 to $2.70 a month per such learner) while the blended margin at typical use sits on the gate at about 50%. What closes the gap is one of: the voice contract at $12 to $15 per million characters (floor $0.41, under the break-even), on-tap rendering ($0.38), 5-minute calls ($0.37), or `two_a_day` at $34.99 (break-even $0.50). These are 10-decision-records §10 items 4 and 5 [OPEN for Muath]; the exit document of 2026-12-22 carries the measured column.
4. Fixed infrastructure is outside this table, as 01 §6 rules, and is printed beside it: at 100 learners it is $3.30 to $4.30 a learner-month, which is why the beta's blended margin is a research number and the 250-learner run-rate figure ($0.14 to $0.17 a session) is the one the gate compares.

The weekly report's section 9 (4.4.2) prints this table from measured data: `plan` on every roll-up row, `episodes` per learner-day, the fee row, `plan_mix` and `blended_margin`; 09 carries the last two as measures and the Tuesday review reads them. Section 6.6's `estimate.py --margin` prints it from `assumptions.yaml` for any session cost, so the price points can be re-tested in a minute when the measured cost moves.

### 6.6 The estimate as code

`tools/cost-model/` holds `assumptions.yaml` (every unit number in 6.1 and 6.5 as a key) and `estimate.py`, which loads `prices.yaml` and `plans.yaml` and prints the tables of 6.1, 6.4 and 6.5 for any `--at` date and `--stack` (gemini, inworld, elevenlabs, floor); `--margin` prints the decisions.md margin table for the stack's session cost and any `--plan-mix`. It is also the test that `prices.yaml` parses, that every role in `vendors.yaml` and in each `packages/languages/<target>/vendors.yaml` has a price row, and that no `assumption` row without `verified` is used by the chosen stack (D11). Muath recomputes with `python -I tools/cost-model/estimate.py --at 2027-01-02 --stack inworld --set call.minutes=5.5 --margin --plan-mix 0.5,0.5,0`. From 2026-12-23 a second mode, `--measured --week 2026-W52`, replaces assumptions with `session_costs` and `learner_costs_daily` means and prints the deltas, which is sections 2 and 9 of the weekly report.

```yaml
# tools/cost-model/assumptions.yaml (excerpt; the generation keys are 02 section 6's)
episode: {minutes: 6.0, read_aloud_minutes: 2.5, recap_minutes: 1.5, chars_per_minute: 830, gemini_tokens_per_second: 25}
teacher: {input_tokens: 16000, cache_read: 7000, cache_write_1h: 7000, cache_pool_learners: 10, output_tokens: 6000, effort: medium, pricing: batch}
writer:  {input_tokens: 13000, cache_read: 7000, cache_write_1h: 7000, cache_pool_learners: 10, output_tokens: 9000, pricing: batch, rewrite_rounds: 1.3, rewrite_input: 9000, rewrite_cache_read: 7000, rewrite_output: 1200}
pipeline_side: {idea_refresh_usd: 0.003, prewrite_rank2_usd: 0.014, batch_escalation_usd: 0.003}
alignment: {always_with: [gemini], minutes: 10}
call:    {minutes: 6.5, learner_turns: 25, host_share: 0.35, host_chars: 1900, host_cache_read: 90000, host_cache_write_5m: 4000, host_uncached: 3000, host_output: 1500, talkback_asks: 3, stt_streams: 2, livekit_participants: 2,
          source: "assumption until tools/m0_import.py writes the pilot's measured minutes of learner speech and turns per call"}
round_two: {minutes: 2.5, uptake: 0.5}
verbatim: {learner_minutes: 7, pronunciation_utterances: 1}
salma_explain: {calls_per_session: 0.3, input_tokens: 3000, cache_read: 2000, output_tokens: 400}
chat: {messages: 5, input_tokens: 4000, cache_read: 3000, output_tokens: 150}
swap: {share_of_sessions: 0.05, cost_usd: 0.55}
proof: {weekly_usd: 0.06, shown_per_session_at_sessions_per_week: 4}
hosting: {egress_usd: 0.006}
plans:   # ADR-04; usage shares from concept-v2 section 8; fee share from decisions.md until the vendor: payments row is real
  one_a_day:   {usd: 19.99, episodes_per_day: 1, typical_use: 0.60}
  two_a_day:   {usd: 29.99, episodes_per_day: 2, typical_use: 0.50}
  three_a_day: {usd: 44.99, episodes_per_day: 3, typical_use: 0.45}
  fee_and_tax_share: 0.15
  days_per_month: 30
  extra_episode_premium_usd: 0.05
  plan_mix_default: [0.5, 0.5, 0.0]
```

### 6.7 Performance of the tracing itself

The middleware adds 1 to 2 ms to a call in `workflows` (one insert in its own short transaction with the `learner_spend_daily` upsert, ADR-13; a round trip, not a lock) and nothing measurable to the live path (the per-turn S3 spool append and the 5-second buffered flush both run off the audio thread; 03's latency budget is untouched). `cost/rollup` over a 15-minute window at 10,000 learners is about 90,000 rows at the plans' usage, one aggregate query under 3 s. `cost/reconcile-spend` hourly touches only learners with an open local day. The weekly report at scale reads roll-ups only. `vendor_calls` grows about 60 rows a session: 180,000 a month at 100 learners (about 75 MB), 18M a month at 10,000 (about 7 GB a month, partitioned, 13 months kept).

---

## 7. Build plan for 2026-11-18 to 2026-12-22

Dates per ADR-07: Milestone 0 runs 2026-10-24 to 11-18 and the English language gate (the vendor tests of 4.6) runs inside it from 11-01 to 11-17, so the voice and recognizer decisions land before build week 1, which is better than the first draft's plan; the build is five weeks from 11-18 to 12-22; the beta opens 12-23; the Gemini doubling falls in beta week 2; the gate review is 2027-01-26. Freezes: 2026-12-21 12:00 to 12-24 12:00 UTC and 12-31 to 2027-01-02.

Team: the topology's E1 builds the middleware and tables in build week 1 alongside the adapters (the two are one piece of work); Muath runs the gate with `vendor-lab` and writes the truth file during Milestone 0; E2 is not needed by this domain until the admin page in week 5. If there is one engineer, the cuts are in the last row.

| Week | Dates | This domain ships (P0 unless marked) | What the pilot data lets you test |
|---|---|---|---|
| 0 (the gate, in parallel with Milestone 0) | 2026-11-01 to 11-17 | `vendor-lab gate --target en` with `tts render/sheet`, `stt run/decide` and the CSV sheets on the adapter package's first cut (4.6); the recognizer test by 11-10; blind test listening sessions (Muath, 10 raters: 5 native English speakers, 5 learners of English) and `vendor-lab decide tts`; `vendor-lab verify-prices` on every finalist the day the dashboards can be read (D11); `packages/languages/en/vendors.yaml` and `gate.yaml` committed with the winners by 11-17 and the paid tier bought for the winner only; quota requests sent (4.9); Hume lockfile check in CI; Langfuse per-user deletion by pseudonym verified with a test user; the vendor-test consent addendum in place before any clip leaves (10-decision-records §10 item 13) | The 30 Milestone 0 clips and Muath's truth file run the 10.14 test by 2026-11-10; the two-host script renders on all three voice vendors for the blind test playlists; every test render is a priced `vendor_calls` row (repriced by `--reprice` once the middleware lands), so the first "cost per 10 minutes of audio" number is real before any episode exists; `tools/m0_import.py` writes the pilot's measured `call.minutes` and `call.learner_turns` into `assumptions.yaml` |
| 1 | 2026-11-18 to 11-24 | `prices.yaml` v2026-11-18 with the 1-hour cache-write rows, the Google embedding row, the `vendor: payments` rows and the `verified` marks, and the `price_book` migration; `vendor_calls` DDL with partitions, RLS, `plan`, `step`, `attempt`, `turn_index` and the two idempotency indexes; `tracing.traced`, `UnitUsage` with `cache_write_ttl`, `price_for`, `record_external`, the own-transaction write with the `learner_spend_daily` upsert (with 07, ADR-13), the worker's per-call S3 spool; `learner_guard_usd(plan)` for 07's `costguard.check` (ADR-15); Langfuse SDK wiring with the trace conventions, the pseudonym as `user_id`, metadata-only by default and the `data_use` gate on text (ADR-09); `SPEND_CAP_USD_PER_DAY` with the Σ episodes formula over the UTC day | Every gate render re-priced through the real middleware; the Milestone 0 scripts' character counts calibrate `chars_per_minute` |
| 2 | 2026-11-25 to 12-01 | `cost/rollup` into `session_costs` (with `plan` and `daily_extra`), `learner_costs_daily` (with `episodes`) and the role-vendor table, plus spool ingestion; `cost/reconcile-spend` hourly; `episodes.cost_usd` fed from `session_costs` for 02's publisher, including `daily_extra` episodes from the on-demand path (ADR-05); `kind_ceiling`, `unpriced`, `cache_hit_low` (floor set from this week's baseline), `escalation_rate`, `price_stale` alarms; `tools/cost-model/estimate.py` with `--margin` and with `--measured` against the week's 20 test episodes; the editor fallback on Opus and the Google embeddings priced (ADR-10, 11); staging stays up from here (ADR-16) | 20 test episodes from the Milestone 0 learner files give the first measured teacher, writer, editor and voice lines against 02 §6's table; the first measured cache hit rate per step sets `cost.cache_hit_floor` |
| 3 | 2026-12-02 to 12-08 | `plan` read from `subscriptions.plan` into `CallMeta` once `plans.yaml` lands (01, ADR-04); pre-account learner id and pseudonym carried in `CallMeta` for onboarding and sample traces, re-keyed at A9; sample episode ceiling alarm on the live endpoint; payment processor fee row after the 12-02 decision (ADR-21); `learner_costs_daily` with the acquisition line and the proof per learner-week; `learner_spend_soft` and `learner_spend_hard` alarms wired to 07's guard and 09's `cost_runaway` | The sample landing page's first real renders measure the $0.05 ceiling; synthetic learners on all three plans exercise the per-plan guards |
| 4 | 2026-12-09 to 12-15 | `record_external` for LiveKit minutes from the worker; `call-bench` cost and cache-hit columns; `calls.metrics.cost_usd` fed; `session_over_alert`, `vendor_error_rate`, `daily_spend_*` alarms and `spend_mode` with the `conserve` (no learner-audible change, ADR-14) and `halt` paths wired into 02's and 03's config reads; the Haiku-host comparison inside the 50-call run (lever 6) as 09's `host.model` flag behind `eval-gate`; the per-plan cost guard end to end (ADR-15) | Milestone 0 call transcripts replayed through the worker give per-call cost and the host cache hit rate before any live learner; a forced task kill mid-call proves the spool loses nothing |
| 5 | 2026-12-16 to 12-22 | `cost/weekly-report` with all nine sections including "Margin by plan", `plan_mix` and `blended_margin`, and `/admin/cost` on `forone_admin`; `cost/reconcile-monthly` skeleton with the Anthropic Admin API pull and the CSV upload; peak concurrency from `learner_schedule` in the vendor section; `learner/delete` aggregation hook; the end-to-end run with the Milestone 0 learners (under a consent that covers it) produces the first weekly report; **the exit document on 12-22: measured cost per session, the costed path (6.4) with a measured first column, and the margin by plan (6.5) at the measured cost** | The 15 Milestone 0 learners' week on prod is the measurement the exit criterion asks for; their heavy-use spread tests the outlier rule and the plan guards |
| Freeze | 2026-12-21 12:00 to 12-24 12:00 UTC | No deploys; the next-week-prices report of 12-21 is the first with the 2027-01-01 rows | |
| P1 (beta) | 2026-12-23 to 2027-01-26 | Daily cap recomputed from the plan mix from 12-23; batch TTS (lever 3) if Gemini is primary; Langfuse sampling switch (off in the beta); automated invoice ingestion for one more vendor; the 12-28 next-week-prices report; the January voice plan executed in the first release after 2027-01-02 (6.1 note 3); the margin by plan read at the Tuesday reviews; the report of 2027-01-25 as the gate evidence for 01-26 | |
| Cuts if one engineer | | No `/admin/cost` page (the weekly report Markdown and SQL suffice); monthly reconciliation fully manual (a notebook); `vendor_invoices` table dropped; `conserve` mode dropped (only `halt` on the cap); `vendor-lab` reduced to render and run commands with decisions in a spreadsheet; the margin section as the SQL query of 4.4.2 run by hand. Not cut: the own-transaction write, the spool, the hourly spend reconcile and the per-plan guards, because they are the spend guard | |

What is too much for this team and is cut or deferred: self-hosted Langfuse (kept only as the fallback if the processor is refused), per-vendor invoice scrapers, a cost dashboard beyond one admin page, multi-currency (one USD list price at launch, decisions.md §2; local-currency display and tax are the merchant of record's, ADR-21), margin-per-learner analytics beyond the per-plan table (one SQL query in the report), a budget forecasting model (the next-week-prices column is enough).

Milestone 0 to code: the kit's evening cycle (04-production.md) maps onto roles as step 1 → `verbatim_stt`, step 2 → `analyst` (the notes half of the pilot's step 2 has no production counterpart after ADR-06), step 5 → `teacher` and `writer`, step 6 → `fitter`, step 7 → `editor`, step 9 → `episode_tts`, step 10 → `host` brief. Milestone 0 itself is untraced (Claude Max, AI Studio, ElevenLabs Pro at $99 a month, about $7 a learner for the fortnight); its cost artifacts worth importing are the character counts of its scripts, the minutes of its calls and the minutes of learner speech and turns per call, which `tools/m0_import.py` (04) copies into `assumptions.yaml` as `episode.chars_per_minute`, `call.minutes` and `call.learner_turns`, because those move the call and verbatim lines more than any price.

---

## 8. Alternatives rejected

| Alternative | Why rejected |
|---|---|
| Cost in `events` only (04's `events.cost_usd`) | Sample episodes, canaries, vendor tests and failed attempts have no learner or session; the log is append-only and learner-scoped, so repricing after a `prices.yaml` fix would be impossible. `events.vendor_call_id` keeps the link without the duplication |
| Cost in Langfuse only | A processor outside the home region, sampled at scale, with its own retention; a reconciliation against invoices needs rows we own |
| OpenTelemetry to Grafana or Honeycomb instead of Langfuse | No prompt and completion view, which is what debugging a wrong episode needs; the adapters still emit OTel spans (02 4.16) so a later move is additive |
| A proxy gateway (Helicone, Portkey, LiteLLM) for tracing and routing | Adds a network hop in the call path (03's 950 ms budget has no room), a second place where vendor keys live, and a dependency on its vendor list; our adapters already exist |
| Vendor dashboards as the cost record | No per-learner or per-session view; monthly granularity; a price change goes unnoticed for a quarter |
| Hard per-learner spend cut-off | Breaks law 4 and trust promise 2; a heavy user is the product working. Outliers are a warning light only |
| Speech-to-speech for the call to save engineering | More expensive per call ($0.18 to $0.50, lens), no verbatim transcript, no shared voice; rejected by the call domain for the same reasons |
| One voice vendor with an enterprise contract from day one | Two vendors are a PRD-v2 14.3 rule; a contract before the blind test buys the wrong vendor |
| Two enterprise voice contracts | Two minimums at 100 learners; the runner-up on pay-as-you-go costs under $20 a month in canaries |
| Sonnet as the beta teacher to hit $0.60 on the Inworld stack | The teacher is the product's brain and the PRD names the strongest class; the $0.05 is found in the host and the episode length first; Sonnet is measured in the offline suite before any switch |
| Monthly instead of weekly cost reports | PRD-v2 14.5 says weekly; the 2027-01-01 jump needs warning before beta week 2, and the margin by plan is a weekly gate input |
| The cost row inside the caller's transaction (the first draft) | A vendor call happens before the step's write, so a rollback on retry loses the row exactly when a retry storm is spending money; the own-transaction write with an idempotency key costs one round trip (ADR-13) |
| Automatic model downgrades in `conserve` (the first draft) | A quality change on a busy day is the product degrading itself when it is working; a person flips the flag after `eval-gate` (ADR-14, 09 D8) |
| Pricing one daily session and leaving the plans to a spreadsheet | decisions.md made the cost model the price-setter; the margin by plan must come from the same rows the gate reads |
| Pre-producing every episode of the allowance in the nightly batch | About a third of the voice line on episodes half the learners never ask for; the on-demand path already meets 30 s (ADR-05) |
| Haiku as the fallback editor | The editor exists to catch what the writer's vendor misses; when it shares that vendor it must be at least as strong as the writer (ADR-11); the $0.05 fallback-day cost is cheaper than an unreviewed episode |
| A nationality-specific vendor test | The tests are the language gate's checks per target language; a learner's own language is a per-learner fact (ADR-02, 03) |
| Computing cost client-side from token counts in the SDK responses only | Streaming TTS and STT vendors report seconds, not tokens; one middleware with `usage_of` per adapter is the only way to one schema |

---

## 9. Assumptions about other domains

Each is an [ASSUMPTION] the integrator should check against that domain's document.

1. **System topology (01).** The adapter middleware described in its 4.5 is this document's `tracing.traced`; `CallMeta` gains `session_id`, `prompt_version`, `inngest_run_id`, `plan` and `episode_kind` (it has `learner_id`, `role`, `episode_id`, `call_id`, `learner_model_version`); `plans.yaml` and `subscriptions.plan` exist with the three ADR-04 values and `founding_locked`; `vendor_config` holds `spend_mode`; `SPEND_CAP_USD_PER_DAY` (the Σ `episodes_per_day` × $1.00 formula over the UTC day) and `SESSION_COST_ALERT_USD` are read by this middleware with the defaults here; `retention/daily` creates `vendor_calls` partitions as it does for `events`; `/admin/cost` is one more `sqladmin` page on `forone_admin` (ADR-17); the `vendor-lab` CLI with `gate --target` is built here on its adapter package; the weekly canary episode is tagged `episode_kind='canary'` and `learner_id=null`; LiveKit minutes are booked through `record_external` by the call worker; the event-spool bucket accepts the worker's per-call cost spool objects (ADR-13); `HOME_REGION` defaults to `eu-central-1` (ADR-08); infrastructure cost stays in 01's section 6 as revised ($800 to $1,100 a month, plus about $180 for staging kept up through the beta, ADR-16) and is printed as a separate line in the report.
2. **Episode generation pipeline (02).** `pipeline_steps.cost_usd` is a sum of this domain's `vendor_calls` rows for that step (via `pipeline_steps.vendor_call_ids uuid[]`), and `price_book` is loaded from `prices.yaml`, not maintained separately; this document's unit table is 02 §6's (writer 9k output, alignment always with Gemini, idea refresh, `prewrite_rank2`, batch escalations, 1-hour cache writes amortized over about 10 learners a pool); the publisher reads `session_costs` (or sums `vendor_calls` by `episode_id` when the roll-up has not run) for `episodes.cost_usd` and `episode.cost_recorded`, for `daily_extra` episodes too (ADR-05); its cut lines set `pricing_escalated`; the fallback episode and `review_items` exist as it describes; `length.default_min` is a dial the teacher reads; the 02 `TtsAdapter` capabilities include `batch` for lever 3; the editor fallback is `claude-opus-5-5` and the similarity check runs on Google's embedding model (ADR-10, 11); `prewrite_extra` follows the 7-day rule.
3. **Live call and voice stack (03).** The worker writes each turn's `vendor_calls` rows to the per-call S3 spool and then through the buffered middleware with `call_id`, `turn_index` and `capability` as the idempotency key (ADR-13); `calls.metrics.cost_usd` is filled at call end from the buffer; `tools/call-bench` (ADR-19) accepts two extra report columns from this domain; the host model is a feature flag (`host.model`) read at call start, never mid-call, and never set by `spend_mode` (ADR-14); the Haiku-host comparison runs inside the build week 4 50-call test; `talkback_stt.languages` is set per call from the learner row (ADR-02).
4. **Learner model, event log and data platform (04).** `events.vendor_call_id` references `vendor_calls.id`; `learners` carries `native_language`, `target_language`, `residence_country`, `plan`, `tz` (ADR-02, 04); `research_pseudonyms(learner_id, pseudonym)` exists and `anonymize()` is the function this middleware calls before any text leaves (ADR-09); `learner/delete` calls this domain's aggregation hook before deleting rows and this domain's `langfuse_admin.delete_user(pseudonym)`, and does not wait on it for the "deleted" email; `forone.learner.pii.scrub_for_processor` exists for metadata; the pre-account learner id of onboarding is re-keyed to the real `learner_id` at A9 by an event this domain subscribes to (`learner.created {pre_session_id, learner_id}`); `proofs.sessions_in_week` is computed (ADR-19).
5. **Assessment engine (05).** Its roles (`analyst`, `memory_keeper`, `salma_explain`, `proof_producer`, `rater`, `verbatim_stt`, `pronunciation`) and per-turn verbatim calls go through the middleware; `salma_text`, the polish TTS and the margin note no longer exist (ADR-06) and the after-session pass is one function; `rater.pinned_until` is enforced by the middleware's refusal of fallback and override; the confidence threshold from 4.6.3 is read from `packages/languages/<target>/recognizer.yaml`; claim-related traces are never sampled out of Langfuse.
6. **Client app and delivery (06).** `client_perf` values are not vendor calls (its assumption 7, accepted); show audio is served by presigned S3 URLs (ADR-12), so egress is booked by `record_external` from the media route's URL issuance and the feed MP3 encode, daily, as one row per learner-day (`capability='media'`), not per request; the sample endpoint reads `spend_mode` and shows its own "try again tomorrow" page in `halt`; the "next one" control calls `POST /v1/episodes/next` and shows the allowance sentence when `halt` pauses extras; the plan picker on day 7 reads `plans.yaml`, never a cost figure.
7. **Security, privacy, consent and compliance (07).** Owns `learner_spend_daily` and `costguard.check`, which take this domain's per-plan thresholds (ADR-15) and are upserted by this middleware in the `vendor_calls` statement and reconciled hourly (ADR-13, amending its "nightly"); approves Langfuse Cloud EU under ADR-09 (metadata and the pseudonym by default; anonymized text only for `data_use` learners; 30 days) and the `forone_cost` cross-learner read role; approves the Anthropic Admin API key as a read-only secret; the payment processor is a merchant of record or Stripe with Tax (ADR-21) and its fee row feeds the margin section; if Langfuse is refused, this domain's fallback is self-hosting (about $150 a month of Fargate and RDS plus two engineer-days).
8. **Evaluation, observability and operations (09).** Owns `ops.page` and `ops.notify`, the on-call rota that receives `cost.alarm_raised`, the ops channel the weekly report posts to, the alert names `cost_runaway` (P1) and `cost_stop_line` (P3 plus the ticket) that this domain's `daily_spend_100`, `learner_spend_hard` and `stop_line` map onto, the feature-flag table with `host.model` and `teacher.model` behind `eval-gate` (ADR-14), the measures `plan_mix` and `blended_margin` (ADR-15), the Tuesday review that reads them, and the day-one "recognizer error by first language" metric seeded by 4.6.3; the offline test suite (P1) reuses `vendor-lab` fixtures and the gate's suites (`recognizers`, `voices-blind`, `calls_50`) are its regression form (ADR-03).

---

## 10. Open for Muath

The shared register is 10-decision-records §10 (ADR-22); the items below that it owns are one line each.

1. **[OPEN for Muath] Tier prices against the break-even (6.5):** see 10-decision-records §10 item 4. This document's current floor figure is $0.43 to $0.45, not the $0.39 to $0.43 quoted there (6.4).
2. **[OPEN for Muath] The last lever to $0.35 and the voice contract (6.4):** see 10-decision-records §10 item 5. The engineering cost of on-tap rendering and the cheaper middle (pre-render the recap, on-tap read-aloud only for learners who never open it) are in the 6.4 row.
3. **[OPEN for Muath] Haiku 5.5 as the call host:** see 10-decision-records §10 item 6. Worth $0.046 a session; a feature flag after `eval-gate`, never an alarm (ADR-14).
4. **[OPEN for Muath] Budget approvals:** see 10-decision-records §10 item 9 (fixed infrastructure $1,000 to $1,300 a month, vendor minimums, the Anthropic prepaid balance of about $2,500 for the beta's first month at the upper plans' usage). Specific to this document: the rater fees for the blind test (10 raters, about one hour each) and the `verify-prices` renders (under $20).
5. **[OPEN for Muath] Payment processor:** see 10-decision-records §10 item 3. This document needs only the fee row by 2026-12-02 for the margin section.
6. **[OPEN for Muath] Consent for the Milestone 0 clips to reach the recognizer and voice vendors:** see 10-decision-records §10 item 13. If the pilot consent does not cover it, the 10.14 test needs a re-consent of the 30 clips' owners before 2026-11-01.
7. **[OPEN for Muath] The daily spend cap formula** `max($50, Σ over active learners of plan.episodes_per_day × $1.00)` over the UTC day, the per-plan guard multiples (2.5 soft, 4 hard, ADR-15) and the stop-line plan window of 48 hours. All three are policy, not engineering; 10-decision-records §10 item 15 leaves them with this document.
8. **[OPEN for Muath] Whether cost figures may appear in the monthly human review packet** (02's review hooks), so the reviewer sees the cost of an episode next to its quality. Internal only; never a learner surface. Default here: yes. 10-decision-records §10 item 15 leaves it with this document.
9. **[OPEN for Muath] The on-demand premium's planning value.** Section 6.5 prices episodes 2 and 3 at about $0.05 over a drop episode [ASSUMPTION from ADR-05]; the measured premium from `daily_extra` rows in build week 2 replaces it, and if it is materially higher the break-even per session on the upper plans falls below $0.42 by more than the $0.02 to $0.03 shown. Decide then whether `prewrite_extra`'s 7-day rule should be loosened (more pre-production, less premium, more waste).

---

## 11. Revision log (2026-11-06)

- conformance blocker "whole document prices one daily session; no margin table" → `plan` added to `vendor_calls`, `session_costs`, `learner_costs_daily` and `learner_spend_daily` (3.1, 4.1, 4.4.1); new section 6.5 "Cost per learner-day and the margin by plan" reproducing the decisions.md table at $0.35, $0.60 and the floor with break-even per session, `plan_mix` and `blended_margin`; report section 9 "Margin by plan" with its query (4.4.2); `estimate.py --margin` and the `plans` block in `assumptions.yaml` (6.6); daily cap = Σ `episodes_per_day` × $1.00 (4.5.1, D14); volumes at 100 learners re-based to 2,400 to 3,000 sessions a month with the 9,000 full-use bound (4.9); the statement that the post-doubling floor is above the 2 and 3 a day break-even, tagged [OPEN for Muath] and pointed at 10-decision-records §10 items 4 and 5 (1, 6.4, 6.5, 10 #1). Decisions D13 and D14 added to the §1 table.
- conformance major "Salma notes, polish TTS, margin note lines" → removed from 3.2, 3.3, 4.4.1 mapping, 4.7 roles, 6.1, 6.4 and 7; the line is "Salma (when asked) and chat" with `salma_explain` (Sonnet, 0.3 calls a session, about $0.002) plus the chat host ($0.021); the mapping row notes that the PRD-v3 thread revises the PRD line (ADR-06).
- conformance major "vendor tests parameterized by one nationality" → 4.6 rewritten as `vendor-lab gate --target <lang>`: raters 5 native speakers of the target plus 5 learners of it from anywhere, 30 real learner clips per target with code-switching into the learner's own language, `talkback_stt.languages = [learner.native_language, learner.target_language]` per call, paths `packages/languages/<target>/recognizer.yaml` and `vendors.yaml`, the Salma voice choice moved to the native-language package build, English as the pilot target (ADR-02, ADR-03). The 14.4 row in §2 no longer names a nationality.
- conformance major "Langfuse: three rules for one processor" → D3, 3.1, 3.2, 4.3.1 to 4.3.5, §5 and §9 #4 and #7 adopt 01 D15: `user_id` is the research pseudonym, metadata only unless `consents.data_use` at call time and after `anonymize()`, 30-day retention, deletion by pseudonym, debugging from the home-region artifacts (ADR-09). §10's Langfuse item removed as settled.
- conformance major "cache write priced at the 5-minute rate; 02 §6's table not adopted" → `cache_write_1h_tokens` rows at 2x input for Opus ($8), Sonnet ($4) and Haiku ($0.20, [ASSUMPTION]) in 4.2 with the TTL recorded per call; 6.1 re-adopts 02 §6's units (teacher 16k in, writer 9k out, rewrites 1.2k out, alignment always with Gemini, idea refresh, `prewrite_rank2`, batch escalations, cached prefix amortized over 10 learners) and says it reproduces 02's $0.42 generation total; `assumptions.yaml` carries the same keys (6.6); D8 amended.
- conformance major "editor fallback Haiku; embeddings OpenAI" → 4.7 editor fallback `claude-opus-5-5` standard flagged `same_vendor_edit` with its $0.05 fallback-day cost in §5; embeddings on Google's model under the Google processor row, OpenAI rows deleted from 4.2 and 4.8 (ADR-10, 11).
- conformance major "fixed infrastructure numbers out of date" → 6.1 note 4 and 6.4 adopt 01 §6 as revised ($2.30 to $2.80 at 15, $0.33 to $0.43 at 100 on the plans' sessions, $0.14 to $0.17 at 250, $0.03 to $0.05 at 10,000; $1,000 to $1,300 a month with staging up, ADR-16); 6.5 shows the share falling faster at the upper plans' usage.
- conformance major "every date is wrong" → front matter, 4.2, 4.4.2, 4.5.1, 4.6, 4.8, 6.3, 6.4, 6.6, 7 and 10 re-dated per ADR-07: recognizer by 2026-11-10, voice decision and `vendors.yaml` by 11-17, build 11-18 to 12-22, cap recomputed from 12-23, next-week-prices report from 12-21, doubling in beta week 2, gate review 2027-01-26; §7 renamed "Build plan for 2026-11-18 to 2026-12-22" with a week 0 for the gate.
- conformance minor "Mondays 06:00 Asia/Riyadh; the 2nd of each month" → Mondays 06:00 UTC and the 2nd at 06:00 UTC; session rows carry each learner's `local_date` (3.1, 4.4.2, 4.4.4; ADR-16).
- skeptic blocker "cost row coupled to the caller's transaction; 5-second buffer and local spool die with the task; nightly reconcile" → 3.2, 4.1, D1, §5, 6.7 and §9 #3 and #7: own short autocommit transaction, idempotency on `(inngest_run_id, step, attempt)` or `(call_id, turn_index, capability)` with two unique indexes, `learner_spend_daily` upserted in the same statement, per-call S3 spool before the buffered flush, `cost/reconcile-spend` hourly (ADR-13). A "retries_paid" count added to the report.
- skeptic major "automatic `conserve` downgrades models" → 4.5.2 rewritten: `conserve` changes only what no learner hears (force batch, cap rewrites at 1, skip canaries and the nightly smoke, defer anonymization, skip pre-writes); model downgrades are 09 feature flags flipped by a person after `eval-gate`, and the middleware refuses a `host` or `teacher` model override from any other source (4.7); `halt` pauses extras with the allowance sentence; D4 and 6.3 lever 6 amended (ADR-14).
- skeptic major "about $0.10 of the session rests on unverified rows; first bill check too late" → D11 gains the one-off `vendor-lab verify-prices` before `vendors.yaml` is committed (10 minutes of audio, 30 minutes transcribed per finalist, same-day dashboard comparison), rows marked `verified: <date>`, `estimate.py` refuses an unverified row in the chosen stack (4.2, 4.4.4, 6.6, 7 week 0).
- skeptic major "peak concurrency and the 'next day' assume one timezone" → the cap day is the UTC day and `spend_mode` resets at 00:00 UTC (4.5.1, 4.5.2); peak concurrency computed weekly from `learner_schedule`, printed in the report's vendor section, concurrency bought at the measured peak plus 50% (4.4.2, 4.6.1 gate row, 4.9).
- skeptic major "on-tap rendering's engineering cost not stated" → the 6.4 row carries about four engineer-days across 02, 03 and 06 and the 2 to 4 s first-sound wait, and proposes the cheaper middle (pre-render the recap, on-tap read-aloud only for learners who never open it); carried into 10-decision-records §10 item 5 and this document's §10 #2.
- skeptic major "proof divided by sessions means nothing across plans" → the proof is a per-learner-week line in the roll-up and the report; only the per-session gate divides it, by the computed `proofs.sessions_in_week` (4.4.1, 4.4.2, 6.1).
- skeptic minor "`{session_id}:after` is not a valid hash input" → the after-pass trace id is `uuid5(NAMESPACE_FORONE, f"{session_id}:after")` (4.3.1, 4.3.4).
- skeptic minor "Langfuse deletion no longer holds up the deleted email" → §5 row and 4.3.4 say so; 04 §10's question closed (ADR-09).
- skeptic minor "import the pilot's measured minutes and turns" → `call.minutes`, `call.learner_turns` and `episode.chars_per_minute` written by `tools/m0_import.py` into `assumptions.yaml` (6.1, 6.6, 7 week 0).
- ADR-01 → front matter cites decisions.md and 10-decision-records where they change a PRD part.
- ADR-02 → package paths `packages/languages/<target>/` (per the coordinator's 2026-11-06 note, not `packages/lang/`) and `packages/native/<lang>/`; per-learner `native_language` and `target_language` drive `talkback_stt`, raters, clips and the Salma voice; the first draft's local-currency revenue note removed from §7 (one USD list price, decisions.md §2).
- ADR-03 → 4.6 as the gate's checks 1, 2 and 4; D9; `gate.yaml` and per-target `vendors.yaml`; the gate's suites named in §9 #8.
- ADR-04 → plans `one_a_day` $19.99, `two_a_day` $29.99, `three_a_day` $44.99, `founding_locked`; `plan` on `CallMeta` and every cost row; the allowance sentence in `halt`; D12.
- ADR-05 → `daily_extra` on the on-demand path at standard pricing, about +$0.05 an episode; the learner-day formula and `prewrite_extra` as lever 11 (3.3, 4.4.1, 6.3, 6.5); `POST /v1/episodes/next` in 3.2 and §9 #6.
- ADR-06 → as the conformance major above; `analyst` and `salma_explain` degrade paths renamed (`claims_withheld_retry_later`, `explanation_unavailable_bubble`); lever 8 reworded to the after-pass budget.
- ADR-07 → as the conformance major above; freezes in §7 and 4.8.
- ADR-08 → `HOME_REGION` default `eu-central-1` in 4.9 and §9 #1; "PDPL fallback" wording for self-hosted Langfuse replaced by "if the processor is refused".
- ADR-09 → as the conformance major above.
- ADR-10, ADR-11 → as the conformance major above.
- ADR-12 → hosting line and 6.4 proof-and-hosting row: show audio on presigned S3 URLs and a CDN at scale; §9 #6.
- ADR-13 → as the skeptic blocker above.
- ADR-14 → as the skeptic major above.
- ADR-15 → per-plan soft (2.5 ×) and hard (4 ×) guards as `learner_spend_soft` and `learner_spend_hard` alarms, `learner_guard_usd(plan)` in 3.4, the hard guard's behaviour in 4.4.3; the daily cap formula; "Margin by plan", `plan_mix`, `blended_margin` in 4.4.2 and 6.5.
- ADR-16 → UTC jobs and reports; staging kept up (+$180 a month) in 6.1 note 4 and §9 #1; the cap day in UTC.
- ADR-17 → `/admin/cost` on `forone_admin` (3.1, §9 #1).
- ADR-19 → `episode_kind` list with `daily_extra`, `rehearsal`, `finale` (4.1, 4.4.2 query); `tools/call-bench` as the one latency tool (4.6.2, §9 #3); `proofs.sessions_in_week` computed (4.4.1); `cost_runaway` and `cost_stop_line` as 09's names for this domain's alarms (4.5.1, §9 #8).
- ADR-21 → `vendor: payments` rows (Paddle MoR about 5%, Stripe with Tax about 3%, both [ASSUMPTION]) in 4.2, the processor decision on 2026-12-02 in 4.8 and §7 week 3, the fee row in the margin section (4.4.2, 6.5), and the transactions row in 4.9.
- ADR-22 → §10 reduced to one-line pointers for the shared items (prices and break-even, the voice contract and last lever, Haiku host, budgets, processor, Milestone 0 consent); removed as settled: the Langfuse-as-processor item (ADR-09; the processor list itself is 10-decision-records §10 item 14); kept in full: the cap formula and guard multiples, cost figures in the review packet, and a new item on the on-demand premium.
- Not applied, and why: none of the review findings was declined. One number was changed against 10-decision-records rather than the review: the post-doubling floor is printed as $0.43 to $0.45 (6.4) instead of the $0.39 to $0.43 that ADR-15's narrative and 10-decision-records §10 item 4 quote, because the re-adopted 02 §6 unit table (writer 9k output, side lines) adds $0.02 to $0.03 and the two figures cannot both be true; the direction of the warning is unchanged and the register's figure should be updated. The conformance fix's "about 3,000 sessions a month at 100 learners" is printed as "2,400 to 3,000" because a 50/50/0 mix at the concept's usage rates gives 2,400 and 3,000 is the all-`two_a_day` case.
