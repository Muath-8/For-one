# Cost model, vendor strategy and tracing

Domain 08 of the For one technical architecture. Written 2026-10-17 against PRD-v2 (Implementation PRD v3.0, 2026-10-10). Implements PRD-v2 1.4 (AI cost line), 14.3 (stack, adapters, two voice vendors, price events), 14.4 (vendor tests), 14.5 (cost per session), 10.14 (recognizer test), 16.1 (cost gate) and 16.2 (heavy-use outliers). It reuses the names the topology (01), pipeline (02), call (03), data (04), assessment (05) and client (06) documents already introduced; where two of them named the same thing differently, this document rules, because cost tracing is this domain's.

Every price in this document is a list price with its date. Anthropic prices are from the API reference cached 2026-10-06; every other vendor's price is from the lens documents' vendor-page reads of 2026-10-09 unless marked [ASSUMPTION]. None is a measurement. The first measurement replaces them on 2026-12-06 (PRD-v2 19.2 exit criterion).

---

## 1. Summary and the decisions in one table

The beta cannot meet the $0.60 budget by accident, and the $0.30 to $0.35 scale target cannot be met at list prices after 2027-01-01. The arithmetic in section 6 says: the recommended beta stack lands at $0.57 to $0.67 a session depending on which voice vendor wins the blind test (Gemini with batch TTS at the bottom, Inworld at the top, ElevenLabs at list price at $0.85 and out). The Gemini price doubling on 2027-01-01 adds $0.18 to a Gemini-voiced session and $0.015 to any session (the editor), which is why the voice vendor decision on 2026-11-13 is the single most important cost decision in the beta. The floor stack reaches $0.33 to $0.36 before the doubling and $0.37 to $0.41 after it; the last $0.05 to the target comes from a negotiated voice rate, a cheaper voice tier that passes the blind test, or a scope change Muath must approve (section 6.4).

Cost is traced the way the topology already specified: one middleware in `forone.adapters` writes one `vendor_calls` row and one Langfuse observation per vendor call, priced from a dated `price_book`. This document owns those two tables, the price file, the Langfuse conventions, the roll-ups, the weekly report, the alarms and the spend guard. Nothing about cost is shown to a learner (PRD-v2 law 1 and 16.2: "a warning light, never a goal").

| # | Decision | Chosen | Reason in one line | Rejected |
|---|---|---|---|---|
| D1 | Single source of cost truth | `vendor_calls` table in Postgres, one row per vendor call, written by the adapter middleware; `pipeline_steps.cost_usd` (02) and `episodes.cost_usd`, `calls.metrics.cost_usd`, `events.cost_usd` (04) are denormalized sums of it [DECISION, PRD-v2 14.5] | One table answers "per role, per vendor, per learner, per session" with one `GROUP BY`; roll-ups can be rebuilt from it | Cost only in `events` (sample episodes, canaries and vendor tests have no learner); cost only in Langfuse (a processor, sampled at scale, outside our region) |
| D2 | Price source | `packages/adapters/prices.yaml`, checked in, dated rows with `valid_from`, loaded into the `price_book` table by migration; the middleware prices from the table, never from the YAML at runtime [DECISION] | 01 named the file and 02 named the table; both are right: the file is reviewed in a pull request, the table is joinable in SQL | Prices hard-coded in adapters; prices fetched from vendor APIs (none publish a machine-readable price list) |
| D3 | Tracing tool | Langfuse Cloud EU, one trace per unit of work, `user_id` = learner id, 100% sampling in the beta [DECISION, PRD-v2 14.3] | Prompts and completions next to cost and latency is what debugging a bad episode needs; managed; EU region is already in the topology's processor list | OpenTelemetry to Grafana only (no prompt views); Helicone-style proxy (a hop in the live path); self-hosted Langfuse (operations for a two-person team; kept as the PDPL fallback) |
| D4 | Budget enforcement in code | A `cost_guard` with three spend modes (`normal`, `conserve`, `halt`) switched by daily spend and per-session alarms; the stop line ($1.00) pages and opens a 48-hour plan window, it does not stop service [DECISION, PRD-v2 1.4, 16.1] | PRD-v2 says "over $1.00 with no costed plan" is the stop signal; the plan is a human decision, the alarms are not | Hard per-learner cut-off (breaks law 4 and the trust contract: a learner would lose a session for our budgeting) |
| D5 | Beta voice rule | The blind test picks the cheapest vendor that passes (PRD-v2 14.5); ElevenLabs can win only at a negotiated rate at or below $25 per million characters [DECISION] | At $80 per million characters the voice line alone is $0.66 and the session is over the stop line | ElevenLabs at list price (quality is not in doubt; the price is) |
| D6 | Text model tiering, beta | Exactly the PRD classes: Opus 5.5 teacher (batch), Sonnet 5.5 writer (batch), host, Salma, chat, proof; Haiku 5.5 fitter, analyst, memory keeper, talkback resolver; Gemini 3.8 Flash editor [DECISION, PRD-v2 14.3] | The text lines sum to about $0.21 of the session; the levers are elsewhere until measured | Haiku host from day one (a quality decision the 50-call test must make, section 6.3) |
| D7 | Batch everywhere nobody waits | Teacher and writer on the Message Batches API with 02's cut lines from week 2; batch TTS where the vendor offers it from P1; after-session roles stay standard (cents) [DECISION, PRD-v2 3.2, 14.5] | Batch halves the two biggest text lines ($0.11 saved); TTS batch saves $0.07 only on Gemini and its turnaround is unverified | Batch for the analyst and memory keeper (saves under $0.002 and delays notes) |
| D8 | Prompt caching contract | Every role has a `cache_prefix` (package prompt, bible, brief) and the middleware records `cache_read_input_tokens`; an alarm fires when a role's cache hit rate falls under 85% over 24 hours [DECISION] | A silent cache invalidator costs about $0.03 a session on the host alone and shows nowhere else | Trusting the prompt layout without measuring it |
| D9 | Vendor tests as code | `vendor-lab` (01) runs the 14.4 and 10.14 tests through the production adapters and writes scoring sheets as CSV; the decision rules are in this document, section 4.6 [DECISION, PRD-v2 14.4, 10.14] | The winners drop into `vendors.yaml` with no new code; the sheets are the evidence Muath signs | Listening in vendor playgrounds (different voices, no timestamps, no cost rows) |
| D10 | Two voice vendors wired, one contract first | Both blind-test finalists are implemented in week 1 (pipeline D9); a paid tier is bought only for the winner, the runner-up stays on pay-as-you-go until the first failover proves it [DECISION, PRD-v2 14.3] | Two minimum commitments for a product with 100 learners is waste; pay-as-you-go keeps the understudy warm | Two enterprise contracts (year two, at 10,000 learners) |
| D11 | Reconciliation | A monthly job compares `vendor_calls` sums with each vendor's billing (Anthropic through the Usage and Cost Admin API; others by CSV upload) and alerts above 5% variance [DECISION] | Without it, a wrong row in `prices.yaml` goes unnoticed for a quarter | Trusting the price file |
| D12 | What the learner sees | Nothing. No cost, no "heavy user" message, no throttle text; the allowance (PRD-v2 3.6) is the only learner-facing limit and it is a product rule, not a cost rule [DECISION, law 1, 11] | Cost is ours to manage | Any cost-driven message to a learner |

---

## 2. Requirements this domain implements

| PRD-v2 part | Requirement | Where in this document |
|---|---|---|
| 1.4 | Budget about $0.60 per session in the beta; scale target $0.30 to $0.35; stop line $1.00 with no plan; cost tracing on every model, voice and recognition call from the first learner | 4.1 to 4.4 (tracing), 4.5 (alarms), 6 (model) |
| 14.1 | Cost tracing is code, not AI | 3, 4 |
| 14.3 | Stack defaults; thin adapters; two voice vendors wired from the start; Gemini 3.8 doubling 2027-01-01; Hume shutdown 2026-11-13; Langfuse logging every call with cost and learner-model version | 4.2 (price book), 4.7 (adapters and fallback), 4.8 (risk calendar), 4.3 (Langfuse) |
| 14.4 | Voice blind test (5 Saudi, 5 native English listeners), the 30-clip recognizer test, 50 scripted calls | 4.6 (procedures and scoring sheets) |
| 14.5 | Cost per session = teacher share, writing, fitting, editing, all audio, call and round two, re-transcription, notes, chat, after-session pass, a quarter of the weekly proof; traced per role, per vendor, per learner; reported weekly; next to heavy-use outliers | 4.4 (roll-ups and the weekly report), 6 (the itemized model) |
| 10.14 | 30 real-learner clips through each streaming and batch recognizer; error survival, filler retention, hallucinations near pauses, code-switch handling; winner per role and the confidence threshold | 4.6.3 |
| 15 | Voice vendor outage: second vendor within the same day's production | 4.7 (fallback order), 5 |
| 16.1 | Gate: cost per session under $0.60; stop and rethink over $1.00 with no plan | 4.5 |
| 16.2 | Minutes per day: heavy-use outliers flagged, a warning light never a goal | 4.4.3 |
| 19.2 | Week 1: cost tracing; exit: measured cost per session and a costed path to $0.35 or less | 7, 6.4 |
| 2.1 | Sample episode cost ceiling $0.05 | 4.5 (per-kind ceilings) |
| 12.5, 12.6 | Data rules for a processor holding learner text (Langfuse); deletion | 4.3.4 |
| Laws 1, 11; trust 2 | No cost-driven surface or message to the learner | D12 |

Laws that bind the design directly: law 1 (no numbers that fill or target; cost dashboards are internal only), law 11 (the allowance is the only cap; cost never shortens a learner's day), trust promise 2 (no cost-driven re-engagement or throttling messages).

---

## 3. Architecture

### 3.1 Components

| Component | Kind | Owner | Job |
|---|---|---|---|
| `forone.adapters.tracing` | Python module (middleware) | this domain | Wraps every adapter call: times it, extracts units, prices them from `price_book`, writes `vendor_calls`, emits the Langfuse observation, enforces the spend guard |
| `forone.adapters.prices` | Python module plus `prices.yaml` | this domain | Loads the price file into `price_book`; `price_for(vendor, model, unit, pricing_mode, at)` |
| `price_book` | Postgres table | this domain | Dated unit prices |
| `vendor_calls` | Postgres table (monthly partitions) | this domain | One row per vendor call |
| `session_costs`, `learner_costs_daily`, `role_vendor_costs_daily` | Postgres tables, filled by `cost/rollup` | this domain | Roll-ups per session, per learner-day, per role-vendor-day |
| `cost_guard` | One row in `vendor_config` (`key='spend_mode'`) plus the `cost/alarms` function | this domain | Spend modes and alarms |
| `cost/rollup`, `cost/alarms`, `cost/weekly-report`, `cost/reconcile-monthly` | Inngest functions in `workflows` | this domain | Roll-ups every 15 minutes; alarms every 15 minutes; report Mondays 06:00 Asia/Riyadh; reconciliation on the 2nd of each month |
| `vendor-lab` | CLI in the monorepo (01) | this domain with the call and pipeline domains | Runs the 14.4 and 10.14 tests through the production adapters, writes scoring sheets |
| `/admin/cost` | One `sqladmin` page in `api` (01's admin pages) | this domain | Last 7 days by role, vendor, learner; outliers; spend mode; price book version |
| Langfuse Cloud EU | Managed | this domain owns conventions; the security domain approves the processor | Traces with prompts, completions, usage, cost, learner-model version |
| Anthropic Usage and Cost Admin API | Vendor API | this domain | Monthly reconciliation for the Anthropic lines |

### 3.2 Data flow, described as a diagram

Draw four lanes left to right: **callers**, **adapter layer**, **cost stores**, **consumers**.

1. Callers: `workflows` (teacher, writer, fitter, editor, voice studio, re-listen, analyst, memory keeper, Salma notes, proof producer, rater), `call-worker` (streaming STT, host LLM, call TTS, talkback resolver, Salma TTS), `api` (sample episode trigger, gloss misses). Each caller constructs a `CallMeta` (01's dataclass) carrying `learner_id`, `role`, `episode_id`, `call_id`, `session_id`, `learner_model_version`, `prompt_version`, `inngest_run_id`.
2. Adapter layer: `adapters.for_role(role)` returns the adapter chosen by `vendors.yaml` and overridden by `vendor_config`. Every public method is wrapped by `tracing.traced`. The wrapper starts a timer and a Langfuse observation, calls the vendor, reads the usage the adapter returns (`UnitUsage`), prices it with `price_for`, and writes one `vendor_calls` row in the same transaction as the caller's own write when there is one (the pipeline's `pipeline_steps` row, the worker's event batch) or in its own short transaction otherwise. On vendor error it writes the row with `outcome='error'` and the fallback adapter's call writes a second row with `fallback_from_vendor` set. Live-path rows are buffered in the worker and flushed every 5 seconds or at call end so the call never waits on Postgres.
3. Cost stores: `vendor_calls` (raw), then `cost/rollup` every 15 minutes into `session_costs` (keyed by `session_id`, with `cost_by_role` jsonb), `learner_costs_daily`, `role_vendor_costs_daily`. The pipeline's publisher reads `session_costs` for `episodes.cost_usd` and emits `episode.cost_recorded` (02); the call worker reads its own buffered sum into `calls.metrics.cost_usd` (03). `events.vendor_call_id` (04) points back to the row for model-produced events.
4. Consumers: `cost/alarms` (reads the roll-ups and `vendor_calls` for the last 15 minutes), `cost/weekly-report` (reads the roll-ups, writes a Markdown report to the ops channel and `/admin/cost`), `cost/reconcile-monthly` (reads `vendor_calls` and the vendors' billing), Langfuse (receives the same observation with the prompt and completion text; never audio).

A fifth element sits above the lanes: `price_book`, read by the adapter layer and written only by migrations from `prices.yaml`.

### 3.3 Where the cost of one session comes from

One daily session on the recommended stack produces about 60 `vendor_calls` rows: 1 teacher, 1 writer, 1 to 3 rewrites, 2 fitter, 1 to 2 editor, 1 embedding, 4 to 6 TTS jobs (scenes, article, recap), 1 alignment (if needed), 1 re-listen ASR, 0 to 10 gloss misses, about 25 host turns (each a `text` row), 1 streaming STT row per stream (2), 25 call TTS rows, 0 to 3 talkback rows, about 25 verbatim rows (per turn, 05), 1 pronunciation, 2 analyst, 1 memory keeper, 1 Salma notes, 1 to 2 polish TTS, 3 to 5 chat host, 0 to 1 margin note. All carry `session_id`, so `session_costs` is one aggregate.

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
    """Cached 60 s from vendor_config. Callers that can degrade read it (section 4.5)."""

def price_for(vendor: str, model: str, unit: str, pricing_mode: str, at: datetime) -> Decimal: ...
```

```sql
-- what other domains read
select cost_usd, cost_by_role from session_costs where session_id = $1;
select learner_id, day, cost_usd, sessions, minutes_heard, minutes_spoken from learner_costs_daily where day >= $1;
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
  session_id            uuid,
  episode_id            uuid,
  call_id               uuid,
  inngest_run_id        text,
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
  episode_kind          text                                   -- daily | swap | return | pilot | sample | fallback | proof | canary
) partition by range (occurred_at);
-- monthly partitions created by retention/daily (01), same as events
create index on vendor_calls (session_id) where session_id is not null;
create index on vendor_calls (learner_id, occurred_at);
create index on vendor_calls (role, vendor, occurred_at);
create index on vendor_calls (occurred_at) where outcome <> 'ok';
```

Rules:
- Row-level security by `learner_id` as in 04, with a `forone_cost` role allowed to read across learners for roll-ups and reports (the only cross-learner read path besides the gloss cache and opt-in research set; the security domain approves it).
- `units` is the raw usage the vendor reported, never derived. Where a vendor reports nothing (streaming TTS by the second), the adapter counts the unit itself and sets `units.estimated = true`.
- Deletion: `learner/delete` (04) aggregates a learner's rows into `learner_costs_daily` with `learner_id = null, deleted_learner_bucket = true` before deleting them, so totals survive.
- Retention: raw rows 13 months (one year of comparisons plus one), roll-ups forever.

### 4.2 `prices.yaml` and `price_book`

```yaml
# packages/adapters/prices.yaml  (every row: who, what, unit, price, dated; the file is the pull-request surface)
version: 2026-10-17
rows:
  # Anthropic, API reference cached 2026-10-06. Cache write = 1.25x input (5-minute TTL); batch = 50% of every token.
  - {vendor: anthropic, model: claude-opus-5-5,   unit: input_tokens,       usd_per_million: 4.00,  valid_from: 2026-10-06, source: anthropic-pricing}
  - {vendor: anthropic, model: claude-opus-5-5,   unit: output_tokens,      usd_per_million: 20.00, valid_from: 2026-10-06}
  - {vendor: anthropic, model: claude-opus-5-5,   unit: cache_read_tokens,  usd_per_million: 0.20,  valid_from: 2026-10-06}
  - {vendor: anthropic, model: claude-opus-5-5,   unit: cache_write_tokens, usd_per_million: 5.00,  valid_from: 2026-10-06}
  - {vendor: anthropic, model: claude-sonnet-5-5, unit: input_tokens,       usd_per_million: 2.00,  valid_from: 2026-10-06}
  - {vendor: anthropic, model: claude-sonnet-5-5, unit: output_tokens,      usd_per_million: 10.00, valid_from: 2026-10-06}
  - {vendor: anthropic, model: claude-sonnet-5-5, unit: cache_read_tokens,  usd_per_million: 0.20,  valid_from: 2026-10-06}
  - {vendor: anthropic, model: claude-sonnet-5-5, unit: cache_write_tokens, usd_per_million: 2.50,  valid_from: 2026-10-06}
  - {vendor: anthropic, model: claude-haiku-5-5,  unit: input_tokens,       usd_per_million: 0.10,  valid_from: 2026-10-06, note: "prompts up to 100K tokens; 0.50 above"}
  - {vendor: anthropic, model: claude-haiku-5-5,  unit: output_tokens,      usd_per_million: 0.50,  valid_from: 2026-10-06}
  - {vendor: anthropic, model: claude-haiku-5-5,  unit: cache_read_tokens,  usd_per_million: 0.01,  valid_from: 2026-10-06, assumption: "0.1x input; verify"}
  - {vendor: anthropic, model: claude-haiku-5-5,  unit: cache_write_tokens, usd_per_million: 0.125, valid_from: 2026-10-06}
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
  - {vendor: openai,  model: text-embedding-3-small, unit: input_tokens, usd_per_million: 0.02, valid_from: 2026-10-09}
  - {vendor: livekit, model: cloud-ship, unit: participant_minutes, usd_per_unit: 0.0010, valid_from: 2026-10-16, assumption: "01 flags this rate for verification"}
  - {vendor: aws,     model: s3-egress,  unit: gigabytes, usd_per_unit: 0.09, valid_from: 2026-10-16}
```

```sql
create table price_book (
  id serial primary key, vendor text not null, model text not null, unit text not null,
  pricing_mode text not null default 'standard', usd_per_unit numeric(14,9) not null,
  multiplier numeric(6,4), valid_from date not null, valid_to date, source text, note text,
  file_version text not null, unique (vendor, model, unit, pricing_mode, valid_from));
```

`price_for` picks the row with the greatest `valid_from <= at` and applies the vendor's `pricing_mode` multiplier row when the call's mode is `batch`. A call priced with a row older than 120 days raises a `price_stale` warning in the weekly report; a call with no matching row is priced at zero, written with `outcome='ok'` and `error_code='unpriced'`, and counted in the alarms (section 4.5) so a new model never silently costs nothing.

The 2027-01-01 doubling is represented exactly as 01 and 02 asked: a second dated row. The weekly report of 2026-12-28 carries a "what this week would have cost at next week's prices" column so the jump is seen before it happens.

### 4.3 Langfuse conventions

**4.3.1 Trace identity.** One trace per unit of work, named and keyed so a trace can be found from any id in Postgres:

| Unit of work | Trace name | `trace_id` | `session_id` | `user_id` |
|---|---|---|---|---|
| Episode production | `episode` | `episode_id` | `session_id` | `learner_id` |
| Live call | `call` | `call_id` | `session_id` | `learner_id` |
| After-session pass | `after_pass` | `{session_id}:after` | `session_id` | `learner_id` |
| Onboarding (A3 to A8) | `onboarding` | the pre-account session id (06) | same | the pre-account learner id, re-keyed at A9 |
| Weekly proof | `proof` | `proof_id` | null | `learner_id` |
| Sample episode | `sample` | `sample_id` | null | null (anonymous) |
| Canary, vendor-lab | `canary`, `vendor_lab` | run id | null | null |

Observations are named `{role}.{capability}` (`host.text`, `episode_tts.tts`, `verbatim_stt.stt_verbatim`). LLM calls are Langfuse generations with `usage` and `cost` set from the same numbers as `vendor_calls` (so the two never disagree), plus `metadata`: `learner_model_version`, `prompt_version`, `vendors_yaml_sha`, `price_book_ids`, `pricing_mode`, `episode_kind`, `spend_mode`. Tags: `env`, `role`, `vendor`, `pricing_mode`.

**4.3.2 What is logged.** Prompts and completions in full for text roles (the point of the tool); for TTS the input text and the voice id, never the audio; for STT the output text, never the audio; for pronunciation the reference sentence and the score object. The learner's name appears inside prompts (the host brief carries it); that is learner content, allowed under the topology's processor approval (open item 01 #2).

**4.3.3 Scrubbing.** Before emission the middleware runs `forone.learner.pii.scrub_for_processor` (04) over metadata and over any field classified as identity: email, phone, birth date, payment ids never leave. Prompt text is not scrubbed (it would destroy the debugging value); it is covered by the processor approval.

**4.3.4 Sampling and deletion.** Beta: 100% of observations. Scale (10,000 learners, about 400,000 observations a day): 20% of `episode` and `call` traces, 100% of `after_pass`, `proof`, `onboarding` and anything whose role is `analyst`, `memory_keeper`, `rater` or `proof_producer` (these feed claims; PRD-v2 10.10 "openable" evidence must be debuggable). Sampling is by trace, decided once at trace start from a hash of the trace id, so a sampled episode is complete. Deletion: `learner/delete` (04) calls Langfuse's deletion by `user_id`; this domain owns the adapter `langfuse_admin.delete_user(user_id)` and the daily retry until `deletion_ledger.verified_empty` (04). [ASSUMPTION] Langfuse Cloud exposes per-user deletion through its API in the plan we buy; verified in week 1 with a test user, and if it does not, the fallback is self-hosting (section 8).

**4.3.5 Cost of Langfuse itself.** Beta: Core plan, $0 to $59 a month (01). At 10,000 learners with the sampling above: about 100,000 observations a day, inside a Pro or Team plan at a few hundred dollars a month; the 01 estimate of $500 a month stands.

### 4.4 Roll-ups, the weekly report and outliers

**4.4.1 Roll-up tables.**

```sql
create table session_costs (
  session_id uuid primary key, learner_id uuid not null, episode_id uuid, local_date date not null,
  episode_kind text not null, cost_usd numeric(10,6) not null,
  cost_by_role jsonb not null,            -- {"teacher":0.0812,"writer":0.0540,...}
  cost_by_vendor jsonb not null,
  cost_by_line jsonb not null,            -- the nine PRD 14.5 lines, section 6.1 mapping
  pricing_escalated bool not null default false,   -- batch cancelled at a cut line (02)
  fallback_used bool not null default false,
  minutes_heard numeric(6,2), minutes_spoken numeric(6,2),
  updated_at timestamptz not null default now());

create table learner_costs_daily (
  learner_id uuid, day date, cost_usd numeric(10,6) not null, sessions int not null,
  calls int not null, swaps int not null, minutes_heard numeric(6,2), minutes_spoken numeric(6,2),
  deleted_learner_bucket bool not null default false, primary key (learner_id, day));

create table role_vendor_costs_daily (
  day date, role text, vendor text, pricing_mode text, calls int, errors int, cost_usd numeric(12,6),
  units jsonb, cache_hit_rate numeric(5,4), p95_latency_ms int, primary key (day, role, vendor, pricing_mode));
```

`cost/rollup` runs every 15 minutes (Inngest cron), takes `vendor_calls` rows with `occurred_at > last_watermark`, and upserts the three tables. A session's cost is final 24 hours after the session closes (the proof share and late verbatim rows arrive after the call); `session_costs.updated_at` says when it last moved. The weekly proof's cost is divided by the learner's sessions in that week and added to each session's `cost_by_line.proof_share` (PRD-v2 14.5 "a quarter of the weekly proof" assumes four sessions; dividing by the actual count is the same rule applied honestly).

The nine PRD lines are computed from roles by this mapping, which is also what the report prints:

| PRD-v2 14.5 line | Roles summed |
|---|---|
| Teacher | `teacher` |
| Writer | `writer` (including rewrites) |
| Fitter, glosses, editor | `fitter`, `gloss`, `editor`, `embeddings` |
| Voice studio | `episode_tts`, `aligner`, `relisten_stt`, media mix |
| Call (main and round two) | `streaming_stt`, `talkback_stt`, `host`, `call_tts`, `talkback_resolver`, `salma_live`, `salma_tts` (in-call), `livekit`, worker compute |
| Re-transcription and pronunciation | `verbatim_stt`, `pronunciation` |
| Salma's notes and chat | `salma_text`, `chat_host`, polish-line `salma_tts`, `margin_note` |
| Analyst and memory keeper | `analyst`, `memory_keeper`, `rater` (amortized), conversation-chunk `embeddings` |
| Proof share and hosting | `proof_producer`, proof `salma_tts` (divided), `s3_egress`, feed encode |

Onboarding (Salma A3, pilot, first call) and the sample episode are not sessions. They are rolled into `learner_costs_daily` on the day they happen and reported as **acquisition cost per learner** on a separate line (about $0.45 at list prices: Salma and first call $0.10 from 03, pilot about $0.30 at standard pricing from 02, sample $0.035). They are deliberately not divided into the per-session number, so the per-session gate (PRD-v2 16.1) measures the steady state.

**4.4.2 The weekly report.** `cost/weekly-report` runs Mondays 06:00 Asia/Riyadh for the previous Monday-to-Sunday week, writes Markdown to the ops channel (through the evaluation domain's `ops.notify`) and stores it at `cost_reports(week, body, csv)` for `/admin/cost`. Sections, in order, each a table:

1. **Headline:** sessions, mean cost per session, median, p90, against $0.60 and $1.00; the same four numbers for the previous week; the share of sessions over $1.00.
2. **By PRD line** (the nine lines plus acquisition and fixed infrastructure): mean per session this week, last week, the PRD estimate (section 6.1) and the delta.
3. **By role and vendor:** calls, errors, cost, units, cache hit rate, p95 latency, share of calls on batch, share escalated at a cut line.
4. **By episode kind:** daily, swap, return, pilot, fallback: count and mean cost.
5. **Heavy-use outliers** (4.4.3).
6. **Vendor health:** failovers this week (`voice.vendor_failover`, STT secondary use), unpriced calls, stale prices, Langfuse sampling rate.
7. **Next week's prices:** from 2026-12-07, the headline recomputed with every `price_book` row whose `valid_from` is within 30 days (the 2027-01-01 doubling shows here four weeks early).
8. **Reconciliation status** (monthly, 4.4.4).

The query behind section 2, so Muath can run it by hand:

```sql
select line, round(avg((cost_by_line->>line)::numeric), 4) as mean_usd, count(*) as sessions
from session_costs, jsonb_object_keys(cost_by_line) as line
where local_date between $1 and $2 and episode_kind in ('daily','swap','return','fallback')
group by line order by mean_usd desc;
```

**4.4.3 Heavy-use outliers (PRD-v2 16.2).** A learner is flagged in the report when, over the trailing 7 days, any of: `cost_usd` above 3 times the cohort median, minutes heard above 3 times the cohort median, or any single day above `cost.daily_learner_cap_usd` ($2.50). The flag goes to the report and to `/admin/cost` only. It triggers no message, no throttle and no change in the learner's allowance (law 11: what is already made can be heard as often as wanted; re-listens cost egress only, about $0.001 each). The one action it can lead to is a human reading the trace to check for a bug (a loop in the chat, a swap storm), because a heavy user in this product is a success, not a problem.

**4.4.4 Reconciliation.** `cost/reconcile-monthly` on the 2nd of each month: pulls the Anthropic Usage and Cost report for the organization through the Admin API (an admin key, `ANTHROPIC_ADMIN_API_KEY`, read-only, stored in Secrets Manager) and compares it to `sum(cost_usd) where vendor='anthropic'` by model; for Google, ElevenLabs, Inworld, Soniox, Deepgram, AssemblyAI, Speechace and LiveKit, reads a CSV Muath uploads at `/admin/cost/invoices` (vendor, period, usd) within 10 days of each invoice. Writes `vendor_invoices(vendor, period, invoiced_usd, traced_usd, variance_pct)`; variance above 5% raises a `cost.alarm_raised{kind: reconciliation}`. [ASSUMPTION] the Admin API's cost report groups by model and workspace, which is enough; per-key grouping is not needed because the beta runs one workspace per environment. Automating the other vendors' invoices is P1 or later; eight CSV uploads a month is cheaper than eight scrapers.

### 4.5 Alarms, the spend guard and the stop line

**4.5.1 Alarm catalog.** `cost/alarms` runs every 15 minutes; each alarm is an event `cost.alarm_raised {kind, severity, value, threshold, learner_id?, role?, vendor?}` consumed by the evaluation domain's paging (`ops.page` for `page`, `ops.notify` for `notify`). Every alarm is idempotent per (kind, subject, day).

| Kind | Condition | Severity | Config key (default) |
|---|---|---|---|
| `session_over_alert` | A `session_costs.cost_usd` crosses the alert line | notify | `SESSION_COST_ALERT_USD` (1.00, from 01) |
| `session_over_budget_trend` | Trailing 7-day mean per daily session above budget | notify (weekly repeat) | `cost.session_budget_usd` (0.60) |
| `session_warn_trend` | Trailing 7-day mean above the warning line | page (once a week) | `cost.session_warn_usd` (0.80) |
| `stop_line` | Trailing 7-day mean above the stop line, or 20% of sessions above it | page; opens a 48-hour plan window (4.5.3) | `cost.stop_line_usd` (1.00) |
| `daily_spend_80` | Environment spend today above 80% of the daily cap | notify; `spend_mode` → `conserve` | `SPEND_CAP_USD_PER_DAY` (50 beta; recomputed as learners × $1.50 from 2026-12-07) |
| `daily_spend_100` | Spend above the cap | page; `spend_mode` → `halt` for new on-demand generation only | same |
| `kind_ceiling` | A sample episode over $0.05, a pilot over $0.40, a swap over $0.60 | notify | `cost.kind_ceilings` |
| `cache_hit_low` | A text role's `cache_read_tokens / (cache_read + input + cache_write)` under 85% over 24 h, at least 50 calls | notify | `cost.cache_hit_floor` (0.85) |
| `unpriced` | Any `error_code='unpriced'` row | notify | |
| `price_stale` | A price row older than 120 days used | notify (weekly) | |
| `escalation_rate` | More than 20% of daily episodes escalated from batch at a cut line in a day | notify | `cost.escalation_rate_max` (0.20) |
| `vendor_error_rate` | A vendor's error rate above 5% over 10 minutes (shared with `vendor/health`, 01) | page | |
| `learner_daily_cap` | A learner's day above `cost.daily_learner_cap_usd` | notify (report only) | 2.50 |
| `reconciliation` | Monthly variance above 5% | notify | `reconcile.variance_alert_pct` (5) |

**4.5.2 Spend modes.** `spend_mode` lives in `vendor_config` (`key='spend_mode'`), read by callers through `tracing.spend_mode()` (cached 60 seconds), set by `cost/alarms` and by hand from `/admin/vendors`. It returns to `normal` at the start of the next day in the environment's clock unless an alarm holds it.

| Mode | Pipeline (02) | Call (03) | After-session (05) | Client-visible effect |
|---|---|---|---|---|
| `normal` | as designed | as designed | as designed | none |
| `conserve` | teacher falls to `claude-sonnet-5-5` batch; writer rewrites capped at 1 round; batch TTS forced where available; swap and return episodes still made; canary episodes skipped | host falls to `claude-haiku-5-5`; round two (P1) not offered on Today | unchanged (claims and notes are never degraded for cost) | none the learner can tell; a human reads the week's episodes (6.8) with extra care |
| `halt` | tomorrow's episodes already queued finish; no new on-demand generation except return episodes (a returning learner must get a show, PRD-v2 3.8); the sample endpoint returns the cached sample text route with a plain "try again tomorrow" page (06 owns the copy) | calls continue (a learner mid-day is never cut off) | unchanged | a swap request shows Salma's one plain sentence already specified for the allowance (PRD-v2 3.6 #6 wording, reused: "One new episode a day...") and no swap; nothing else |

`halt` is for a runaway (a bug generating in a loop), not for budgeting; in three weeks of beta it should never fire. If it fires on a normal day, the cap is wrong and is raised.

**4.5.3 The stop line (PRD-v2 1.4, 16.1).** The stop line is a rule about plans, not about service. When `stop_line` fires, the on-call engineer and Muath get the page with the week's section-2 table attached. Within 48 hours Muath records a plan in `cost_reports` (`plan_text`, `plan_by`) naming which levers of section 6.3 are pulled and the expected per-session effect; the next weekly report prints the plan and the measured effect. If no plan is recorded within 48 hours, the alarm repeats daily. This is the "no costed plan to reduce it" condition made operational; the decision to stop and rethink stays with Muath, as PRD-v2 16.1 says.

### 4.6 Vendor tests as runnable procedures (PRD-v2 14.4, 10.14)

All three tests run from `vendor-lab`, use the production adapters (so every render and transcription is also a `vendor_calls` row tagged `service='vendor-lab'`), and write CSV scoring sheets under `vendor-lab/results/{date}/`. The decision rules are code (`vendor-lab decide`) so the winner is reproducible from the sheets. Muath signs the result by committing `vendors.yaml` with the winners by 2026-11-13.

**4.6.1 Voice blind test (14.4 #1), build week 1 to 2.**

Materials: the Milestone 0 two-host sample script (05-prompts.md, 10 lines, about 650 characters) extended to 90 seconds with four more lines in the same register, in both accents; three candidate voices per host per accent per vendor from the package voice pools (PRD-v2 7.1), rendered with the same speech rate (1.0) and no style tags; one 20-second Salma passage (Arabic, the A3 opening lines) rendered on each Arabic voice candidate: Gulf-dialect voices and neutral educated voices (PRD-v2 7.3).

```
vendor-lab tts render --script lang/ar-en/tests/two-host-90s.{british,american}.txt \
    --vendors gemini,inworld,elevenlabs --voices-from lang/ar-en/voices.yaml --rate 1.0 --out results/2026-11-05/tts/
vendor-lab tts render --script lang/ar-en/tests/salma-20s.ar.txt --vendors gemini,inworld,elevenlabs --voices-from lang/ar-en/voices.yaml --out results/2026-11-05/salma/
vendor-lab tts sheet  --from results/2026-11-05/tts/ --raters 10 --design latin-square   # prints 10 playlists and the blank sheet
```

Technical gate, run first, automatic (a vendor that fails any row is excluded before anyone listens):

| Check | Gate | Why |
|---|---|---|
| Two-speaker or per-line rendering of a full scene | works | pipeline 4.8 |
| Word timestamps returned, or alignment cost booked | either | 02 D10 |
| Rate control between 0.85 and 1.0 | vendor or `atempo` | PRD-v2 5.1 |
| Render p95 for a 90-second scene | under 20 s | on-demand kinds, 02 4.13 |
| Streaming TTFB p95 (call voice) | under 300 ms | 03 D8 `tts_stream_tfb_gate_ms` |
| Concurrent streams on the tier we would buy | at least 20 | beta peak of 15 concurrent calls |
| Name respelling or phoneme tag accepted | one of them | 02 name pronunciation |
| Batch endpoint | noted, not gated | lever 6.3 #3 |
| Cost per 10 minutes of episode audio at list | printed | D5 |

Listening protocol: 10 raters (5 Saudi learners from the Milestone 0 pool who are not in the beta cohort, 5 native English speakers, paid), each hears every vendor's rendering of one accent (British and American split 5 and 5 across raters) in a Latin-square order with vendor names hidden, on earphones, on a phone. Per rendering they answer: naturalness 1 to 5; "would you listen to this on your commute?" yes or no; for native raters, accent authenticity 1 to 5; one free-text line. Then one forced pairwise choice between each pair of vendors (3 pairs). Salma: 5 Saudi raters, same form, plus "which Arabic sounds like someone who would produce my show?" forced choice between the best Gulf and the best neutral voice.

Scoring sheet columns (`tts-sheet.csv`): `rater_id, rater_group(saudi|native), accent, vendor_blind_code, voice_candidate, naturalness_1_5, commute_yes_no, accent_1_5, pairwise_wins, free_text`. `vendor-lab decide tts` computes per vendor: mean naturalness (both groups), commute-yes share, mean accent (native group), pairwise win rate, list cost per 10 minutes.

Decision rule (D5, PRD-v2 14.5 "the cheapest voice that passes"): a vendor passes if commute-yes is at least 60% and its mean naturalness is within 0.3 of the best vendor's. Among passing vendors the cheapest at list price wins; the next cheapest passing vendor is the runner-up and provides the understudy voices (02 D9); if only one passes, the runner-up is the best non-passing vendor and the on-air announcement text for a failover is written to say the voice is temporary. If ElevenLabs is the only passing vendor, the win is conditional on a negotiated rate at or below $25 per million characters by 2026-11-20 [OPEN for Muath]; until then Gemini (the cheapest) is configured as primary and ElevenLabs as runner-up. Salma's voice is chosen by the forced choice (majority of 5), ties to neutral Arabic because it ages better across the Gulf and Levant markets (PRD-v2 19.4).

**4.6.2 Call latency (14.4 #3).** Owned by the call domain's `tools/call-bench` (03, 4.13). This domain adds two columns to its report, read from `vendor_calls`: cost per call by line, and the cache hit rate of the host role across the 50 calls (gate: at least 90%, since every turn after the first should read the cached brief). A run whose host cache hit rate is under 90% fails the cost gate even if latency passes, because the $0.034 host input line in 03's estimate assumes it.

**4.6.3 The recognizer test (10.14), before build week 2 (deadline 2026-11-08).**

Materials from Milestone 0 (PRD-v2 19.1 #7): 30 clips of real Saudi learners, 20 to 90 seconds each, with consent, chosen to cover at least 10 clips with mid-clause pauses over 1.5 s, at least 8 with Arabic code-switching, at least 5 with fillers and restarts, and the rest ordinary turns. Ground truth per clip, hand-made by Muath: a verbatim human transcript (fillers kept), the list of learner errors with their exact span (from the Milestone 0 tags), the filler spans, the Arabic spans.

```
vendor-lab stt run --clips m0/clips/ --truth m0/truth.jsonl \
    --streaming soniox,deepgram,assemblyai --batch assemblyai,elevenlabs_scribe \
    --out results/2026-11-06/stt/
vendor-lab stt decide --from results/2026-11-06/stt/
```

Per clip and vendor the runner records (`stt-sheet.csv`): `clip_id, vendor, mode(streaming|batch), wer_vs_human, errors_total, errors_survived, errors_corrected_silently, fillers_total, fillers_kept, hallucinated_phrases, hallucinated_near_pause, code_switch_words_total, code_switch_words_correct_language, word_timings(bool), confidences(bool), streaming_final_latency_ms, cost_usd`. "Survived" means the learner's error appears verbatim in the transcript; "corrected silently" means the transcript shows the correct form where the learner was wrong (the failure mode the voice lens warned about). Hallucination near a pause is a phrase in the transcript with no counterpart in the human transcript, inside or right after a pause over 1.5 s.

Decision rules:
- **Batch verbatim winner:** highest mean error survival rate among vendors with filler retention at least 80% and at most 1 hallucinated phrase per 30 clips; ties broken by cost. Minimum to be usable at all: error survival at least 85%; if no vendor reaches it, the assessment domain's confidence filter must be stricter and the claim gate stays on first-ever events and words owned until a second test (PRD-v2 10.10 already allows this).
- **Streaming winner:** lowest WER with code-switch words in the correct language at least 80% and final-after-end-of-speech p95 under 400 ms (03's STT budget); ties by cost. The talkback stream (`talkback_stt`) can use a different vendor from the host stream if code-switch handling differs.
- **Confidence threshold** (PRD-v2 10.2 #4, Part 18 #10): on the batch winner, sort every tagged error by the recognizer's mean word confidence over its span and find the lowest threshold at which the precision of "a transcribed deviation is a real learner error" reaches 0.8; written to `packages/language/ar-en/recognizer.yaml` as `confidence_threshold` with the test date. The streaming winner's threshold is computed the same way but used only for planning signals.
- The recognizer error by first language (PRD-v2 10.14 last sentence) starts here: the clips' WER by vendor is the day-one baseline the evaluation domain tracks.

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
# packages/adapters/vendors.yaml (this domain's view of every role's chain; models as 01 and 03 spell them)
roles:
  teacher:          {vendor: anthropic, model: claude-opus-5-5,   pricing: batch, pricing_escalation: [batch, standard],
                     fallback: [{vendor: anthropic, model: claude-sonnet-5-5, pricing: standard}], degrade: rule_based_brief}        # PRD 9.8
  writer:           {vendor: anthropic, model: claude-sonnet-5-5, pricing: batch, pricing_escalation: [batch, standard],
                     fallback: [{vendor: google, model: gemini-3.8-flash, pricing: standard, note: "editor must switch to anthropic"}], degrade: fallback_episode}   # PRD 6.3
  fitter:           {vendor: anthropic, model: claude-haiku-5-5, fallback: [{vendor: google, model: gemini-3.8-flash}], degrade: code_only_coverage}
  gloss:            {vendor: anthropic, model: claude-haiku-5-5, fallback: [{vendor: google, model: gemini-3.8-flash}], degrade: ship_without_gloss_mark_miss}
  editor:           {vendor: google, model: gemini-3.8-flash, fallback: [{vendor: anthropic, model: claude-haiku-5-5, note: "breaks second-vendor rule; review item"}], degrade: code_checks_only}
  embeddings:       {vendor: openai, model: text-embedding-3-small, fallback: [], degrade: skip_similarity_check_review_item}
  episode_tts:      {vendor: VOICE_WINNER, fallback: [{vendor: VOICE_RUNNER_UP, note: "understudy voice; on-air announcement"}], degrade: wait_and_retry_until_t_switch_then_yesterday_stays}
  aligner:          {vendor: elevenlabs_alignment, fallback: [{vendor: whisperx_local}], degrade: sentence_level_timings}
  relisten_stt:     {vendor: VERBATIM_WINNER, fallback: [{vendor: VERBATIM_RUNNER_UP}], degrade: ship_unchecked_mark_review}
  host:             {vendor: anthropic, model: claude-sonnet-5-5, retries: 0,
                     fallback: [{vendor: anthropic, model: claude-haiku-5-5}, {vendor: google, model: gemini-3.8-flash}], degrade: voice_notes}   # PRD 5.4.10
  call_tts:         {vendor: VOICE_WINNER, retries: 0, fallback: [{vendor: VOICE_RUNNER_UP, note: "understudy"}], degrade: voice_notes}
  salma_tts:        {vendor: SALMA_WINNER, fallback: [{vendor: SALMA_RUNNER_UP}], degrade: text_bubble_only}
  streaming_stt:    {vendor: STREAM_WINNER, retries: 0, fallback: [{vendor: STREAM_RUNNER_UP}], degrade: voice_notes}
  talkback_stt:     {vendor: STREAM_WINNER, languages: [ar, en], code_switch: true, fallback: [{vendor: STREAM_RUNNER_UP}], degrade: talkback_unavailable_bubble}
  talkback_resolver:{vendor: anthropic, model: claude-haiku-5-5, retries: 0, fallback: [], degrade: cache_only}
  salma_live:       {vendor: anthropic, model: claude-sonnet-5-5, retries: 0, fallback: [{vendor: anthropic, model: claude-haiku-5-5}], degrade: typed_intake}
  verbatim_stt:     {vendor: VERBATIM_WINNER, fallback: [{vendor: VERBATIM_RUNNER_UP}], degrade: low_confidence_no_claims}   # PRD 5.4.11
  pronunciation:    {vendor: speechace, fallback: [{vendor: microsoft}], degrade: score_null}
  analyst:          {vendor: anthropic, model: claude-haiku-5-5, fallback: [{vendor: google, model: gemini-3.8-flash}], degrade: notes_header_only_retry_later}
  memory_keeper:    {vendor: anthropic, model: claude-haiku-5-5, fallback: [{vendor: google, model: gemini-3.8-flash}], degrade: retry_next_pass}
  salma_text:       {vendor: anthropic, model: claude-sonnet-5-5, fallback: [{vendor: anthropic, model: claude-haiku-5-5}], degrade: notes_header_only}
  chat_host:        {vendor: anthropic, model: claude-sonnet-5-5, fallback: [{vendor: anthropic, model: claude-haiku-5-5}], degrade: opener_only_then_quiet}
  proof_producer:   {vendor: anthropic, model: claude-sonnet-5-5, pricing: batch, fallback: [{vendor: anthropic, model: claude-sonnet-5-5, pricing: standard}], degrade: slow_week_template}
  rater:            {vendor: anthropic, model: claude-sonnet-5-5, pinned_until: 2026-12-31, fallback: [], degrade: code_metrics_only}   # PRD 10.11, 05
```

Two rules the middleware enforces regardless of the file: a `pinned_until` role refuses any fallback or `vendor_config` override while pinned (05); and the writer and editor may not resolve to the same vendor in one run unless the row carries a `note` (PRD-v2 6.1), in which case the middleware tags the episode `review_items(kind='same_vendor_edit')` for the human reviewer (6.8).

### 4.8 Vendor risk calendar

| Date | Event | Exposure | Action and owner |
|---|---|---|---|
| 2026-10-12 | ElevenLabs v4 launch promotion ended | List price $80 per million characters applies to any ElevenLabs render | `prices.yaml` carries the list price; D5 rule |
| 2026-11-08 | 10.14 recognizer test deadline (before build week 2) | Verbatim and streaming winners unknown until then | `vendor-lab stt`; Muath's truth file by 2026-11-04 |
| 2026-11-13 | Hume shuts its voice APIs | None if nothing imports Hume | CI check: no `hume` dependency in the lockfile; `vendors.yaml` schema rejects `vendor: hume` |
| 2026-11-13 | Voice vendor decision (14.4) due | The $0.18 voice line and the $0.03 to $0.08 call voice line | `vendors.yaml` committed with winners; paid tier bought for the winner only (D10) |
| 2026-11-16 | Payment processor decision (Part 18 #2) | Processor fees (about 3 to 4% web) are outside the AI cost but in the margin report | Fee schedule row in `prices.yaml` under `vendor: payments` for the margin section of the weekly report |
| 2026-11-17 | Google shuts older Cloud speech models | None (Gemini 3.8 Flash TTS is not among them) [ASSUMPTION; verify in week 1] | Week-1 check in `vendor-lab tts` against the deprecations page |
| 2026-11-20 | ElevenLabs negotiated-rate deadline if it won the blind test | Whether ElevenLabs can be primary | [OPEN for Muath] |
| 2026-12-07 | Beta starts; daily spend cap recomputed from learner count | Cap too low halts; too high hides a loop | `SPEND_CAP_USD_PER_DAY = max(50, learners × 1.50)` |
| 2026-12-28 | Weekly report prints next-week prices | First sight of the 2027-01-01 jump | Report section 7 |
| 2026-12-31 | Rater pin window ends | Re-pin for the next 4-week window (PRD-v2 10.11) | Assessment domain updates `pinned_until`; calibration set re-run |
| 2027-01-01 | Gemini 3.8 prices double (Flash text, Flash TTS; Live) | Editor +$0.015 a session; a Gemini-voiced session +$0.17 (episode voice +$0.135, call voice +$0.032) | Second dated rows already in `prices.yaml`; the costed path (6.4) treats post-doubling prices as the base case |
| 2027-01-06 | OpenAI deprecates its text-to-speech models | None (not used); the embeddings model is unaffected | Note only |
| 2027-01-10 | Beta gate review | Cost gate: under $0.60; stop over $1.00 with no plan | Report of 2027-01-11 is the gate evidence |
| Open-ended | Deepgram's promotional rate ends; Inworld pricing is young; Anthropic Haiku 5.5 tier above 100K-token prompts | Streaming STT, voice, and any prompt that grows past 100K tokens (the teacher brief must stay under it) | `price_stale` alarm after 120 days; `cache_hit_low` and a per-role input-token p95 in the report |

### 4.9 Contracts and quotas at 100 and 10,000 learners

Volumes assume 20 sessions a learner a month, one 6:30 call a session, a 6-minute episode plus 2.5 minutes of read-aloud and 1.5 of recap (10 minutes of produced audio), 7 minutes of learner audio re-transcribed, and anchors clustering so that peak concurrency is about 15% of the day's calls in one hour.

| Vendor | Unit | 100 learners (2,000 sessions/month) | 10,000 learners (200,000 sessions/month) | What to ask for |
|---|---|---|---|---|
| Anthropic | Tokens a day (all roles, cached reads included) | about 17M | about 1.7B; batch about 40% of it | Beta: usage tier with 1M-token-a-minute Sonnet limits (self-serve). Scale: a committed-spend agreement, higher Batch API queue limits, and a workspace per environment; about $50,000 a month of text at the floor stack |
| Voice vendor (winner) | Characters a month (episodes, read-aloud, recap, proof, call host turns) | about 20M | about 2B | Beta: the paid API tier that gives 20 concurrent streams (ElevenLabs Business or Inworld paid; Gemini paid tier with a TTS requests-per-minute quota raise). Scale: enterprise contract with a per-million-character rate; the voice line is the biggest negotiable line |
| Voice vendor (runner-up) | Same, only on failover and canaries | under 1M | about 50M (canaries plus failover days) | Pay-as-you-go; one weekly canary keeps the account live |
| Streaming STT | Concurrent streams at peak; minutes a month | 15 concurrent; about 16,000 min (two streams per call) | 600 concurrent; 1.6M min | Beta: a concurrency raise to 50 in week 1 (03). Scale: contract with concurrency 1,000 |
| Verbatim STT | Minutes a month | 14,000 (calls) + 20,000 (re-listen) | 3.4M | Scale: volume pricing below $0.003 a minute |
| Pronunciation | Utterances a month | 2,000 to 6,000 | 200,000 to 600,000 | Speechace plan sized to utterances; Microsoft as the secondary needs an Azure Speech resource in the home region or EU |
| LiveKit Cloud | Participant minutes a month | about 28,000 | about 2.8M | Beta: Ship plan. Scale: enterprise; the per-minute rate is the largest infrastructure line (01) |
| Langfuse | Observations a day | about 4,000 | about 100,000 after sampling | Beta: Core. Scale: Pro or Team, or self-host |
| Inngest | Steps a day | about 5,000 | about 500,000 | Beta: free or Pro. Scale: verify tier pricing; 01 names the switch rule (above $0.01 a session) |
| Alignment (if the voice winner lacks timestamps) | Minutes a month | 20,000 | 2M | Scale: a self-hosted aligner on one GPU task is cheaper than $0.0037 a minute above about 300,000 minutes a month (P1 or later) |
| Payment processor | Transactions | 100 to 350 | 10,000 to 30,000 | Outside this document except the fee row |

Quotas to request in build week 1 (so no test or canary is throttled): Anthropic rate tier for 1M tokens a minute on Sonnet and 200K on Opus and the Batch API enabled; the voice finalists' 20-stream concurrency; Soniox and Deepgram 50 concurrent streams; AssemblyAI 50 concurrent batch jobs; Speechace a developer plan; LiveKit Ship.

---

## 5. Failure modes, fallbacks and degraded modes

| Failure | Detection | Automatic response | What the learner notices | What this domain records |
|---|---|---|---|---|
| Vendor rejects or times out (any role) | middleware retry exhaustion | fallback chain (4.7), then the calling domain's `degrade` path | nothing, or the degraded surface that domain specifies | rows with `outcome='error'` then `'fallback_used'`; `vendor_error_rate` alarm at 5% |
| Both voice vendors down at production time | `episode_tts` chain exhausted | retry every 5 minutes until `t_switch` (02); then the pipeline marks the run failed and yesterday's episode stays (PRD-v2 3.6 #2 behaviour reused); `pipeline.human_page` | no new episode today; no notification | `escalation_rate` and `vendor_error_rate` alarms |
| Batch not back by a cut line | 02's poll loop | cancel and run standard; `pricing_escalated=true` | nothing | `escalation_rate` alarm if above 20% of the day; the saving lost is printed in the report |
| A price row missing for a new model or voice | `unpriced` rows | priced at zero, alarm | nothing | report line until `prices.yaml` is fixed and `cost/rollup --reprice --since` is run (re-prices rows from `units`, the reason `units` is raw) |
| Prompt cache silently broken (timestamp in a prefix, tool list reordered) | `cache_hit_low` | alarm with the role and the first hour it fell | nothing | the cost of the breakage computed as (expected cache reads × (input price − cache price)) |
| Spend loop (a bug re-running a step) | `daily_spend_80` then `_100` | `conserve` then `halt`; page | at most: no swap today | spend mode changes as `cost.spend_mode_changed` |
| Postgres write of `vendor_calls` fails in the live path | buffered writer error | rows kept in the worker's memory and retried; after call end, flushed to a local file and re-ingested by `cost/rollup` (`vendor_calls_spool` bucket) | nothing | a `spool_recovered` count in the report |
| Langfuse unreachable | SDK async queue errors | observations dropped after the queue fills (the SDK is fire-and-forget); `vendor_calls` is unaffected | nothing | `langfuse_dropped` count; the trace is reconstructable from `vendor_calls` plus the artifacts the pipeline stored |
| Langfuse deletion API fails for a deleted learner | `deletion_ledger.verified_empty=false` (04) | daily retry 30 days; alert | nothing | [OPEN for Muath] in 04 whether the "deleted" email waits for it |
| Reconciliation variance above 5% | `cost/reconcile-monthly` | alarm; the report names the vendor and the month | nothing | `vendor_invoices` row |
| Vendor announces a price change | a person reads it | a dated row in `prices.yaml` through a pull request; the weekly report's section 7 shows the effect before it lands | nothing | |
| A new learner cohort is heavier than modelled (more talk, longer calls) | `session_over_budget_trend` | nothing automatic; the levers in 6.3 are human decisions | nothing | the report shows which line moved |

The principle, repeated from 01: no learner ever sees a cost error. The cost domain degrades the product's own spending, never the learner's day.

---

## 6. Cost and performance against the budgets

### 6.1 The itemized model, beta stack, list prices

Unit assumptions behind every line (each is an `assumptions.yaml` key so Muath can recompute; section 6.5):

- Episode 6:00 min, article read-aloud 2:30, recap 1:30; 830 characters per minute of speech; 10 minutes of produced audio = 8,300 characters = 15,000 Gemini audio tokens (25 a second).
- Teacher: 14,000 input tokens (6,000 cache reads, 1,000 cache writes, 7,000 uncached), 6,000 output tokens including thinking. Writer: 12,000 input (7,000 cached), 6,000 output; rewrites 1.3 rounds of 9,000 input (7,000 cached) and 900 output at standard pricing. Fitter and gloss misses: 8,000 in, 3,000 out on Haiku. Editor: 1.2 calls of 9,000 in, 1,500 out on Gemini Flash. (All from 02, section 6, which this document adopts.)
- Call (03, section 6): 6:30 main call; 25 learner turns; host share 35% (1,900 characters); host cached reads 90,000 tokens, cache writes 4,000, uncached 3,000, output 1,500; 3 talkback asks; Soniox for 7 minutes on two streams; LiveKit 2 participants × 7 minutes.
- Round two [P1]: 2.5 minutes, used after 50% of sessions [ASSUMPTION].
- Verbatim: 7 minutes of learner audio; one pronunciation utterance.
- Notes and chat (05 and 03): Salma notes 3,000 in (2,000 cached), 400 out on Sonnet; two polish lines of 120 characters; chat host 5 messages of 4,000 in (3,000 cached), 150 out on Sonnet; one margin note.
- Analyst and memory keeper (05): $0.0035 of Haiku plus $0.0005 of embeddings plus the rater amortized.
- Proof (05): $0.06 a week divided by 4 sessions; hosting (06): $0.006 egress and feed encode.
- Swap: 5% of sessions have a swap at standard pricing, about $0.50 each [ASSUMPTION; 02 assumed 20% of learners, which is the same order].

Arithmetic (standard rate unless noted; batch = half):

| Line | Arithmetic | Gemini voice | Inworld voice | ElevenLabs v4 list | PRD-v2 14.5 |
|---|---|---|---|---|---|
| Teacher (Opus 5.5, batch) | standard: 7k × $4 + 6k × $0.20 + 1k × $5 + 6k × $20 per M = $0.028 + $0.0012 + $0.005 + $0.12 = $0.154; batch ÷ 2 | $0.077 | $0.077 | $0.077 | $0.08 |
| Writer (Sonnet 5.5, batch) + rewrites (standard) | batch: (5k × $2 + 7k × $0.20 + 6k × $10) ÷ 2 = ($0.010 + $0.0014 + $0.06) ÷ 2 = $0.036; rewrites 1.3 × (2k × $2 + 7k × $0.20 + 0.9k × $10) = 1.3 × $0.0144 = $0.019 | $0.055 | $0.055 | $0.055 | $0.07 |
| Fitter, glosses, editor, embedding | Haiku 8k × $0.10 + 3k × $0.50 = $0.0023; Gemini 1.2 × (9k × $0.75 + 1.5k × $3.75) = 1.2 × $0.0124 = $0.015; embedding under $0.001 | $0.018 | $0.018 | $0.018 | $0.03 |
| Voice studio: episode, read-aloud, recap | Gemini: 15,000 tokens × $9/M = $0.135 + alignment 10 min × $0.0037 = $0.037; Inworld: 8,300 × $25/M = $0.208, timestamps included [unverified]; ElevenLabs: 8,300 × $80/M = $0.664; plus re-listen 10 min × $0.004 = $0.04 and mix under $0.005 for all | $0.217 (batch TTS: $0.150) | $0.253 | $0.709 | $0.18 |
| Call, main | STT 7 min × $0.002 × 2 streams = $0.015 (talkback stream rounded in); host Sonnet 90k × $0.20 + 4k × $2.50 + 3k × $2 + 1.5k × $10 per M = $0.018 + $0.010 + $0.006 + $0.015 = $0.049, re-requests $0.002; call TTS 1,900 chars: Gemini 3,500 tokens × $9/M = $0.032, Inworld Flash × $15/M = $0.029, ElevenLabs Flash × $40/M = $0.076; talkback resolver $0.001; Salma TTS $0.005; LiveKit 14 min × $0.001 = $0.014; worker compute $0.004 | $0.122 | $0.119 | $0.166 | $0.16 (with round two) |
| Round two [P1], 50% uptake | about $0.05 × 0.5 | $0.025 | $0.025 | $0.025 | (in the line above) |
| Re-transcription and pronunciation | 7 min × $0.004 = $0.028; Speechace $0.008 | $0.036 | $0.036 | $0.036 | $0.03 |
| Salma's notes and chat | notes 1k × $2 + 2k × $0.20 + 0.4k × $10 = $0.0064; polish TTS 240 chars about $0.006; chat 5 × (1k × $2 + 3k × $0.20 + 150 × $10) = 5 × $0.0041 = $0.021; margin note $0.004 | $0.037 | $0.037 | $0.037 | $0.04 |
| Analyst and memory keeper | $0.0035 + $0.0005 + $0.001 | $0.005 | $0.005 | $0.005 | $0.04 |
| Proof share and hosting | $0.06 ÷ 4 = $0.015; hosting $0.006 | $0.021 | $0.021 | $0.021 | $0.03 |
| Swap allowance | 5% × $0.50 | $0.025 | $0.025 | $0.025 | (not itemized) |
| **Per daily session, standard TTS** | | **$0.638** | **$0.671** | **$1.174** | **$0.66** |
| **With batch TTS where offered** (P1) | Gemini only | **$0.571** | $0.671 | $1.174 | |
| **After 2027-01-01** (Gemini text and TTS doubled, standard TTS) | editor +$0.015; Gemini voice +$0.135 episode, +$0.032 call | **$0.820** | **$0.686** | **$1.189** | |

What the table says:

1. The PRD's $0.66 is reproduced within 2 cents on the Gemini and Inworld stacks. The voice studio line is $0.04 to $0.07 over the PRD's $0.18 because the PRD line was priced before read-aloud and recap were added to the voice studio (02 noted the same); the analyst line is $0.035 under. They net out.
2. ElevenLabs at list price cannot be the beta voice: $1.17 a session is over the stop line before any lever. At v4 Turbo ($40 per million characters) the session is $0.85; at a negotiated $25 it is $0.67, the same as Inworld. Hence D5.
3. The Gemini stack is cheapest until 2027-01-01 and the most expensive of the two viable stacks after it ($0.82 against $0.69). If Gemini wins the blind test, the runner-up must be Inworld and the January plan is a vendor swap for the episode voice with the on-air announcement (PRD-v2 7.1 #3), or a negotiated Google rate [OPEN for Muath].
4. Fixed infrastructure (01) is on top of these numbers: about $1.30 a session at 15 learners, $0.25 at 100, $0.10 at 250, $0.05 to $0.06 at 10,000. The PRD's "hosting" sits inside its $0.03 line only at scale; in the beta the fixed cost is the research budget the business lens priced at about $2,000 a month. The weekly report prints it as its own line so the gate compares like with like.

### 6.2 Where the money goes and what the learner's behaviour does to it

On the Inworld stack: voice studio 38%, call 21%, teacher and writer 20%, everything else 21%. The lines that move with behaviour: the call and the verbatim lines grow with learner talk (the goal: every extra minute of learner speech costs about $0.006 of STT and verbatim and nothing else); the voice studio grows with episode length (about $0.03 a minute on Inworld, $0.017 on Gemini); chat grows with messages (capped at 5 host messages, PRD-v2 5.6); swaps and round two grow with uptake. The lines that do not move: teacher, writer, editor, analyst, proof. A learner who re-listens ten times a day costs $0.01 more than one who listens once (egress), which is the design intent of law 11.

### 6.3 Levers to the $0.60 beta budget

In the order they are pulled, with the arithmetic and who decides:

| # | Lever | Saving per session | Status | Decision |
|---|---|---|---|---|
| 1 | Batch for teacher and writer with 02's cut lines | $0.11 (already in the table) | week 2, in | pipeline D2 |
| 2 | Episode default 6 → 5.5 minutes (PRD-v2 14.5 "5 to 6 minutes by default"; dial in 9.6) | voice −8%: $0.012 Gemini, $0.017 Inworld; writer output −$0.004 | week 2, configuration `length.default_min` | [DECISION] 5.5 as the default dial for learners with no low-energy signal; 5 when one fires; the teacher's dial moves it ±1 within 4:00 to 8:00 |
| 3 | Batch TTS (Gemini only; Inworld and ElevenLabs have no batch tier on their pages) with the same cut lines | $0.067 on Gemini | P1 (turnaround unverified, 02) | pipeline |
| 4 | Cheapest voice that passes the blind test | $0 to $0.50 depending on the winner | week 2 | D5, the test |
| 5 | Host cache hit at 90%+ verified by the 50-call test | prevents a $0.03 loss | week 4 | D8 |
| 6 | Haiku 5.5 as the call host if the 50-call test's move-contract score holds | host text $0.049 → $0.003: $0.046 | week 4 test; a quality decision | [OPEN for Muath] with the call domain: run 25 of the 50 calls on Haiku and compare `violations`, talk share and the human read; switch only if equal |
| 7 | Round two uptake measured, not assumed | up to $0.025 | beta | none needed |
| 8 | One analyst call instead of fast plus full once notes latency is proven | $0.0005 | P1 | assessment domain |
| 9 | Re-listen ASR per line only on lines that changed after a resynthesis; never on the cached Salma feed tag or hello clips; the gloss cache shared across learners (02) | about $0.005 a session plus $0.02 on every resynthesis | week 2 | pipeline, already designed; this domain measures it |
| 10 | Teacher effort `low` for ordinary nights, `high` on the nightly weekly-mix run and at season boundaries (Opus 5.5's effort is the only thinking control) | output 6k → 3k tokens on 4 of 5 nights: $0.024 | week 2 configuration `roles.teacher.effort` | [DECISION] default `medium` kept in the beta; `low` is the first lever if the measured teacher line is over $0.09 |

Stack after levers 1, 2, 5 and 9 (all in by week 2 at no quality cost): Gemini $0.62 standard TTS, $0.55 with batch TTS; Inworld $0.65. Lever 6 (Haiku host) takes Inworld to $0.60. So: the Gemini stack meets the budget before 2027-01-01 with configuration alone; the Inworld stack meets it only with the Haiku host or the 5-minute default, both of which are quality decisions for the 50-call test and Milestone 0's "worth it" data. This is the honest state of the budget on 2026-10-17.

### 6.4 The path to $0.30 to $0.35 at 10,000 learners (PRD-v2 1.4, 19.2 exit criterion)

Base case: list prices after 2027-01-01 (the scale target is a 2027 number). Each row is a configuration change unless marked.

| Line | Beta (Inworld) | Floor at scale | How |
|---|---|---|---|
| Teacher | $0.077 | $0.045 | Opus 5.5 batch at effort `low` (3k output) on 4 nights in 5 ($0.047), effort `high` weekly ($0.08): (4 × 0.047 + 0.08) ÷ 5 = $0.054; minus 1,000 fewer input tokens as the brief compiler tightens: about $0.045. Sonnet 5.5 batch instead would be $0.024 (a quality decision for the offline suite, PRD-v2 6.7) |
| Writer | $0.055 | $0.040 | recap and shadow-line text from Haiku ($0.01 saved, 02 lever 4); rewrite rounds at 1.0 on average once the fitter's known-word list is mature ($0.005) |
| Fitter, editor | $0.018 | $0.030 | Gemini doubles; no lever (the editor must stay on a second vendor) |
| Voice studio | $0.253 | $0.140 | 5-minute episode default plus 2.5 read-aloud plus 1.5 recap = 9 minutes = 7,500 characters; Inworld at a negotiated $15 per million (TTS-2 at the Flash price, plausible at 2B characters a month) = $0.113 + re-listen 9 min × $0.003 = $0.027; or Gemini Flash-Lite TTS batch post-doubling about $0.079 + alignment $0.033 + re-listen $0.027 = $0.139 if it passes a blind test |
| Call | $0.119 | $0.070 | Haiku host ($0.046 saved); 5.5-minute call; Inworld Flash or Gemini call voice; LiveKit enterprise rate |
| Round two | $0.025 | $0.015 | same levers at 2.5 minutes |
| Verbatim, pronunciation | $0.036 | $0.023 | volume rate $0.0025 a minute on 6 minutes; one utterance |
| Notes and chat | $0.037 | $0.025 | chat host kept on Sonnet (the host's voice in text matters), notes on Sonnet, margin note on Haiku; shorter cached prefixes |
| Analyst, memory keeper | $0.005 | $0.005 | none |
| Proof share and hosting | $0.021 | $0.020 | CDN for produced audio once the security domain allows a service key (06) |
| Swap allowance | $0.025 | $0.015 | measured uptake; a swap at the floor stack costs $0.30 |
| **Total, list prices post-doubling** | **$0.671** | **$0.428** | |
| with Sonnet teacher | | $0.407 | quality decision |
| with a negotiated voice rate at $12 per million characters, or Flash-Lite at the pre-doubling rate | | $0.385 | [OPEN for Muath]: contract |
| with read-aloud and recap rendered on first tap instead of pre-rendered | | $0.360 | [OPEN for Muath]: PRD-v2 3.7 says the recap is made in the same pipeline run and 6.1 pre-renders the read-aloud; rendering them on first tap (streamed, under 5 s to first sound) saves the audio for the 60 to 90% of sessions that never open them [ASSUMPTION on uptake], at the cost of a 2 to 4 s wait on the tap and a PRD change |
| with 5-minute calls and the 4:30 close | | $0.345 | PRD-v2 5.4.2 says 5 to 7 minutes target; a 5-minute default is inside it; the beta's "4+ minutes of learner speech" gate (16.1) must still be met |

Reading: at list prices after the doubling the floor stack is $0.39 to $0.43; before the doubling (the same stack on Gemini Flash TTS batch at $0.0068 a minute) it is $0.33 to $0.36, which is where the concept's "$0.25 to $0.36" range came from. The target of $0.30 to $0.35 in 2027 therefore needs, beyond configuration, one of three things Muath must choose: a voice contract (the cheapest and least visible), a scope change to on-tap rendering (visible as a short wait), or shorter calls (visible as less talking, and in tension with the speech gate). The "costed path to $0.35 or less" the exit criterion asks for is this table with measured numbers in the first column by 2026-12-06; the choice among the three is in section 10.

Fixed infrastructure at 10,000 learners adds $0.05 to $0.06 (01), which the PRD's scale target absorbs inside its "hosting" line only if the CDN move happens; the report keeps it separate.

### 6.5 The estimate as code

`tools/cost-model/` holds `assumptions.yaml` (every unit number in 6.1 as a key) and `estimate.py`, which loads `prices.yaml` and prints the tables of 6.1 and 6.4 for any `--at` date and `--stack` (gemini, inworld, elevenlabs, floor). It is also the test that `prices.yaml` parses and that every role in `vendors.yaml` has a price row. Muath recomputes with `python -I tools/cost-model/estimate.py --at 2027-01-02 --stack inworld --set call.minutes=5.5`. From 2026-12-07 a second mode, `--measured --week 2026-W50`, replaces assumptions with `session_costs` means and prints the deltas, which is section 2 of the weekly report.

```yaml
# tools/cost-model/assumptions.yaml (excerpt)
episode: {minutes: 6.0, read_aloud_minutes: 2.5, recap_minutes: 1.5, chars_per_minute: 830, gemini_tokens_per_second: 25}
teacher: {input_tokens: 14000, cache_read: 6000, cache_write: 1000, output_tokens: 6000, pricing: batch}
writer:  {input_tokens: 12000, cache_read: 7000, output_tokens: 6000, pricing: batch, rewrite_rounds: 1.3, rewrite_input: 9000, rewrite_cache_read: 7000, rewrite_output: 900}
call:    {minutes: 6.5, learner_turns: 25, host_share: 0.35, host_chars: 1900, host_cache_read: 90000, host_cache_write: 4000, host_uncached: 3000, host_output: 1500, talkback_asks: 3, stt_streams: 2, livekit_participants: 2}
round_two: {minutes: 2.5, uptake: 0.5}
verbatim: {learner_minutes: 7, pronunciation_utterances: 1}
swap: {share_of_sessions: 0.05, cost_usd: 0.50}
proof: {weekly_usd: 0.06, sessions_per_week: 4}
hosting: {egress_usd: 0.006}
```

### 6.6 Performance of the tracing itself

The middleware adds under 1 ms to a call in `workflows` (one insert, same transaction) and nothing measurable to the live path (buffered, flushed every 5 s off the audio thread; 03's latency budget is untouched). `cost/rollup` over a 15-minute window at 10,000 learners is about 60,000 rows, one aggregate query under 2 s. The weekly report at scale reads roll-ups only. `vendor_calls` grows about 60 rows a session: 120,000 a month at 100 learners (about 50 MB), 12M a month at 10,000 (about 5 GB a month, partitioned, 13 months kept).

---

## 7. Build plan for 2026-11-02 to 2026-12-06

Team: the topology's E1 builds the middleware and tables in week 1 alongside the adapters (the two are one piece of work); Muath runs the vendor tests with `vendor-lab` and writes the truth file; E2 is not needed by this domain until the admin page in week 5. If there is one engineer, the cuts are in the last row.

| Week | Dates | This domain ships (P0 unless marked) | What the pilot data lets you test |
|---|---|---|---|
| 1 | 2026-11-02 to 11-08 | `prices.yaml` v2026-11-02 and the `price_book` migration; `vendor_calls` DDL with partitions and RLS; `tracing.traced`, `UnitUsage`, `price_for`, `record_external`, the live-path buffer and spool; Langfuse SDK wiring with the trace conventions and the PII scrub call; `SPEND_CAP_USD_PER_DAY` enforced; `vendor-lab tts render/sheet` and `vendor-lab stt run/decide` with the CSV sheets; Hume lockfile check in CI; quota requests sent (4.9); Langfuse per-user deletion verified with a test user | The 30 Milestone 0 clips and Muath's truth file run the 10.14 test by 2026-11-08; the two-host script renders on all three voice vendors for the blind test playlists; every test render is a priced `vendor_calls` row, so the first "cost per 10 minutes of audio" number is real before any episode exists |
| 2 | 2026-11-09 to 11-15 | Blind test listening sessions (Muath, 10 raters) and `vendor-lab decide tts`; `vendors.yaml` committed with winners by 11-13; paid tier for the winner; `cost/rollup` into `session_costs` and the role-vendor table; `episodes.cost_usd` fed from `session_costs` for 02's publisher; `kind_ceiling`, `unpriced`, `cache_hit_low`, `escalation_rate` alarms; `tools/cost-model/estimate.py` with `--measured` against the week's 20 test episodes | 20 test episodes from the Milestone 0 learner files give the first measured teacher, writer, editor and voice lines; the Milestone 0 scripts' character counts calibrate `chars_per_minute` |
| 3 | 2026-11-16 to 11-22 | Pre-account learner id carried in `CallMeta` for onboarding and sample traces, re-keyed at A9; sample episode ceiling alarm on the live endpoint; payment processor fee row after the 11-16 decision; `learner_costs_daily` with the acquisition line | The sample landing page's first real renders measure the $0.05 ceiling |
| 4 | 2026-11-23 to 11-29 | Call-worker buffered writer and `record_external` for LiveKit minutes; `call-bench` cost and cache-hit columns; `calls.metrics.cost_usd` fed; `session_over_alert`, `vendor_error_rate`, `daily_spend_*` alarms and `spend_mode` with the `conserve` and `halt` paths wired into 02's and 03's config reads; the Haiku-host comparison inside the 50-call run (lever 6) | Milestone 0 call transcripts replayed through the worker give per-call cost and the host cache hit rate before any live learner |
| 5 | 2026-11-30 to 12-06 | `cost/weekly-report` with all eight sections and `/admin/cost`; `cost/reconcile-monthly` skeleton with the Anthropic Admin API pull and the CSV upload; proof-share division; `learner/delete` aggregation hook; the end-to-end run with the Milestone 0 learners produces the first weekly report; **the exit document: measured cost per session and the costed path (6.4) with measured first column** | The 15 Milestone 0 learners' week on prod is the measurement the exit criterion asks for; their heavy-use spread tests the outlier rule |
| P1 (beta) | 2026-12-07 to 2027-01-10 | Batch TTS (lever 3) if Gemini is primary; Langfuse sampling switch (off in the beta); automated invoice ingestion for one more vendor; the 2026-12-28 next-week-prices report; the January voice plan executed (6.1 note 3) | |
| Cuts if one engineer | | No `/admin/cost` page (the weekly report Markdown and SQL suffice); reconciliation fully manual (a notebook, monthly); `vendor_invoices` table dropped; `conserve` mode dropped (only `halt` on the cap); `vendor-lab` reduced to render and run commands with decisions in a spreadsheet | |

What is too much for this team and is cut or deferred: self-hosted Langfuse (kept only as the PDPL fallback), per-vendor invoice scrapers, a cost dashboard beyond one admin page, multi-currency (USD only; SAR revenue is the processor's report), margin-per-learner analytics (one SQL query in the report), a budget forecasting model (the next-week-prices column is enough).

Milestone 0 to code: the kit's evening cycle (04-production.md) maps onto roles as step 1 → `verbatim_stt`, step 2 → `analyst` and `salma_text`, step 5 → `teacher` and `writer`, step 6 → `fitter`, step 7 → `editor`, step 9 → `episode_tts`, step 10 → `host` brief. Milestone 0 itself is untraced (Claude Max, AI Studio, ElevenLabs Pro at $99 a month, about $7 a learner for the fortnight); its only cost artifacts worth importing are the character counts of its scripts and the minutes of its calls, which `tools/m0_import.py` (04) can copy into `assumptions.yaml`.

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
| Monthly instead of weekly cost reports | PRD-v2 14.5 says weekly; the 2027-01-01 jump needs a four-week warning |
| Computing cost client-side from token counts in the SDK responses only | Streaming TTS and STT vendors report seconds, not tokens; one middleware with `usage_of` per adapter is the only way to one schema |

---

## 9. Assumptions about other domains

Each is an [ASSUMPTION] the integrator should check against that domain's document.

1. **System topology (01).** The adapter middleware described in its 4.5 is this document's `tracing.traced`; `CallMeta` gains `session_id`, `prompt_version` and `inngest_run_id` (it has `learner_id`, `role`, `episode_id`, `call_id`, `learner_model_version`); `vendor_config` holds `spend_mode`; `SPEND_CAP_USD_PER_DAY` and `SESSION_COST_ALERT_USD` are read by this middleware with the defaults here; `retention/daily` creates `vendor_calls` partitions as it does for `events`; `/admin/cost` is one more `sqladmin` page; the `vendor-lab` CLI is built here on its adapter package; the weekly canary episode is tagged `episode_kind='canary'` and `learner_id=null`; LiveKit minutes are booked through `record_external` by the call worker; infrastructure cost stays in 01's section 6 and is printed as a separate line in the report.
2. **Episode generation pipeline (02).** `pipeline_steps.cost_usd` is a sum of this domain's `vendor_calls` rows for that step (via `pipeline_steps.vendor_call_ids uuid[]`), and `price_book` is loaded from `prices.yaml`, not maintained separately; the publisher reads `session_costs` (or sums `vendor_calls` by `episode_id` when the roll-up has not run) for `episodes.cost_usd` and `episode.cost_recorded`; its cut lines set `pricing_escalated`; the fallback episode and `review_items` exist as it describes; `length.default_min` is a dial the teacher reads; the 02 `TtsAdapter` capabilities include `batch` for lever 3.
3. **Live call and voice stack (03).** The worker writes `vendor_calls` through the buffered middleware with `call_id` and `turn_n` in `units`; `calls.metrics.cost_usd` is filled at call end from the buffer; `call-bench` accepts two extra report columns from this domain; the host role honours `spend_mode='conserve'` by selecting its first fallback (Haiku) at call start, never mid-call; the Haiku-host comparison can run inside the week-4 50-call test.
4. **Learner model, event log and data platform (04).** `events.vendor_call_id` references `vendor_calls.id`; `learner/delete` calls this domain's aggregation hook before deleting rows and this domain's `langfuse_admin.delete_user`; `forone.learner.pii.scrub_for_processor` exists for metadata; the pre-account learner id of onboarding is re-keyed to the real `learner_id` at A9 by an event this domain subscribes to (`learner.created {pre_session_id, learner_id}`).
5. **Assessment engine (05).** Its roles (`analyst`, `memory_keeper`, `salma_text`, `proof_producer`, `rater`, `verbatim_stt`, `pronunciation`) and per-turn verbatim calls go through the middleware; `rater.pinned_until` is enforced by the middleware's refusal of fallback and override; the confidence threshold from 4.6.3 is read from `packages/language/ar-en/recognizer.yaml`; claim-related traces are never sampled out of Langfuse.
6. **Client app and delivery (06).** `client_perf` values are not vendor calls (its assumption 7, accepted); media egress and the feed MP3 encode are booked by `record_external` from the feed and media routes, daily, as one row per learner-day (`capability='media'`), not per request; the sample endpoint reads `spend_mode` and shows its own "try again tomorrow" page in `halt`.
7. **Security, privacy, consent and compliance (07).** Approves Langfuse Cloud EU holding prompts and completions with learner text (01 open item 2) and the `forone_cost` cross-learner read role; approves the Anthropic Admin API key as a read-only secret; if Langfuse is refused, this domain's fallback is self-hosting (about $150 a month of Fargate and RDS plus two engineer-days; section 10).
8. **Evaluation, observability and operations (09).** Owns `ops.page` and `ops.notify`, the on-call rota that receives `cost.alarm_raised`, the ops channel the weekly report posts to, and the day-one "recognizer error by first language" metric seeded by 4.6.3; the offline test suite (P1) reuses `vendor-lab` fixtures.

---

## 10. Open for Muath

1. **[OPEN for Muath] The voice contract, by 2026-11-20.** If ElevenLabs wins the blind test, it can be primary only at a negotiated rate at or below $25 per million characters (D5); if Gemini wins, decide the January plan now: swap the episode voice to the runner-up on 2027-01-01 with the on-air announcement, or ask Google for a rate. Either way the scale target needs a voice rate near $12 to $15 per million characters at about 2 billion characters a month; that conversation can start in December with the measured volumes.
2. **[OPEN for Muath] Which of the three last levers to $0.35 (6.4):** a negotiated voice rate (no product change), read-aloud and recap rendered on first tap (a PRD change to 3.7 and 6.1 and a 2 to 4 second wait), or 5-minute calls (inside PRD-v2 5.4.2 but in tension with the 4-minute speech gate). The exit document on 2026-12-06 will carry the measured numbers; the choice is yours and can wait until then.
3. **[OPEN for Muath] Haiku 5.5 as the call host** if the week-4 50-call comparison shows no difference in move-contract violations, talk share and the human read. It is worth $0.046 a session and is the single largest configuration lever on the call.
4. **[OPEN for Muath] Langfuse Cloud EU as a processor of learner text** (shared with 01 #2 and 04 #3). If refused: self-hosted Langfuse in the home region, about $150 a month and two engineer-days in week 1, and the deletion question disappears because the data is ours.
5. **[OPEN for Muath] Budget approvals:** vendor minimums for the beta (the voice winner's paid tier, about $100 to $330 a month depending on vendor; LiveKit Ship $50; Langfuse Core up to $59; Speechace developer plan), the Anthropic prepaid balance for the beta (about $1,500 for December at 100 learners on the text lines plus tests), and the rater fees for the blind test (10 raters, about one hour each).
6. **[OPEN for Muath] The daily spend cap formula** `max($50, learners × $1.50)` and the stop-line plan window of 48 hours. Both are policy, not engineering.
7. **[OPEN for Muath] Whether cost figures may appear in the monthly human review packet** (6.8), so the reviewer sees the cost of an episode next to its quality. Internal only; never a learner surface. Default here: yes.
8. **[OPEN for Muath] Whether the Milestone 0 clips may be sent to all four recognizer vendors and all three voice vendors** under the Milestone 0 consent (the clips contain learners' voices). The security domain and counsel decide what the consent covers; if not, the 10.14 test needs a re-consent of the 30 clips' owners by 2026-11-04.
