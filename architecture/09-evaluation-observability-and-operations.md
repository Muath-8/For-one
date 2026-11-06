# Evaluation, observability and operations

*For one architecture, domain 9 of 9. Written 2026-10-16 against PRD-v2 (Implementation PRD v3.0), concept-v2 sections 7 to 10, decisions.md, the ai-architecture, learning-science and assessment-progress lenses, and the Milestone 0 kit (04-production, 05-prompts, 07-measures-and-gates, 08-runbook). Sibling documents 01 to 07 were read for names; where this document consumes something they defined, the name is theirs and is marked. Tags: [DECISION], [ASSUMPTION], [OPEN for Muath].*

## 1. Summary and the decisions in one table

This domain answers one question for a team of one to two engineers plus Muath: **how do we know the product works, and how do we keep it working, without building an observability product?** The answer is to make every signal a row in the Postgres the team already runs, to make every alert a SQL query with a runbook link, and to make every change to a prompt, a model or a rule pass the same offline suite that the Milestone 0 learners' files and tags seed. Three managed tools (Sentry for errors, Better Stack for uptime, heartbeats and paging, Langfuse for model traces, the last owned by the cost domain) plus CloudWatch, which comes with Fargate, cover the rest. Nothing in this domain is ever shown to a learner (PRD-v2 16, law 1).

| # | Decision | Chosen | Reason in one line | Rejected |
|---|---|---|---|---|
| D1 | Where measures live | Every 16.1 and 16.2 measure is a row in one table, `measure_points`, computed nightly by `measures/daily` from the event log and the sibling domains' tables, with the definition as versioned SQL in `forone.measures` [DECISION, PRD-v2 16.2 "tracked from day one"] | One table, one job, one version; a measure can be recomputed from day one when its definition changes, like the stores (8.5) | A metrics vendor (Datadog, Mixpanel): a PDPL processor holding learner ids for nothing the event log does not already hold; counters in memory (lost on deploy) |
| D2 | Team dashboards | Server-rendered pages in `api` under `/admin/measures`, `/admin/gates`, `/admin/alerts`, `/admin/review`, `/admin/flags`, `/admin/incidents`, read from `measure_points` and the sibling tables through the `forone_readonly` role; CloudWatch dashboards for infrastructure; the Inngest and Langfuse consoles for runs and traces [DECISION] | RDS sits in a private VPC with no public endpoint, so a SaaS dashboard would need a tunnel or a replica; at 100 to 500 learners the numbers fit in a table | Grafana Cloud (needs a reachable datasource), Metabase on Fargate (one more container; revisit at 1,000 learners, section 8) |
| D3 | Alerts are SQL | `ops/alerts.yaml` holds every rule (a SQL predicate, a window, a severity, a dedupe key, a runbook path); the Inngest cron `ops/watch` evaluates them every 5 minutes, writes `alert_state`, and calls `ops.page()` [DECISION, PRD-v2 15, 14.5] | The latency budgets of Part 15 and the cost stop line are facts about rows (`calls.metrics`, `notes.created_at`, `vendor_calls`), so the alert is the query; the team reviews rules as code | CloudWatch metric alarms for product budgets (they would need a metrics emitter per budget); vendor alerting UIs edited by hand (no review, no runbook link) |
| D4 | Paging | Better Stack: uptime checks on the three public hostnames, heartbeat monitors for the four crons that must never stop, one on-call schedule, phone-call escalation; `ops.page()` posts to its incident API; everything below P1 goes to the ops Slack channel or the morning digest [DECISION] | The topology already named it; it is the cheapest tool that calls a phone; one API to wrap | PagerDuty (price), Opsgenie (Atlassian stack), Slack only (no phone at 05:30) |
| D5 | Logging | Structured JSON on stdout from all four services to CloudWatch Logs (30-day retention), scrubbed at emission by `forone.ops.logscrub` using the data domain's `forone.learner.pii` classification; learner ids and event ids are allowed, names, emails, transcripts, facts and audio are not; CloudWatch Embedded Metric Format lines carry the few service counters the data domain emits [DECISION, PRD-v2 12.6] | Zero agents, zero extra processors; the scrubber is one function with a test corpus; EMF turns a log line into a CloudWatch metric for free | A log SaaS (another processor holding learner text), OpenTelemetry collectors (operations) |
| D6 | The offline suite | One package `forone.eval` and one CLI `tools/eval` running named suites from `eval/suites.yaml` against thresholds in `eval/thresholds.yaml`; fixtures seeded from Milestone 0 (learner files, tags, 30 clips, scripts, Muath's editor reads); results in `eval_runs` and `bench/reports/`; a CI job `eval-gate` runs the relevant suite when a prompt, model, rule or measure version changes and blocks the merge on regression [DECISION, PRD-v2 6.7 [P1], 10.11, 10.14, 14.4] | The PRD's rule is "a change that worsens any of these does not ship"; a rule needs a gate in CI, a baseline, and fixtures that exist before the beta | A separate eval vendor; manual "run it when you remember" (Milestone 0's mode) |
| D7 | Versioning of what models see | Every prompt, rubric, rule table and threshold is a file in the language package with a `prompt_version` in `packages/package_ar_en/versions.yaml`; `release_manifest` records which versions each deploy carried; a version bump is a PR that must pass `eval-gate` [DECISION, PRD-v2 10.11.3, 8.5] | "Pinned for each 4-week window" and "re-run on every model change" are only enforceable if versions are explicit and deploys record them | Editing prompts in the admin UI (the pipeline domain's D17 already forbids it) |
| D8 | Feature flags | A `feature_flags` table (key, state, learner allowlist, percentage, changed_by), read by services with a 60 s cache, edited on `/admin/flags`; flags exist only for P1 features, vendor levers and kill switches, never for a law [DECISION, PRD-v2 19.3] | P1 items ship during a paid beta and need a way to reach 5 learners before 100; a kill switch is the first half of every runbook | LaunchDarkly or similar (processor, price); environment variables (a deploy per flip) |
| D9 | Release process | Trunk-based; CI on every PR (unit, PII scrub test, Inngest payload test, `eval-gate` when versions change); merge deploys staging; prod deploys from a tag after a manual approval, runs a canary episode and a canary call on the synthetic learner, then flips; release window Sunday to Thursday 10:00 to 16:00 Riyadh; no deploy inside any learner's drop window where it can be avoided; freeze 2026-12-05 to 2026-12-08 [DECISION] | Confirms topology D13 and D14 and adds the one thing they lack: when, and what proves a release is good before a learner hears it | Continuous deploy to prod (a bad prompt would reach a drop at 05:40), release trains (too slow for a five-week build) |
| D10 | Human review | The pipeline's `review_items` queue for episodes (10 per learner per month plus every degraded, fallback and soft-fail item), a new `call_review_items` queue for calls (2 per learner per month plus every call with a move violation, a crisis activation or `end_reason: abandoned` in week 1), a monthly `claim_audits` sample of shown claims, all served by `/admin/review` with the security domain's role matrix [DECISION, PRD-v2 6.8, 16.1] | The PRD names the episode reviewer and the false-claim audit; the call review is the only way to know the move contract holds on real learners, and the governor's counters say what was declared, not what was heard | Reviewing calls by listening (audio access needs break-glass; transcripts with timings are enough) |
| D11 | On-call | One primary engineer per week, Muath as escalation, phone paging only for P1 rules (the six in 4.6), the 05:00 to 08:30 Riyadh drop window as the protected hour; everything else waits for 08:30; a weekly 30-minute ops review on Tuesdays [DECISION] | Two people cannot staff 24/7; the product's critical hour is the drop, so that is where attention goes | A follow-the-sun rota (no sun to follow), no paging (an unready 05:40 drop found at 09:00 is a lost day for every commuter) |
| D12 | Runbooks | Twelve one-page runbooks in `ops/runbooks/`, each with the same five headings (detect, first five minutes, fix, verify, tell the learner), every alert rule linking to one, two admin actions behind them (`pull episode`, `re-run after-pass`) [DECISION] | A runbook nobody can find at 05:40 is a document, not a runbook | A wiki |
| D13 | The beta gates | `/admin/gates` computes the eleven 16.1 gates per weekly invite cohort from `measure_points` with target and stop lines, with the date each gate first becomes readable; nothing is decided from a gate before its cohort is old enough [DECISION, PRD-v2 16.1, 19.3] | "Active in week 4" for the 2026-12-07 cohort is unreadable before 2027-01-04; a dashboard that shows it earlier invites a wrong decision | A single cross-cohort number |

What this domain does not build: a metrics pipeline, a log search product, an experimentation platform, a status page for learners (there is none; the product says "Weak signal" and falls back), and anything a learner can see.

## 2. Requirements this domain implements

| PRD-v2 part | Requirement | Where in this document |
|---|---|---|
| 1.2 law 1, law 12; 1.3 promises 1, 4, 7 | Nothing game-like reaches a learner; no claim without proof; a wrong memory is counted | Law-scan corpus in the suite (4.2.4); claim-gate property tests (4.2.6); the false-claim audit (4.5.3); the wrong-memory measure (4.1) |
| 6.3 | Editor fallback after a second fail; page a human after 3 fallbacks in 7 days | Alert `fallback_3_in_7` (4.6); runbook R4 (4.8); editor-gate eval set (4.2.3) |
| 6.4, 6.5 | Re-listen fallbacks and similarity are counted; the human read updates the ban list | Degraded-mode counters (4.1); review findings loop (4.5) |
| 6.7 [P1] | Offline suite: 30 to 50 synthetic learners, simulated caller, seven regression measures, run on every prompt or model change, a regression does not ship | 4.2 entire; CI wiring 4.3 |
| 6.8 | A paid native reviewer reads 10 random episodes per learner per month, flags errors, sameness, law breaks; findings update the ban list, prompts, similarity threshold | 4.5.1 with the access rules in 4.5.4 |
| 10.11 | Calibration bars before claims; rater pinned per 4-week window; re-run on model change | `calibration/run` (assessment domain) wired into `eval-gate` and the calendar (4.3, 4.10) |
| 10.14 | 30-clip recognizer test, before build week 2; recognizer error by first language from day one | Suite `recognizers` (4.2.5); monthly `vendor/regress` (4.10) |
| 14.4 | Vendor tests in weeks 1 to 2; 50 scripted calls, median host reply under 1.5 s | Suites `voices-blind` and `calls-50` (4.2.5); the latency alert rules (4.6) |
| 14.5 | Cost per session reported weekly, next to heavy-use outliers; stop line $1.00 | Weekly cost review in the calendar (4.10); alert rules `cost_session_p50_7d`, `cost_stop_line` (4.6); the cost domain owns the report itself |
| 15 | Every latency and reliability budget | Each budget has a measured signal, a source and an alert rule (4.6, table 4.6.1) |
| 16.1 | Eleven beta gates with target and stop lines | `/admin/gates` (4.4) |
| 16.2 | Eighteen quality and health measures from day one | `forone.measures` definitions (4.1) |
| 19.2, 19.3 | Exit criteria on 2026-12-07; P1 items during the beta; switch-to-native triggers | Build plan (7); flags (4.7); the two switch measures (4.1 rows 17, 18) |
| 7.9 | Every crisis activation logged; human follow-up | Alert `crisis_activation` and runbook R10 (4.6, 4.8) |
| 12.5, 12.6 (through the security domain) | Deletion windows verified; staff access logged; PII never in logs | Log scrubbing (4.9); the paging channel for `privacy.audit_failed` (4.6) |

Budgets that bind this domain: the fixed monthly cost of its tools (section 6, about $120 to $200 a month in the beta); the cost of running the suite (about $15 to $20 per full run, section 6); zero per-session cost on the learner path (nothing here runs in a learner's request); and the engineering budget of the five build weeks, where this domain must stay under about one engineer-week in total before 2026-12-07 (section 7 says which week).

## 3. Architecture

### 3.1 Components

Draw six boxes in a row across the top, the four deployables plus two managed consoles, and three boxes below them owned by this domain.

- **Producers (top row, left to right):** `api`, `workflows`, `call-worker`, `web` (the topology's four services). Each emits three things: structured log lines to stdout (CloudWatch), Sentry events on exceptions, and rows (`events`, `calls.metrics`, `pipeline_steps`, `vendor_calls`, `notes`, `claims`, `review_items`, `privacy_audit_runs`, and the rest of the sibling tables). `web` emits only client events (`app_open`, `client_perf`, `pwa_install`, `push_permission`) through `POST /v1/events`, and Sentry browser events.
- **Consoles (top row, right):** Inngest (run history, replay), Langfuse (every model call with cost and `learner_model_version`; owned by the cost domain).
- **`forone.measures` (bottom left):** a Python package of SQL definitions, one function per measure, each stamped with `MEASURES_VERSION`. Run by the Inngest crons `measures/daily` (06:30 Riyadh, 03:30 UTC) and `measures/weekly` (Monday 06:30 Riyadh). Writes `measure_points`.
- **`forone.ops` (bottom middle):** `ops/watch` (cron, every 5 minutes) evaluates `ops/alerts.yaml` against Postgres, writes `alert_state`, calls `ops.page()`; `ops.page()` is the interface the topology, pipeline and security domains already call (`pipeline.human_page`, `vendor.degraded`, `privacy.audit_failed`, `cost_guard.tripped`, `security.incident_opened` all land here); `ops/canary` (weekly) runs one episode and one call on the synthetic learner through each voice vendor; `review/sample` (nightly) fills the review queues; `claims/audit-sample` (monthly) fills `claim_audits`; `vendor/regress` (monthly) re-runs the recognizer and pronunciation clip suites; `feature_flags` and `release_manifest` live here.
- **`forone.eval` (bottom right):** the offline suite. Fixtures under `eval/fixtures/` (seeded from `/mnt/project-files/milestone-0/` artifacts by `tools/import_m0.py`), suites in `eval/suites.yaml`, thresholds in `eval/thresholds.yaml`, the runner `tools/eval`. It runs on a developer laptop, in CI (`eval-gate`), and nightly on staging (`eval/nightly`, the 10-fixture smoke). Results go to `eval_runs` and `bench/reports/{date}-{sha}.json` (the call domain's `call-bench` already uses that directory).
- **Sinks (right edge):** Sentry (errors, scrubbed), Better Stack (uptime, heartbeats, incidents, phone), the ops Slack channel `#forone-ops` (every alert at P2 and above, every page, every deploy, every canary result), the morning digest (P3, one Slack message at 08:30 Riyadh).

Arrows: producers write rows to Postgres and lines to CloudWatch; `forone.measures` reads Postgres and writes `measure_points`; `forone.ops` reads Postgres and CloudWatch alarms (through SNS) and writes to Better Stack and Slack; `forone.eval` reads fixtures and calls the production adapters (real vendors at the gate level, `FORONE_FAKE_VENDORS=1` recorded fixtures at the unit level) and writes `eval_runs`; the `/admin` pages read everything through `forone_readonly` and write only `feature_flags`, `review_findings`, `claim_audits`, `incidents` and the two admin actions, each as an `audit_log` row (security domain D13).

### 3.2 Data flows

1. **A budget to an alert.** A call ends; the worker writes `calls.metrics` (`reply_latency_ms` percentiles, `connect_ms`, `talkback_ms`, `moves.violations`, `end_reason`). Five minutes later `ops/watch` runs rule `host_reply_p50_20calls`: median of `reply_latency_ms` over the last 20 completed calls. Over 1.5 s for two consecutive evaluations, it writes `alert_state{rule, state: firing, since, dedupe_key}` and posts to Slack with the runbook link (P2). Under 1.5 s for two evaluations, it resolves. Nothing in this path touches a learner.
2. **An event to a measure.** The client sends `app_open {entry: "home_screen", drop_delta_min: 12}`. At 06:30 the next morning `measures/daily` computes `unprompted_return` for yesterday: sessions started without `entry in (push, gap_note)` and within 60 minutes of the learner's drop time, per learner-day, and the cohort share. It writes `measure_points(measure='unprompted_return_share', scope='cohort', scope_id='2026-12-07', period_start=yesterday, value=0.62, n=41)`. `/admin/measures` reads the last 28 days.
3. **A prompt change to a deploy.** An engineer edits `packages/package_ar_en/prompts/host_system.md` and bumps `versions.yaml: host_system: 1.4.0`. CI sees the path, runs `eval-gate` with suite `host` (the governor replay on Milestone 0 transcripts, the simulated caller on 10 scripted calls against staging, the law scan), compares with the baseline run for `main`, and fails the check if any metric in `thresholds.yaml` regressed beyond its allowance. On merge, staging deploys; on tag, prod deploys and `release_manifest` records `host_system: 1.4.0` with the image digest and the time. `calibration/run` (assessment domain) is part of `eval-gate` for assessment paths and blocks the same way.
4. **A review to a config change.** `review/sample` picks 10 shipped episodes for learner L in December into `review_items`. The reviewer (role `reviewer`, script with the display name tokenized) files `review_findings {flags: [sameness], ban_proposals: ["a quiet café"]}`. Muath accepts the proposal on the same page; the `ban_list` row is inserted by code with `source: review_finding`, and the next `eval-gate` run of the `writer` suite includes the new ban word in its scan. Nothing edits a prompt.
5. **A page to a runbook.** `episode/produce` emits `pipeline.human_page {learner_id, reason: "fallback_3_in_7", count_7d: 3}`. `ops.page()` opens a Better Stack incident with severity P1, title "3 fallbacks in 7 days for learner L", link `ops/runbooks/R4-bad-or-fallback-episode.md`, and the Slack post. The on-call engineer opens `/admin/episodes?learner=L`, reads the three editor verdicts, and follows R4.

### 3.3 Interfaces this domain exposes

```python
# packages/ops/forone/ops/api.py
from typing import Literal
Severity = Literal["P1", "P2", "P3"]

def page(*, severity: Severity, rule: str, summary: str, runbook: str,
         dedupe_key: str, learner_id: str | None = None, context: dict | None = None) -> str:
    """Opens or updates an incident. P1 -> Better Stack incident (phone escalation) + Slack.
    P2 -> Slack #forone-ops. P3 -> morning digest. Returns the incident id.
    Context must contain ids and scalars only; the scrubber rejects anything else."""

def resolve(dedupe_key: str, note: str = "") -> None: ...

def flag(key: str, *, learner_id: str | None = None) -> bool:
    """Feature flag read with a 60 s process cache. Falls back to the flag's `default` when
    Postgres is unreachable, never to True for a kill switch."""

def heartbeat(monitor: str) -> None:
    """Called at the end of a cron that must never stop (measures/daily, ops/watch, privacy/verify,
    retention/daily). Better Stack pages when a heartbeat is late by more than its grace period."""
```

```python
# packages/measures/forone/measures/api.py
MEASURES_VERSION = "1.0.0"

def compute(measure: str, *, period_start, period_end, scope: Literal["learner","cohort","all"]) -> list[MeasurePoint]: ...
def compute_all(period_start, period_end) -> None:       # measures/daily calls this
def recompute(measure: str, since) -> None:              # when a definition changes, like a rebuild
```

```python
# packages/eval/forone/eval/api.py
def run(suite: str, *, against: Literal["local","staging"], baseline: str | None = None,
        fake_vendors: bool = False) -> EvalRun:
    """Runs every check in the suite, writes eval_runs, writes bench/reports/{date}-{sha}.json,
    compares with the baseline run (the last passing run of this suite on `main`) and returns
    passed=False when any metric regresses beyond thresholds.yaml."""
```

Inngest events this domain emits: `ops.alert_fired {rule, severity, dedupe_key}`, `ops.alert_resolved {rule, dedupe_key}`, `ops.canary_completed {vendor, kind, passed}`, `episode.pulled {learner_id, episode_id, reason}`, `flag.changed {key, state, changed_by}`, `eval.completed {suite, run_id, passed}`, `measures.completed {date, measures_version}`.

Inngest events this domain consumes: `pipeline.human_page`, `vendor.degraded`, `voice.vendor_failover`, `episode.fallback_shipped`, `episode.failed`, `privacy.audit_failed`, `cost_guard.tripped`, `security.incident_opened`, `crisis.activated`, `claims.retracted`, `assessment.rebuild_completed`, `calibration.completed`, `memory.flagged`.

## 4. Detailed design

### 4.1 Measures: every 16.1 and 16.2 number, computed from the log

**Grain and scope.** Every measure is computed per learner-day where that makes sense, then rolled up to `cohort` (the weekly invite batch, keyed by the Monday of the invite week, PRD-v2 2.1.6) and `all`. `measure_points` keeps all three scopes so that a cohort number can always be opened to its learners. Learner-scope rows are internal, never shown to a learner, and are deleted by `learner/delete` like any learner-scoped row.

```sql
create table measure_points (
  measure           text not null,                       -- key from the table below
  scope             text not null check (scope in ('learner','cohort','all')),
  scope_id          text not null,                       -- learner_id, cohort monday (YYYY-MM-DD), or 'all'
  period_start      date not null,
  period_days       smallint not null,                   -- 1, 7 or 28
  value             numeric,                             -- null when n < min_n (never a fake zero)
  n                 int not null,                        -- denominator or sample size
  extra             jsonb,                               -- p50/p95, numerator, breakdown
  measures_version  text not null,
  computed_at       timestamptz not null default now(),
  primary key (measure, scope, scope_id, period_start, period_days, measures_version)
);
create index on measure_points (measure, scope, period_start desc);
alter table measure_points enable row level security;   -- learner scope rows under the data domain's policies
```

**Definitions.** `src` names the tables and events of the sibling domains. "Session" is the data domain's `sessions` row; "active day" is PRD-v2 3.6 rule 1 as `day.became_active`.

| # | Measure key | PRD | Grain | Definition (numerator / denominator) | src |
|---|---|---|---|---|---|
| 1 | `worth_it_share` | 16.2, 11.1 | cohort, 7 d | `worth_it_answer = yes` / all `worth_it_answer` in the period; `extra` holds mostly and no, and the free-text count | `events: worth_it_answer` |
| 2 | `regret_share` | 16.2 | cohort, 28 d | learners whose last worth-it answer was `no` twice running / learners with 2+ answers [ASSUMPTION: "regret" is read from the worth-it series; the PRD names no separate question] | same |
| 3 | `unprompted_return_share` | 16.2 | learner-day, cohort 7 d | sessions whose first `app_open.entry not in (push, gap_note)` / sessions; `extra.within_hour` = share with `abs(drop_delta_min) <= 60` | `app_open`, `sessions` |
| 4 | `tomorrow_chosen_share` | 16.2 | cohort, 7 d | sessions with an `idea_chosen` where `source in (pick, tell_salma, remix)` / sessions that ended (`sessions.state=done or closed`) | `idea_chosen` |
| 5 | `weeks_on_rhythm` | 16.2, 3.9 | learner, 7 d | 1 when active days in the local week ≥ the rhythm's chosen days; cohort value = share of learner-weeks met | `day.became_active`, `goals.rhythm` |
| 6 | `return_after_gap_14d` | 16.2 | cohort, 28 d | learners who had a gap ≥ 7 days and started a session within 14 days of the gap's start / learners with such a gap; `extra.median_gap_days` | `sessions` |
| 7 | `retention_w{4,12,26,52}` | 16.2 | cohort | learners with ≥ 1 active day in week k after onboarding / cohort size; computed only when the cohort is ≥ k weeks old | `learners`, `day.became_active` |
| 8 | `delayed_recall_share` | 16.2 | cohort, 28 d | target items (words and structures first met in the period) with a clean, unprompted correct use ≥ 7 days after first exposure / target items with any obligatory context ≥ 7 days after first exposure | `word_bank`, `structure_observations` |
| 9 | `targets_hold_share` | 16.2, 10.6 | cohort, 28 d | structures that were `stable` before a recording and were confirmed by it (`stable_confirmed_at` set) / structures `stable` before a recording | `structure_map`, `recording_ratings` |
| 10 | `huh_per_min`, `taps_per_100w` | 16.2 | learner-day, cohort 28 d | `huh` events / minutes played; `tap` events / running words heard or read | `huh`, `tap`, `play` |
| 11 | `followed_vs_predicted` | 16.2 | cohort, 28 d | mean of (`followed_answer` mapped most=1, about_half=0.5, little=0) minus the episode's `why.predicted` coverage band mapped the same way; `extra` holds the confusion table | `followed_answer`, episode `why` artifact |
| 12 | `talkback_per_call` | 16.2 | learner, 7 d; cohort by learner-week-number | `talkback` events / calls; cohort view is by week since onboarding so the trend over weeks is visible | `talkback`, `calls` |
| 13 | `notes_opened_share`, `say_it_once_share` | 16.2 | cohort, 7 d | notes with `shown_at` / notes created; `say_it_once` events / polish cards shown | `notes`, `say_it_once` |
| 14 | `fact_edits_week1` | 16.2 | cohort | learners with ≥ 1 `fact_card_edit` or `notebook_edit` in their first 7 days / cohort size | events |
| 15 | `similarity_p90` | 16.2, 6.5 | learner, 28 d | 90th percentile of the max cosine of each shipped script against the learner's previous 20; `extra.too_alike_human` = reviewer "too_alike" share | `script_embeddings`, `review_findings` |
| 16 | `minutes_per_day_outliers` | 16.2 | all, 1 d | learners with > 90 minutes of app playback plus call time in a local day, listed with learner id and minutes; this is a warning light for the team, never a goal [ASSUMPTION: 90 minutes, tuned in the beta] | `play`, `calls` |
| 17 | `recognizer_err_by_l1` | 16.2, 10.14 | all, 28 d | word error rate of streaming text against verbatim text on clean turns, grouped by `learners.native_language` (one group in the beta; the measure exists so the second pair does not start blind) | `call_turns_v` |
| 18 | `time_to_first_sound_p50`, `time_to_first_sentence_p50` | 16.2, 15 | cohort, 7 d | medians of `client_perf.first_sound_ms` and `first_english_ms` per onboarding | `client_perf` |
| 19 | `calls_abandoned_on_move_share`, `feed_to_call_handoff_share` | 16.2, 19.3 | cohort, 7 d | `end_reason=abandoned` with `client_perf.bg_play_stop` or motion hint / calls; calls with `app_open.entry=feed_link` that reached `call_started` / feed call-link exchanges | `calls`, `app_open`, `feed_links` |
| 20 | `wrong_memories_per_100` | 16.1 | all, 28 d | `wrong_memory_flag` events × 100 / callbacks spoken (`show_canon.kind=callback_made` plus Today's memory line shown); the data domain's formula | `events`, `show_canon` |
| 21 | `false_claim_rate` | 16.1 | all, 28 d | `claim_audits.verdict=false` / audited claims (4.5.3) | `claim_audits` |
| 22 | `cost_per_session_p50`, `cost_per_session_mean` | 16.1, 14.5 | all and cohort, 7 d | per session: sum of `vendor_calls.cost_usd` attributed to the session's episode, call, after-pass, notes and chat, plus a quarter of that learner's weekly proof cost; p50 and mean over sessions; `extra.top10` = the heaviest learners by cost that week | `vendor_calls`, `pipeline_steps` (the cost domain's attribution rule) |
| 23 | `speech_min_per_session_p50` | 16.1 | cohort, 7 d | median over sessions of (`calls.metrics.learner_speech_ms` for main and round two + shadow + say-it-once durations) / 60,000 | `calls.metrics`, events |
| 24 | `sessions_per_active_learner_week` | 16.1 | cohort, 7 d | median over learners active that week of sessions started | `sessions` |
| 25 | `trial_to_paid`, `active_w4_paid`, `renewal_m2`, `referral_trials_share`, `very_disappointed_share` | 16.1 | cohort | see 4.4 | `learners.status`, `subscriptions`, `payment_events`, `waitlist.source`, `events: pmf_answer` [new event, 4.4] |
| 26 | `recording_improved_share` | 16.1 | cohort, per season | learners whose finale had ≥ 1 passed claim of kind `fluency_change`, `accuracy_change` or `complexity_change` with a positive direction / learners with two rated recordings | `claims`, `recording_ratings` |

Rules for every definition: a value is `null` when `n` is below the measure's `min_n` (5 for cohort shares, 3 for medians), never zero; a definition change bumps `MEASURES_VERSION` and `recompute()` rewrites history under the new version while the old rows stay (the same "never silently retract" rule as 8.5); nothing in `forone.measures` reads audio or transcript text.

Three definitions in full, so the shape is clear:

```sql
-- 3. unprompted_return_share, learner-day grain, one local day
with first_open as (
  select s.learner_id, s.id as session_id,
         (select e.payload->>'entry' from events e
           where e.learner_id = s.learner_id and e.type = 'app_open'
             and e.occurred_at between s.started_at - interval '10 minutes' and s.started_at
           order by e.occurred_at desc limit 1) as entry,
         (select (e.payload->>'drop_delta_min')::int from events e
           where e.learner_id = s.learner_id and e.type = 'app_open'
             and e.occurred_at between s.started_at - interval '10 minutes' and s.started_at
           order by e.occurred_at desc limit 1) as drop_delta_min
  from sessions s
  where s.started_at >= :period_start and s.started_at < :period_end)
select learner_id,
       count(*) filter (where coalesce(entry,'browser') not in ('push','gap_note')) as unprompted,
       count(*) filter (where coalesce(entry,'browser') not in ('push','gap_note')
                          and abs(coalesce(drop_delta_min, 999)) <= 60) as within_hour,
       count(*) as sessions
from first_open group by learner_id;
```

```sql
-- 8. delayed_recall_share, cohort, 28 days. "Target item" = a word or structure the teacher targeted.
with targeted as (
  select learner_id, unit_id as item, 'word' as kind, first_seen_at as first_at
    from word_bank where targeted_first_at between :p0 and :p1
  union all
  select learner_id, structure_id, 'structure', first_targeted_at
    from structure_map where first_targeted_at between :p0 and :p1),
later_use as (
  select t.*, exists (
    select 1 from structure_observations o
     where o.learner_id = t.learner_id and o.structure_id = t.item and t.kind = 'structure'
       and o.clean and o.correct and not o.prompted and o.occurred_at >= t.first_at + interval '7 days'
    union all
    select 1 from word_uses u
     where u.learner_id = t.learner_id and u.unit_id = t.item and t.kind = 'word'
       and u.clean and u.correct and not u.prompted and u.occurred_at >= t.first_at + interval '7 days') as recalled,
  exists (select 1 from structure_observations o where o.learner_id = t.learner_id and o.structure_id = t.item
            and o.occurred_at >= t.first_at + interval '7 days'
          union all
          select 1 from word_uses u where u.learner_id = t.learner_id and u.unit_id = t.item
            and u.occurred_at >= t.first_at + interval '7 days') as had_context
  from targeted t)
select l.cohort_monday, count(*) filter (where recalled) as num, count(*) filter (where had_context) as den
from later_use lu join learners l using (learner_id) group by 1;
```

`word_uses` is the data domain's per-use evidence table for words [ASSUMPTION: it exists under that name or the word bank exposes an equivalent view; the measure needs per-use rows with `clean`, `correct`, `prompted`, `occurred_at`].

```sql
-- 22. cost_per_session, one week, all scope; attribution rule from the cost domain:
-- vendor_calls.session_id is set for call, after-pass, notes and chat calls; episode cost joins by episode_id;
-- the weekly proof cost is split equally over that learner's sessions in the proof week.
with per_session as (
  select s.id as session_id, s.learner_id,
         coalesce((select sum(cost_usd) from vendor_calls v where v.session_id = s.id), 0)
       + coalesce((select cost_usd from episodes e where e.id = s.episode_id), 0)
       + coalesce((select p.cost_usd / nullif(p.sessions_in_week,0) from proofs p
                    where p.learner_id = s.learner_id and s.started_at >= p.week_start
                      and s.started_at < p.week_start + 7), 0) as cost_usd
  from sessions s where s.started_at >= :p0 and s.started_at < :p1)
select percentile_cont(0.5) within group (order by cost_usd) as p50, avg(cost_usd) as mean, count(*) as n,
       jsonb_agg(jsonb_build_object('learner_id', learner_id, 'cost', cost_usd) order by cost_usd desc) filter (where rn <= 10) as top10
from (select *, row_number() over (order by cost_usd desc) rn from per_session) x;
```

### 4.2 The offline test suite

**What Milestone 0 hands over and where it lands** (PRD-v2 19.1.7). `tools/import_m0.py` reads the kit's artifacts once, in build week 1, and writes fixtures. Every fixture derived from a real pilot learner is covered by the pilot consent (02-consent.md) [ASSUMPTION: the consent covers use of de-identified transcripts and clips for building and testing the product; the security domain confirms] and is stored with the display name tokenized and the learner id replaced by `m0-L03`-style refs.

| Milestone 0 artifact | Fixture path | Used by suite |
|---|---|---|
| 15 learner files (Google Docs exported as Markdown) | `eval/fixtures/learners/m0-L01..L15.json` as `TeacherInput` (the pipeline's 4.3 schema) | `pipeline`, `teacher` |
| Scripts and articles with Muath's hand-checked coverage (step 6 of the evening cycle) | `eval/fixtures/scripts/*.json` with `coverage_hand`, `new_words`, `level` | `fitter` |
| Every package with Muath's step-8 read and the human reviewer's flags, plus the Gemini editor's verdict at the time | `eval/fixtures/editor/*.json` with `human_verdict`, `flags` | `editor` |
| Call transcripts (Scribe v2) with Muath's error tags, structure ids, categories and "blurred meaning" marks | `calibration_samples` (assessment domain, via its `tools/import_m0_tags.py`) and `eval/fixtures/transcripts/*.json` | `analyst`, `host` (governor replay) |
| 30 consented clips with verbatim hand transcripts, code-switch and long-pause marks | `eval/fixtures/clips/recognizer/` | `recognizers` |
| Week-0 and week-3 then-and-now recordings with blind ratings | `test_retest_pairs` (assessment domain) and `eval/fixtures/recordings/` | `rater` |
| Confirmed and rejected life-fact candidates with quotes | `eval/fixtures/facts/*.json` | `memory` |
| The first ban list (show bible section BANNED) and scripts judged "too alike" | `packages/package_ar_en/ban_list.yaml`, `eval/fixtures/similarity/pairs.json` | `writer`, `editor` |
| Salma's notes as sent, with any learner reaction | `eval/fixtures/notes/*.json` | `notes` (law scan on real notes) |
| Say-it-once and voice-note clips (where consented) with a hand mark good/unclear | `eval/fixtures/clips/pronunciation/` | `pronunciation` (P1) |

**Synthetic learners** (PRD-v2 6.7: 30 to 50). The 15 pilot files give 15; `tools/eval synth --n 25` makes 25 more by varying level (A2+, B1-, B1, B1+, B2-), vocabulary size (2,000 to 5,000), interests (from the generic topic pool), rhythm, and by planting error patterns from the analyst prompt's list: missing *be*, articles with singular countables, present perfect versus past simple, prepositions after verbs, resumptive pronouns, questions without inversion, uncountable plurals, third-person *-s*. Each synthetic learner is a `TeacherInput` plus a **caller profile**: a list of 20 to 25 scripted turns written to contain its planted errors at known positions, with pause marks, rendered to audio once with a TTS voice of the vendor not under test (so the recognizer under test never hears its own vendor's synthesis) [DECISION]. The call domain's `tools/call-bench` plays these as the simulated caller; this domain owns the profiles and the scoring.

**Suites.** Each suite is a list of checks; each check is a function in `forone.eval.checks` that returns named metrics; `thresholds.yaml` says, per metric, the floor or ceiling and the allowed regression against the baseline. The suite names are the keys CI uses.

```yaml
# eval/suites.yaml
fitter:         # code only, free, seconds
  checks: [coverage_accuracy, chunk_recall, new_word_budget]
  fixtures: [scripts]
  vendors: fake
law_scan:       # code only, free
  checks: [law_words_precision_recall, arabic_law_words, lesson_word_near_misses]
  fixtures: [law_corpus, notes]
  vendors: fake
claim_gate:     # property tests, free
  checks: [no_claim_without_evidence, no_claim_across_version, no_metric_claim_without_sem,
           like_for_like_only, first_ever_requires_zero_prior, shown_never_deleted]
  vendors: fake
analyst:        # Haiku on the calibration set, about $1
  checks: [tag_precision_claim_tags, tag_precision_all, tag_recall_all, quote_exactness, needed_structure_agreement]
  fixtures: [calibration_samples]
  vendors: real
  external: calibration/run        # the assessment domain's job; its pass/fail is this suite's
memory:         # Haiku, cents
  checks: [fact_precision, sensitive_never_unconfirmed, quote_in_transcript, no_inference]
  fixtures: [facts]
  vendors: real
editor:         # Gemini, about $0.50
  checks: [editor_agreement_with_human, fact_leak_catch_rate, law_catch_rate, generic_catch_rate]
  fixtures: [editor]
  vendors: real
writer:         # Sonnet, about $3 for 15 fixtures
  checks: [ban_hits, similarity_vs_prior, target_presence, fun_carries_language_share, length_bounds]
  fixtures: [learners(15)]
  vendors: real
pipeline:       # teacher to editor, no voice, about $9 for 50 fixtures
  checks: [editor_pass_first_try, fallback_rate, coverage_prediction_vs_fitter, cost_per_step, latency_per_step, why_reasons_traceable]
  fixtures: [learners(50)]
  vendors: real
host:           # governor replay (free) + simulated caller on staging (about $3 for 20 calls)
  checks: [violations_share, recast_rate_on_planted, clarification_rate_on_planted, nudge_budget,
           recall_gap_count, learner_talk_share, reply_latency_p50_p95, connect_p95, talkback_p50, cutoffs_per_call,
           law_words_in_host_lines, ai_disclosure_on_ask]
  fixtures: [transcripts, callers(20)]
  vendors: real
  tool: tools/call-bench calls --n 20
notes:          # Sonnet, cents
  checks: [cards_at_most_3, own_sentence_first, no_numbers_or_grades, arabic_share_ge_80, polish_on_active_target]
  fixtures: [transcripts]
  vendors: real
recognizers:    # the 10.14 test as a regression, about $0.50
  checks: [error_survival_rate, filler_retention, hallucinations_near_pauses, code_switch_handling, wer_vs_hand]
  fixtures: [clips/recognizer]
  vendors: real
  tool: tools/call-bench recognizers
pronunciation:  # P1
  checks: [known_sentence_score_separates_good_unclear]
  fixtures: [clips/pronunciation]
  vendors: real
injection:      # the security domain's 30 cases, Sonnet, cents
  checks: [no_law_break_on_request, no_cross_learner_text, disclosure_holds]
  fixtures: [injection]
  vendors: real
calls_50:       # PRD 14.4 #3, staging only, about $8
  tool: tools/call-bench calls --n 50
  checks: [reply_latency_p50_p95, connect_p95, talkback_p50, violations_share, learner_talk_share, cutoffs_per_call, cost_per_call]
```

```yaml
# eval/thresholds.yaml (excerpt). floor/ceiling are absolute gates; max_regression is against the baseline run.
tag_precision_claim_tags:   {floor: 0.80, max_regression: 0.02}      # PRD 10.11
qwk_band:                   {floor: 0.70, max_regression: 0.03}      # PRD 10.11 (from calibration/run)
coverage_accuracy:          {ceiling_abs_error_pts: 1.0, max_regression: 0.3}   # fitter vs hand coverage
error_survival_rate:        {floor: 0.85, max_regression: 0.03}      # share of hand-tagged learner errors kept by the recognizer
violations_share:           {ceiling: 0.05, max_regression: 0.01}    # governor violations / host turns
recast_rate_on_planted:     {floor: 0.60, max_regression: 0.05}      # planted target errors that got a recast or clarification
clarification_rate_on_planted: {floor: 0.50, max_regression: 0.05}   # planted meaning-blurring errors that got a clarification first
nudge_budget:               {ceiling: 1, max_regression: 0}          # per call, hard
recall_gap_count:           {floor: 2, ceiling: 4}                   # per non-anxiety call
learner_talk_share:         {floor: 0.60, max_regression: 0.03}      # PRD 5.4.3: host at most 40%
reply_latency_p50_ms:       {ceiling: 1500}                          # PRD 15
reply_latency_p95_ms:       {ceiling: 2500}
law_words_precision:        {floor: 0.95}                            # near-miss corpus
law_words_recall:           {floor: 1.0}                             # every violating line is caught, hard
fact_precision:             {floor: 0.95, max_regression: 0.02}
sensitive_never_unconfirmed:{floor: 1.0}                             # hard
editor_pass_first_try:      {floor: 0.70, max_regression: 0.05}
fallback_rate:              {ceiling: 0.05, max_regression: 0.02}
ban_hits:                   {ceiling: 0}
similarity_vs_prior_p90:    {ceiling: 0.85}                          # Part 18 #10 starting value, replaced by the M0 judgment
cost_per_episode_text_usd:  {ceiling: 0.25, max_regression: 0.03}    # teacher+writer+fitter+editor at standard price
```

**Baselines.** `eval_runs` keeps every run; the baseline for a suite is the most recent run on `main` with `passed=true` and the same `against`. A metric with no baseline is judged on its floor or ceiling only. The first baselines are the week-2 runs on the Milestone 0 fixtures (section 7).

```sql
create table eval_runs (
  id uuid primary key, suite text not null, git_sha text not null, branch text not null,
  against text not null check (against in ('local','staging')),
  versions jsonb not null,            -- the versions.yaml snapshot the run used
  baseline_run_id uuid references eval_runs(id),
  metrics jsonb not null,             -- {metric: value}
  regressions jsonb not null,         -- [{metric, value, baseline, allowed}]
  passed boolean not null, cost_usd numeric(8,4), duration_s int,
  report_path text, ran_at timestamptz not null default now(), ran_by text not null
);
```

**The law-scan corpus** (`eval/fixtures/law_corpus.jsonl`, 200 lines, grown by every reviewer finding flagged `law`): 100 violating lines across every surface the scan covers (host line, Salma note, chat message, feed note, push text, proof script), in English and Arabic, including game words (streak, points, level, badge, score, grade, percent), lesson words (lesson, test, exercise, homework), guilt and attachment ("we missed you", "don't go", "اشتقنا لك"), explicit host corrections ("the correct form is"), and progress claims from a host; and 100 clean near-misses ("the water level", "a test drive", "the next level of the car park", "I scored the goal", "let's test the theory", Salma using "notes" and "polish"). The check runs the shared `guard/law_words.yaml` scanner (security domain) and the editor's check 10; recall must be 1.0 on the violating half, precision at least 0.95 on the clean half. A new false negative found in production (a reviewer `law` flag on a shipped line) is added to the corpus in the same PR that fixes it.

**The editor-gate set** (`eval/fixtures/editor/`): every Milestone 0 package with Muath's `SHIP / SHIP AFTER FIXES / REWRITE`, plus 20 mutated packages built by `tools/eval mutate`: one unconfirmed fact inserted, one real-world statistic asserted, one "don't bring up" topic mentioned, one joke that carries nothing, one episode that needs the previous one, one banned name. `fact_leak_catch_rate` and `law_catch_rate` must be 1.0 (these are code checks 4 and 10, so a miss is a bug, not a model variance); `editor_agreement_with_human` is the model's share of agreement with Muath's reads, reported, with a floor of 0.8 on the REWRITE cases.

**Fitter coverage tests**: the server fitter must reproduce `coverage-checker.html` to within 0.1 point on the 20 hand-checked scripts (the pipeline's own week-1 regression), and predict the learners' `followed_answer` direction on the Milestone 0 reactions (❤️/👍/😐 as the proxy) with the correlation reported, no floor in the beta.

**Claim-gate property tests** (free, run on every PR): generate random `claims` candidates with Hypothesis over the gate's inputs; assert that no row reaches `status=passed` without a `claim_evidence` row, never across two `assessment_version`s, never a metric kind without a `metric_calibration` row with `n_pairs ≥ 12`, never a `first_ever` with a prior clean use, and that `status=shown` rows are never deleted by `assessment/rebuild` (they become `retracted` with `notice_pending`). These encode PRD-v2 10.10 and 8.5 as tests the assessment domain's module must pass.

### 4.3 CI wiring and the release process

**Versions.** `packages/package_ar_en/versions.yaml` lists every versioned artifact a model sees or a measure depends on:

```yaml
# packages/package_ar_en/versions.yaml
prompts:
  teacher_system: 1.2.0
  writer_system: 1.3.1
  fitter_tagging: 1.0.0
  editor_rubric: 1.1.0
  host_system: 1.4.0
  salma_live: 1.0.2
  salma_notes: 1.1.0
  chat_host: 1.0.0
  analyst_full: 1.2.0
  analyst_fast: 1.0.1
  memory_keeper: 1.0.0
  proof_producer: 1.0.0
  rater: 1.0.0            # pinned per 4-week window (assessment D12); a bump here is refused inside a window
rules:
  structure_rules: 1.0.0  # structure_rules.yaml
  law_words: 1.1.0        # guard/law_words.yaml
  ban_list: 2026-11-20    # dated, grows monthly
  crisis_keywords: 1.0.0
thresholds:
  asr_confidence: 0.70    # set by the 10.14 run
  similarity_cosine: 0.85 # Part 18 #10
assessment_version: 1.0.0 # semver stamped on stores and claims (assessment D12)
measures_version: 1.0.0
```

**CI jobs on every PR:** `unit` (all packages, `FORONE_FAKE_VENDORS=1`), `pii_scrub` (the log scrubber and Sentry scrubber against `eval/fixtures/pii_corpus.jsonl`, 4.9), `inngest_payloads` (no event model carries `text`, `quote`, `transcript` or `audio`; the security domain's test), `law_scan`, `claim_gate`, `fitter`, `migrations` (upgrade and downgrade on a fresh database). **`eval-gate`** runs only when the diff touches a path in the map below, with the mapped suites, against `staging` for `host` and `calls_50` and `local` otherwise; it is a required check on `main`.

| Path changed | Suites run | Cost | Minutes |
|---|---|---|---|
| `prompts/teacher_*`, `prompts/writer_*`, `ban_list.yaml`, `vendors.yaml roles.teacher|writer` | `writer`, `pipeline` | about $12 | 12 |
| `prompts/editor_*`, `vendors.yaml roles.editor` | `editor` | $0.50 | 3 |
| `prompts/host_*`, `prompts/salma_live*`, governor code, `vendors.yaml roles.host|call_tts|streaming_stt` | `host` (20 calls on staging), `injection` | about $4 | 15 |
| `prompts/analyst_*`, `structure_rules.yaml`, measures code, `claims.py` | `analyst` (runs `calibration/run`), `claim_gate` | about $1 | 6 |
| `prompts/salma_notes*`, notes selection code | `notes`, `law_scan` | cents | 3 |
| `prompts/memory_keeper*`, facts code | `memory` | cents | 2 |
| `prompts/rater*`, `vendors.yaml roles.rater` | `analyst` (rater component of `calibration/run`), and the job refuses the bump when `pinned_until` is in the future | about $1 | 6 |
| `guard/law_words.yaml` | `law_scan`, `notes`, `host` (replay half only) | free | 2 |
| `vendors.yaml roles.verbatim_stt|streaming_stt` | `recognizers` | $0.50 | 5 |
| `forone/measures/**` | `measures_replay` (recompute 7 days on the staging copy and diff against the previous version; any measure that moves more than 5 points is listed in the PR) | free | 4 |

**Release.** `main` deploys to staging on merge (topology `deploy-staging.yml`). A prod release is a tag `v2026.12.03-1` created from `main` by `tools/release cut`, which writes the `release_manifest` row (versions snapshot, image digest, flags snapshot, the `eval_runs` ids that cover this diff), opens the manual approval in GitHub, and posts to Slack. After approval: migrations, rolling deploy, then `ops/canary` runs one `episode/produce` and one scripted call for the synthetic learner through the primary voice vendor; a failed canary rolls back to the previous image automatically (ECS task definition revision minus one) and pages P2. The deploy is announced in Slack with the manifest diff.

```sql
create table release_manifest (
  tag text primary key, git_sha text not null, image_digest text not null,
  versions jsonb not null, flags jsonb not null, eval_run_ids uuid[] not null,
  cut_by text not null, cut_at timestamptz not null, approved_by text, deployed_at timestamptz,
  canary_passed boolean, rolled_back_at timestamptz, notes text
);
```

Release rules: Sunday to Thursday, 10:00 to 16:00 Riyadh; never while `/admin/alerts` shows a firing P1; never inside the 30 minutes before any learner's drop time when the diff touches `episode/produce` or `day/next` (the tool checks `learner_schedule` and warns; the engineer can override with a reason); migrations are expand-then-contract, forward-only in prod, and a contract migration ships at least one release after its expand; a prompt version bump and a code change that depends on it ship in the same release; **freeze** from 2026-12-05 12:00 to 2026-12-08 12:00 Riyadh (launch) and from 2026-12-31 to 2027-01-02 (the Gemini price change lands on 2027-01-01 and the first finales start 2027-01-03). Rollback is "deploy the previous tag"; a rollback of a prompt version is the same PR reverted plus a release, because versions are files.

### 4.4 The beta gates as a team dashboard

`/admin/gates` shows one row per gate per cohort (cohorts are the weekly invite batches: `2026-12-07`, `2026-12-14`, ...) and an "all cohorts old enough" column. Each cell shows the value, `n`, the target, the stop line, and the date the cell first became readable. Cells before their readable date show "not yet" and nothing else, so no one reads a 3-day-old cohort's week-4 retention.

| Gate (16.1) | Measure key | Readable for a cohort from | Numerator / denominator | Notes |
|---|---|---|---|---|
| Trial to paid 30%+ (stop under 15%) | `trial_to_paid` | cohort start + 10 days (day 7 ask plus 3 days grace) | `learners.status` reached `paid` / learners who completed A9 (`trial_started_at` set) | Founding price only; a declined-card retry counts once |
| Active in week 4 (paid) 40%+ (stop 25%) | `active_w4_paid` | cohort start + 28 days | paid learners with ≥ 1 active day in days 22 to 28 / paid learners | First readable 2027-01-04 for the first cohort |
| Sessions per active learner per week 4+ (stop 2.5) | `sessions_per_active_learner_week` | cohort start + 7 days, then weekly | median over learners active that week | Shown per week since onboarding |
| Learner's own speech per session 4+ min (stop 2) | `speech_min_per_session_p50` | cohort start + 7 days | see 4.1 row 23 | Main call plus round two plus shadow plus say-it-once |
| The 4-weekly recording improves for most | `recording_improved_share` | first finale (cohort start + 28 days, on the learner's next session) | see 4.1 row 26 | Claims through the gate only; "no measurable change" is the stop line |
| Second-month renewal 60%+ (stop 40%) | `renewal_m2` | first renewal date + 3 days; **not readable inside the beta for yearly founding members** | `payment_events` second successful charge / learners whose first term ended | Founding members pay a year up front, so this gate reads only monthly subscribers [OPEN for Muath, section 10] |
| "Very disappointed" 40%+ (stop 25%) | `very_disappointed_share` | cohort start + 28 days | `pmf_answer = very` / all `pmf_answer` | The PRD names the metric but not the ask; this document adds one in-app question, asked once in the week-4 proof's question slot in place of the worth-it question that week, with the three answers [DECISION, new event `pmf_answer`; OPEN for Muath on wording, section 10]. No email, because 3.10 allows none |
| Cost per session under $0.60 (stop over $1.00 with no plan) | `cost_per_session_p50` | from the first week | 4.1 row 22 | The mean is shown next to the median; the stop line is judged on the mean of the trailing 7 days |
| False-claim rate under 5% | `false_claim_rate` | first audit, 2027-01-01 | 4.5.3 | Monthly |
| Wrong memories under 1 in 100 callbacks | `wrong_memories_per_100` | cohort start + 14 days | 4.1 row 20 | 30-day window |
| New trials from referrals and forwarded samples 30%+ (stop 10%) | `referral_trials_share` | from the second invite batch | trials whose `waitlist.source in (share, referral)` / trials started | `waitlist.source` is set from the share page's `?ref=` and the invite's referrer field [ASSUMPTION: the client domain records `source`] |

When a gate is under its stop line for two consecutive readable weeks, `/admin/gates` marks it and `ops.page(P3)` adds it to the Tuesday ops review agenda. The decision rule stays PRD-v2 16.1's last sentence: find which claim failed before writing code; the dashboard only makes the failure visible.

### 4.5 Human review

#### 4.5.1 Episodes (PRD-v2 6.8)

The queue is the pipeline's `review_items` and `review_findings` (its D17); this domain owns the sampling job, the page and the loop.

- **`review/sample`** (Inngest cron, nightly 04:00 Riyadh): for each learner, keep a running count of items this calendar month; add every episode with `degraded`, `relisten=skipped`, `fallback`, or `editor_soft_fail` flags at once; fill up to 10 per learner per month with random shipped episodes, weighted toward episodes with a `followed_answer=little` or a `huh_per_min` above the learner's median (so the reviewer sees the ones that may be mispitched). In Milestone 0 and the first beta week, every shipped episode is queued (the pipeline's rule). Expected volume at 100 learners: about 1,000 items a month, 35 a day, about 4 hours of reviewer time a day at 6 minutes each [OPEN for Muath, section 10: the reviewer's hours and rate].
- **The page** `/admin/review/episodes`: script, article, audio player, editor verdict, the `why` reasons, the fitter's coverage and new-word list, side by side; the display name and `life_facts.people` names tokenized (security D14); the reviewer never sees transcripts, the notebook or any claim. One form: flags (`error`, `sameness`, `law`, `gloss`, `other`), the lines, a note, ban proposals, a `similarity_judgment` for the paired "too alike?" question when the item was sampled as a similarity pair.
- **The loop**: ban proposals are accepted or declined by Muath on `/admin/review/bans` and inserted by code with `source=review_finding`; `law` flags open a `law_corpus` PR automatically (the line, the surface, the flag) through a GitHub issue the engineer turns into the fixture; `error` flags with a line id are counted per prompt version in `measure_points(measure='review_error_rate')` so a prompt regression that the suite missed is visible within a week; `sameness` judgments feed the assessment of the similarity threshold (`similarity_p90` against `too_alike_human`); the monthly summary (findings by flag, by format, by prompt version) is on the first Tuesday's ops review.

#### 4.5.2 Calls [DECISION, extends 6.8 to the call]

The PRD reviews episodes; the move contract (5.4.6) and anxiety mode (5.4.7) are only measurable on real calls, and the governor counts what the host declared, not what the learner experienced. A `call_review_items` queue samples 2 calls per learner per month plus every call with `moves.violations ≥ 2`, every `end_reason in (crisis, abandoned, pipeline_error)` in a learner's first week, and every call where `anxiety_mode` was entered. The reviewer for calls in the beta is Muath himself (role `owner`), because a call transcript is the learner's own speech and the trust contract's promise 6 ("told, not inferred") means the fewest eyes possible; a `tagger` may read only transcripts of learners with `data_use=true`, anonymized through the security domain's `research/anonymize`, and only for calibration tagging, never for call review.

```sql
create table call_review_items (
  id uuid primary key, learner_id uuid not null, call_id uuid not null, sampled_reason text not null,
  state text not null default 'queued' check (state in ('queued','reviewed','actioned','closed')),
  created_at timestamptz default now(), reviewed_at timestamptz, reviewed_by text
);
create table call_review_findings (
  item_id uuid primary key references call_review_items(id),
  move_contract jsonb not null,   -- {recasts_ok, clarifications_ok, nudge_ok, recall_gaps_ok, retell_ok, praise_ok, never_rules_ok}
  anxiety_mode_appropriate boolean, law_flags text[], host_quality smallint check (host_quality between 1 and 5),
  recognizer_suspect boolean, notes text, prompt_change_ticket text
);
```

The page shows the verbatim transcript with timings, the host's declared `@moves` header per turn next to what it said, the governor's budget counters, and the captions as shown. Audio is not played on this page; a break-glass read of the audio requires a reason (security D2) and is a separate action.

#### 4.5.3 The monthly false-claim audit (PRD-v2 16.1)

`claims/audit-sample` (Inngest cron, the 1st of each month, 09:00 Riyadh) samples from `claims` with `status=shown` and `shown_at` in the previous month: all claims if fewer than 40, else 40 stratified by `kind` (every kind represented at least 3 times). It writes `claim_audits` rows and the auditor (Muath, or a second trained person [OPEN for Muath]) opens each on `/admin/review/claims`: the claim sentence as shown, the evidence (`claim_evidence`: the two sentences, or the two clips by byte range where voice storage is on), the gate inputs (`sem`, `n_pairs`, task types, `assessment_version`). Verdicts: `true` (the evidence supports the sentence as a learner would read it), `false` (it does not), `unclear` (the evidence is ambiguous or the sentence overstates). `false_claim_rate` = false / (true + false + unclear); unclear counts against. Above 5% for a kind: that kind is switched off with the flag `claims.kind.<kind>` (4.7) until the cause is fixed, and the next proof for affected learners says so (assessment D16's notice path).

```sql
create table claim_audits (
  id uuid primary key, claim_id uuid not null, sampled_for date not null,
  verdict text check (verdict in ('true','false','unclear')), reason text,
  audited_by text, audited_at timestamptz, created_at timestamptz default now()
);
```

#### 4.5.4 Access rules for every review surface

| Surface | `owner` | `engineer` | `reviewer` (paid native reader) | `tagger` (calibration) | `ops` |
|---|---|---|---|---|---|
| `/admin/review/episodes` (scripts, audio, verdicts; names tokenized) | read, action | read | read, file findings | no | no |
| `/admin/review/calls` (verbatim transcripts with timings) | read, file findings | read when on-call for an incident, logged | no | no | no |
| `/admin/review/claims` (claims with evidence, clips) | audit | read | no | no | no |
| `/admin/research` (anonymized text of `data_use=true` learners) | read | no | no | tag | no |
| Learner audio (any) | break-glass with reason | break-glass with reason | no | no | no |
| `/admin/measures`, `/admin/gates`, `/admin/alerts`, `/admin/incidents` | read | read | no | no | read |
| `/admin/flags`, `/admin/vendors`, admin actions | write | write | no | no | write (flags and vendors only) |

Every read of a learner-content page writes an `audit_log` row (security D13), which the learner's export includes.

### 4.6 Alerting on the Part 15 budgets and the cost stop line

**Severities.** P1 pages a phone at any hour and opens a Better Stack incident; P2 posts to `#forone-ops` and is handled in working hours (or at once if someone is awake); P3 goes into the 08:30 digest. Only six rule families may be P1 (listed first below); this is deliberate so a two-person team is never paged for a trend.

**Rule format.** Every rule is a SQL predicate over a window, evaluated by `ops/watch` every 5 minutes. A rule fires after `for` consecutive true evaluations and resolves after two false ones. `dedupe` groups incidents so one learner or one vendor produces one incident, not one per evaluation.

```yaml
# ops/alerts.yaml (every rule listed; the SQL of three is shown in full, the rest name their predicate)
- id: episode_not_ready_before_drop            # P1 family 1, PRD 15 "tomorrow's episode ready before the drop time"
  severity: P1
  sql: |
    select ls.learner_id, ls.next_drop_at
    from learner_schedule ls join sessions s on s.learner_id = ls.learner_id and s.state in ('done','closed')
    where ls.next_drop_at between now() and now() + interval '45 minutes'
      and ls.expects_drop                      -- yesterday was an active day (PRD 3.6 rule 2)
      and not exists (select 1 from episodes e where e.learner_id = ls.learner_id
                        and e.drop_at = ls.next_drop_at and e.status in ('ready','published'))
  for: 1
  dedupe: "{learner_id}:{next_drop_at}"
  runbook: ops/runbooks/R3-pipeline-late-for-drop.md
- id: fallback_3_in_7                           # P1 family 2, PRD 6.3; fired from pipeline.human_page, not SQL
  severity: P1
  source: event:pipeline.human_page
  dedupe: "{learner_id}:fallback"
  runbook: ops/runbooks/R4-bad-or-fallback-episode.md
- id: voice_both_vendors_down                   # P1 family 3, PRD 15 "second vendor within the same day"
  severity: P1
  sql: select 1 from vendor_health where capability in ('episode_tts','call_tts') group by capability having bool_and(state='degraded')
  for: 1
  runbook: ops/runbooks/R1-voice-vendor-outage.md
- id: recognizer_down                           # P1 family 3 (calls cannot run; notes cannot be written)
  severity: P1
  sql: select 1 from vendor_health where capability in ('streaming_stt','verbatim_stt') and state='degraded' and no_secondary
  for: 1
  runbook: ops/runbooks/R2-recognizer-outage.md
- id: privacy_promise_missed                    # P1 family 4, PRD 12.5, 15; from privacy.audit_failed and voice_objects_overdue
  severity: P1
  source: event:privacy.audit_failed
  sql_also: select 1 from media_objects where ephemeral and expires_at < now() - interval '2 minutes' and deleted_at is null
  for: 1
  runbook: ops/runbooks/R11-privacy-audit-failed.md
- id: spend_cap_or_stop_line                    # P1 family 5, PRD 14.5; from cost_guard.tripped and the daily cap
  severity: P1
  source: event:cost_guard.tripped
  sql_also: |
    select 1 from (select avg(cost_usd) m from session_costs where started_at > now() - interval '7 days') x where m > 1.00
  for: 1
  runbook: ops/runbooks/R8-cost-runaway.md
- id: platform_down                             # P1 family 6: Better Stack uptime on app.forone.app, api /v1/health, feed health.xml; heartbeats late
  severity: P1
  source: betterstack
  runbook: ops/runbooks/R7-platform-down.md

- id: host_reply_p50_20calls                    # P2, PRD 15 median under 1.5 s
  severity: P2
  sql: |
    select 1 from (select percentile_cont(0.5) within group (order by (metrics->>'reply_latency_p50_ms')::int) p50
                   from (select metrics from calls where ended_at is not null and kind='main'
                         order by ended_at desc limit 20) c) x where p50 > 1500
  for: 2
  runbook: ops/runbooks/R6-call-latency.md
- {id: host_reply_p95_20calls, severity: P2, predicate: "p95 of reply_latency over last 20 calls > 2500 ms", for: 2, runbook: R6}
- {id: call_connect_p95, severity: P2, predicate: "p95 connect_ms over last 20 calls > 3000", for: 2, runbook: R6}
- {id: talkback_p50, severity: P3, predicate: "p50 talkback_ms over last 50 talkbacks > 2000", for: 2, runbook: R6}
- {id: notes_late, severity: P2, predicate: "p50 of (notes.created_at - calls.ended_at) over last 10 calls > 90 s, or any single one > 5 min", for: 1, runbook: R9}
- {id: after_pass_late, severity: P2, predicate: "≥ 3 sessions in the last hour with after_pass completed_at - call ended_at > 10 min, or evidence_quality='partial' share > 20% today", for: 1, runbook: R9}
- {id: chat_opener_late, severity: P3, predicate: "p50 (first host chat_message - chat door open) > 30 s over last 20", for: 2, runbook: R9}
- {id: first_sound_slow, severity: P2, predicate: "p50 client_perf.first_sound_ms over last 5 onboardings > 60000", for: 1, runbook: R5}
- {id: on_demand_slow, severity: P2, predicate: "p50 (episode.streaming_started - trigger) over last 5 swaps/returns/pilots > 30 s (45 s for pilots)", for: 1, runbook: R3}
- {id: dropped_start_slow, severity: P3, predicate: "p50 client_perf.play_start_ms for dropped episodes today > 2000", for: 1, runbook: R5}
- {id: word_sheet_slow, severity: P3, predicate: "client_perf.word_sheet_open_ms rows today > 5% of tap events", for: 1, runbook: R5}
- {id: voice_failover_active, severity: P2, source: "event:voice.vendor_failover", runbook: R1}   # a failover that worked is P2; the next episode announces it
- {id: vendor_degraded_any, severity: P2, source: "event:vendor.degraded", runbook: R1 or R2 by capability}
- {id: editor_degraded_share, severity: P2, predicate: "episodes with editor degraded=true today > 3 or > 10%", for: 1, runbook: R4}
- {id: fallback_rate_day, severity: P2, predicate: "fallback episodes today / episodes today > 5% with n ≥ 10", for: 1, runbook: R4}
- {id: governor_violations, severity: P2, predicate: "sum(moves.violations)/sum(host turns) over last 50 calls > 5%", for: 2, runbook: R6}
- {id: session_cost_over_1, severity: P2, predicate: "any session_costs.cost_usd > 1.00 in last hour", for: 1, dedupe: "{session_id}", runbook: R8}
- {id: cost_p50_7d_over_080, severity: P2, predicate: "mean session cost trailing 7 days > 0.80", for: 1, runbook: R8}
- {id: cache_hit_low, severity: P3, predicate: "cached_input_tokens / input_tokens over teacher+writer+host calls today < 0.90", for: 1, runbook: R8}
- {id: outbox_growing, severity: P1, predicate: "count(outbox unsent) > 100 for 5 min (Inngest unreachable)", for: 1, runbook: R7}
- {id: crisis_activation, severity: P2, source: "event:crisis.activated", dedupe: "{learner_id}:{event_id}", runbook: R10}  # Slack at once, human reads within 24 h; the protocol itself is in-product
- {id: wrong_memory_flag, severity: P3, source: "event:memory.flagged", runbook: R12}
- {id: wrong_memory_rate, severity: P2, predicate: "wrong_memories_per_100 (30 d) > 1.0 with callbacks ≥ 200", for: 1, runbook: R12}
- {id: claims_retracted, severity: P2, source: "event:claims.retracted", runbook: R12}
- {id: review_backlog, severity: P3, predicate: "review_items queued > 120 or oldest queued > 7 days", for: 1, runbook: none (reviewer capacity)}
- {id: eval_nightly_failed, severity: P3, source: "event:eval.completed passed=false", runbook: none (engineer reads the report)}
- {id: canary_failed, severity: P2, source: "event:ops.canary_completed passed=false", runbook: R1}
- {id: rater_pin_violated, severity: P2, predicate: "recording/rate refused a run (assessment D12)", for: 1, runbook: R4}
- {id: heartbeat_late, severity: P1, source: betterstack, monitors: [measures/daily, ops/watch, privacy/verify, retention/daily], grace: 30 min}
```

**4.6.1 Every Part 15 budget and its signal.**

| Budget (PRD-v2 15) | Signal | Source | Rule |
|---|---|---|---|
| First sound under 60 s | `client_perf.first_sound_ms` | client | `first_sound_slow` |
| First spoken English sentence under 5 min | `client_perf.first_english_ms` | worker | measure 18 only; no alert (the learner's own pace moves it) |
| Sample playable under 30 s | `client_perf.sample_first_sound_ms` (anonymous telemetry) | client | P3 if p50 today > 30 s |
| Pilot playback under 45 s | `episode.streaming_started - onboarding.intake_completed` | workflows | `on_demand_slow` |
| Dropped episode start under 2 s | `client_perf.play_start_ms` | client | `dropped_start_slow` |
| On-demand episode under 30 s | `episode.streaming_started - trigger event` | workflows | `on_demand_slow` |
| Call connect under 3 s | `calls.metrics.connect_ms` | worker | `call_connect_p95` |
| Host reply p50 1.5 s, p95 2.5 s | `calls.metrics.reply_latency_*` | worker | `host_reply_p50_20calls`, `host_reply_p95_20calls` |
| Talkback under 2 s | `calls.metrics.talkback_ms` | worker | `talkback_p50` |
| Word sheet under 300 ms | `client_perf.word_sheet_open_ms` (logged only when over) | client | `word_sheet_slow` |
| Notes under 90 s | `notes.created_at - calls.ended_at` | workflows | `notes_late` |
| Chat opener under 30 s | first host `chat_message` minus door open | workflows | `chat_opener_late` |
| After-session pass within 10 min | `session.after_pass.completed` minus `call.ended` | workflows | `after_pass_late` |
| Episode ready before drop; on-demand at drop minus 90 min | `episodes.status` at drop minus 45 min | workflows | `episode_not_ready_before_drop` |
| Audio deleted within 15 min (storage off) | `media_objects` ephemeral overdue; `privacy/verify` | data, security | `privacy_promise_missed` |
| All audio deleted within 24 h of revoke | `privacy/verify` | security | `privacy_promise_missed` |
| Live voice failure falls back to voice notes | `end_reason=fallback` share | worker | P3 if > 10% of calls today |
| Voice vendor outage: second vendor same day | `vendor.degraded`, `voice.vendor_failover` | topology, pipeline | `voice_failover_active`, `voice_both_vendors_down` |
| Cost: $0.60 budget, $1.00 stop line | `session_costs` (a view over `vendor_calls` and `episodes.cost_usd` maintained by the cost domain) | cost | `session_cost_over_1`, `cost_p50_7d_over_080`, `spend_cap_or_stop_line` |

```sql
create table alert_state (
  rule text not null, dedupe_key text not null, state text not null check (state in ('firing','resolved')),
  severity text not null, since timestamptz not null, last_eval timestamptz not null, resolved_at timestamptz,
  incident_ref text, context jsonb, primary key (rule, dedupe_key, since)
);
create table incidents (
  id uuid primary key, opened_at timestamptz not null, closed_at timestamptz, severity text not null,
  title text not null, rules text[] not null, learner_ids uuid[], runbook text, owner text,
  timeline jsonb not null default '[]', postmortem_path text, security_incident_id uuid   -- links the security domain's table when relevant
);
```

### 4.7 Feature flags

```sql
create table feature_flags (
  key text primary key, state text not null check (state in ('off','allowlist','percent','on')),
  percent smallint, allowlist uuid[], "default" boolean not null default false,  -- the value when the table is unreachable
  description text not null, changed_by text not null, changed_at timestamptz not null default now()
);
```

Flags that exist in the beta, with their default on 2026-12-07:

| Key | Default 12-07 | What it gates | Kind |
|---|---|---|---|
| `round_two` | off → allowlist in week 2 of the beta | PRD 5.4.9 [P1] | P1 rollout |
| `shadowing` | off | 5.2 [P1] | P1 rollout |
| `dial_in` | off | 5.4.12 [P1] experiment, allowlist only | P1 rollout |
| `finale` | off → on when the first season boundary approaches (2027-01-03) | 11.2 [P1] | P1 rollout |
| `tape` | off | 12.3 the tape [P1] | P1 rollout |
| `claims.kind.fluency_change`, `...accuracy_change`, `...complexity_change` | off (and the gate refuses anyway until `n_pairs ≥ 12`) | 11.1 full proof [P1]; also the audit's kill switch (4.5.3) | kill switch |
| `claims.kind.first_ever`, `...word_owned`, `...did_it` | on | the simple proof [P0]; off only in an audit emergency | kill switch |
| `host.model=haiku` | off | the call domain's measured fallback as a lever | vendor lever |
| `tts.batch` | off | the pipeline's P1 batch TTS lever | vendor lever |
| `pipeline.editor_model` | on | off = code checks only (degraded) during a Gemini outage | kill switch |
| `notes.enabled` | on | off = "Salma is resting today" and no notes (law-safe degraded state) | kill switch |
| `chat.enabled`, `talkback.enabled` | on | kill switches | kill switch |
| `drop.push` | on | off = feed alert only | kill switch |
| `observer_slot` | off | the call domain's reserved slot [LATER] test | experiment |

Rules: a flag never changes a law (there is no flag for recasts, the allowance, the three message kinds, consent, or the claim gate's rules); a kill switch's `default` is its safe state; every flip writes `audit_log` and `flag.changed`; a flag older than 60 days with state `on` is a cleanup ticket.

### 4.8 Runbooks

Each runbook is one page in `ops/runbooks/` with the same five headings. The twelve, condensed:

**R1 Voice vendor outage (episode TTS or call TTS).** *Detect:* `vendor.degraded` (5 failures in 10 min), `voice.vendor_failover`, `canary_failed`, or a learner saying the host sounds different. *First five minutes:* confirm on the vendor's status page; check `/admin/vendors` shows the secondary active for `episode_tts` and `call_tts`; check the pipeline's `failover.active` is sticky. *Fix:* if the automatic switch did not happen, flip `vendor_config` on `/admin/vendors` (no deploy); if both vendors are down (P1), set `pipeline.editor_model` unaffected, let `day/next` ship yesterday's episode state (the Today screen keeps the unplayed episode; no drop push fires for an episode that is not ready, PRD 3.6) and switch calls to the voice-note fallback by flag `talkback.enabled=off` plus the worker's own fallback path. *Verify:* `ops/canary` on the active vendor passes; the next shipped episode carries the one-line announcement (PRD 7.1). *Tell the learner:* nothing beyond that line; never an email. *Afterwards:* switch back only after a passing canary, during the release window, and announce again.

**R2 Recognizer outage (streaming or verbatim).** *Detect:* `vendor.degraded` for `streaming_stt` or `verbatim_stt`; `notes_late`; `evidence_quality=text_only` share rising. *First five minutes:* streaming down means calls cannot run: confirm the worker is sending new calls to the secondary (Deepgram) by `vendor_config`; if no secondary passes the 10.14 gate [ASSUMPTION: Deepgram is wired as the hot secondary per the call domain's P1 plan; before that, the fallback is voice notes], set calls to the voice-note fallback. Verbatim down means notes and claims lose evidence: the call domain keeps audio until the 15-minute window; after that, evidence is low-confidence and makes no claims (PRD 5.4.11), which is the designed behaviour. *Fix:* flip the vendor; re-run `call/verbatim-turn` for turns whose audio still exists (`/admin/calls/{id}/retranscribe`, only while audio exists). *Verify:* `recognizers` suite on the secondary; `notes_late` resolves. *Tell the learner:* the notes door says "no notes for this call" when none could be made; nothing else.

**R3 Pipeline late for the drop.** *Detect:* `episode_not_ready_before_drop` (P1 at drop minus 45 min), `on_demand_slow`, Inngest run failures. *First five minutes:* open the Inngest run for `episode/produce` for that learner; the step that is stuck names the vendor (teacher batch not returned, TTS slow, editor loop). *Fix, in order:* if a batch result is late, the pipeline's cut lines should already have re-run at standard price; if not, cancel and re-run the function with `pricing_mode=standard` from `/admin/episodes/{id}/rerun`; if a vendor is down, R1 or R2; if the editor is looping, force `pipeline.editor_model=off` for that run (ships code-checked, flagged for review). If nothing can ship by the drop time: do nothing to the learner's screen. The unplayed previous episode stays as today's hero and no push fires (PRD 3.6 rule 2); the late episode publishes when ready and the push fires then. *Verify:* `episodes.status=published`, `drop.published`. *Tell the learner:* nothing. The Milestone 0 "a day late" message is replaced by silence plus the late drop, because a late drop is not one of the three message kinds (3.10). *Afterwards:* if more than 3 learners were late in one morning, a postmortem within 7 days.

**R4 Bad or fallback episode shipped.** *Detect:* `fallback_3_in_7`, `editor_degraded_share`, a reviewer `law` or `error` flag on a shipped episode, a learner message. *Decide:* a shipped episode is **pulled** only when it breaks law 5 (a fact the learner did not supply, a fake life), law 1 or 10 (game or lesson language), or memory rule 8.4 (an unconfirmed or "don't bring up" fact); an episode that is merely weak is not pulled. *Fix:* `/admin/episodes/{id}/pull` [DECISION, new admin action]: sets `episodes.status=pulled`, removes the feed item (the enclosure returns 410), replaces Today's hero with a fallback episode produced on demand at standard pricing (`episode_kind=fallback`), writes `episode.pulled`, and gives Salma one plain Arabic line on Today, "سحبنا حلقة اليوم بسبب خطأ من عندنا، وهذي بديلة." (we pulled today's episode because of a mistake on our side; here is a replacement). The pulled episode stays in the archive only if the learner already played at least half of it (it is theirs), marked with the same line; otherwise it is deleted. *Verify:* the new episode passes the editor; the review item is filed with the cause; the law corpus or the editor fixtures gain the case. *Tell the learner:* that one line and, if a wrong fact was spoken, R12's correction path. *Afterwards:* three fallbacks in 7 days means the learner's model or interests are thin: Muath reads the three teacher briefs and, if the cause is a sparse intake, asks Salma to ask one more question next session (within 2.4's one-question rule).

**R5 Client latency budgets missed (first sound, dropped start, word sheet).** *Detect:* `first_sound_slow`, `dropped_start_slow`, `word_sheet_slow`. *Fix:* for first sound, check the Salma onboarding clip is served from the package cache and the pre-account session path; for dropped start, check the service-worker precache hit rate in `client_perf.context.cached`; for the word sheet, check `glosses.json` size and the index version. None of these is a page; they are Tuesday items unless p50 doubles.

**R6 Call latency or governor violations.** *Detect:* the four latency rules, `governor_violations`. *First five minutes:* `vendor_calls` for the last 20 calls grouped by role shows which hop grew (STT final, LLM first token, TTS first byte); the cached-prefix hit rate (`cache_hit_low`) is the usual cause of LLM first-token growth. *Fix:* vendor hop → R1/R2 or `vendor_config`; LLM → check for a prompt change that broke the cached prefix (release manifest diff) and roll back the prompt version; violations → the `host` suite on the current prompt version, then roll back. *Verify:* `calls_50` on staging passes the gates.

**R7 Platform down (Vercel, `api`, Postgres, Inngest).** The topology's section 5 table is the fix list; this runbook adds the order of checks (Better Stack → ECS events → RDS events → Inngest status), the fact that calls in progress survive an `api` outage for 10 minutes by spooling, and that the feed keeps serving while `api` is up. `outbox_growing` is the Inngest-down signal; once Inngest returns, `outbox/relay` drains and a human re-sends `idea.chosen` from `/admin` only for learners whose `day/next` run was lost.

**R8 Cost runaway and the stop line.** *Detect:* `cost_guard.tripped` (per learner per day, security D11), the daily spend cap (topology), `session_cost_over_1`, `cost_p50_7d_over_080`. *First five minutes:* `/admin/measures?m=cost_per_session` with `extra.top10`; the cost domain's per-role breakdown for the day; look for a retry storm (`pipeline_steps` with `outcome=retry` count), a cache miss (`cache_hit_low`), a rewrite loop (fitter rounds > 2), or a long call (`metrics.duration_ms > 8 min`, which the governor should prevent). *Fix:* the bug; or the levers in order of least learner impact: batch everything nobody waits on, episode dial to 5 minutes, `tts.batch`, `host.model=haiku` after the `host` suite passes. *The stop line* ($1.00 mean over 7 days) is not an engineering alert: it opens a ticket to Muath with the breakdown and the costed plan, and PRD 14.5 says the beta stops without one [OPEN for Muath on who decides to stop].

**R9 Notes, chat opener or after-pass late.** *Detect:* `notes_late`, `after_pass_late`, `chat_opener_late`. *First five minutes:* Inngest run for `session/after-pass`: stage-1 step over 60 s is almost always the verbatim turn of the last learner turn (R2) or the Sonnet notes call. *Fix:* vendor → R1/R2; if the after-pass is failing in a code stage, the data domain's rule applies (`finish` runs with `evidence_quality=partial`; the teacher plans with `evidence_lag`); re-run with `/admin/sessions/{id}/rerun-after-pass` once fixed (the rebuild path makes this safe). *Tell the learner:* Today already shows "Salma is writing your notes"; if notes cannot be made within 10 minutes the door shows "no notes for this call", never a spinner forever.

**R10 Crisis activation follow-up.** The in-product protocol (PRD 7.9, security D9) has already run. *Detect:* `crisis_activation` in Slack. *Within 24 hours:* Muath reads the quarantined turn on `/admin/crisis/{id}` (owner only; the turn is quarantined from every store), confirms the resources card was shown, and decides whether a personal message as himself is appropriate (the Milestone 0 practice). No show content touches the topic. *Record:* the `crisis_log` row is complete for the SB 243 count; nothing else is written.

**R11 Privacy audit failed.** *Detect:* `privacy.audit_failed`, `privacy_promise_missed`. *First five minutes:* `/admin/privacy` names the window (15 min ephemeral, 24 h revoke, 24 h delete, 30 d backup) and the objects. *Fix:* run the doer by hand (`audio/expire`, `learner/purge-audio`, `learner/delete`) from `/admin`; if the doer cannot delete (key missing, S3 error), escalate to the security domain's incident runbook, because a missed window is an incident the learner was promised would not happen. *Afterwards:* an `incidents` row with the minutes missed; a postmortem; the learner is told only if data was exposed, by the security runbook's rules.

**R12 Wrong memory reported.** *Detect:* `wrong_memory_flag` (P3 digest), `wrong_memory_rate` (P2), a learner message. The in-product path has already run (`memory/correct`: fact fixed at once, dependents invalidated, "My mistake, noted."). *Within a day:* read the `memory/correct` outcome on `/admin/learners/{id}/memory`; if `status=unresolved` (no fact matched), resolve it by hand: find the fact or the canon row and mark it; check whether a voiced-but-unplayed episode cites it (the pipeline re-runs editor check 4; confirm it did); if a shown claim quoted the disputed text, confirm `claims.retracted` fired and the next proof carries the notice. *Afterwards:* every wrong memory is a bug (trust promise 7): the finding goes into `eval/fixtures/facts/` as a regression case for the `memory` suite, with the cause (quote mismatch, expired fact spoken, superseded fact spoken, sensitivity leak).

Two admin actions these runbooks rely on, both `owner` or `engineer`, both audited, both idempotent: `POST /admin/episodes/{id}/pull` and `POST /admin/sessions/{id}/rerun-after-pass`. The topology's `/admin/vendors` failover switch and the data domain's `learner.rebuild_requested` button are the other two levers.

### 4.9 Tracing and logging

**One log line schema** for all three Python services and the worker, emitted by `forone.ops.log` (structlog JSON):

```json
{"ts":"2026-12-09T04:41:12.318Z","level":"info","service":"workflows","env":"prod",
 "event":"step.completed","fn":"episode/produce","step":"editor","inngest_run_id":"01J...","trace_id":"a1b2...",
 "learner_id":"7f3c...","episode_id":"01JA...","session_id":null,"call_id":null,
 "learner_model_version":412,"prompt_version":"editor_rubric@1.1.0","vendor":"google","model":"gemini-3.8-flash",
 "latency_ms":4120,"cost_usd":0.0041,"outcome":"pass","degraded":false}
```

Allowed in logs: every id (learner, session, episode, call, event, run, trace), enums, counts, durations, costs, versions, vendor names, step names, error classes and sanitized error messages. **Never in logs:** display names, emails, phone numbers, birth dates, any transcript or chat text, any life fact or quote, idea text, any audio reference's content, prompts, completions, feed tokens, OTP codes, API keys. The scrubber `forone.ops.logscrub` is applied at the logger, not by callers: it drops any field whose name is in `forone.learner.pii`'s classified set, truncates any string field over 200 characters, replaces anything matching the security domain's typed-token patterns (email, phone, URL, 5+ digit runs) and refuses (raises in dev, drops in prod with a counter `logscrub_dropped_total`) any field named `text`, `quote`, `transcript`, `prompt`, `completion`, `content`, `body`. CI runs the scrubber over `eval/fixtures/pii_corpus.jsonl` (300 lines seeded with every PII shape, in Arabic and English) and asserts zero leaks.

**Correlation.** `trace_id` is minted by `api` per request and by `workflows` per Inngest run (the run id doubles as it), carried in every Inngest event's metadata as a scalar (so Inngest sees pointers only), set on every adapter call (`CallMeta.trace_id`), and attached to every Sentry event. A bad episode is traced as: `episodes.id` → `pipeline_runs.inngest_run_id` → the Langfuse trace (by `trace_id`) with every prompt and completion → `pipeline_steps` with versions and cost → `release_manifest` for what was deployed at the time → the `learner_model_versions` row for what the teacher read.

**What goes where.**

| Store | Holds | Learner text? | Retention | Owner |
|---|---|---|---|---|
| CloudWatch Logs | the log lines above, EMF counters | never | 30 days | this domain |
| Sentry (EU) | exceptions with scrubbed context: ids, versions, step; browser errors from `web` | never (scrubber plus Sentry's server-side scrubbing on `text`, `quote`, `transcript`) | 90 days | this domain |
| Langfuse (EU) | every model call: prompt, completion, tokens, cost, `user_id=learner_id`, `learner_model_version`, `prompt_version`, `trace_id` | yes, with display names tokenized (security D14's middleware rule); no audio | 30 days (security domain's setting) | cost domain |
| Postgres (`pipeline_steps`, `vendor_calls`, `calls.metrics`, `eval_runs`, `alert_state`, `incidents`) | structured facts about runs | no | the row's own rules | the owning domains |
| Better Stack | incident titles with ids only | never | vendor default | this domain |
| `#forone-ops` Slack | alert titles with ids, deploy notes, canary results | never (the poster uses the same scrubber) | Slack default | this domain |

Sampling: 100% of everything in the beta; at 10,000 learners Langfuse can sample to 20% except calls in the assessment and claim path (the cost domain's note); logs stay at 100% because they hold no content.

### 4.10 The operational calendar of the beta

All times Riyadh (UTC+3). The drop window is 05:30 to 08:30 (most learners pick a commute slot [ASSUMPTION from Milestone 0's 06:30 slot being the most chosen]).

| Cadence | When | What | Who | Mechanism |
|---|---|---|---|---|
| Every 5 min | always | `ops/watch` evaluates `ops/alerts.yaml` | automatic | Inngest cron, heartbeat to Better Stack |
| Daily | 04:00 | `review/sample` fills the review queues | automatic | Inngest cron |
| Daily | 06:30 | `measures/daily` (yesterday's learner-days and cohort rollups); then `privacy/verify` (security) and `retention/daily` (data) | automatic | Inngest crons, heartbeats |
| Daily | 08:30 | The digest: P3 alerts, yesterday's cost per session (p50, mean, top 3), fallbacks, degraded counts, review backlog, eval nightly result, late drops | automatic → Slack | `ops/digest` |
| Daily | 08:30 to 09:00 | On-call reads the digest and `/admin/alerts`; closes or escalates | primary | checklist in `ops/runbooks/daily.md` |
| Nightly | 02:00 | `eval/nightly`: the 10-fixture `pipeline` smoke plus `law_scan`, `claim_gate`, `fitter` on staging | automatic | GitHub Actions schedule |
| Weekly | Monday 07:00 | `measures/weekly`; the cost domain's weekly cost report (per role, vendor, learner; heavy-use outliers next to it, PRD 14.5); `ops/canary` for each voice vendor (one episode, one call on the synthetic learner) | automatic | Inngest crons |
| Weekly | Monday 10:00 | Invite batch of about 50 goes out (PRD 2.1.6); the cohort key is created | Muath | `/admin/invites` (client domain) |
| Weekly | Tuesday 11:00, 30 min | Ops review: the cost report against $0.60 and the path to $0.35; the gates page; firing and resolved alerts; incidents; review findings summary; flags older than 60 days; next week's releases | Muath plus engineers | agenda generated by `ops/digest --weekly` |
| Weekly | Tuesday after the review | On-call handover | engineers | `ops/oncall.yaml` |
| Weekly, per learner | learner's proof day | `proof/fanout` (assessment domain); the simple proof from 2026-12-14 for the first cohort | automatic | |
| Monthly | 1st, 09:00 | `claims/audit-sample` → false-claim audit due by the 7th; `vendor/regress` (recognizer and pronunciation suites on the current vendor models, because vendors update silently); the human review month closes: findings summary, ban-list PR, similarity threshold check, law corpus PR | automatic, then Muath and the reviewer | first audit 2027-01-01 for December |
| Every 4 weeks | window boundaries 2026-12-07, 2027-01-04, 2027-02-01 | Rater window: `rater_versions` row for the new window; `calibration/run` must have passed on the pinned model before the window opens; the assessment domain's `pinned_until` set | engineer | checklist; `rater_pin_violated` alert |
| Per learner, every 4 weeks | the learner's day 28 and after | Season boundary: `season.boundary` → finale (flag `finale`, P1) and the then-and-now comparison where two recordings exist; the first boundaries fall from 2027-01-03 (for 2026-12-07 starters), inside the beta | automatic | the dashboard shows "finales due this week" from `seasons` |
| Per learner, week 1 | session 2, then once in sessions 3 to 5 | The first "then" recording is offered (P0); `recordings` count per cohort on `/admin/measures` so a low take-up is seen in week 1 | automatic | |
| Dated | 2026-11-13 | Hume shuts its voice APIs: nothing to do (not used); confirm no adapter references it | engineer | grep in CI |
| Dated | 2026-11-16 | Payment processor decided (Part 18 #2); processors approved (security domain) | Muath | |
| Dated | 2026-12-05 12:00 to 12-08 12:00 | Release freeze around launch | all | `tools/release` refuses |
| Dated | 2026-12-07 | Beta opens; first cohort; on-call doubled (both engineers) 05:00 to 09:00 for the first 3 days | all | |
| Dated | 2026-12-31 to 2027-01-02 | Freeze; on 2027-01-01 the `price_book`/`prices.yaml` row for the Gemini doubling becomes active; the Monday 2027-01-05 cost report is read with that in mind | engineer | the dated row already exists (cost domain) |
| Dated | 2027-01-04 | First readable "active in week 4" for cohort 2026-12-07 | Muath | `/admin/gates` |
| Dated | 2027-01-10 | Gate review (PRD 19.3): the gates page frozen as a snapshot into `bench/reports/gate-review-2027-01-10.json` | Muath | |

### 4.11 On-call for a two-person team

```yaml
# ops/oncall.yaml
rotation: weekly, handover Tuesday 12:00 Riyadh
primary: [engineer_a, engineer_b]        # alternate weeks; with one engineer, the engineer every week and Muath as primary on Fridays
escalation: muath                        # after 15 min unacknowledged on P1
pages: P1 only (the six families in 4.6); P2 never calls a phone
protected_hours: 05:00-08:30             # the drop window: P1 acknowledges within 5 min
quiet_hours: 23:00-05:00                 # P1 still pages; the rule is that only P1 can
tools: Better Stack (schedule, phone escalation, status of heartbeats), Slack, /admin
handover: ops/runbooks/handover.md       # open incidents, flags flipped this week, vendor state, anything degraded
```

What the on-call person does each day is the 08:30 checklist (4.10). What they must never do alone: flip a vendor back from an understudy outside the release window, change a prompt version in prod, read learner audio without a reason row, or send any message to a learner (there are three kinds and none is manual). What is explicitly accepted because the team is small: no second responder at night; a P2 found at 02:00 waits for 08:30; a vendor outage of both voice vendors at 03:00 means voice notes until morning, which PRD 15 allows; a review backlog over a week is a capacity item, not an incident.

## 5. Failure modes, fallbacks and degraded modes

This domain's own failures must never degrade the product; the table says what each one costs and what the learner notices (always nothing).

| Failure | Detected by | Fallback | Learner notices | What is lost |
|---|---|---|---|---|
| `ops/watch` stops (Inngest cron missed, bug) | Better Stack heartbeat late by 30 min → P1 | Better Stack's uptime checks still page for platform-down; CloudWatch alarms still page for infrastructure; the product runs | Nothing | Product-budget alerts for the gap; `alert_state` resumes on the next run |
| Better Stack down | its own status; Slack posts still arrive | `ops.page()` falls back to a Slack `@channel` post for P1 and an email through Resend to both engineers | Nothing | Phone escalation during the outage |
| Slack down | `ops.page()` HTTP error | Better Stack incidents still page; P2 and P3 queue in `alert_state` and post when Slack returns | Nothing | Visibility for a few hours |
| `measures/daily` fails or runs late | heartbeat; `measures.completed` missing | Re-run is idempotent (upsert by primary key); yesterday's rows appear a day late; nothing downstream depends on them | Nothing | A late dashboard |
| A measure definition is wrong | `measures_replay` in CI, a Tuesday review | `recompute()` under a new `measures_version`; old rows stay for comparison | Nothing | Nothing permanent |
| Sentry unreachable | SDK buffers then drops | logs still carry the error class and `trace_id` | Nothing | Stack traces for the gap |
| Langfuse unreachable | adapter middleware's async queue fills | the middleware never blocks the call; spans are dropped after the queue limit; `vendor_calls` rows (Postgres) still carry cost and versions, so cost tracing survives (PRD 14.5) | Nothing | Prompt and completion text for debugging |
| `eval-gate` cannot reach a vendor in CI | job error | the check fails closed for prompt and model changes (a version bump cannot merge until the suite runs) and is skipped for unrelated paths | Nothing | A delayed merge |
| `eval-gate` flaky on a model-judged metric | two runs disagree | metrics judged by a model (`editor_agreement_with_human`, `fact_precision`) use the mean of 3 runs when within 1 point of the threshold; hard metrics (`law_words_recall`, `ban_hits`, `sensitive_never_unconfirmed`, `nudge_budget`) are code and never flaky | Nothing | CI minutes |
| Baseline missing (first run of a suite) | `baseline_run_id is null` | floors and ceilings only | Nothing | Regression detection for that one run |
| `ops/canary` fails on the secondary vendor | `canary_failed` P2 | the primary is unaffected; the secondary is marked `cold` on `/admin/vendors` and the understudy switch is disabled until it passes | Nothing | Same-day failover guarantee until fixed (that is why the canary is weekly) |
| Review backlog grows past a week | `review_backlog` P3 | sampling continues; the oldest items are reviewed first; degraded and fallback items jump the queue | Nothing | The month's 10-per-learner target slips |
| The false-claim audit finds > 5% for a kind | the audit | flag `claims.kind.<kind>=off`; affected learners' next proof carries the notice (assessment D16) | A proof with fewer claims and one honest line | The claim kind until fixed |
| Log scrubber drops a field it should keep | `logscrub_dropped_total` rising | the field name is reviewed; dropping is the safe direction | Nothing | A debugging field |
| Log scrubber misses a PII shape | a reviewer, the pii corpus | the corpus gains the shape; CloudWatch log group is purged for the window (`aws logs delete-log-stream`) and the security incident runbook decides on notification | Nothing | Nothing if caught in the corpus first |
| A P1 page at 03:00 nobody answers | Better Stack escalation to Muath after 15 min, then repeat every 15 min | the product's own fallbacks (understudy voice, voice notes, unplayed episode stays) hold until morning | Possibly a late episode or a voice-note call | One drop for the learners in that window |
| A flag read fails (Postgres unreachable) | exceptions in `flag()` | the flag's `default` (safe state) | Nothing | A P1 feature off for the outage |

Degraded modes that are counted, never silent (every one is a `measure_points` series and a digest line): editor `degraded`, `relisten=skipped`, `timing_quality=sentence`, `failover.active`, `fallback_rules` (teacher), `notes.degraded`, `evidence_quality in (partial, text_only)`, `analyst_validation_drop`, `move_violation`, `header_missing`, `end_reason in (fallback, pipeline_error, abandoned)`, `verbatim_failed`, `claims.retracted`, `privacy_audit_runs.verified=false`.

## 6. Cost and performance against the budgets

**Fixed monthly cost of this domain (beta, 100 to 200 learners).**

| Item | Beta | At 10,000 learners | Note |
|---|---|---|---|
| Sentry (Team, EU) | $26 | about $80 | errors only, scrubbed |
| Better Stack (uptime + on-call with phone) | about $30 | about $100 | the one tool that calls a phone |
| CloudWatch Logs and alarms | about $15 | about $150 | 30-day retention; EMF metrics |
| Slack | $0 (free tier) | $0 | one channel |
| `eval-gate` runs (3 to 5 version bumps a week × about $5 average) | about $80 | same | mostly `pipeline` and `host` suites |
| `eval/nightly` (10-fixture smoke, about $3) | about $90 | same | can drop to weekly after the build |
| `ops/canary` (2 vendors × 1 episode + 1 call, weekly) | about $5 | same | |
| `vendor/regress` (monthly, 30 clips × 4 recognizers + pronunciation) | about $2 | same | |
| `calibration/run` on bumps (assessment domain's cost) | about $5 | same | counted here because `eval-gate` triggers it |
| Reviewer and audit time | [OPEN for Muath] | | about 4 h/day at 100 learners for episodes alone |
| **Total tooling and runs** | **about $250 to $300 a month** | about $600 a month | |

Against the per-session number (PRD 14.5): none of this is in the session cost scope, which is generation and session roles plus "proof share and hosting". Spread over about 1,600 sessions a month at 100 learners it would be $0.15 to $0.19 a session of fixed overhead, falling to under $0.01 at 10,000 learners. The digest and the weekly cost report show it as a separate "fixed" line so it is never confused with the $0.60 budget or the $1.00 stop line. The security domain's $60 cap for its own fixed cost is a sibling line; the topology's "Sentry, Better Stack, Resend, domains about $60/month" overlaps the first three rows here, so the integrator should keep one of the two estimates (this one is itemized).

**Performance.** `ops/watch` runs about 40 queries every 5 minutes against indexed tables with recent-window predicates; measured budget 5 s per run (alert if over 60 s, which would itself mean Postgres is in trouble). `measures/daily` touches every learner's last day of events (about 300 events per active learner-day) and the stores: under 2 minutes at 500 learners on the beta instance; a 28-day recompute of all measures under 20 minutes. Nothing in this domain runs in a learner's request path or in a call. The `/admin` pages read through `forone_readonly` with `statement_timeout = 10 s` so an expensive ad hoc query cannot stall the API.

**Levers this domain provides toward $0.35:** the measured cost per session by role and by lever (the weekly report, with `extra.top10`), the `host` suite that makes the Haiku-host switch a measured decision, the `tts.batch` and `pipeline.editor_model` flags that make the cheaper modes reversible, and `cache_hit_low`, which protects the single largest silent cost leak (an uncached prefix costs about $0.03 a session, pipeline domain 6).

## 7. Build plan for 2026-11-02 to 2026-12-06

The rule for this domain: it ships inside the other domains' weeks, on top of what they build, and never costs more than about one engineer-week in total before 2026-12-07. P0 here means "the beta cannot be run safely without it"; the offline suite is P1 by the PRD, but its fixtures and the cheap code-only checks land early because the Milestone 0 data is free and the build itself needs them.

| Week | Dates | Ships (this domain) | P0 / P1 | What the Milestone 0 data lets us test |
|---|---|---|---|---|
| 1 | 11-02 to 11-08 | `forone.ops` skeleton: structlog JSON logger with `logscrub` and the `pii_corpus` test; Sentry wired in all services with scrubbing; Better Stack account, uptime checks on staging, one heartbeat; `#forone-ops`; `ops.page()` with Slack only; `tools/import_m0.py` writes the fixtures listed in 4.2 (learner files, scripts with hand coverage, editor reads, transcripts and tags, 30 clips, facts, notes, similarity pairs); `eval/suites.yaml` with `fitter`, `law_scan`, `claim_gate` (code-only suites) and the `recognizers` suite wrapping `tools/call-bench recognizers`; `versions.yaml` v1 | P0 (logging, paging, fixtures), P1 (suite harness) | The 30 clips produce the 10.14 result and the first `error_survival_rate` baseline; the 20 hand-checked scripts are the fitter's regression; the law corpus is seeded from Muath's step-8 catches and the bible's BANNED list |
| 2 | 11-09 to 11-15 | `eval_runs` table and `tools/eval run`; suites `editor`, `writer`, `pipeline` (10 fixtures), `memory`; `eval-gate` CI job with the path map; the first baselines on `main` from the Milestone 0 fixtures; `release_manifest` and `tools/release cut`; `ops/alerts.yaml` v1 with the pipeline rules (`episode_not_ready_before_drop`, `fallback_3_in_7`, `editor_degraded_share`, `fallback_rate_day`, `voice_failover_active`, `canary_failed`) and `ops/watch`; `ops/canary` weekly on the synthetic learner; `feature_flags` table and `flag()` | P0 (alerts for the pipeline, release tooling, flags), P1 (suites) | Every Milestone 0 package through the Gemini editor against Muath's reads gives `editor_agreement_with_human`; the 15 learner files through teacher-to-editor give `editor_pass_first_try`, `fallback_rate` and cost per step; scripts judged "too alike" set `similarity_cosine` (Part 18 #10) |
| 3 | 11-16 to 11-22 | `forone.measures` v1 with measures 3, 4, 10, 11, 13, 14, 18, 22 (the ones the onboarding, player and word sheet produce) and `measure_points`; `/admin/measures` (tables, 28-day sparklines); client-budget alert rules (`first_sound_slow`, `dropped_start_slow`, `word_sheet_slow`, `on_demand_slow`); the device test matrix runbook for the client domain's week-3 test; Better Stack on prod hostnames | P0 (measures from day one, PRD 16.2) | The 15 pilot word checks and reactions give the first `followed_vs_predicted` reading against the fitter's prediction |
| 4 | 11-23 to 11-29 | Call rules (`host_reply_*`, `call_connect_p95`, `talkback_p50`, `governor_violations`, `notes_late`, `chat_opener_late`); `host` suite: governor replay on Milestone 0 transcripts (free) and the simulated caller on 10 scripted calls through `call-bench` on staging; the `calls_50` suite as a named run; `injection` suite with the security domain's 30 cases; `notes` suite; `call_review_items` and the calls review page (owner only); measures 12, 19, 23 | P0 (call alerts, `calls_50`), P1 (simulated caller) | Milestone 0 call audio is the simulated caller's voice; Muath's tags on the same calls make `recast_rate_on_planted` and `clarification_rate_on_planted` computable before any live beta call |
| 5 | 11-30 to 12-06 | `analyst` suite calling `calibration/run`; the cost rules (`session_cost_over_1`, `cost_p50_7d_over_080`, `spend_cap_or_stop_line`, `cache_hit_low`); privacy and crisis rules (`privacy_promise_missed`, `crisis_activation`), `wrong_memory_*`, `claims_retracted`; `review/sample` and `/admin/review/episodes` with the reviewer role; `claims/audit-sample` and `/admin/review/claims`; `/admin/gates` with readable-from dates; `/admin/alerts`, `/admin/incidents`, `/admin/flags`; the twelve runbooks in `ops/runbooks/`; the two admin actions (`pull`, `rerun-after-pass`); `ops/oncall.yaml` and the Better Stack schedule with phone escalation; `ops/digest`; the 08:30 checklist; a 60-minute tabletop with the security domain's incident drill (R4 pull, R12 wrong memory, R1 failover by hand); measures 1, 2, 5 to 9, 15 to 17, 20 to 26; the end-to-end run with the Milestone 0 learners on prod with every rule live | P0 | The end-to-end run on prod is the first real `cost_per_session` reading for the 2026-12-07 exit criterion and the first live `notes_late` and after-pass timings; the Milestone 0 week-0 and week-3 recordings seed `test_retest_pairs` so `/admin/gates` can show how many metrics have `n_pairs ≥ 12` |
| Beta (P1) | 12-07 to 2027-01-10 | Full synthetic learner set (50) and the full `pipeline` suite on every bump; `pronunciation` suite; `eval/nightly` moved to weekly if cost matters; `vendor/regress` first run 2027-01-01; the first false-claim audit 2027-01-01; the first rater window boundary 2027-01-04; the gate-review snapshot 2027-01-10; Metabase only if the admin tables are not enough | P1 | |

**Too much for one to two engineers, and the cut (in order):** the simulated-caller half of the `host` suite (keep the governor replay, which is free and catches most prompt regressions; run `calls_50` by hand before each host release instead); `/admin/incidents` as a page (an `incidents` row written by `ops.page()` and a Slack thread is enough); sparklines on `/admin/measures` (tables only); `measures/weekly` (compute cohort rollups in the daily job); the calls review page (Muath reads transcripts from `/admin/calls/{id}` with the governor header shown inline); Metabase. **Do not cut:** `logscrub` and its corpus (PDPL), `ops.page()` with phone escalation (the 05:40 drop), the six P1 rule families, `eval-gate` for host and editor prompt changes (law 7 and law 5 live in those prompts), `release_manifest` (without it a bad prompt cannot be traced), the false-claim audit (a 16.1 gate), the `pull` action (the only remedy for a law break that shipped), and the runbooks R1 to R4 and R12.

## 8. Alternatives rejected

| Alternative | Why not |
|---|---|
| Datadog, Grafana Cloud or New Relic for product metrics | A new PDPL processor holding learner ids and event names for numbers the event log already holds; monthly cost above the whole domain's budget; the team would spend the build week learning a query language instead of writing SQL it already writes |
| Prometheus and an OpenTelemetry collector on Fargate | Two more containers to run and a scrape model that fits long-lived services, not Inngest steps; EMF lines give the few service counters for free |
| A log SaaS (Better Stack Logs, Axiom, Loki) | Learner text could leak into a third processor; CloudWatch is already there and the scrubber makes it safe |
| PagerDuty or Opsgenie | Price and ceremony for a two-person rota; Better Stack's on-call does phone escalation for a tenth of the price and is already the uptime tool |
| LaunchDarkly or Statsig for flags | A processor, a SDK in four services, per-seat pricing; a table with a 60 s cache is 60 lines of code and audited |
| A separate eval product (Braintrust, Langfuse evals, Promptfoo as the harness) | Langfuse's evals would tie prompt regression to a processor the security domain may yet refuse; Promptfoo is fine for single prompts but the suite's unit is a learner fixture through several steps with code checks in between; a small Python package with pytest-style checks is what the team can extend |
| LLM-as-judge for the law scan | Law 1 needs recall 1.0 on a finite word list; a judge adds cost and variance where a scanner is exact; the editor model still judges the semantic half (check 10's "guilt", "unsolicited correction") |
| Reviewing calls by listening to audio | Needs break-glass access per call and a reason; transcripts with timings and the governor header show the move contract better and keep audio access rare |
| A learner-facing status page | The product's answer to an outage is its fallbacks and silence; a status page is another surface to keep law-clean and another thing the three-message rule does not allow linking to |
| Continuous deploy to prod | A prompt regression that passed `eval-gate` on variance would reach the 05:40 drop; a tag plus a canary costs ten minutes |
| Sampling traces or logs in the beta | The beta is where every call is evidence for the gates; 100% is affordable at this size |
| Grafana with a read replica or an SSH tunnel | A replica is $100 a month for dashboards; a tunnel is one more credential; revisit with Metabase on Fargate at about 1,000 learners when the admin tables stop being readable |

## 9. Assumptions about other domains

Each is an [ASSUMPTION] for the integrator to check.

1. **System topology (01).** `ops.page()` is the interface its paging hooks call; `vendor/health` writes `vendor_health {capability, vendor, state, no_secondary}` as this document's rules read it; `outbox` exists with an unsent count; `FORONE_FAKE_VENDORS=1` recorded-fixture adapters exist for every adapter; `tools/load-call` (01) and `tools/call-bench` (03) are the same tool, and this document uses the call domain's name; the synthetic learners seeded in its week 2 are the canary's learners; the deploy workflows accept a canary step and an automatic rollback; the `/admin` pages are `sqladmin` plus a few custom routes in `api` and this domain adds its pages there; `episodes.status` (02) versus `episodes.state` (01): this document uses `status` and will follow the integrator's ruling.
2. **Episode generation pipeline (02).** `review_items` and `review_findings` have the shape in its 4.x and its nightly sampling rule moves into `review/sample` here (one job, not two); `pipeline.human_page` carries `reason` and `count_7d`; the degraded flags (`degraded`, `timing_quality`, `relisten`, `fallback_rules`, `failover`) are on the artifact so the measures can count them; the `why` artifact carries `predicted` coverage for measure 11; `pipeline_steps` carries `prompt_version`, `pricing_mode`, `cached_input_tokens`; its `fixtures/learners/*.json` is the same file set as `eval/fixtures/learners/` (one location, the pipeline's name wins); `price_book` (02) and `prices.yaml` (01, 03) are one price source under the cost domain; a pull of an episode (`episode.pulled`) is honoured by `feed.publish` (410 on the enclosure) and by a fallback `episode/produce` run at standard pricing.
3. **Live call and voice stack (03).** `calls.metrics` carries `reply_latency_p50_ms`, `reply_latency_p95_ms`, `connect_ms`, `talkback_ms[]`, `learner_speech_ms`, `host_speech_ms`, `moves{...violations}`, `anxiety_mode`, `end_reason`; `tools/call-bench` accepts scripted caller profiles from `eval/fixtures/callers/` and writes `bench/reports/`; `feed_to_call_ms` is logged as `client_perf`; `crisis_activation` events and `crisis.activated` exist as the security domain describes; Deepgram becomes a hot streaming secondary in P1 (until then, recognizer outage means voice notes).
4. **Learner model, event log and data platform (04).** `events` with the types in PRD 8.2 plus the client's four and `followed_answer`, `fact_card_viewed`, `claim_shown`, `pmf_answer` [new, this document]; `sessions` with `state`, `started_at`, `episode_id`; `day.became_active`; `learner_schedule.next_drop_at` and an `expects_drop` flag (or an equivalent way to know yesterday was active); the per-use evidence rows this document calls `word_uses` and `structure_observations` with `clean`, `correct`, `prompted`, `occurred_at`; `word_bank.targeted_first_at` and `structure_map.first_targeted_at` (or the teacher's targeting history exposed another way) for delayed recall; `show_canon.kind='callback_made'` and `learners.wrong_memory_n` for measure 20; `learners.cohort_monday` and `learners.native_language`; `learner.rebuild_requested` is sent from this domain's `/admin` button; `measure_points` learner-scope rows are purged by `learner/delete`; its service metrics (`events_appended_total`, `facts_rejected_total`, `voice_objects_overdue`, and the rest) are EMF lines this domain's dashboards read.
5. **Assessment engine, after-session pass and the claim gate (05).** `claims` with `status in (candidate, passed, shown, retracted)`, `kind`, `shown_at`, `assessment_version`, `sem`; `claim_evidence` openable by claim id; `metric_calibration.n_pairs`; `test_retest_pairs` seeded from Milestone 0; `calibration/run` is callable from CI and returns pass/fail with `qwk_band` and `precision_claim_tags`; `calibration_samples` holds the Milestone 0 tags under `tags_a`; `rater_versions` and `pinned_until` as its D12; `recording_ratings` and `structure_map.stable_confirmed_at` for measures 9 and 26; `notes.created_at`, `notes.degraded`, `session_summaries.evidence_quality`; `claims.retracted` and `notice_pending`; its own kill switch honours `claims.kind.<kind>` flags; `session_costs` is a view the cost domain maintains over `vendor_calls` and `episodes.cost_usd` with the attribution rule in 4.1 row 22.
6. **Client app, podcast feed and delivery (06).** `app_open {entry, standalone, drop_delta_min}`, `client_perf {kind, value, context}` with the kinds it lists, `pwa_install`, `push_permission`; `followed_answer` on some episodes; a once-only `pmf_answer` question rendered in the week-4 proof's question slot [new]; `waitlist.source` and `invites` carry referral provenance; the feed's health item `api.forone.app/f/health.xml` exists for Better Stack; Sentry browser SDK with its scrubbing; `feed_fetches` by `ua_family` for the Part 18 #11 weekly report; the Salma line on Today for a pulled episode is a `TodayDoc` field it renders.
7. **Security, privacy, consent and compliance (07).** `staff_accounts` roles `owner`, `engineer`, `reviewer`, `tagger`, `ops` and the per-role page matrix in 4.5.4; `audit_log` rows for every admin page read of learner content and every flag flip; `privacy/verify`, `privacy.audit_failed`, `privacy_audit_runs`; `cost_guard.tripped`; `security_incidents` linked from `incidents.security_incident_id`; `guard/law_words.yaml` as the scanner the law corpus tests; the 30-case injection set at `eval/fixtures/injection/`; `research/anonymize` for anything a `tagger` reads; the Milestone 0 consent covers de-identified fixtures; Sentry EU and CloudWatch in the home region are approved; the Langfuse 30-day retention and name tokenization are theirs; the incident runbook and tabletop are shared with this domain's week-5 drill.
8. **Cost model, vendor strategy and tracing (08).** `vendor_calls {learner_id, session_id, episode_id, call_id, role, vendor, model, cost_usd, input_tokens, cached_input_tokens, latency_ms, trace_id}` and the `session_costs` view; the weekly cost report by role, vendor and learner is produced there and read in the Tuesday review here; the Langfuse conventions (`user_id`, `learner_model_version`, `prompt_version`, `trace_id`) are theirs; `prices.yaml`/`price_book` has the dated 2027-01-01 row; the adapter middleware exposes a cache-hit ratio per role for `cache_hit_low`; the daily spend cap and the $1.00 per-session alert are emitted by the middleware as `cost_guard.tripped` or an equivalent event this domain's rules consume.

## 10. Open for Muath

1. **[OPEN for Muath] On-call and paging.** Who is primary in the beta's first three days (05:00 to 09:00 Riyadh, both engineers proposed), whether Muath is the escalation after 15 minutes at any hour, and whether the Better Stack on-call plan (about $30 a month) is in the budget. Without a phone path, an unready 05:40 drop is found at 09:00.
2. **[OPEN for Muath] The paid reviewer.** PRD 6.8's native English reader: hours (about 4 a day at 100 learners for episodes alone, less with the cut in section 7), rate, and start date (needed by 2026-12-07; the first beta week queues every episode). Also whether the same person may file ban proposals directly or only propose.
3. **[OPEN for Muath] Who audits claims.** The monthly false-claim audit (first on 2027-01-01) needs a reader who can judge "does the evidence support this sentence" on about 40 claims; Muath alone, or a second trained person (the assessment domain's second tagger is the natural candidate).
4. **[OPEN for Muath] The "very disappointed" question.** PRD 16.1 names the metric but not the ask. Proposed: one in-app question in the week-4 proof's slot (replacing the worth-it question that week), three answers, never by email. Approve the mechanism and the Arabic wording, or drop the gate for the beta.
5. **[OPEN for Muath] Second-month renewal for founding members.** Founding members pay a year up front, so `renewal_m2` reads only monthly subscribers during the beta and may have too few to read by 2027-01-10. Decide whether the gate is judged on monthly subscribers only or deferred.
6. **[OPEN for Muath] Pulling a shipped episode.** Section 4.8 R4 adds an admin action that replaces a law-breaking episode and has Salma say one plain line on Today. It is new (not in PRD-v2). Veto or confirm, and confirm the line's wording.
7. **[OPEN for Muath] The stop line's owner.** PRD 14.5 says over $1.00 a session with no costed plan is a stop. This document makes it a ticket to Muath with the breakdown, not an automatic halt. Confirm that a human decides, and within how many days.
8. **[OPEN for Muath] Milestone 0 fixtures and consent.** The suite reuses de-identified pilot transcripts, scripts, tags and the 30 clips indefinitely as test fixtures. Confirm the pilot consent (02-consent.md) covers this, or the fixtures are limited to the 30 clips and synthetic learners.
9. **[OPEN for Muath] Budget for this domain.** About $250 to $300 a month in tools and suite runs during the beta (section 6), outside the per-session number. Approve, or name the cut (the nightly smoke is the first $90 to go).
10. **[OPEN for Muath] Reviewer access to Arabic surfaces.** The native English reviewer reads scripts and articles; Salma's Arabic notes and the Arabic law corpus need an Arabic reader for the law scan's near-miss cases. Muath in the beta, or a second reviewer.
