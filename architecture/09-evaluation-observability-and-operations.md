# Evaluation, observability and operations

*For one architecture, domain 9 of 9. Written 2026-10-16 against PRD-v2 (Implementation PRD v3.0), concept-v2 sections 7 to 10, decisions.md, the ai-architecture, learning-science and assessment-progress lenses, and the Milestone 0 kit (04-production, 05-prompts, 07-measures-and-gates, 08-runbook); revised 2026-11-06 against the 2026-10-23 decisions (decisions.md), its two design reviews of 2026-11-06 (conformance and skeptic, in `_review-findings.md`) and the cross-domain rulings in 10-decision-records.md. Sibling documents 01 to 08 were read for names; where this document consumes something they defined, the name is theirs and is marked. "PRD x.y" means PRD-v2 part x.y. Tags: [DECISION], [ASSUMPTION], [OPEN for Muath].*

*What changed in this revision, in one paragraph. The operational model no longer assumes one timezone or one commute: every job is learner-local-day aware (`measures/hourly`, `privacy/verify` hourly), reports run at fixed UTC times, the release window is computed from `learner_schedule` and is binding, per-learner lateness is P2 and systemic lateness (`drops_late_systemic`) is the P1, and on-call pages at any hour with the honest statement that a one-engineer beta accepts some overnight P1s being answered by the product's fallbacks (ADR-16). Salma's after-call notes and the other retired teaching surfaces, and everything that measured, alerted on or flagged them, are gone; the law-7 promise is now measured on real calls by `explicit_corrections_per_100_turns` (ceiling 0) and `echo_uptake_share`, and the `notes` suite became a `salma` suite (ADR-06). Versions, corpora, fixtures and reviewers are per language package (`packages/languages/<target>/`, `packages/native/<lang>/`; ADR-02). The gates read the three monthly USD plans (`renewal_m2` over every paid learner, `plan_mix` and `blended_margin` reported; ADR-04, ADR-15). The stop-line alert is split into `cost_runaway` (P1) and `cost_stop_line` (P3 plus the ticket), so the stop line is never paged. Vendor error bodies never reach a log. Dashboards read through `forone_admin` (ADR-17); Langfuse carries the research pseudonym (ADR-09); `episodes.state`, `call_turn_verbatim`, `word_uses`, `learner_schedule.expects_drop`, `tools/call-bench`, `cohort_key = invite_date` and a computed `proofs.sessions_in_week` are used as ruled (ADR-19). Dates follow ADR-07. Section 11 is the revision log.*

## 1. Summary and the decisions in one table

This domain answers one question for a team of one to two engineers plus Muath: **how do we know the product works, and how do we keep it working, without building an observability product?** The answer is to make every signal a row in the Postgres the team already runs, to make every alert a SQL query with a runbook link, and to make every change to a prompt, a model or a rule pass the same offline suite that the Milestone 0 learners' files and tags seed. Three managed tools (Sentry for errors, Better Stack for uptime, heartbeats and paging, Langfuse for model traces, the last owned by the cost domain) plus CloudWatch, which comes with Fargate, cover the rest. Learners are anywhere (decisions.md §1), so nothing here has a home timezone: jobs are learner-local-day aware, reports run at fixed UTC times, and the one critical moment, the drop, happens at every hour of the clock. Nothing in this domain is ever shown to a learner (PRD-v2 16, law 1).

| # | Decision | Chosen | Reason in one line | Rejected |
|---|---|---|---|---|
| D1 | Where measures live | Every 16.1 and 16.2 measure is a row in one table, `measure_points`, computed by `measures/hourly` for every learner-local day that closed in the previous hour (idempotent upserts), from the event log and the sibling domains' tables, with the definition as versioned SQL in `forone.measures` [DECISION, PRD-v2 16.2 "tracked from day one"; ADR-16] | One table, one job, one version; "yesterday" is a different calendar day for each learner, so the job runs hourly and asks which learners' days just closed; a measure can be recomputed from day one when its definition changes, like the stores (8.5) | A metrics vendor (Datadog, Mixpanel): one more processor under every regime in 07 §4.9, holding learner ids for nothing the event log does not already hold; counters in memory (lost on deploy); a nightly job at one fixed hour (right for one timezone, wrong for the rest) |
| D2 | Team dashboards | Server-rendered pages in `api` under `/admin/measures`, `/admin/gates`, `/admin/alerts`, `/admin/review`, `/admin/flags`, `/admin/incidents`, read from `measure_points` and the sibling tables through the `forone_admin` role (aggregate reads across learners, writes only to the admin tables, every content read in `audit_log`, no pgaudit; pgaudit applies only to `forone_human`, the role psql sessions use; ADR-17); CloudWatch dashboards for infrastructure; the Inngest and Langfuse consoles for runs and traces [DECISION] | RDS sits in a private VPC with no public endpoint, so a SaaS dashboard would need a tunnel or a replica; at 100 to 500 learners the numbers fit in a table; pgaudit on the dashboards' role would bury the human-SQL audit it exists for | Grafana Cloud (needs a reachable datasource), Metabase on Fargate (one more container; revisit at 1,000 learners, section 8); dashboards on `forone_readonly` under pgaudit (the first draft) |
| D3 | Alerts are SQL | `ops/alerts.yaml` holds every rule (a SQL predicate, a window, a severity, a dedupe key, a runbook path); the Inngest cron `ops/watch` evaluates them every 5 minutes, writes `alert_state`, and calls `ops.page()` [DECISION, PRD-v2 15, 14.5] | The latency budgets of Part 15 and the cost stop line are facts about rows (`calls.metrics`, `session_summaries.completed_at`, `vendor_calls`), so the alert is the query; the team reviews rules as code | CloudWatch metric alarms for product budgets (they would need a metrics emitter per budget); vendor alerting UIs edited by hand (no review, no runbook link) |
| D4 | Paging | Better Stack: uptime checks on the three public hostnames, heartbeat monitors for the four crons that must never stop, one on-call schedule, phone-call escalation; `ops.page()` posts to its incident API; everything below P1 goes to the ops Slack channel or the daily digest at 06:00 UTC [DECISION] | The topology already named it; it is the cheapest tool that calls a phone; one API to wrap | PagerDuty (price), Opsgenie (Atlassian stack), Slack only (no phone when a drop somewhere in the world is late at 03:00 for the engineer) |
| D5 | Logging | Structured JSON on stdout from all four services to CloudWatch Logs (30-day retention), scrubbed at emission by `forone.ops.logscrub` using the data domain's `forone.learner.pii` classification; learner ids and event ids are allowed, names, emails, transcripts, facts and audio are not; a vendor error is logged as its class, HTTP status and the vendor's request id, never its message body (vendor 4xx bodies quote the request, which is the learner's turn; the policy is 07's, the implementation is here); CloudWatch Embedded Metric Format lines carry the few service counters the data domain emits [DECISION, PRD-v2 12.6] | Zero agents, zero extra processors; the scrubber is one function with a test corpus; EMF turns a log line into a CloudWatch metric for free | A log SaaS (another processor holding learner text), OpenTelemetry collectors (operations) |
| D6 | The offline suite | One package `forone.eval` and one CLI `tools/eval` running named suites from `eval/suites.yaml` against thresholds in `eval/thresholds.yaml`; fixtures seeded from Milestone 0 (learner files, tags, 30 clips, scripts, Muath's editor reads); results in `eval_runs` and `bench/reports/`; a CI job `eval-gate` runs the relevant suite when a prompt, model, rule or measure version changes and blocks the merge on regression; suites and fixtures are per `target_language` package, and the pilot runs them for English only; staging stays up from build week 2 through the beta so the `host` suite can run against it (about +$180 a month, carried in 01 §6; ADR-16) [DECISION, PRD-v2 6.7 [P1], 10.11, 10.14, 14.4; ADR-02, ADR-03] | The PRD's rule is "a change that worsens any of these does not ship"; a rule needs a gate in CI, a baseline, and fixtures that exist before the beta | A separate eval vendor; manual "run it when you remember" (Milestone 0's mode) |
| D7 | Versioning of what models see | Every prompt, rubric, rule table and threshold is a file in a language package with a version in that package's `versions.yaml`: `packages/languages/<target>/versions.yaml` (prompts, structure rules, law and correction words, crisis keywords, recognizer threshold, `assessment_version`) and `packages/native/<lang>/versions.yaml` (interface strings, consent texts, Salma's voice and lines); `release_manifest` records which versions each deploy carried; a version bump is a PR that must pass `eval-gate`, whose path map keys on the package directory [DECISION, PRD-v2 10.11.3, 8.5; ADR-02] | "Pinned for each 4-week window" and "re-run on every model change" are only enforceable if versions are explicit and deploys record them | Editing prompts in the admin UI (the pipeline domain's D17 already forbids it) |
| D8 | Feature flags | A `feature_flags` table (key, state, learner allowlist, percentage, changed_by), read by services with a 60 s cache, edited on `/admin/flags`; flags exist only for P1 features, vendor levers and kill switches, never for a law; a model lever (`host.model=haiku`, a Sonnet teacher) is flipped by a person after `eval-gate` passes, never by a spend alarm (ADR-14) [DECISION, PRD-v2 19.3] | P1 items ship during a paid beta and need a way to reach 5 learners before 100; a kill switch is the first half of every runbook; a quality change is a human decision, not an alarm's | LaunchDarkly or similar (processor, price); environment variables (a deploy per flip) |
| D9 | Release process | Trunk-based; CI on every PR (unit, PII scrub test, Inngest payload test, `eval-gate` when versions change); merge deploys staging; prod deploys from a tag after a manual approval, runs a canary episode and a canary call on the synthetic learner, then flips; a failed canary rolls back to the last image with `canary_passed = true` in `release_manifest`; the deploy window is not an hour of day but a computed fact: `tools/release` refuses a deploy while more than 2% of learners who expect a drop have one in the next 45 minutes (an override needs a reason row), and a `call-worker` deploy drains first and never starts while `active_jobs > 0`; freezes 2026-12-21 12:00 to 12-24 12:00 UTC and 2026-12-31 to 2027-01-02 [DECISION; ADR-16, ADR-07] | Confirms topology D13 and D14 and adds the one thing they lack: when, and what proves a release is good before a learner hears it; with learners in every timezone there is no hour that is outside every drop, so the check must be relative to the schedule and binding | Continuous deploy to prod (a bad prompt would reach someone's drop within the hour), release trains (too slow for a five-week build), a fixed weekday window in one timezone (the first draft) |
| D10 | Human review | The pipeline's `review_items` queue for episodes (10 random per learner per month plus every degraded, fallback and soft-fail item; the sampled share falls on the 2 and 3 a day plans and is printed in the monthly summary), a new `call_review_items` queue for calls (1 per learner per month plus every call with a move violation, a correction-guard block, a crisis activation or `end_reason: abandoned` in week 1), a monthly `claim_audits` sample of shown claims, all served by `/admin/review` with the security domain's role matrix; reviewers are per target language (`staff_accounts.languages`), the native-language law-scan reader per native language [DECISION, PRD-v2 6.8, 16.1; ADR-02, ADR-04] | The PRD names the episode reviewer and the false-claim audit; the call review is the only way to know the move contract and law 7 hold on real learners, and the governor's counters say what was declared, not what was heard | Reviewing calls by listening (audio access needs break-glass; transcripts with timings are enough) |
| D11 | On-call | One primary engineer per week, Muath as escalation, phone paging at any hour for P1 rules only (the six families in 4.6); there is no protected hour, because with learners in every timezone some learner's drop is always within 45 minutes; everything below P1 waits for the next working hour; a weekly 30-minute ops review on Tuesdays. The honest statement: a one-engineer rota means some overnight P1s are answered by the product's fallbacks (yesterday's episode stays, voice notes) and by a human at the next working hour [DECISION; ADR-16; 10-decision-records §10 item 7 asks Muath to accept this or fund a second responder] | Two people cannot staff 24/7, and there is no quiet hour to protect; what a human can fix faster than the pipeline is a systemic failure, so that is what pages | A follow-the-sun rota (no sun to follow), a protected hour in one timezone (the first draft), no paging (a systemic late drop found hours later is a lost day for every learner in that band of the clock) |
| D12 | Runbooks | Twelve one-page runbooks in `ops/runbooks/`, each with the same five headings (detect, first five minutes, fix, verify, tell the learner), every alert rule linking to one, two admin actions behind them (`pull episode`, `re-run after-pass`) [DECISION] | A runbook nobody can find at 03:00 is a document, not a runbook | A wiki |
| D13 | The beta gates | `/admin/gates` computes the eleven 16.1 gates per weekly invite cohort (`cohort_key = invite_date`) from `measure_points` with target and stop lines, with the date each gate first becomes readable; `plan_mix` and `blended_margin` are shown next to the gates as reported lines, not gates; nothing is decided from a gate before its cohort is old enough [DECISION, PRD-v2 16.1, 19.3; ADR-07, ADR-15, ADR-19] | "Active in week 4" for the 2026-12-23 cohort is unreadable before 2027-01-20; a dashboard that shows it earlier invites a wrong decision | A single cross-cohort number |
| D14 | Law 7 is measured, not declared | Measure 27 `explicit_corrections_per_100_turns` (the correction guard's blocks from 07 plus `call_review_findings.move_contract.never_rules_ok = false`, per 100 host turns) with a ceiling of 0 as the law-7 gate in `eval-gate` and on `/admin/gates`; measure 28 `echo_uptake_share` (planted or observed learner errors that the host recast and the learner reproduced correctly within the same call or the next session) as the evidence for the riskiest assumption in concept-v2 §10; `recast_rate_on_planted` is reported separately for synthetic callers (labelled "upper bound") and for real-audio replays, and the gate moves to the real-audio number once 20 replays exist [DECISION, decisions.md §3, concept-v2 law 7 and §10; ADR-06] | The product's defining promise is that nobody is ever told they were wrong; the governor's self-declared counters cannot prove it, and a TTS-voiced synthetic caller flatters the host | Trusting the governor's counters; gating on synthetic callers alone |
| D15 | The stop line is a trend, never a page | `cost_runaway` (P1) fires from `cost_guard.tripped {level: hard}` and the daily spend cap `daily_spend_100`; `cost_stop_line` (P3) fires when the trailing 7-day mean session cost is over $1.00, lands in the digest and the Tuesday review, and opens a ticket to Muath with the breakdown and 08 §4.5.3's 48-hour plan window; six P1 families stay six [DECISION, PRD-v2 14.5; 08 §4.5.3] | A seven-day mean is a business decision for a human in working hours, not a phone call at 03:00; only runaway spend is an engineering signal | One `spend_cap_or_stop_line` P1 rule (the first draft) |

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
| 14.5 | Cost per session reported weekly, next to heavy-use outliers; stop line $1.00 | Weekly cost review in the calendar (4.10); alert rules `cost_p50_7d_over_080`, `cost_runaway`, `cost_stop_line` (4.6); the cost domain owns the report itself, including "Margin by plan" (ADR-15) |
| decisions.md §3, concept-v2 law 7 | Teaching is invisible: no explicit correction from any host or Salma line, on any call | Measures 27 and 28 (4.1); the correction guard in the law-scan corpus (4.2) and the `salma` suite; `explicit_corrections_per_100_turns` ceiling 0 in `thresholds.yaml`; the call review's `never_rules_ok` (4.5.2) |
| decisions.md §1, §2 | Learners anywhere on three monthly USD plans | Learner-local-day measures and hourly jobs (4.1, 4.10); the computed deploy window (4.3); `renewal_m2` over every paid learner, `plan_mix`, `blended_margin` (4.4); per-package versions, corpora and reviewers (4.2, 4.3, 4.5) |
| 15 | Every latency and reliability budget | Each budget has a measured signal, a source and an alert rule (4.6, table 4.6.1) |
| 16.1 | Eleven beta gates with target and stop lines | `/admin/gates` (4.4) |
| 16.2 | Eighteen quality and health measures from day one | `forone.measures` definitions (4.1) |
| 19.2, 19.3 | Exit criteria on 2026-12-22; P1 items during the beta; switch-to-native triggers | Build plan (7); flags (4.7); the two switch measures (4.1 row 19) |
| 7.9 | Every crisis activation logged; human follow-up | Alert `crisis_activation` and runbook R10 (4.6, 4.8) |
| 12.5, 12.6 (through the security domain) | Deletion windows verified; staff access logged; PII never in logs | Log scrubbing (4.9); the paging channel for `privacy.audit_failed` (4.6) |

Budgets that bind this domain: the fixed monthly cost of its tools (section 6, about $150 to $200 a month in the beta, plus the staging environment it keeps up, about $180, carried in 01 §6); the cost of running the suite (about $15 to $20 per full run, and $300 to $500 a month of `eval-gate` runs during the build weeks when prompt edits are daily, section 6); zero per-session cost on the learner path (nothing here runs in a learner's request); and the engineering budget of the five build weeks, where this domain must stay under about one engineer-week in total before 2026-12-22 (section 7 says which week).

## 3. Architecture

### 3.1 Components

Draw six boxes in a row across the top, the four deployables plus two managed consoles, and three boxes below them owned by this domain.

- **Producers (top row, left to right):** `api`, `workflows`, `call-worker`, `web` (the topology's four services). Each emits three things: structured log lines to stdout (CloudWatch), Sentry events on exceptions, and rows (`events`, `calls.metrics`, `pipeline_steps`, `vendor_calls`, `session_summaries`, `claims`, `review_items`, `privacy_audit_runs`, and the rest of the sibling tables). `web` emits only client events (`app_open`, `client_perf`, `pwa_install`, `push_permission`) through `POST /v1/events`, and Sentry browser events.
- **Consoles (top row, right):** Inngest (run history, replay), Langfuse (every model call with cost and `learner_model_version`; owned by the cost domain).
- **`forone.measures` (bottom left):** a Python package of SQL definitions, one function per measure, each stamped with `MEASURES_VERSION`. Run by the Inngest crons `measures/hourly` (at :10 every hour: for every learner whose local day, by `learners.tz`, closed in the previous hour, compute that learner-day and refresh the cohort and `all` rollups the day belongs to; idempotent upserts, so a re-run is harmless) and `measures/weekly` (Monday 06:00 UTC, cohort rollups over complete learner-weeks). Writes `measure_points`. [ADR-16]
- **`forone.ops` (bottom middle):** `ops/watch` (cron, every 5 minutes) evaluates `ops/alerts.yaml` against Postgres, writes `alert_state`, calls `ops.page()`; `ops.page()` is the interface the topology, pipeline and security domains already call (`pipeline.human_page`, `vendor.degraded`, `privacy.audit_failed`, `cost_guard.tripped`, `security.incident_opened` all land here); `ops/canary` (weekly) runs one episode and one call on the synthetic learner through each voice vendor; `review/sample` (daily, 03:00 UTC) fills the review queues; `claims/audit-sample` (monthly) fills `claim_audits`; `vendor/regress` (monthly) re-runs the recognizer and pronunciation clip suites; `feature_flags` and `release_manifest` live here.
- **`forone.eval` (bottom right):** the offline suite. Fixtures under `eval/fixtures/` (seeded from `/mnt/project-files/milestone-0/` artifacts by `tools/import_m0.py`), suites in `eval/suites.yaml`, thresholds in `eval/thresholds.yaml`, the runner `tools/eval`. It runs on a developer laptop, in CI (`eval-gate`), and nightly on staging (`eval/nightly`, the 10-fixture smoke). Results go to `eval_runs` and `bench/reports/{date}-{sha}.json` (the call domain's `call-bench` already uses that directory).
- **Sinks (right edge):** Sentry (errors, scrubbed), Better Stack (uptime, heartbeats, incidents, phone), the ops Slack channel `#forone-ops` (every alert at P2 and above, every page, every deploy, every canary result), the daily digest (P3, one Slack message at 06:00 UTC; "morning" for the team, not for any learner).

Arrows: producers write rows to Postgres and lines to CloudWatch; `forone.measures` reads Postgres and writes `measure_points`; `forone.ops` reads Postgres and CloudWatch alarms (through SNS) and writes to Better Stack and Slack; `forone.eval` reads fixtures and calls the production adapters (real vendors at the gate level, `FORONE_FAKE_VENDORS=1` recorded fixtures at the unit level) and writes `eval_runs`; the `/admin` pages read everything through `forone_admin` (ADR-17) and write only `feature_flags`, `review_findings`, `claim_audits`, `incidents` and the two admin actions, each as an `audit_log` row (security domain D13); `forone_readonly` stays for ad hoc read-only tooling, and `forone_human` (pgaudit) for a person at psql.

### 3.2 Data flows

1. **A budget to an alert.** A call ends; the worker writes `calls.metrics` (`reply_latency_ms` percentiles, `connect_ms`, `talkback_ms`, `moves.violations`, `end_reason`). Five minutes later `ops/watch` runs rule `host_reply_p50_20calls`: median of `reply_latency_ms` over the last 20 completed calls. Over 1.5 s for two consecutive evaluations, it writes `alert_state{rule, state: firing, since, dedupe_key}` and posts to Slack with the runbook link (P2). Under 1.5 s for two evaluations, it resolves. Nothing in this path touches a learner.
2. **An event to a measure.** The client sends `app_open {entry: "home_screen", drop_delta_min: 12}`. In the hour after that learner's local day closes (midnight in `learners.tz`), `measures/hourly` computes `unprompted_return` for the day: sessions started without `entry in (push, gap_note)` and within 60 minutes of the learner's drop time, per learner-day, and refreshes the cohort share for that date. It writes `measure_points(measure='unprompted_return_share', scope='cohort', scope_id='2026-12-23', period_start=that_day, value=0.62, n=41)`; a cohort row for a date is complete once every learner in the cohort has closed that local day, which the row's `extra.learners_closed` says. `/admin/measures` reads the last 28 days.
3. **A prompt change to a deploy.** An engineer edits `packages/languages/en/prompts/host_system.md` and bumps `packages/languages/en/versions.yaml: host_system: 1.4.0`. CI sees the path, runs `eval-gate` with suite `host` for the `en` package (the governor replay on Milestone 0 transcripts and the law and correction scan on every push; the simulated caller on 20 scripted calls against staging once the PR carries the `ready-for-review` label), compares with the baseline run for `main`, and fails the check if any metric in `thresholds.yaml` regressed beyond its allowance, or if `explicit_corrections_per_100_turns` is above 0. On merge, staging deploys; on tag, prod deploys and `release_manifest` records `host_system: 1.4.0` with the image digest and the time. `calibration/run` (assessment domain) is part of `eval-gate` for assessment paths and blocks the same way.
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
    P2 -> Slack #forone-ops. P3 -> the daily digest (06:00 UTC). Returns the incident id.
    Context must contain ids and scalars only; the scrubber rejects anything else."""

def resolve(dedupe_key: str, note: str = "") -> None: ...

def flag(key: str, *, learner_id: str | None = None) -> bool:
    """Feature flag read with a 60 s process cache. Falls back to the flag's `default` when
    Postgres is unreachable, never to True for a kill switch."""

def heartbeat(monitor: str) -> None:
    """Called at the end of a cron that must never stop (measures/hourly, ops/watch, privacy/verify,
    retention/daily). Better Stack pages when a heartbeat is late by more than its grace period."""
```

```python
# packages/measures/forone/measures/api.py
MEASURES_VERSION = "1.0.0"

def compute(measure: str, *, period_start, period_end, scope: Literal["learner","cohort","all"]) -> list[MeasurePoint]: ...
def compute_all(period_start, period_end, *, learner_ids: list[str] | None = None) -> None:
    # measures/hourly calls this once per learner-local date that closed in the last hour, with the
    # learners whose day it was; measures/weekly calls it with learner_ids=None for complete weeks
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

**Grain and scope.** Every measure is computed per learner-day where that makes sense (a learner-day is a calendar day in `learners.tz`, which is why the job is hourly, 3.1), then rolled up to `cohort` (the weekly invite batch, `cohort_key = invite_date`, PRD-v2 2.1.6 and ADR-19) and `all`. Where a measure differs by plan, `extra.by_plan` carries the split by `learners.plan` (ADR-04). `measure_points` keeps all three scopes so that a cohort number can always be opened to its learners. Learner-scope rows are internal, never shown to a learner, and are deleted by `learner/delete` like any learner-scoped row.

```sql
create table measure_points (
  measure           text not null,                       -- key from the table below
  scope             text not null check (scope in ('learner','cohort','all')),
  scope_id          text not null,                       -- learner_id, cohort_key = invite_date (YYYY-MM-DD), or 'all'
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
| 13 | `say_it_once_share` | 16.2 | cohort, 7 d | `say_it_once` events / say-it-once prompts offered (`say_it_once_offered`, the client's event when the "say it once" affordance is shown after a call); the notes half of this row is gone with the notes (ADR-06) | `say_it_once_offered`, `say_it_once` |
| 14 | `fact_edits_week1` | 16.2 | cohort | learners with ≥ 1 `fact_card_edit` or `notebook_edit` in their first 7 days / cohort size | events |
| 15 | `similarity_p90` | 16.2, 6.5 | learner, 28 d | 90th percentile of the max cosine of each shipped script against the learner's previous 20; `extra.too_alike_human` = reviewer "too_alike" share | `script_embeddings`, `review_findings` |
| 16 | `minutes_per_day_outliers` | 16.2 | all, 1 d | learners with > 90 minutes of app playback plus call time in a local day, listed with learner id and minutes; this is a warning light for the team, never a goal [ASSUMPTION: 90 minutes, tuned in the beta] | `play`, `calls` |
| 17 | `recognizer_err_by_l1` | 16.2, 10.14 | all, 28 d | word error rate of streaming text (`call_turn`) against verbatim text (`call_turn_verbatim`, the second event appended by `workflows`) on clean turns, grouped by `learners.native_language` and `learners.target_language` from day one; a group with fewer than 50 turns is `null`, never a guess (ADR-02, ADR-19) | `events: call_turn, call_turn_verbatim` |
| 18 | `time_to_first_sound_p50`, `time_to_first_sentence_p50` | 16.2, 15 | cohort, 7 d | medians of `client_perf.first_sound_ms` and `first_sentence_ms` (the learner's first spoken sentence in the target language; `first_english_ms` in the first draft) per onboarding | `client_perf` |
| 19 | `calls_abandoned_on_move_share`, `feed_to_call_handoff_share` | 16.2, 19.3 | cohort, 7 d | `end_reason=abandoned` with `client_perf.bg_play_stop` or motion hint / calls; calls with `app_open.entry=feed_link` that reached `call_started` / feed call-link exchanges | `calls`, `app_open`, `feed_links` |
| 20 | `wrong_memories_per_100` | 16.1 | all, 28 d | `wrong_memory_flag` events × 100 / callbacks spoken (`show_canon.kind=callback_made` plus Today's memory line shown); the data domain's formula | `events`, `show_canon` |
| 21 | `false_claim_rate` | 16.1 | all, 28 d | `claim_audits.verdict=false` / audited claims (4.5.3) | `claim_audits` |
| 22 | `cost_per_session_p50`, `cost_per_session_mean` | 16.1, 14.5 | all and cohort, 7 d | per session: sum of `vendor_calls.cost_usd` attributed to the session's episode (the drop or a `daily_extra`), call, after-pass, Salma when asked and chat, plus that learner's weekly proof cost split over the sessions of the proof week; p50 and mean over sessions; `extra.top10` = the heaviest learners by cost that week; `extra.by_plan` = p50 and mean per plan (ADR-15) | `session_costs` (08's table, filled by `cost/rollup`, with `plan`) |
| 23 | `speech_min_per_session_p50` | 16.1 | cohort, 7 d | median over sessions of (`calls.metrics.learner_speech_ms` for main and round two + shadow + say-it-once durations) / 60,000 | `calls.metrics`, events |
| 24 | `sessions_per_active_learner_week` | 16.1 | cohort, 7 d | median over learners active that week of sessions started | `sessions` |
| 25 | `trial_to_paid`, `active_w4_paid`, `renewal_m2`, `referral_trials_share`, `very_disappointed_share` | 16.1 | cohort | see 4.4 | `learners.status`, `subscriptions.plan`, `payment_events`, `waitlist.source`, `events: pmf_answer` [new event, 4.4] |
| 26 | `recording_improved_share` | 16.1 | cohort, per season | learners whose finale had ≥ 1 passed claim of kind `fluency_change`, `accuracy_change` or `complexity_change` with a positive direction / learners with two rated recordings | `claims`, `recording_ratings` |
| 27 | `explicit_corrections_per_100_turns` | law 7, decisions.md §3 | all and cohort, 7 d; per prompt version | (correction-guard blocks on host and Salma lines, 07's `guard.check_output` item 6, counted in `moves.violations` with `kind = correction` + call review findings with `move_contract.never_rules_ok = false`) × 100 / host turns; the ceiling is 0: any value above 0 is a law-7 incident, not a trend (D14) | `calls.metrics.moves`, `call_review_findings`, `events: call_turn` |
| 28 | `echo_uptake_share` | concept-v2 §10 (riskiest assumption), law 7 | cohort, 28 d | learner errors that the host recast (the brief's `recasts` field matched to a host turn with a recast move) and that the learner then produced correctly, unprompted, in the same call or in the next session / errors recast; `extra.same_call`, `extra.next_session`; reported, no floor in the beta | `calls.metrics.moves`, `structure_observations`, `word_uses` |
| 29 | `plan_mix`, `blended_margin` | concept-v2 §9, ADR-15 | all, 7 d | share of paying learners per plan (`one_a_day`, `two_a_day`, `three_a_day`, with `founding_locked` as a sub-count); blended margin = (Σ net price − Σ measured cost) / Σ net price over paying learners, taken from 08's "Margin by plan" section of the weekly report; reported next to the gates, not a gate in the beta (4.4) | `subscriptions`, `session_costs`, 08's `cost_reports` |

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
select l.cohort_key, count(*) filter (where recalled) as num, count(*) filter (where had_context) as den
from later_use lu join learners l using (learner_id) group by 1;
```

`word_uses(learner_id, unit_id, event_id, occurred_at, clean, correct, prompted, quote)` is the data domain's per-use evidence table for words, written by 05's `apply_after_pass`, the word twin of `structure_observations` [ruled, ADR-19; it was an assumption in the first draft]. Nothing here reads its `quote` column.

```sql
-- 22. cost_per_session, one week, all scope; attribution rule from the cost domain (08), which fills
-- session_costs by cost/rollup: vendor_calls.session_id is set for call, after-pass, Salma and chat calls;
-- episode cost joins by episode_id (a daily_extra episode belongs to the session that asked for it);
-- the weekly proof cost is split equally over that learner's sessions in the proof week, and
-- proofs.sessions_in_week is computed here, not stored (ADR-19). Shown in full so the shape is clear;
-- the production measure reads session_costs and groups by plan for extra.by_plan.
with per_session as (
  select s.id as session_id, s.learner_id, l.plan,
         coalesce((select sum(cost_usd) from vendor_calls v where v.session_id = s.id), 0)
       + coalesce((select cost_usd from episodes e where e.id = s.episode_id), 0)
       + coalesce((select p.cost_usd / nullif((select count(*) from sessions s2
                                                 where s2.learner_id = p.learner_id
                                                   and s2.started_at >= p.week_start
                                                   and s2.started_at < p.week_start + 7), 0)
                    from proofs p
                    where p.learner_id = s.learner_id and s.started_at >= p.week_start
                      and s.started_at < p.week_start + 7), 0) as cost_usd
  from sessions s join learners l on l.id = s.learner_id
  where s.started_at >= :p0 and s.started_at < :p1)
select percentile_cont(0.5) within group (order by cost_usd) as p50, avg(cost_usd) as mean, count(*) as n,
       jsonb_agg(jsonb_build_object('learner_id', learner_id, 'cost', cost_usd) order by cost_usd desc) filter (where rn <= 10) as top10,
       jsonb_object_agg(plan, plan_mean) as by_plan
from (select *, row_number() over (order by cost_usd desc) rn,
             avg(cost_usd) over (partition by plan) as plan_mean from per_session) x;
```

### 4.2 The offline test suite

**What Milestone 0 hands over and where it lands** (PRD-v2 19.1.7). `tools/import_m0.py` reads the kit's artifacts once, in build week 1, and writes fixtures. Every fixture derived from a real pilot learner is covered by the pilot consent (02-consent.md) [ASSUMPTION: the consent covers use of de-identified transcripts and clips for building and testing the product; the security domain confirms] and is stored with the display name tokenized and the learner id replaced by `m0-L03`-style refs.

| Milestone 0 artifact | Fixture path | Used by suite |
|---|---|---|
| 15 learner files (Google Docs exported as Markdown) | `eval/fixtures/learners/m0-L01..L15.json` as `TeacherInput` (the pipeline's 4.3 schema) | `pipeline`, `teacher` |
| Scripts and articles with Muath's hand-checked coverage (step 6 of the evening cycle) | `eval/fixtures/scripts/*.json` with `coverage_hand`, `new_words`, `level` | `fitter` |
| Every package with Muath's step-8 read and the human reviewer's flags, plus the Gemini editor's verdict at the time | `eval/fixtures/editor/*.json` with `human_verdict`, `flags` | `editor` |
| Call transcripts (Scribe v2) with Muath's error tags, structure ids, categories and "blurred meaning" marks | `calibration_samples` (assessment domain, via its `tools/import_m0_tags.py`) and `eval/fixtures/transcripts/*.json` | `analyst`, `host` (governor replay) |
| The pilot's call recordings, where the consent covers them, with Muath's tags as the planted positions | `eval/fixtures/recordings/m0_calls/` (learner audio only, display names tokenized in the metadata) | `host` (real-audio replay: `recast_rate_on_planted_real_audio`, 4.2) |
| 30 consented clips with verbatim hand transcripts, code-switch and long-pause marks | `eval/fixtures/clips/recognizer/` | `recognizers` |
| Week-0 and week-3 then-and-now recordings with blind ratings | `test_retest_pairs` (assessment domain) and `eval/fixtures/recordings/` | `rater` |
| Confirmed and rejected life-fact candidates with quotes | `eval/fixtures/facts/*.json` | `memory` |
| The first ban list (show bible section BANNED) and scripts judged "too alike" | `packages/languages/en/ban_list.yaml`, `eval/fixtures/similarity/pairs.json` | `writer`, `editor` |
| Salma's lines as spoken in the pilot (talkback, the two questions, explanations when asked), and the pilot's retired after-call notes kept only as lines for the correction-guard corpus, never as a product fixture (ADR-06) | `eval/fixtures/salma/*.json`; the explicit corrections among the retired notes go into `law_corpus.jsonl` as violating lines | `salma` (law scan and correction guard on real Salma lines) |
| Say-it-once and voice-note clips (where consented) with a hand mark good/unclear | `eval/fixtures/clips/pronunciation/` | `pronunciation` (P1) |

**Synthetic learners** (PRD-v2 6.7: 30 to 50). The 15 pilot files give 15; `tools/eval synth --n 25 --target en` makes 25 more by varying level (A2+, B1-, B1, B1+, B2-), vocabulary size (2,000 to 5,000), interests (from the generic topic pool), rhythm, native language (from the native packages that exist), plan (`one_a_day`, `two_a_day`, `three_a_day`, so the multi-episode day plan is exercised) and by planting error patterns from the target package's analyst prompt list (for `languages/en`: missing *be*, articles with singular countables, present perfect versus past simple, prepositions after verbs, resumptive pronouns, questions without inversion, uncountable plurals, third-person *-s*; another target package brings its own list). Each synthetic learner is a `TeacherInput` plus a **caller profile**: a list of 20 to 25 scripted turns written to contain its planted errors at known positions, with pause marks, rendered to audio once with a TTS voice of the vendor not under test (so the recognizer under test never hears its own vendor's synthesis) [DECISION]. The call domain's `tools/call-bench` plays these as the simulated caller; this domain owns the profiles and the scoring.

**Why the synthetic number is an upper bound** (skeptic review). A TTS voice reads a planted error cleanly; a real learner's turn is hesitant, code-switched and sometimes silently repaired by the streaming recognizer (concept-v2 §3), so a host that recasts 70% of planted errors on synthetic callers may recast far fewer on real ones. `recast_rate_on_planted` and `clarification_rate_on_planted` are therefore reported twice: `_synthetic` (labelled "upper bound" in every report and on `/admin/gates`) and `_real_audio`, computed by replaying the Milestone 0 call recordings (and, in the beta, consented `data_use` learners' turns anonymized through 07's `research/anonymize`) as the caller against the current host prompt, with Muath's error tags as the planted positions. The gate in `thresholds.yaml` applies to the synthetic number until 20 real-audio replays exist, then moves to the real-audio number and the synthetic one becomes a smoke check [DECISION].

**Suites.** Each suite is a list of checks; each check is a function in `forone.eval.checks` that returns named metrics; `thresholds.yaml` says, per metric, the floor or ceiling and the allowed regression against the baseline. The suite names are the keys CI uses.

```yaml
# eval/suites.yaml. Every suite runs for one target package (`--target en`; the pilot is English only) and,
# where a check reads Salma's or the interface's lines, for each native package that exists (ADR-02).
fitter:         # code only, free, seconds
  checks: [coverage_accuracy, chunk_recall, new_word_budget]
  fixtures: [scripts]
  vendors: fake
law_scan:       # code only, free
  checks: [law_words_precision_recall, native_law_words, lesson_word_near_misses, explicit_correction_phrases]
  fixtures: [law_corpus, salma]
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
host:           # governor replay (free, every push) + simulated caller on staging (about $3 for 20 calls, on the ready-for-review label)
  checks: [violations_share, explicit_corrections_per_100_turns,
           recast_rate_on_planted_synthetic, recast_rate_on_planted_real_audio,
           clarification_rate_on_planted_synthetic, clarification_rate_on_planted_real_audio, nudge_budget,
           recall_gap_count, learner_talk_share, reply_latency_p50_p95, connect_p95, talkback_p50, cutoffs_per_call,
           law_words_in_host_lines, ai_disclosure_on_ask]
  fixtures: [transcripts, callers(20), recordings/m0_calls]
  vendors: real
  tool: tools/call-bench calls --n 20
salma:          # Sonnet, cents; Salma's lines when the learner asks, per native package (ADR-06)
  checks: [law_scan_on_lines, no_explicit_correction, native_language_share_ge_80, no_progress_claims,
           explains_only_when_asked, no_notes_or_summaries]
  fixtures: [transcripts, salma]
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
explicit_corrections_per_100_turns: {ceiling: 0}                     # law 7, hard: a correction-guard block or a never-rule finding is a failure (D14)
recast_rate_on_planted_synthetic:  {floor: 0.60, max_regression: 0.05, gate_until: real_audio_n >= 20}  # upper bound; TTS-voiced callers
recast_rate_on_planted_real_audio: {floor: 0.60, max_regression: 0.05, gate_from: real_audio_n >= 20}   # the number that counts, once 20 replays exist
clarification_rate_on_planted_synthetic: {floor: 0.50, max_regression: 0.05, gate_until: real_audio_n >= 20}
clarification_rate_on_planted_real_audio: {floor: 0.50, max_regression: 0.05, gate_from: real_audio_n >= 20}
echo_uptake_share:          {report_only: true}                      # measure 28; no floor in the beta
no_explicit_correction:     {floor: 1.0}                             # salma suite, hard
native_language_share_ge_80: {floor: 0.80}                           # Salma speaks the learner's native language
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

**The law-scan corpus** (`eval/fixtures/law_corpus/<lang>.jsonl`, one file per language, English first and 200 lines each, grown by every reviewer finding flagged `law`): 100 violating lines across every surface the scan covers (host line, Salma line, chat message, feed note, push text, proof script), including game words (for English: streak, points, level, badge, score, grade, percent), lesson words (lesson, test, exercise, homework), guilt and attachment ("we missed you", "don't go"), explicit corrections from a host or from Salma ("the correct form is", "you should say", "not X, Y", a repeated learner sentence introduced with "actually"), and progress claims from a host; and 100 clean near-misses ("the water level", "a test drive", "the next level of the car park", "I scored the goal", "let's test the theory", a host saying "note the time", a recast that repeats the learner's meaning in the right form without naming the error). The target language's file is scanned against `packages/languages/<target>/guard/law_words.yaml` and `guard/correction_words.yaml` (the correction guard, 07's `guard.check_output` item 6; ADR-06), the native language's file (Arabic for `native/ar`, with its own guilt and attachment phrases) against `packages/native/<lang>/guard/`; the editor's check 10, widened to "nothing reads as a correction or a lesson", runs on the same lines. Recall must be 1.0 on the violating half, precision at least 0.95 on the clean half, for each language file. A new false negative found in production (a reviewer `law` flag on a shipped line, or a `never_rules_ok = false` finding from the call review) is added to the corpus in the same PR that fixes it. A native-language file needs a reader of that language (Muath for Arabic in the beta; 10-decision-records §10 item 11).

**The editor-gate set** (`eval/fixtures/editor/`): every Milestone 0 package with Muath's `SHIP / SHIP AFTER FIXES / REWRITE`, plus 20 mutated packages built by `tools/eval mutate`: one unconfirmed fact inserted, one real-world statistic asserted, one "don't bring up" topic mentioned, one joke that carries nothing, one episode that needs the previous one, one banned name, one line that reads as a correction or a lesson (ADR-06). `fact_leak_catch_rate` and `law_catch_rate` must be 1.0 (these are code checks 4 and 10, so a miss is a bug, not a model variance; the correction half of check 10 is a model check and is reported with a floor of 0.9 on the mutated set); `editor_agreement_with_human` is the model's share of agreement with Muath's reads, reported, with a floor of 0.8 on the REWRITE cases.

**Fitter coverage tests**: the server fitter must reproduce `coverage-checker.html` to within 0.1 point on the 20 hand-checked scripts (the pipeline's own week-1 regression), and predict the learners' `followed_answer` direction on the Milestone 0 reactions (❤️/👍/😐 as the proxy) with the correlation reported, no floor in the beta.

**Claim-gate property tests** (free, run on every PR): generate random `claims` candidates with Hypothesis over the gate's inputs; assert that no row reaches `status=passed` without a `claim_evidence` row, never across two `assessment_version`s, never a metric kind without a `metric_calibration` row with `n_pairs ≥ 12`, never a `first_ever` with a prior clean use, and that `status=shown` rows are never deleted by `assessment/rebuild` (they become `retracted` with `notice_pending`). These encode PRD-v2 10.10 and 8.5 as tests the assessment domain's module must pass.

### 4.3 CI wiring and the release process

**Versions.** Each language package carries its own `versions.yaml` listing every versioned artifact a model sees or a measure depends on (ADR-02). The target package holds what the target language needs; the native package holds what the learner's own language needs. `MEASURES_VERSION` lives in `forone.measures` (3.3), not in a package, because a measure spans languages.

```yaml
# packages/languages/en/versions.yaml  (one per target language; the pilot has `en` only)
prompts:
  teacher_system: 1.2.0
  writer_system: 1.3.1
  fitter_tagging: 1.0.0
  editor_rubric: 1.1.0    # check 10 widened to "nothing reads as a correction or a lesson" (ADR-06)
  host_system: 1.4.0      # carries the brief's `recasts` echo plan, the only correction channel
  chat_host: 1.0.0
  analyst_full: 1.2.0
  analyst_fast: 1.0.1
  memory_keeper: 1.0.0
  proof_producer: 1.0.0
  rater: 1.0.0            # pinned per 4-week window (assessment D12); a bump here is refused inside a window
rules:
  structure_rules: 1.0.0  # structure_rules.yaml
  law_words: 1.1.0        # guard/law_words.yaml
  correction_words: 1.0.0 # guard/correction_words.yaml, the correction guard's phrase list (07, ADR-06)
  ban_list: 2026-12-04    # dated, grows monthly
  crisis_keywords: 1.0.0
thresholds:
  asr_confidence: 0.70    # set by the 10.14 run for this target
  similarity_cosine: 0.85 # Part 18 #10
assessment_version: 1.0.0 # semver stamped on stores and claims (assessment D12); calibration is per target
gate: 2026-11-17          # the date `vendor-lab gate --target en` passed (ADR-03); a package without it cannot be deployed
```

```yaml
# packages/native/ar/versions.yaml  (one per native language; `native/en` is the universal fallback)
prompts:
  salma_live: 1.0.2       # talkback and the two questions
  salma_explain: 1.0.0    # explanations when the learner asks (Sonnet, on demand; ADR-06)
strings: 1.3.0            # interface strings, including the one line for a pulled episode (R4) and the pmf question (4.4)
consent: 1.1.0            # consent texts and the privacy notice, counsel-reviewed
guard:
  law_words: 1.0.0        # the native language's guilt, attachment and game words
  correction_words: 1.0.0
crisis_resources: 2026-12-15  # per ISO country, with the international directory fallback (ADR-20)
```

**CI jobs on every PR:** `unit` (all packages, `FORONE_FAKE_VENDORS=1`), `pii_scrub` (the log scrubber and Sentry scrubber against `eval/fixtures/pii_corpus.jsonl`, 4.9), `inngest_payloads` (no event model carries `text`, `quote`, `transcript` or `audio`; the security domain's test), `law_scan`, `claim_gate`, `fitter`, `migrations` (upgrade and downgrade on a fresh database). **`eval-gate`** runs only when the diff touches a path in the map below, with the mapped suites, for the package directory the path sits in (`packages/languages/<target>/...` runs the suite with `--target <target>`; `packages/native/<lang>/...` runs the native-side checks for that language); it runs against `staging` for `host` and `calls_50` and `local` otherwise, and it is a required check on `main`. Because prompt edits are daily during the build weeks, not weekly, the gate runs in two halves [DECISION, skeptic review]: the **cheap half** (governor replay, `law_scan`, `claim_gate`, `fitter`, `measures_replay`, anything with `vendors: fake`) on every push; the **paid half** (`writer`, `pipeline`, `editor`, `analyst`, the simulated caller, `injection`) when the PR carries the `ready-for-review` label and again on the merge commit. A merge needs both halves green on the final commit.

| Path changed (under `packages/languages/<target>/` unless stated) | Suites run | Cost | Minutes |
|---|---|---|---|
| `prompts/teacher_*`, `prompts/writer_*`, `ban_list.yaml`, `vendors.yaml roles.teacher|writer` | `writer`, `pipeline` (paid half) | about $12 | 12 |
| `prompts/editor_*`, `vendors.yaml roles.editor` | `editor` (paid half) | $0.50 | 3 |
| `prompts/host_*`, governor code, `guard/correction_words.yaml`, `vendors.yaml roles.host|call_tts|streaming_stt` | `host` replay and law scan (cheap half, every push); `host` with 20 calls on staging and `injection` (paid half, 15 minutes, which is why it waits for the label) | about $4 | 2 + 15 |
| `prompts/analyst_*`, `structure_rules.yaml`, measures code, `claims.py` | `analyst` (runs `calibration/run`), `claim_gate` | about $1 | 6 |
| `packages/native/<lang>/prompts/salma_*`, `strings`, `guard/` | `salma`, `law_scan` for that native language | cents | 3 |
| `prompts/memory_keeper*`, facts code | `memory` | cents | 2 |
| `prompts/rater*`, `vendors.yaml roles.rater` | `analyst` (rater component of `calibration/run`), and the job refuses the bump when `pinned_until` is in the future | about $1 | 6 |
| `guard/law_words.yaml` (either package kind) | `law_scan`, `salma`, `host` (replay half only) | free | 2 |
| `vendors.yaml roles.verbatim_stt|streaming_stt` | `recognizers` for that target | $0.50 | 5 |
| `forone/measures/**` | `measures_replay` (recompute 7 days on the staging copy and diff against the previous version; any measure that moves more than 5 points is listed in the PR) | free | 4 |

**Release.** `main` deploys to staging on merge (topology `deploy-staging.yml`); staging stays up from build week 2 through the beta, because `eval-gate` on the host prompt is the only thing between a prompt edit and the law-7 promise on a live call (ADR-16; after the beta the `host` suite runs against an ephemeral worker that CI starts). A prod release is a tag `v2026.12.17-1` created from `main` by `tools/release cut`, which writes the `release_manifest` row (versions snapshot per package, image digest, flags snapshot, the `eval_runs` ids that cover this diff), opens the manual approval in GitHub, and posts to Slack. After approval: migrations, rolling deploy, then `ops/canary` runs one `episode/produce` and one scripted call for the synthetic learner through the primary voice vendor; a failed canary rolls back automatically to the image digest of the most recent `release_manifest` row with `canary_passed = true` (not "revision minus one": a failed deploy also registers an ECS revision) and pages P2. The deploy is announced in Slack with the manifest diff.

```sql
create table release_manifest (
  tag text primary key, git_sha text not null, image_digest text not null,
  versions jsonb not null, flags jsonb not null, eval_run_ids uuid[] not null,
  cut_by text not null, cut_at timestamptz not null, approved_by text, deployed_at timestamptz,
  canary_passed boolean, rolled_back_at timestamptz, notes text
);
```

Release rules [ADR-16]: there is no fixed release day or hour, because learners are in every timezone and some learner's drop is always near; instead `tools/release deploy` computes the window from `learner_schedule` and the check is **binding**: it refuses the deploy while more than 2% of learners with `expects_drop = true` have `next_drop_at` in the next 45 minutes (the figure is printed; the tool also prints the next time the share falls under 2%, which at 100 learners spread over the clock is usually within the hour), and an override needs a reason row (`release_manifest.notes` plus an `audit_log` row, both shown in the Slack announcement); a `call-worker` deploy drains as 01 §4.4 #7 says and never starts a new task while `active_jobs > 0`, at any hour; never while `/admin/alerts` shows a firing P1; migrations are expand-then-contract, forward-only in prod, and a contract migration ships at least one release after its expand; a prompt version bump and a code change that depends on it ship in the same release; **freeze** from 2026-12-21 12:00 to 2026-12-24 12:00 UTC (around the beta opening on 12-23) and from 2026-12-31 to 2027-01-02 (the Gemini price change lands on 2027-01-01, beta week 2); the first finales start 2027-01-19 and the voice plan from 08 §6.1 note 3, if taken, ships in the first release after 2027-01-02 (ADR-07). Rollback is "deploy the last `canary_passed` tag"; a rollback of a prompt version is the same PR reverted plus a release, because versions are files.

### 4.4 The beta gates as a team dashboard

`/admin/gates` shows one row per gate per cohort (cohorts are the weekly invite batches keyed by `cohort_key = invite_date`: `2026-12-23`, `2026-12-30`, `2027-01-06`, ...; the beta opened on a Wednesday, so the cadence is Wednesdays, ADR-07) and an "all cohorts old enough" column. Each cell shows the value, `n`, the target, the stop line, and the date the cell first became readable. Cells before their readable date show "not yet" and nothing else, so no one reads a 3-day-old cohort's week-4 retention.

| Gate (16.1) | Measure key | Readable for a cohort from | Numerator / denominator | Notes |
|---|---|---|---|---|
| Trial to paid 30%+ (stop under 15%) | `trial_to_paid` | cohort start + 10 days (day 7 ask plus 3 days grace) | `learners.status` reached `paid` on any of the three plans / learners who completed A9 (`trial_started_at` set) | `extra.by_plan` shows which plan was chosen (the trial plan is `two_a_day`, ADR-04); a declined-card retry counts once; first readable 2027-01-02 |
| Active in week 4 (paid) 40%+ (stop 25%) | `active_w4_paid` | cohort start + 28 days | paid learners with ≥ 1 active day in days 22 to 28 / paid learners | First readable 2027-01-20 for the first cohort (ADR-07) |
| Sessions per active learner per week 4+ (stop 2.5) | `sessions_per_active_learner_week` | cohort start + 7 days, then weekly | median over learners active that week | Shown per week since onboarding |
| Learner's own speech per session 4+ min (stop 2) | `speech_min_per_session_p50` | cohort start + 7 days | see 4.1 row 23 | Main call plus round two plus shadow plus say-it-once |
| The 4-weekly recording improves for most | `recording_improved_share` | first finale (cohort start + 28 days, on the learner's next session) | see 4.1 row 26 | Claims through the gate only; "no measurable change" is the stop line |
| Second-month renewal 60%+ (stop 40%) | `renewal_m2` | first renewal date + 3 days | `payment_events` second successful monthly charge / all paid learners whose first month ended, on every plan; founding is a price lock, not a term, so there is no exception (ADR-04) | For the first cohort (trial from 12-23, first charge about 12-30) the second charge falls about 2027-01-30, so this gate first reads about 2027-02-02, **after the gate review of 2027-01-26**; the gates page shows "not yet" on that day and the review reads `trial_to_paid` and the cancellation count instead; `extra.by_plan` |
| "Very disappointed" 40%+ (stop 25%) | `very_disappointed_share` | cohort start + 28 days | `pmf_answer = very` / all `pmf_answer` | The PRD names the metric but not the ask; this document adds one in-app question, asked once in the week-4 proof's question slot in place of the worth-it question that week, with the three answers; the wording is a string in `packages/native/<lang>/strings` [DECISION, new event `pmf_answer`; OPEN for Muath on mechanism and wording, section 10]. No email, because 3.10 allows none |
| Cost per session under $0.60 (stop over $1.00 with no plan) | `cost_per_session_p50` | from the first week | 4.1 row 22 | The mean is shown next to the median and the split by plan next to both; the stop line is judged on the mean of the trailing 7 days and is a P3 with a ticket, never a page (D15) |
| False-claim rate under 5% | `false_claim_rate` | first audit, 2027-01-01 (nine days of claims, mostly `did_it`); a second, mid-month sample on 2027-01-19 so the gate review of 2027-01-26 has a reading [DECISION] | 4.5.3 | Monthly thereafter |
| Wrong memories under 1 in 100 callbacks | `wrong_memories_per_100` | cohort start + 14 days | 4.1 row 20 | 30-day window |
| New trials from referrals and forwarded samples 30%+ (stop 10%) | `referral_trials_share` | from the second invite batch (2026-12-30) | trials whose `waitlist.source in (share, referral)` / trials started | `waitlist.source` is set from the share page's `?ref=` and the invite's referrer field [ASSUMPTION: the client domain records `source`] |
| *Reported, not a gate:* plan mix | `plan_mix` | from the first paid learner | share of paying learners per plan, `founding_locked` as a sub-count | concept-v2 §9 asks for it at the public-launch gate; in the beta it is a line, not a gate (ADR-15) |
| *Reported, not a gate:* blended margin | `blended_margin` | from the first complete week with paid learners | from 08's "Margin by plan" section (net price less measured cost, over paying learners) | concept-v2 §9 wants it above about 50% at public launch; shown next to the cost gate with the break-even per plan from decisions.md ($0.57 / $0.42 / $0.42 at full use) so the Tuesday review sees the two together |

When a gate is under its stop line for two consecutive readable weeks, `/admin/gates` marks it and `ops.page(P3)` adds it to the Tuesday ops review agenda. The decision rule stays PRD-v2 16.1's last sentence: find which claim failed before writing code; the dashboard only makes the failure visible.

### 4.5 Human review

#### 4.5.1 Episodes (PRD-v2 6.8)

The queue is the pipeline's `review_items` and `review_findings` (its D17); this domain owns the sampling job, the page and the loop.

- **`review/sample`** (Inngest cron, daily 03:00 UTC; the hour does not matter because the queue is read in the reviewer's working hours): for each learner, keep a running count of items this calendar month; add every episode with `degraded`, `relisten=skipped`, `fallback`, `same_vendor_edit` or `editor_soft_fail` flags at once; fill up to 10 per learner per month with random shipped episodes (drops and `daily_extra` alike), weighted toward episodes with a `followed_answer=little` or a `huh_per_min` above the learner's median (so the reviewer sees the ones that may be mispitched). The sample stays 10 per learner per month on every plan [DECISION, conformance review]: PRD 6.8 set it for one episode a day, so on `two_a_day` and `three_a_day` the sampled share falls (10 of up to 60 or 90 shipped episodes instead of 10 of 30), which is acceptable because the flagged items are all queued regardless; the monthly summary prints the sampled share per plan so nobody mistakes 10 for a third. In Milestone 0 and the first beta week, every shipped episode is queued (the pipeline's rule). Expected volume at 100 learners: about 1,000 sampled items a month plus flagged items, 35 to 40 a day, about 4 hours of reviewer time a day at 6 minutes each, per target language (the pilot has one). Reviewer hours, rate and start date: 10-decision-records §10 item 11.
- **The page** `/admin/review/episodes`: script, article, audio player, editor verdict, the `why` reasons, the fitter's coverage and new-word list, side by side; the display name and `life_facts.people` names tokenized (security D14); the reviewer never sees transcripts, the notebook or any claim. One form: flags (`error`, `sameness`, `law`, `gloss`, `other`), the lines, a note, ban proposals, a `similarity_judgment` for the paired "too alike?" question when the item was sampled as a similarity pair.
- **The loop**: ban proposals are accepted or declined by Muath on `/admin/review/bans` and inserted by code with `source=review_finding`; `law` flags open a `law_corpus` PR automatically (the line, the surface, the flag) through a GitHub issue the engineer turns into the fixture; `error` flags with a line id are counted per prompt version in `measure_points(measure='review_error_rate')` so a prompt regression that the suite missed is visible within a week; `sameness` judgments feed the assessment of the similarity threshold (`similarity_p90` against `too_alike_human`); the monthly summary (findings by flag, by format, by prompt version) is on the first Tuesday's ops review.

#### 4.5.2 Calls [DECISION, extends 6.8 to the call]

The PRD reviews episodes; the move contract (5.4.6), anxiety mode (5.4.7) and law 7 are only measurable on real calls, and the governor counts what the host declared, not what the learner experienced. A `call_review_items` queue samples 1 call per learner per month [DECISION, skeptic review: 2 per learner at 100 learners was about 200 transcripts and 20 hours of Muath's time a month; 1 plus the flagged calls is about 100 transcripts and 10 hours] plus every call with `moves.violations ≥ 2`, every call with a correction-guard block (`moves.violations` with `kind = correction`, however many), every `end_reason in (crisis, abandoned, pipeline_error)` in a learner's first week, and every call where `anxiety_mode` was entered. The reviewer for calls in the beta is Muath himself (role `owner`) for the English target, because a call transcript is the learner's own speech and the trust contract's promise 6 ("told, not inferred") means the fewest eyes possible; a further target language needs a call reviewer who reads it (`staff_accounts.languages`), which is one of the costs of opening a language; a `tagger` may read only transcripts of learners with `data_use=true`, anonymized through the security domain's `research/anonymize`, and only for calibration tagging, never for call review. A finding with `move_contract.never_rules_ok = false` counts in measure 27 and is a law-7 incident: the line goes into the law corpus and the correction guard's phrase list in the same PR.

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

`claims/audit-sample` (Inngest cron, the 1st of each month, 06:00 UTC, and once on 2027-01-19 for the gate review) samples from `claims` with `status=shown` and `shown_at` in the previous month (or since the last sample): all claims if fewer than 40, else 40 stratified by `kind` (every kind represented at least 3 times). It writes `claim_audits` rows and the auditor (Muath, or a second trained person [OPEN for Muath]) opens each on `/admin/review/claims`: the claim sentence as shown, the evidence (`claim_evidence`: the two sentences, or the two clips by byte range where voice storage is on), the gate inputs (`sem`, `n_pairs`, task types, `assessment_version`). Verdicts: `true` (the evidence supports the sentence as a learner would read it), `false` (it does not), `unclear` (the evidence is ambiguous or the sentence overstates). `false_claim_rate` = false / (true + false + unclear); unclear counts against. Above 5% for a kind: that kind is switched off with the flag `claims.kind.<kind>` (4.7) until the cause is fixed, and the next proof for affected learners says so (assessment D16's notice path).

```sql
create table claim_audits (
  id uuid primary key, claim_id uuid not null, sampled_for date not null,
  verdict text check (verdict in ('true','false','unclear')), reason text,
  audited_by text, audited_at timestamptz, created_at timestamptz default now()
);
```

#### 4.5.4 Access rules for every review surface

| Surface | `owner` | `engineer` | `reviewer` (paid native reader of a target language; `staff_accounts.languages` limits the queue to that language's learners) | `tagger` (calibration) | `ops` |
|---|---|---|---|---|---|
| `/admin/review/episodes` (scripts, audio, verdicts; names tokenized) | read, action | read | read, file findings | no | no |
| `/admin/review/calls` (verbatim transcripts with timings) | read, file findings | read when on-call for an incident, logged | no | no | no |
| `/admin/review/claims` (claims with evidence, clips) | audit | read | no | no | no |
| `/admin/research` (anonymized text of `data_use=true` learners) | read | no | no | tag | no |
| Learner audio (any) | break-glass with reason | break-glass with reason | no | no | no |
| `/admin/measures`, `/admin/gates`, `/admin/alerts`, `/admin/incidents` | read | read | no | no | read |
| `/admin/flags`, `/admin/vendors`, admin actions | write | write | no | no | write (flags and vendors only) |

Every read of a learner-content page writes an `audit_log` row (security D13), which the learner's export includes; the pages run as `forone_admin` (ADR-17), so the row is written by the page, not by pgaudit.

### 4.6 Alerting on the Part 15 budgets and the cost stop line

**Severities.** P1 pages a phone at any hour and opens a Better Stack incident; P2 posts to `#forone-ops` and is handled in working hours (or at once if someone is awake); P3 goes into the 06:00 UTC digest. Only six rule families may be P1 (listed first below); this is deliberate so a two-person team is never paged for a trend, and it is why the stop line (a seven-day mean) is P3 and why lateness for one learner is P2: what a human can fix faster than the pipeline is a systemic failure, so that is what pages (ADR-16). No alert changes what a learner hears: a spend alert may force batch pricing, cap rewrites or skip a canary, never switch a model (ADR-14).

**Rule format.** Every rule is a SQL predicate over a window, evaluated by `ops/watch` every 5 minutes. A rule fires after `for` consecutive true evaluations and resolves after two false ones. `dedupe` groups incidents so one learner or one vendor produces one incident, not one per evaluation.

```yaml
# ops/alerts.yaml (every rule listed; the SQL of three is shown in full, the rest name their predicate)
- id: drops_late_systemic                      # P1 family 1, PRD 15 "tomorrow's episode ready before the drop time" (ADR-16)
  severity: P1
  sql: |
    with due as (
      select ls.learner_id, ls.next_drop_at
      from learner_schedule ls
      where ls.next_drop_at between now() and now() + interval '45 minutes'
        and ls.expects_drop),                  -- 04's column: the learner's previous local day was active (PRD 3.6 rule 2)
    late as (
      select d.* from due d
      where not exists (select 1 from episodes e where e.learner_id = d.learner_id
                          and e.drop_at = d.next_drop_at and e.state in ('ready','published')))
    select count(*) as late_n, (select count(*) from due) as due_n
    from late
    having count(*) >= 3 or count(*) >= 0.05 * greatest((select count(*) from due), 1)
  for: 1
  dedupe: "systemic:{date_trunc('hour', now())}"
  runbook: ops/runbooks/R3-pipeline-late-for-drop.md
- id: episode_not_ready_before_drop            # P2 per learner (was P1 in the first draft): Slack with the learner id, one incident per learner
  severity: P2                                 # the pipeline's own escalation (on-demand at drop minus 90 min, 02 §4.2) is still allowed to be finishing
  sql: |
    select ls.learner_id, ls.next_drop_at
    from learner_schedule ls
    where ls.next_drop_at between now() and now() + interval '45 minutes'
      and ls.expects_drop
      and not exists (select 1 from episodes e where e.learner_id = ls.learner_id
                        and e.drop_at = ls.next_drop_at and e.state in ('ready','published'))
  for: 1
  dedupe: "{learner_id}"                       # one Slack thread per learner, not one per drop
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
- id: recognizer_down                           # P1 family 3 (calls cannot run; verbatim evidence cannot be made)
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
- id: cost_runaway                              # P1 family 5, PRD 14.5: runaway spend only (D15). From cost_guard.tripped at the
  severity: P1                                 # hard per-learner level (4 × episodes_per_day × budget, ADR-15) and the daily spend cap
  source: "event:cost_guard.tripped {level: hard}"
  sql_also: |
    -- daily_spend_100: today's spend against the cap Σ plan.episodes_per_day × $1.00 over learners active today (ADR-15)
    select 1 from (select sum(cost_usd) spent from vendor_calls where occurred_at >= date_trunc('day', now())) s,
                  (select sum(p.episodes_per_day) * 1.00 cap from learners l join plans p on p.key = l.plan where l.status = 'paid' or l.status = 'trial') c
    where s.spent > c.cap
  for: 1
  dedupe: "cost_runaway:{date_trunc('day', now())}"
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
- {id: after_pass_late, severity: P2, predicate: "≥ 3 sessions in the last hour with session_summaries.completed_at - call ended_at > 10 min, or evidence_quality='partial' share > 20% today", for: 1, runbook: R9}
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
- {id: cost_stop_line, severity: P3, predicate: "mean session cost trailing 7 days > 1.00, or > 20% of sessions over 1.00 (08 §4.5)", for: 1, dedupe: "stop_line:{week}", runbook: R8}   # the stop line is a trend and a business decision: digest, Tuesday review, and a ticket to Muath with 08 §4.5.3's 48-hour plan window; never a page (D15)
- {id: cost_guard_soft, severity: P3, source: "event:cost_guard.tripped {level: soft}", dedupe: "{learner_id}:{date}", runbook: R8}   # 2.5 × episodes_per_day × budget for one learner: a digest line, the guard already forced batch pricing for that learner
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
- {id: heartbeat_late, severity: P1, source: betterstack, monitors: [measures/hourly, ops/watch, privacy/verify, retention/daily], grace: 30 min}   # measures/hourly and privacy/verify are hourly, so a 30-minute grace means a missed run pages within 90 minutes
```

**4.6.1 Every Part 15 budget and its signal.**

| Budget (PRD-v2 15) | Signal | Source | Rule |
|---|---|---|---|
| First sound under 60 s | `client_perf.first_sound_ms` | client | `first_sound_slow` |
| First spoken sentence in the target language under 5 min | `client_perf.first_sentence_ms` | worker | measure 18 only; no alert (the learner's own pace moves it) |
| Sample playable under 30 s | `client_perf.sample_first_sound_ms` (anonymous telemetry) | client | P3 if p50 today > 30 s |
| Pilot playback under 45 s | `episode.streaming_started - onboarding.intake_completed` | workflows | `on_demand_slow` |
| Dropped episode start under 2 s | `client_perf.play_start_ms` | client | `dropped_start_slow` |
| On-demand episode under 30 s | `episode.streaming_started - trigger event` | workflows | `on_demand_slow` |
| Call connect under 3 s | `calls.metrics.connect_ms` | worker | `call_connect_p95` |
| Host reply p50 1.5 s, p95 2.5 s | `calls.metrics.reply_latency_*` | worker | `host_reply_p50_20calls`, `host_reply_p95_20calls` |
| Talkback under 2 s | `calls.metrics.talkback_ms` | worker | `talkback_p50` |
| Word sheet under 300 ms | `client_perf.word_sheet_open_ms` (logged only when over) | client | `word_sheet_slow` |
| Chat opener under 30 s | first host `chat_message` minus door open | workflows | `chat_opener_late` |
| After-session pass within 10 min (one stage; the 90-second notes budget is gone, ADR-06) | `session.after_pass.completed` minus `call.ended` | workflows | `after_pass_late` |
| Episode ready before drop; on-demand at drop minus 90 min | `episodes.state` at drop minus 45 min, per learner and in aggregate | workflows | `episode_not_ready_before_drop` (P2), `drops_late_systemic` (P1) |
| "Next one" episode (`daily_extra`) streaming under 30 s | `episode.streaming_started - POST /v1/episodes/next` | workflows | `on_demand_slow` (ADR-05) |
| Audio deleted within 15 min (storage off) | `media_objects` ephemeral overdue; `privacy/verify` | data, security | `privacy_promise_missed` |
| All audio deleted within 24 h of revoke | `privacy/verify` | security | `privacy_promise_missed` |
| Live voice failure falls back to voice notes | `end_reason=fallback` share | worker | P3 if > 10% of calls today |
| Voice vendor outage: second vendor same day | `vendor.degraded`, `voice.vendor_failover` | topology, pipeline | `voice_failover_active`, `voice_both_vendors_down` |
| Cost: $0.60 budget, $1.00 stop line | `session_costs` (08's table, filled by `cost/rollup` from `vendor_calls` and `episodes.cost_usd`, with `plan`) | cost | `session_cost_over_1`, `cost_p50_7d_over_080` (P2); `cost_runaway` (P1); `cost_stop_line` (P3 plus the ticket) |

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

Flags that exist in the beta, with their default on 2026-12-23:

| Key | Default 12-23 | What it gates | Kind |
|---|---|---|---|
| `round_two` | off → allowlist in week 2 of the beta | PRD 5.4.9 [P1] | P1 rollout |
| `shadowing` | off | 5.2 [P1] | P1 rollout |
| `dial_in` | off | 5.4.12 [P1] experiment, allowlist only | P1 rollout |
| `finale` | off → on when the first season boundary approaches (2027-01-19) | 11.2 [P1] | P1 rollout |
| `tape` | off | 12.3 the tape [P1] | P1 rollout |
| `claims.kind.fluency_change`, `...accuracy_change`, `...complexity_change` | off (and the gate refuses anyway until `n_pairs ≥ 12`) | 11.1 full proof [P1]; also the audit's kill switch (4.5.3) | kill switch |
| `claims.kind.first_ever`, `...word_owned`, `...did_it` | on | the simple proof [P0]; off only in an audit emergency | kill switch |
| `host.model=haiku` | off | the call domain's measured fallback as a lever; flipped by a person after the `host` suite passes, never by a spend mode (ADR-14; 10-decision-records §10 item 6) | vendor lever |
| `teacher.model=sonnet` | off | the same rule for the teacher | vendor lever |
| `tts.batch` | off | the pipeline's P1 batch TTS lever; a spend mode may set it because no learner hears the difference (ADR-14) | vendor lever |
| `pipeline.editor_model` | on | off = the editor runs on `claude-opus-5-5` flagged `same_vendor_edit` for review during a Gemini outage (ADR-11); there is no "code checks only" state | kill switch |
| `episodes.extra` | on | off = `POST /v1/episodes/next` answers "not today" and the "next one" control hides; the spend guard may pause it under the daily cap (ADR-14, ADR-15) | kill switch |
| `chat.enabled`, `talkback.enabled`, `salma.explain` | on | kill switches (`salma.explain` off = Salma answers "let's keep going" when asked, never a note) | kill switch |
| `drop.push` | on | off = feed alert only | kill switch |
| `observer_slot` | off | the call domain's reserved slot [LATER] test | experiment |

Rules: a flag never changes a law (there is no flag for recasts, the correction guard, the allowance, the three message kinds, consent, or the claim gate's rules; the notes feature is removed, not flagged off, ADR-06); a kill switch's `default` is its safe state; every flip writes `audit_log` and `flag.changed`; a flag older than 60 days with state `on` is a cleanup ticket.

### 4.8 Runbooks

Each runbook is one page in `ops/runbooks/` with the same five headings. The twelve, condensed:

**R1 Voice vendor outage (episode TTS or call TTS).** *Detect:* `vendor.degraded` (5 failures in 10 min), `voice.vendor_failover`, `canary_failed`, or a learner saying the host sounds different. *First five minutes:* confirm on the vendor's status page; check `/admin/vendors` shows the secondary active for `episode_tts` and `call_tts`; check the pipeline's `failover.active` is sticky. *Fix:* if the automatic switch did not happen, flip `vendor_config` on `/admin/vendors` (no deploy); if both vendors are down (P1), leave the editor alone, let `day/next` ship yesterday's episode state (the Today screen keeps the unplayed episode; no drop push fires for an episode that is not ready, PRD 3.6) and switch calls to the voice-note fallback by flag `talkback.enabled=off` plus the worker's own fallback path. *Verify:* `ops/canary` on the active vendor passes; the next shipped episode carries the one-line announcement (PRD 7.1). *Tell the learner:* nothing beyond that line; never an email. *Afterwards:* switch back only after a passing canary, inside a computed deploy window (4.3), and announce again.

**R2 Recognizer outage (streaming or verbatim).** *Detect:* `vendor.degraded` for `streaming_stt` or `verbatim_stt` (keyed by target language, ADR-03); `after_pass_late`; `evidence_quality=text_only` share rising. *First five minutes:* streaming down means calls cannot run: confirm the worker is sending new calls to the secondary (Deepgram) by `vendor_config`; if no secondary passes the 10.14 gate for that target [ASSUMPTION: Deepgram is wired as the hot secondary per the call domain's P1 plan; before that, the fallback is voice notes], set calls to the voice-note fallback. Verbatim down means the after-pass and the claims lose evidence: the call domain keeps audio until the 15-minute window; after that, evidence is low-confidence and makes no claims (PRD 5.4.11), which is the designed behaviour; the `call_turn_verbatim` events are appended late or never. *Fix:* flip the vendor; re-run `call/verbatim-turn` for turns whose audio still exists (`/admin/calls/{id}/retranscribe`, only while audio exists). *Verify:* `recognizers` suite on the secondary; `after_pass_late` resolves. *Tell the learner:* nothing; the after-pass runs with `evidence_quality=text_only` and the notebook simply gains less that day.

**R3 Pipeline late for the drop.** *Detect:* `drops_late_systemic` (P1: 3 or more learners, or 5% of those with a drop in the next 45 minutes, have no `ready` episode), `episode_not_ready_before_drop` (P2, one learner), `on_demand_slow`, Inngest run failures. The P1 means something shared is broken (a vendor, a batch, Inngest, a deploy); the P2 is usually one learner's run and the pipeline's own escalation (on-demand at drop minus 90 minutes, 02 §4.2) may still be finishing it. *First five minutes:* for the P1, `/admin/alerts` lists the late learners; open the Inngest runs for `episode/produce`; the step that is stuck in most of them names the cause (teacher batch not returned, TTS slow, editor loop, a bad deploy in `release_manifest`). *Fix, in order:* if a batch result is late, the pipeline's cut lines should already have re-run at standard price; if not, cancel and re-run the functions with `pricing_mode=standard` from `/admin/episodes/{id}/rerun` (bulk from the alert's list); if a vendor is down, R1 or R2; if the editor is looping, the editor fallback on Opus (`same_vendor_edit`, ADR-11) is automatic when the second vendor is down and can be forced per run from the same page; if the cause is the last deploy, roll back to the last `canary_passed` tag. If nothing can ship by the drop time: do nothing to the learner's screen. The unplayed previous episode stays as today's hero and no push fires (PRD 3.6 rule 2); the late episode publishes when ready and the push fires then. *Verify:* `episodes.state=published`, `drop.published`, the P1 resolves on the next evaluation. *Tell the learner:* nothing. The Milestone 0 "a day late" message is replaced by silence plus the late drop, because a late drop is not one of the three message kinds (3.10). *Afterwards:* every `drops_late_systemic` firing gets a postmortem within 7 days; a P2 that repeats for the same learner three days running becomes a ticket.

**R4 Bad or fallback episode shipped.** *Detect:* `fallback_3_in_7`, `editor_degraded_share`, a reviewer `law` or `error` flag on a shipped episode, a learner message. *Decide:* a shipped episode is **pulled** only when it breaks law 5 (a fact the learner did not supply, a fake life), law 1 or 10 (game or lesson language), or memory rule 8.4 (an unconfirmed or "don't bring up" fact); an episode that is merely weak is not pulled. *Fix:* `/admin/episodes/{id}/pull` [DECISION, new admin action]: sets `episodes.state=pulled`, removes the feed item (the enclosure returns 410), replaces Today's hero with a fallback episode produced on demand at standard pricing (`episode_kind=fallback`), writes `episode.pulled`, and gives Salma one plain line on Today in the learner's native language, the string `episode_pulled` in `packages/native/<lang>/strings` (for `native/ar`: "سحبنا حلقة اليوم بسبب خطأ من عندنا، وهذي بديلة."; in English: "we pulled today's episode because of a mistake on our side; here is a replacement"). The pulled episode stays in the archive only if the learner already played at least half of it (it is theirs), marked with the same line; otherwise it is deleted. *Verify:* the new episode passes the editor; the review item is filed with the cause; the law corpus or the editor fixtures gain the case. *Tell the learner:* that one line and, if a wrong fact was spoken, R12's correction path. *Afterwards:* three fallbacks in 7 days means the learner's model or interests are thin: Muath reads the three teacher briefs and, if the cause is a sparse intake, asks Salma to ask one more question next session (within 2.4's one-question rule).

**R5 Client latency budgets missed (first sound, dropped start, word sheet).** *Detect:* `first_sound_slow`, `dropped_start_slow`, `word_sheet_slow`. *Fix:* for first sound, check the Salma onboarding clip is served from the package cache and the pre-account session path; for dropped start, check the service-worker precache hit rate in `client_perf.context.cached`; for the word sheet, check `glosses.json` size and the index version. None of these is a page; they are Tuesday items unless p50 doubles.

**R6 Call latency or governor violations.** *Detect:* the four latency rules, `governor_violations`. *First five minutes:* `vendor_calls` for the last 20 calls grouped by role shows which hop grew (STT final, LLM first token, TTS first byte); the cached-prefix hit rate (`cache_hit_low`) is the usual cause of LLM first-token growth. *Fix:* vendor hop → R1/R2 or `vendor_config`; LLM → check for a prompt change that broke the cached prefix (release manifest diff) and roll back the prompt version; violations → the `host` suite on the current prompt version, then roll back. *Verify:* `calls_50` on staging passes the gates.

**R7 Platform down (Vercel, `api`, Postgres, Inngest).** The topology's section 5 table is the fix list; this runbook adds the order of checks (Better Stack → ECS events → RDS events → Inngest status), the fact that calls in progress survive an `api` outage for 10 minutes by spooling, and that the feed keeps serving while `api` is up. `outbox_growing` is the Inngest-down signal; once Inngest returns, `outbox/relay` drains and a human re-sends `idea.chosen` from `/admin` only for learners whose `day/next` run was lost.

**R8 Cost runaway and the stop line.** *Detect:* `cost_guard.tripped` (per learner per day, security D11), the daily spend cap (topology), `session_cost_over_1`, `cost_p50_7d_over_080`. *First five minutes:* `/admin/measures?m=cost_per_session` with `extra.top10`; the cost domain's per-role breakdown for the day; look for a retry storm (`pipeline_steps` with `outcome=retry` count), a cache miss (`cache_hit_low`), a rewrite loop (fitter rounds > 2), or a long call (`metrics.duration_ms > 8 min`, which the governor should prevent). *Fix:* the bug; or the levers in order of least learner impact: batch everything nobody waits on, cap rewrites, skip the nightly smoke, pause `episodes.extra` under the daily cap (all of which a spend mode may do on its own, because no learner hears the difference), then, by a person only and after the matching suite passes, `tts.batch`, `host.model=haiku`, `teacher.model=sonnet` (ADR-14). The levers are per plan: the cost guard's levels are 2.5 × and 4 × `plan.episodes_per_day` × budget (ADR-15), so a `three_a_day` learner at $2.00 a day is not a runaway. *The stop line* (`cost_stop_line`, P3) is not an engineering alert and never pages: it lands in the digest and the Tuesday review and opens a ticket to Muath with the breakdown by role and by plan and the costed plan; 08 §4.5.3 gives him 48 hours to record the plan in `cost_reports`, after which the ticket repeats daily; PRD 14.5 says the beta stops without one, and the decision to stop is his (10-decision-records §10 item 15).

**R9 After-pass or chat opener late.** *Detect:* `after_pass_late`, `chat_opener_late`. *First five minutes:* Inngest run for `session/after-pass` (one function with the 10-minute budget, ADR-06): a step over 60 s is almost always the verbatim turn of the last learner turn (R2) or the analyst call. *Fix:* vendor → R1/R2; if the after-pass is failing in a code step, the data domain's rule applies (`finish` runs with `evidence_quality=partial`; the teacher plans with `evidence_lag`); re-run with `/admin/sessions/{id}/rerun-after-pass` once fixed (the rebuild path makes this safe). *Tell the learner:* nothing; there is no surface that waits for the after-pass (the notebook and the next episode simply use what exists), so there is nothing to show and no spinner anywhere.

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

Allowed in logs: every id (learner, session, episode, call, event, run, trace), enums, counts, durations, costs, versions, vendor names, step names, error classes, HTTP status codes and the vendor's request id. **Never in logs:** display names, emails, phone numbers, birth dates, any transcript or chat text, any life fact or quote, idea text, any audio reference's content, prompts, completions, feed tokens, OTP codes, API keys, and **any vendor error message body**: Anthropic and Google 400 responses quote the offending input, so a "sanitized error message" truncated to 200 characters is the first 200 characters of a learner's turn reaching CloudWatch and Sentry through a field not named `text` (skeptic review). The adapters' error path therefore goes through `forone.ops.logscrub.vendor_error(exc)`, which returns `{vendor, error_class, http_status, vendor_request_id, retryable}` and nothing else; the body is never read into a log record, and the Sentry hook strips `response.text`, `response.body` and `error.message` on vendor exceptions before send. 07 owns the policy (nothing a learner said leaves the home region's stores); this domain owns the implementation and the test. The scrubber `forone.ops.logscrub` is applied at the logger, not by callers: it drops any field whose name is in `forone.learner.pii`'s classified set, truncates any string field over 200 characters, replaces anything matching the security domain's typed-token patterns (email, phone, URL, 5+ digit runs) and refuses (raises in dev, drops in prod with a counter `logscrub_dropped_total`) any field named `text`, `quote`, `transcript`, `prompt`, `completion`, `content`, `body`, `message` (vendor errors carry their class in `error_class`, so `message` is never needed). CI runs the scrubber over `eval/fixtures/pii_corpus.jsonl` (300 lines seeded with every PII shape in every native and target language the beta serves, English and Arabic first, and including a recorded Anthropic 400 and a Google 400 whose bodies embed a learner sentence) and asserts zero leaks.

**Correlation.** `trace_id` is minted by `api` per request and by `workflows` per Inngest run (the run id doubles as it), carried in every Inngest event's metadata as a scalar (so Inngest sees pointers only), set on every adapter call (`CallMeta.trace_id`), and attached to every Sentry event. A bad episode is traced as: `episodes.id` → `pipeline_runs.inngest_run_id` → `pipeline_steps` with versions, cost and the step artifacts (the prompts and completions themselves live here, in the home region, 02) → the Langfuse trace (by `trace_id`) for usage, latency and the prompt hash, and for the text too when the learner is in the research set → `release_manifest` for what was deployed at the time → the `learner_model_versions` row for what the teacher read. Debugging reads prompts from the home region, not from Langfuse (ADR-09).

**What goes where.**

| Store | Holds | Learner text? | Retention | Owner |
|---|---|---|---|---|
| CloudWatch Logs | the log lines above, EMF counters | never | 30 days | this domain |
| Sentry (EU) | exceptions with scrubbed context: ids, versions, step; browser errors from `web` | never (scrubber plus Sentry's server-side scrubbing on `text`, `quote`, `transcript`) | 90 days | this domain |
| Langfuse (EU) | every model call: ids, versions, usage, cost, latency, prompt hash, `user_id` = the research pseudonym from `research_pseudonyms`, never the learner id; prompt and completion text only for learners with `data_use = true`, after `anonymize()` (ADR-09, 01 D15) | only for `data_use` learners, anonymized; no audio | 30 days; deletion by pseudonym | cost domain |
| Postgres (`pipeline_steps`, `vendor_calls`, `calls.metrics`, `eval_runs`, `alert_state`, `incidents`) | structured facts about runs | no | the row's own rules | the owning domains |
| Better Stack | incident titles with ids only | never | vendor default | this domain |
| `#forone-ops` Slack | alert titles with ids, deploy notes, canary results | never (the poster uses the same scrubber) | Slack default | this domain |

Sampling: 100% of everything in the beta; at 10,000 learners Langfuse can sample to 20% except calls in the assessment and claim path (the cost domain's note); logs stay at 100% because they hold no content.

### 4.10 The operational calendar of the beta

All job times are UTC, and no job assumes a learner's local time of day: drops happen at every hour of the clock, because learners choose a slot in their own timezone (`learners.tz`) and live anywhere (decisions.md §1; ADR-16). Jobs that depend on a learner's day run hourly and ask which learners' local days just closed; reports and reviews run at fixed UTC times that suit the team, which is a fact about the team, not about any learner. The old "drop window" of the first draft is gone; "a drop within 45 minutes" is the only drop-relative notion left, and it is evaluated against `learner_schedule`, never against a clock.

| Cadence | When (UTC) | What | Who | Mechanism |
|---|---|---|---|---|
| Every 5 min | always | `ops/watch` evaluates `ops/alerts.yaml`, including `drops_late_systemic` over the next 45 minutes of `learner_schedule` | automatic | Inngest cron, heartbeat to Better Stack |
| Hourly | :10 | `measures/hourly`: every learner-local day that closed in the previous hour (learner-day rows, then the cohort and `all` rollups for that date); idempotent upserts | automatic | Inngest cron, heartbeat |
| Hourly | :20 | `privacy/verify` (security): the last 25 hours of `media_objects` and deletion requests against `expires_at`, so a window promised in any timezone is checked within the hour; `retention/daily` (data) runs per learner-local midnight inside the same hourly cadence | automatic | Inngest crons, heartbeats |
| Daily | 03:00 | `review/sample` fills the review queues | automatic | Inngest cron |
| Daily | 06:00 | The digest: P3 alerts (including `cost_stop_line` if firing), the last 24 hours' cost per session (p50, mean, by plan, top 3), fallbacks, degraded counts, review backlog, eval nightly result, late drops (P2 count and whether `drops_late_systemic` fired) | automatic → Slack | `ops/digest` |
| Daily | the on-call's first working hour | On-call reads the digest and `/admin/alerts`; closes or escalates | primary | checklist in `ops/runbooks/daily.md` |
| Nightly | 02:00 | `eval/nightly`: the 10-fixture `pipeline` smoke plus `law_scan`, `claim_gate`, `fitter`, `salma` on staging (which stays up, ADR-16) | automatic | GitHub Actions schedule |
| Weekly | Monday 06:00 | `measures/weekly`; the cost domain's weekly cost report (per role, vendor, plan and learner; "Margin by plan", `plan_mix`, `blended_margin`; heavy-use outliers next to it, PRD 14.5, ADR-15); `ops/canary` for each voice vendor (one episode, one call on the synthetic learner) | automatic | Inngest crons |
| Weekly | Wednesday, the team's working hours | Invite batch of about 50 goes out (PRD 2.1.6); `cohort_key = invite_date` is set on the invited learners (the beta opened on Wednesday 2026-12-23, so Wednesdays, ADR-07) | Muath | `/admin/invites` (client domain) |
| Weekly | Tuesday, 30 min | Ops review: the cost report against $0.60 and the path to $0.35, with the margin by plan; the gates page; firing and resolved alerts; incidents and any `drops_late_systemic` postmortem; review findings summary (with the sampled share per plan); flags older than 60 days; next week's releases | Muath plus engineers | agenda generated by `ops/digest --weekly` |
| Weekly | Tuesday after the review | On-call handover | engineers | `ops/oncall.yaml` |
| Weekly, per learner | learner's proof day, in the learner's local time | `proof/fanout` (assessment domain); the simple proof from 2026-12-30 for the first cohort | automatic | |
| Monthly | 1st, 06:00 | `claims/audit-sample` → false-claim audit due by the 7th; `vendor/regress` (recognizer and pronunciation suites per target language on the current vendor models, because vendors update silently); the human review month closes: findings summary, ban-list PR, similarity threshold check, law corpus PR per language | automatic, then Muath and the reviewer | first audit 2027-01-01 for 12-23 to 12-31; an extra sample on 2027-01-19 for the gate review (4.4) |
| Every 4 weeks | window boundaries 2026-12-23, 2027-02-17 (05 4.15: the first window is long so no cohort's first finale crosses it), then every 4 weeks | Rater window: `rater_versions` row for the new window; `calibration/run` must have passed on the pinned model before the window opens; the assessment domain's `pinned_until` set | engineer | checklist; `rater_pin_violated` alert |
| Per learner, every 4 weeks | the learner's day 28 and after | Season boundary: `season.boundary` → finale (flag `finale`, P1) and the then-and-now comparison where two recordings exist; the first boundaries fall from 2027-01-19 (for 2026-12-23 starters), inside the beta (ADR-07) | automatic | the dashboard shows "finales due this week" from `seasons` |
| Per learner, week 1 | session 2, then once in sessions 3 to 5 | The first "then" recording is offered (P0); `recordings` count per cohort on `/admin/measures` so a low take-up is seen in week 1 | automatic | |
| Dated | 2026-11-10, 11-17 | Recognizer test result (by 11-10) and the voice decision with `vendors.yaml` committed (by 11-17) from `vendor-lab gate --target en` (ADR-03, ADR-07); the `recognizers` and `voices-blind` suites are the gate's regression form | engineer, Muath | `langgate/en/<date>/` |
| Dated | 2026-11-13 | Hume shuts its voice APIs: nothing to do (not used); confirm no adapter references it | engineer | grep in CI |
| Dated | 2026-11-25 | Staging comes up and stays up through the beta (build week 2, ADR-16) | engineer | Terraform |
| Dated | 2026-12-02 | Payment processor decided (10-decision-records §10 item 3); processors approved (security domain, item 14) | Muath | |
| Dated | 2026-12-21 12:00 to 12-24 12:00 | Release freeze around the beta opening | all | `tools/release` refuses |
| Dated | 2026-12-23 | Beta opens; first cohort (a Wednesday); both engineers on call for the first 72 hours, in shifts, because drops fall at every hour | all | |
| Dated | 2026-12-31 to 2027-01-02 | Freeze; on 2027-01-01 (beta week 2) the `price_book`/`prices.yaml` row for the Gemini doubling becomes active; the Monday 2027-01-04 cost report is read with that in mind; the voice plan from 08 §6.1 note 3, if taken, ships in the first release after 01-02 | engineer | the dated row already exists (cost domain) |
| Dated | 2027-01-19 | First finales; the extra false-claim sample | automatic, Muath | `/admin/review/claims` |
| Dated | 2027-01-20 | First readable "active in week 4" for cohort 2026-12-23 | Muath | `/admin/gates` |
| Dated | 2027-01-26 | Gate review (PRD 19.3): the gates page frozen as a snapshot into `bench/reports/gate-review-2027-01-26.json`; `renewal_m2` is still "not yet" on that day (4.4) | Muath | |

### 4.11 On-call for a two-person team

```yaml
# ops/oncall.yaml
rotation: weekly, handover Tuesday 12:00 UTC
primary: [engineer_a, engineer_b]        # alternate weeks; with one engineer, the engineer every week and Muath as primary on the engineer's rest day
escalation: muath                        # after 15 min unacknowledged on P1
pages: P1 only (the six families in 4.6); P2 never calls a phone
protected_hours: none                    # learners are in every timezone, so some drop is always within 45 minutes (ADR-16);
                                         # drops_late_systemic is the rule that protects the drop, and it pages at any hour
acknowledge_within: 5 min                # for any P1, at any hour
tools: Better Stack (schedule, phone escalation, status of heartbeats), Slack, /admin
handover: ops/runbooks/handover.md       # open incidents, flags flipped this week, vendor state, anything degraded
```

What the on-call person does each day is the first-working-hour checklist (4.10). What they must never do alone: flip a vendor back from an understudy outside a computed deploy window, change a prompt version in prod, read learner audio without a reason row, or send any message to a learner (there are three kinds and none is manual). What is explicitly accepted because the team is small, and what 10-decision-records §10 item 7 asks Muath to accept or to fund a second responder for: there is no second responder at night; a P2 found at 02:00 waits for the next working hour; a P1 at 03:00 for the engineer is a real drop somewhere in the world, and if nobody answers within the escalation chain the product's fallbacks hold (the unplayed episode stays as today's hero and no push fires; a voice outage means voice notes; a recognizer outage means voice notes) until a human answers, which for the learners in that band of the clock may mean a late drop; a review backlog over a week is a capacity item, not an incident. The honest summary for the beta: the product never shows a learner a broken state, but a one-engineer rota cannot promise every learner in every timezone an on-time drop on a bad night, and the gates will show it in `unprompted_return_share` and the late-drop count if it matters [DECISION, ADR-16].

## 5. Failure modes, fallbacks and degraded modes

This domain's own failures must never degrade the product; the table says what each one costs and what the learner notices (always nothing).

| Failure | Detected by | Fallback | Learner notices | What is lost |
|---|---|---|---|---|
| `ops/watch` stops (Inngest cron missed, bug) | Better Stack heartbeat late by 30 min → P1 | Better Stack's uptime checks still page for platform-down; CloudWatch alarms still page for infrastructure; the product runs | Nothing | Product-budget alerts for the gap; `alert_state` resumes on the next run |
| Better Stack down | its own status; Slack posts still arrive | `ops.page()` falls back to a Slack `@channel` post for P1 and an email through Resend to both engineers | Nothing | Phone escalation during the outage |
| Slack down | `ops.page()` HTTP error | Better Stack incidents still page; P2 and P3 queue in `alert_state` and post when Slack returns | Nothing | Visibility for a few hours |
| `measures/hourly` fails or runs late | heartbeat; `measures.completed` missing | Re-run is idempotent (upsert by primary key) and the next run picks up every learner-day that closed since the last success, not just the last hour; rows appear late; nothing downstream depends on them | Nothing | A late dashboard |
| Staging down or unreachable (ADR-16 keeps it up) | `eval-gate` paid half fails to connect; Better Stack uptime on staging (P3) | The cheap half still runs; a host prompt bump cannot merge until staging is back (fail closed); `tools/release` is unaffected | Nothing | A delayed merge |
| `tools/release` refuses a deploy for hours (more than 2% of learners always have a drop in the next 45 minutes) | the tool prints the share and the next opening | At 100 learners spread over the clock the share rarely stays over 2%; if the cohort clusters (one timezone dominates), the engineer deploys in the trough the tool names, or overrides with a reason row for a hotfix | Nothing | Nothing; a slower release cadence |
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
| A P1 page at 03:00 (the engineer's night) nobody answers | Better Stack escalation to Muath after 15 min, then repeat every 15 min | the product's own fallbacks (understudy voice, voice notes, unplayed episode stays) hold until a human answers (4.11; 10-decision-records §10 item 7) | Possibly a late episode or a voice-note call, for the learners whose drop falls in that band of the clock | One drop for those learners |
| `drops_late_systemic` fires because of a vendor night, not a bug | R3 | the pipeline's on-demand escalation at drop minus 90 min and standard-price re-runs keep working on their own; the page tells a human that many learners are affected and the runbook starts with the shared cause | Late drops for some | The on-time promise for that hour |
| A flag read fails (Postgres unreachable) | exceptions in `flag()` | the flag's `default` (safe state) | Nothing | A P1 feature off for the outage |

Degraded modes that are counted, never silent (every one is a `measure_points` series and a digest line): editor `degraded`, `same_vendor_edit` (ADR-11), `relisten=skipped`, `timing_quality=sentence`, `failover.active`, `fallback_rules` (teacher), `evidence_quality in (partial, text_only)`, `analyst_validation_drop`, `move_violation` (with `kind = correction` listed on its own, because it is measure 27), `header_missing`, `end_reason in (fallback, pipeline_error, abandoned)`, `verbatim_failed`, `claims.retracted`, `privacy_audit_runs.verified=false`, `episodes.extra` paused by a spend mode (ADR-14), `release.override` (a deploy forced through the drop-window check with a reason).

## 6. Cost and performance against the budgets

**Fixed monthly cost of this domain (beta, 100 to 200 learners).**

| Item | Beta | At 10,000 learners | Note |
|---|---|---|---|
| Sentry (Team, EU) | $26 | about $80 | errors only, scrubbed |
| Better Stack (uptime + on-call with phone) | about $30 | about $100 | the one tool that calls a phone |
| CloudWatch Logs and alarms | about $15 | about $150 | 30-day retention; EMF metrics |
| Slack | $0 (free tier) | $0 | one channel |
| `eval-gate` runs, build weeks (prompt edits daily: the cheap half on every push is free, the paid half on `ready-for-review` and merge about 3 to 5 times a day × about $5) | about $300 to $500 a month during 2026-11-18 to 12-22 (skeptic review) | n/a | mostly `pipeline` and `host` suites; the two-halves rule in 4.3 is what keeps it at the low end |
| `eval-gate` runs, beta (3 to 5 version bumps a week × about $5 average) | about $80 | same | |
| Staging kept up through the beta (ADR-16) | about $180 | n/a (an ephemeral worker started by CI after the beta) | carried in 01 §6 and 10-decision-records §10 item 9; listed here because this domain is the reason it stays up |
| `eval/nightly` (10-fixture smoke, about $3) | about $90 | same | can drop to weekly after the build |
| `ops/canary` (2 vendors × 1 episode + 1 call, weekly) | about $5 | same | |
| `vendor/regress` (monthly, 30 clips × 4 recognizers + pronunciation) | about $2 | same | |
| `calibration/run` on bumps (assessment domain's cost) | about $5 | same | counted here because `eval-gate` triggers it |
| Reviewer and audit time | 10-decision-records §10 item 11 | | about 4 h/day at 100 learners for episodes alone, per target language; about 10 h/month of Muath's time for calls |
| **Total tooling and runs** | **about $250 to $300 a month in the beta; about $500 to $700 during the build weeks (eval-gate) plus $180 staging in both** | about $600 a month | |

Against the per-session number (PRD 14.5): none of this is in the session cost scope, which is generation and session roles plus "proof share and hosting". Spread over about 1,600 to 2,400 sessions a month at 100 learners (one to three episodes a day at the measured use of 45 to 60% of the allowance, ADR-05) it would be $0.10 to $0.19 a session of fixed overhead, falling to under $0.01 at 10,000 learners. The digest and the weekly cost report show it as a separate "fixed" line so it is never confused with the $0.60 budget or the $1.00 stop line. The security domain's $60 cap for its own fixed cost is a sibling line; the topology's "Sentry, Better Stack, Resend, domains about $60/month" overlaps the first three rows here, so the integrator should keep one of the two estimates (this one is itemized).

**Performance.** `ops/watch` runs about 45 queries every 5 minutes against indexed tables with recent-window predicates (`drops_late_systemic` is one index scan on `learner_schedule(next_drop_at)`); measured budget 5 s per run (alert if over 60 s, which would itself mean Postgres is in trouble). `measures/hourly` touches the events of the learners whose local day just closed (about 300 events per active learner-day; at 500 learners spread over 24 timezones that is about 20 learner-days an hour, under 10 seconds; if the cohort clusters in a few timezones, the busiest hour is still under 2 minutes) and the stores; a 28-day recompute of all measures under 20 minutes. Nothing in this domain runs in a learner's request path or in a call. The `/admin` pages read through `forone_admin` with `statement_timeout = 10 s` so an expensive ad hoc query cannot stall the API (ADR-17).

**Levers this domain provides toward $0.35:** the measured cost per session by role, by plan and by lever (the weekly report, with `extra.top10` and `extra.by_plan`), the `host` suite that makes the Haiku-host switch a measured human decision (ADR-14), the `tts.batch` and `episodes.extra` flags that make the cheaper modes reversible, `plan_mix` and `blended_margin` next to the break-even per plan so the price question in 10-decision-records §10 item 4 is answered with measured numbers, and `cache_hit_low`, which protects the single largest silent cost leak (an uncached prefix costs about $0.03 a session, pipeline domain 6).

## 7. Build plan for 2026-11-18 to 2026-12-22

The rule for this domain: it ships inside the other domains' weeks, on top of what they build, and never costs more than about one engineer-week in total before 2026-12-22. P0 here means "the beta cannot be run safely without it"; the offline suite is P1 by the PRD, but its fixtures and the cheap code-only checks land early because the Milestone 0 data is free and the build itself needs them. Dates follow ADR-07 (every first-draft date moved 16 days) and the cross-domain items of 10-decision-records §7 that belong to this document are placed in their weeks.

| Week | Dates | Ships (this domain) | P0 / P1 | What the Milestone 0 data lets us test |
|---|---|---|---|---|
| 0 (Milestone 0, in parallel) | 11-01 to 11-17 | `vendor-lab gate --target en` on the pilot's clips and scripts (ADR-03): the `recognizers` run by 11-10 and the `voices-blind` run by 11-17 are the gate's checks 1 and 2 and this domain's first baselines; `vendors.yaml` committed by 11-17 | P0 | The 30 clips produce the 10.14 result and the first `error_survival_rate` baseline |
| 1 | 11-18 to 11-24 | `forone.ops` skeleton: structlog JSON logger with `logscrub`, `vendor_error()` and the `pii_corpus` test (with the two recorded vendor 400s); Sentry wired in all services with scrubbing; Better Stack account, uptime checks on staging, one heartbeat; `#forone-ops`; `ops.page()` with Slack only; `tools/import_m0.py` writes the fixtures listed in 4.2 (learner files, scripts with hand coverage, editor reads, transcripts and tags, 30 clips, facts, Salma's lines, similarity pairs); `eval/suites.yaml` with `fitter`, `law_scan` (with the correction-guard phrases from 07's `guard/correction_words.yaml`), `claim_gate` (code-only suites) and the `recognizers` suite wrapping `tools/call-bench recognizers`; `packages/languages/en/versions.yaml` and `packages/native/ar/versions.yaml` v1 (10-decision-records §7 week 1: logging and paging skeleton) | P0 (logging, paging, fixtures), P1 (suite harness) | The 20 hand-checked scripts are the fitter's regression; the law corpus is seeded from Muath's step-8 catches, the bible's BANNED list and the explicit corrections among the pilot's retired notes |
| 2 | 11-25 to 12-01 | `eval_runs` table and `tools/eval run --target en`; suites `editor` (check 10 widened to corrections), `writer`, `pipeline` (10 fixtures), `memory`; `eval-gate` CI job with the per-package path map and the two halves (cheap on every push, paid on `ready-for-review`); **staging comes up and stays up** (ADR-16); the first baselines on `main` from the Milestone 0 fixtures; `release_manifest` and `tools/release cut`; `ops/alerts.yaml` v1 with the pipeline rules (`drops_late_systemic`, `episode_not_ready_before_drop` as P2, `fallback_3_in_7`, `editor_degraded_share`, `fallback_rate_day`, `voice_failover_active`, `canary_failed`) and `ops/watch`; `ops/canary` weekly on the synthetic learner; `feature_flags` table and `flag()`; Langfuse metadata-only wiring with the research pseudonym, checked by this domain's `inngest_payloads`-style test on the middleware (ADR-09) | P0 (alerts for the pipeline, release tooling, flags), P1 (suites) | Every Milestone 0 package through the Gemini editor against Muath's reads gives `editor_agreement_with_human`; the 15 learner files through teacher-to-editor give `editor_pass_first_try`, `fallback_rate` and cost per step; scripts judged "too alike" set `similarity_cosine` (Part 18 #10) |
| 3 | 12-02 to 12-08 | `forone.measures` v1 with measures 3, 4, 10, 11, 13, 14, 18, 22 (the ones the onboarding, player and word sheet produce) as `measures/hourly` over learner-local days, and `measure_points` with `cohort_key`; `/admin/measures` (tables, 28-day sparklines) on `forone_admin` (ADR-17); client-budget alert rules (`first_sound_slow`, `dropped_start_slow`, `word_sheet_slow`, `on_demand_slow` including the `daily_extra` path); the device test matrix runbook for the client domain's week-3 test; Better Stack on prod hostnames; `plan_mix` from `subscriptions.plan` as soon as the plans scaffold exists (10-decision-records §7 week 3) | P0 (measures from day one, PRD 16.2) | The 15 pilot word checks and reactions give the first `followed_vs_predicted` reading against the fitter's prediction |
| 4 | 12-09 to 12-15 | Call rules (`host_reply_*`, `call_connect_p95`, `talkback_p50`, `governor_violations`, `chat_opener_late`); `host` suite: governor replay on Milestone 0 transcripts (free), the real-audio replay of the Milestone 0 calls, and the simulated caller on 20 scripted calls through `call-bench` on staging; `explicit_corrections_per_100_turns` from the correction guard that lands in the worker this week (ADR-06); the `calls_50` suite as a named run (the 50-call run on the English stack, 10-decision-records §7 week 4); `injection` suite with the security domain's 30 cases; `salma` suite; `call_review_items` and the calls review page (owner only); measures 12, 19, 23, 27 | P0 (call alerts, `calls_50`, measure 27), P1 (simulated caller) | Milestone 0 call audio is the real-audio caller; Muath's tags on the same calls make `recast_rate_on_planted_real_audio` and `clarification_rate_on_planted_real_audio` computable before any live beta call, and the retired notes make the correction guard's first false-negative test |
| 5 | 12-16 to 12-22 | `analyst` suite calling `calibration/run`; the cost rules (`session_cost_over_1`, `cost_p50_7d_over_080`, `cost_runaway`, `cost_stop_line`, `cost_guard_soft`, `cache_hit_low`) on 08's `session_costs` table with `plan`; privacy and crisis rules (`privacy_promise_missed` with `privacy/verify` hourly, `crisis_activation`), `wrong_memory_*`, `claims_retracted`; **the binding deploy window in `tools/release deploy`** (ADR-16); `review/sample` and `/admin/review/episodes` with the reviewer role; `claims/audit-sample` and `/admin/review/claims`; `/admin/gates` with readable-from dates, `renewal_m2` over every paid learner, `plan_mix` and `blended_margin`; `/admin/alerts`, `/admin/incidents`, `/admin/flags`; the twelve runbooks in `ops/runbooks/`; the two admin actions (`pull`, `rerun-after-pass`); `ops/oncall.yaml` and the Better Stack schedule with phone escalation at any hour; `ops/digest` at 06:00 UTC; the first-working-hour checklist; a 60-minute tabletop with the security domain's incident drill (R3 systemic, R4 pull, R12 wrong memory, R1 failover by hand); measures 1, 2, 5 to 9, 15 to 17, 20 to 26, 28, 29; the end-to-end run with the Milestone 0 learners on prod with every rule live, under a consent that covers it (10-decision-records §10 item 13); the measured cost per session by plan for the exit document (ADR-07) | P0 | The end-to-end run on prod is the first real `cost_per_session` reading for the 2026-12-22 exit criterion and the first live after-pass timings; the Milestone 0 week-0 and week-3 recordings seed `test_retest_pairs` so `/admin/gates` can show how many metrics have `n_pairs ≥ 12` |
| Freeze | 12-21 12:00 to 12-24 12:00 UTC | `tools/release` refuses; only a hotfix with a reason row | | |
| Beta (P1) | 12-23 to 2027-01-26 | Full synthetic learner set (50) and the full `pipeline` suite on every bump; `pronunciation` suite; `eval/nightly` moved to weekly if cost matters; the gate moves to the real-audio recast number once 20 replays exist; `vendor/regress` first run 2027-01-01; the first false-claim audit 2027-01-01 and the extra sample 2027-01-19; the Gemini doubling in the 2027-01-04 cost report; the first rater window boundary 2027-01-20; the gate-review snapshot 2027-01-26; Metabase only if the admin tables are not enough; after the beta, the `host` suite moves to an ephemeral worker started by CI and staging goes back to being stopped between runs | P1 | |

## 8. Alternatives rejected

| Alternative | Why not |
|---|---|
| Datadog, Grafana Cloud or New Relic for product metrics | A new processor under every regime in 07 §4.9, holding learner ids and event names for numbers the event log already holds; monthly cost above the whole domain's budget; the team would spend the build week learning a query language instead of writing SQL it already writes |
| Prometheus and an OpenTelemetry collector on Fargate | Two more containers to run and a scrape model that fits long-lived services, not Inngest steps; EMF lines give the few service counters for free |
| A log SaaS (Better Stack Logs, Axiom, Loki) | Learner text could leak into a third processor; CloudWatch is already there and the scrubber makes it safe |
| PagerDuty or Opsgenie | Price and ceremony for a two-person rota; Better Stack's on-call does phone escalation for a tenth of the price and is already the uptime tool |
| LaunchDarkly or Statsig for flags | A processor, a SDK in four services, per-seat pricing; a table with a 60 s cache is 60 lines of code and audited |
| A separate eval product (Braintrust, Langfuse evals, Promptfoo as the harness) | Langfuse's evals would tie prompt regression to a processor the security domain may yet refuse; Promptfoo is fine for single prompts but the suite's unit is a learner fixture through several steps with code checks in between; a small Python package with pytest-style checks is what the team can extend |
| LLM-as-judge for the law scan | Law 1 needs recall 1.0 on a finite word list; a judge adds cost and variance where a scanner is exact; the editor model still judges the semantic half (check 10's "guilt", "unsolicited correction") |
| Reviewing calls by listening to audio | Needs break-glass access per call and a reason; transcripts with timings and the governor header show the move contract better and keep audio access rare |
| A learner-facing status page | The product's answer to an outage is its fallbacks and silence; a status page is another surface to keep law-clean and another thing the three-message rule does not allow linking to |
| Continuous deploy to prod | A prompt regression that passed `eval-gate` on variance would reach somebody's drop within the hour, because some learner's drop is always within the hour; a tag plus a canary costs ten minutes |
| A fixed release window and a protected hour in one timezone (the first draft) | Learners are anywhere (decisions.md §1), so no hour of day is outside every drop; the window must be computed from `learner_schedule` and must be binding, not a warning (ADR-16) |
| Paging per learner when an episode is late, as P1 | At 250 learners spread over the clock a slow vendor night is a page every few minutes all night, and the page tells the engineer nothing the pipeline's own escalation is not already doing; the systemic rule (3 or more learners, or 5%) is what a human can act on (ADR-16) |
| Paging the cost stop line | A seven-day mean is a trend and a business decision with a 48-hour window (08 §4.5.3); this document's own rule says a two-person team is never paged for a trend; only runaway spend pages (D15) |
| Automatic model downgrade when spend is high (08's first-draft `conserve`) | A quality change is a human decision after `eval-gate`, not an alarm's; a spend mode may change only what no learner hears (ADR-14) |
| Gating law 7 on the governor's counters or on synthetic callers alone | The counters say what the host declared; a TTS voice reads a planted error cleanly; the real-audio replay and the call review are the evidence (D14) |
| Keeping Salma's notes behind a flag | A flag never changes a law (D8); the correction guard would need a hole (ADR-06) |
| Sampling traces or logs in the beta | The beta is where every call is evidence for the gates; 100% is affordable at this size |
| Grafana with a read replica or an SSH tunnel | A replica is $100 a month for dashboards; a tunnel is one more credential; revisit with Metabase on Fargate at about 1,000 learners when the admin tables stop being readable |

## 9. Assumptions about other domains

Each is an [ASSUMPTION] for the integrator to check, except where marked "ruled", which means 10-decision-records settled it and this document now relies on it.

1. **System topology (01).** `ops.page()` is the interface its paging hooks call; `vendor/health` writes `vendor_health {capability, vendor, state, no_secondary}` keyed by target language where the capability depends on it (ADR-03), as this document's rules read it; `outbox` exists with an unsent count; `FORONE_FAKE_VENDORS=1` recorded-fixture adapters exist for every adapter; `tools/call-bench` is the one load and latency tool (ruled, ADR-19; `tools/load-call` is gone); the synthetic learners seeded in its week 2 are the canary's learners; the deploy workflows accept a canary step and the rollback to the last `canary_passed` digest; `tools/release deploy` can read `learner_schedule` from CI to compute the binding window and `call-worker`'s `active_jobs` to drain (ADR-16, 01 §4.4 #7); `day/next` creates up to `plan.episodes_per_day` episode rows and `POST /v1/episodes/next` exists (ADR-05); staging stays up from build week 2 (ruled, ADR-16; about $180 a month in its §6); `episodes.state` is the lifecycle column (ruled, ADR-19; this document used `status` in the first draft); the `/admin` pages are `sqladmin` plus a few custom routes in `api` running as `forone_admin` (ADR-17) and this domain adds its pages there; `HOME_REGION` is one config key (`eu-central-1` by default, ADR-08) and CloudWatch and Sentry EU sit in or beside it.
2. **Episode generation pipeline (02).** `review_items` and `review_findings` have the shape in its 4.x and its nightly sampling rule moves into `review/sample` here (one job, not two); `pipeline.human_page` carries `reason` and `count_7d`; the degraded flags (`degraded`, `same_vendor_edit`, `timing_quality`, `relisten`, `fallback_rules`, `failover`) are on the artifact so the measures can count them; the `why` artifact carries `predicted` coverage for measure 11; `pipeline_steps` carries `prompt_version`, `pricing_mode`, `cached_input_tokens` and keeps the step artifacts (the prompts and completions this domain reads when debugging, ADR-09); `episode_kind = daily_extra` is produced through the on-demand path and carries `session_id` for attribution (ADR-05); the editor's check 10 is widened to "nothing reads as a correction or a lesson" (ADR-06) and its fallback is Opus with `same_vendor_edit`, never code checks only (ADR-11); its `fixtures/learners/*.json` is the same file set as `eval/fixtures/learners/` (one location, the pipeline's name wins); prompts load from `packages/languages/<target>/prompts/` (ADR-02); `price_book` (02) and `prices.yaml` (01, 03) are one price source under the cost domain; a pull of an episode (`episode.pulled`) is honoured by `feed.publish` (410 on the enclosure) and by a fallback `episode/produce` run at standard pricing.
3. **Live call and voice stack (03).** `calls.metrics` carries `reply_latency_p50_ms`, `reply_latency_p95_ms`, `connect_ms`, `talkback_ms[]`, `learner_speech_ms`, `host_speech_ms`, `moves{...violations, kinds[]}` with `kind = correction` for a correction-guard block (ADR-06), `anxiety_mode`, `end_reason`; the host brief's `recasts` field (the teacher's echo plan) is recorded per call so measure 28 can match recasts to later uses; `tools/call-bench` accepts scripted caller profiles from `eval/fixtures/callers/` and recorded real-audio callers from `eval/fixtures/recordings/m0_calls/`, and writes `bench/reports/`; `call_turn_verbatim` is the second event appended by `workflows` through `events.append()` (ruled, ADR-19); `talkback_stt.languages = [native, target]` per call (ADR-02); `feed_to_call_ms` is logged as `client_perf`; `crisis_activation` events and `crisis.activated` exist as the security domain describes; Deepgram becomes a hot streaming secondary in P1 (until then, recognizer outage means voice notes); the `say_it_once_offered` event is emitted when the affordance is shown (for measure 13).
4. **Learner model, event log and data platform (04).** `events` with the types in PRD 8.2 plus the client's four and `followed_answer`, `fact_card_viewed`, `claim_shown`, `pmf_answer` [new, this document], `say_it_once_offered` [new, this document, emitted by 03 or 06]; `sessions` with `state`, `started_at`, `episode_id`; `day.became_active`; `learner_schedule.next_drop_at` and `learner_schedule.expects_drop` (ruled, ADR-19: set when the learner's previous local day was active; this document consumes it in `drops_late_systemic` and the release window); `word_uses(learner_id, unit_id, event_id, occurred_at, clean, correct, prompted, quote)` written by 05 (ruled, ADR-19) and `structure_observations`, both with `clean`, `correct`, `prompted`, `occurred_at`; `word_bank.targeted_first_at` and `structure_map.first_targeted_at` (or the teacher's targeting history exposed another way) for delayed recall; `show_canon.kind='callback_made'` and `learners.wrong_memory_n` for measure 20; `learners.{native_language, target_language, residence_country, plan, tz}` and `learners.cohort_key = invite_date` (ruled, ADR-02, ADR-19; `cohort_monday` is gone); `research_pseudonyms(learner_id, pseudonym)` deleted with the learner (ADR-09); `learner.rebuild_requested` is sent from this domain's `/admin` button; `measure_points` learner-scope rows are purged by `learner/delete`; its service metrics (`events_appended_total`, `facts_rejected_total`, `voice_objects_overdue`, and the rest) are EMF lines this domain's dashboards read; `retention/daily` runs per learner-local midnight (ADR-16).
5. **Assessment engine, after-session pass and the claim gate (05).** `claims` with `status in (candidate, passed, shown, retracted)`, `kind`, `shown_at`, `assessment_version`, `sem`; `claim_evidence` openable by claim id; `metric_calibration.n_pairs`; `test_retest_pairs` seeded from Milestone 0; `calibration/run` is callable from CI per target language and returns pass/fail with `qwk_band` and `precision_claim_tags`; `calibration_samples` holds the Milestone 0 tags under `tags_a`; `rater_versions` and `pinned_until` as its D12 (windows from 2026-12-23); `recording_ratings` and `structure_map.stable_confirmed_at` for measures 9 and 26; `session/after-pass` is one function with the 10-minute budget and `session_summaries.completed_at` and `evidence_quality` (ADR-06; the `notes` table, `notes.created_at` and `notes.degraded` no longer exist); `apply_after_pass` writes `word_uses` (ADR-19); `proofs.sessions_in_week` is computed, not stored (ruled, ADR-19; measure 22 counts sessions itself); `salma_explain` is Salma's on-demand explanation prompt in the native package (ADR-06); `claims.retracted` and `notice_pending`; its own kill switch honours `claims.kind.<kind>` flags.
6. **Client app, podcast feed and delivery (06).** `app_open {entry, standalone, drop_delta_min}`, `client_perf {kind, value, context}` with the kinds it lists, including `first_sentence_ms` (the first spoken sentence in the target language; `first_english_ms` in the first drafts), `pwa_install`, `push_permission`; `followed_answer` on some episodes; a once-only `pmf_answer` question rendered in the week-4 proof's question slot [new] with its wording in `packages/native/<lang>/strings`; the "next one" control calls `POST /v1/episodes/next` and hides when `episodes.extra` is off (ADR-05); the plan picker writes `subscriptions.plan` (ADR-04); `waitlist.source` and `invites` carry referral provenance and `invite_date`; the feed's health item `api.forone.app/f/health.xml` exists for Better Stack; Sentry browser SDK with its scrubbing; `feed_fetches` by `ua_family` for the Part 18 #11 weekly report; the Salma line on Today for a pulled episode is a `TodayDoc` field it renders from the native package's `episode_pulled` string; `dir` and `lang` come from the native package (ADR-02).
7. **Security, privacy, consent and compliance (07).** `staff_accounts` roles `owner`, `engineer`, `reviewer`, `tagger`, `ops` with `languages` per account and the per-role page matrix in 4.5.4; `audit_log` rows for every admin page read of learner content and every flag flip, written by the pages running as `forone_admin`; `forone_human` is the psql role under pgaudit (ADR-17); `privacy/verify` runs hourly over the last 25 hours against `expires_at` and emits `privacy.audit_failed` and `privacy_audit_runs` (ADR-16); `cost_guard.tripped {level: soft | hard}` (ADR-15); `security_incidents` linked from `incidents.security_incident_id`; `guard/law_words.yaml` and `guard/correction_words.yaml` per language package as the scanners the law corpus tests, and `guard.check_output` item 6 (the correction guard) counts its blocks into `moves.violations` with `kind = correction` (ADR-06); the 30-case injection set at `eval/fixtures/injection/`; `research/anonymize` for anything a `tagger` reads and for the real-audio replays; the Milestone 0 consent covers de-identified fixtures (10-decision-records §10 item 13); the policy that no vendor error body is logged is its (this document implements it in 4.9); Sentry EU and CloudWatch in the home region are approved processors under its regime table (ADR-20); the Langfuse rule is ADR-09's; the incident runbook and tabletop are shared with this domain's week-5 drill.
8. **Cost model, vendor strategy and tracing (08).** `vendor_calls {learner_id, session_id, episode_id, call_id, role, vendor, model, cost_usd, input_tokens, cached_input_tokens, latency_ms, trace_id, occurred_at}` written in its own transaction (ADR-13); `session_costs` is a table filled by `cost/rollup` with `plan` (ruled, 10-decision-records §4; this document called it a view in the first draft); the weekly cost report by role, vendor, plan and learner, with "Margin by plan", `plan_mix` and `blended_margin` (ADR-15), is produced there and read in the Tuesday review here; `cost_reports.plan_text` and `plan_by` carry the stop line's 48-hour plan (08 §4.5.3); the Langfuse conventions (`user_id` = research pseudonym, metadata only unless `data_use`; ADR-09) are theirs; `prices.yaml`/`price_book` has the dated 2027-01-01 row; the adapter middleware exposes a cache-hit ratio per role for `cache_hit_low`; the per-plan cost guard (2.5 × and 4 × `episodes_per_day` × budget) emits `cost_guard.tripped` with `level`, and the daily spend cap Σ `episodes_per_day × $1.00` is computable from `plans.yaml` (`plans.key`, `plans.episodes_per_day`) and `learners.plan` for `daily_spend_100` (ADR-15); spend modes never switch a model (ADR-14); the vendor adapters surface errors as typed exceptions with `error_class`, `http_status` and `vendor_request_id` so that `vendor_error()` never needs the body.

## 10. Open for Muath

Items that 10-decision-records §10 now owns are one line each and point there (ADR-22); items specific to this document stay in full.

1. **[OPEN for Muath] On-call for a worldwide cohort.** See 10-decision-records §10 item 7: accept that a one-engineer rota answers overnight P1s with the product's fallbacks and a human at the next working hour, or fund a second responder; and approve Better Stack's on-call plan (about $30 a month).
2. **[OPEN for Muath] The paid reviewer, the claims auditor and the native-language law-scan reader.** See 10-decision-records §10 item 11 (a native reader per target language, about 4 hours a day at 100 learners, less with the cut in section 7, who also performs the language gate's writing check; the claims auditor; Muath for the Arabic law-scan file in the beta). Specific to this document: whether the reviewer may file ban proposals directly or only propose, and that the call review costs about 10 hours of Muath's time a month at 100 learners (4.5.2).
3. **[OPEN for Muath] The "very disappointed" question.** PRD 16.1 names the metric but not the ask. Proposed: one in-app question in the week-4 proof's slot (replacing the worth-it question that week), three answers, never by email; the wording is a string in `packages/native/<lang>/strings`, so one approval per native language. Approve the mechanism and the wording, or drop the gate for the beta. (10-decision-records §10 item 15 leaves this with this document.)
4. **[OPEN for Muath] Pulling a shipped episode.** Section 4.8 R4 adds an admin action that replaces a law-breaking episode and has Salma say one plain line on Today in the learner's native language. It is new (not in PRD-v2). Veto or confirm, and confirm the line's wording per native language (the Arabic and English lines are in R4). (10-decision-records §10 item 15 leaves this with this document.)
5. **[OPEN for Muath] The stop line's owner and window.** PRD 14.5 says over $1.00 a session with no costed plan is a stop. This document makes it `cost_stop_line`, a P3 with a ticket to Muath, never a page (D15), and 08 §4.5.3 gives 48 hours to record a plan in `cost_reports`. Confirm that a human decides and that 48 hours is the window. (10-decision-records §10 item 15 leaves this with 08 and this document.)
6. **[OPEN for Muath] Milestone 0 fixtures and consent.** See 10-decision-records §10 item 13. Specific to this document: the real-audio replays of the Milestone 0 calls (4.2) are the law-7 gate's evidence, so if the consent does not cover them the gate stays on the synthetic upper bound until 20 beta learners with `data_use = true` have been replayed.
7. **[OPEN for Muath] Budget for this domain.** See 10-decision-records §10 item 9 (the fixed infrastructure budget, including staging kept up through the beta, ADR-16). Specific to this document: about $250 to $300 a month in tools and suite runs during the beta and $500 to $700 during the build weeks (section 6); the nightly smoke is the first $90 to go, the paid half of `eval-gate` on every merge the next.
8. **[OPEN for Muath] The invite weekday.** The beta opens on Wednesday 2026-12-23 and ADR-07 makes the invite cadence weekly on that weekday (`cohort_key = invite_date`). The alternative is a Monday 12-28 first cohort, which loses five beta days before the gate review. Confirm Wednesdays.

## 11. Revision log (2026-11-06)

- conformance blocker "one timezone and one commute" → §1 D1, D4, D9, D11; §3.1 (`measures/hourly`, digest 06:00 UTC); §3.2 flow 2; §4.3 release rules (binding computed window, override reason row, `call-worker` drain); §4.6 severities; §4.10 rewritten in UTC with hourly jobs; §4.11 (`protected_hours: none`, the honest statement); §5 and §8 rows; "protected hour" replaced everywhere by "a drop within 45 minutes" (ADR-16).
- conformance major "notes measures, suite, rule, flag; law 7 unmeasured" → §4.1 measure 13 redefined (`say_it_once_offered` denominator), measures 27 `explicit_corrections_per_100_turns` and 28 `echo_uptake_share` added, D14; §4.2 `notes` suite replaced by `salma`, fixtures row replaced, law corpus gains the correction guard; §4.3 path map rows; §4.6 `notes_late` and the "Notes under 90 s" budget removed; §4.7 `notes.enabled` removed; R2, R9 rewritten; §5 `notes.degraded` removed (ADR-06).
- conformance major "founding year, renewal, plan mix, margin" → §4.4 `trial_to_paid` on all plans, `renewal_m2` over every paid learner with the honest readable date (after the gate review), `plan_mix` and `blended_margin` as reported lines; measure 29; D13; old §10 item 5 removed (ADR-04, ADR-15).
- conformance major "one language pair throughout" → §4.3 versions per package (`packages/languages/<target>/versions.yaml`, `packages/native/<lang>/versions.yaml`; path map keyed on the package directory); §4.2 corpus and injection set per language, synthetic learners per target; measure 17 per native and target language from day one; §4.5 reviewers per target language (`staff_accounts.languages`), the Arabic law-scan reader is Muath; §4.1 and §4.9 copy and PII corpus per language (ADR-02, ADR-03).
- conformance major "dates" → §1 D9, D13; §4.3 freezes; §4.4 readable dates; §4.7 defaults on 12-23 and `finale` 2027-01-19; §4.10 dated rows; §7 re-dated and renamed; invite cadence Wednesdays, `cohort_key = invite_date` (ADR-07, ADR-19).
- conformance major "`word_uses` and `proofs.sessions_in_week`" → §4.1 `word_uses` ruled as 04's table written by 05 (assumption removed), measure 22 SQL computes sessions in the proof week; §9 items 4 and 5 (ADR-19).
- conformance minor "copy per native package" → §4.4 `pmf_answer` wording and R4's line reference `packages/native/<lang>/strings`.
- conformance minor "`episodes.status`" → `episodes.state` in §4.6 (both rules and the budget table), R3, R4, §9 item 1 (ADR-19).
- skeptic blocker "per-learner P1 at drop minus 45" → §4.6 `episode_not_ready_before_drop` is P2 with dedupe per learner; new P1 `drops_late_systemic` at 3 or more learners or 5% of due drops; `expects_drop` consumed as 04's column; R3 rewritten around the two rules; D11; §7 week 2 (ADR-16).
- skeptic major "staging off versus eval-gate nightly" → staging stays up from build week 2 through the beta (D6, §4.3 release paragraph, §4.10 dated row 11-25, §5 row, §6 row of about $180, §7 week 2 and beta row); after the beta an ephemeral worker (ADR-16).
- skeptic major "stop line paged as P1" → the rule is split: `cost_runaway` P1 (hard guard and `daily_spend_100`) and `cost_stop_line` P3 with the ticket and 08 §4.5.3's 48-hour window; `cost_guard_soft` P3 added; D15; R8; §4.6.1; §8 row; §10 item 5 (the contradiction between D11 "never paged for a trend" and the first draft's rule is resolved in favour of D11).
- skeptic major "vendor error bodies in logs" → §4.9: only error class, HTTP status and vendor request id are logged; `logscrub.vendor_error()`; `message` added to the refused field names; the Sentry hook strips response bodies; `pii_corpus.jsonl` gains a recorded Anthropic 400 and Google 400 with an embedded learner sentence; D5; §7 week 1. 07 owns the policy, this document the implementation (§9 item 7).
- skeptic major "synthetic callers flatter the host" → §4.2 "why the synthetic number is an upper bound": `recast_rate_on_planted` and `clarification_rate_on_planted` reported as `_synthetic` (upper bound) and `_real_audio`; the gate moves to the real-audio number once 20 replays exist; `thresholds.yaml` `gate_until` / `gate_from`; D14; §7 week 4 and beta row.
- skeptic major "review volume with 2 and 3 a day plans" → §4.5.1 keeps 10 random per learner per month plus every flagged item, says the sampled share falls on the upper plans, prints the share in the monthly summary; D10.
- skeptic major "`eval-gate` cost during the build" → §4.3 two halves (cheap on every push, paid on `ready-for-review` and merge); §6 build-period row of $300 to $500; §2 budgets paragraph.
- skeptic minor "call review hours" → §4.5.2 1 call per learner per month plus all flagged calls, about 10 hours of Muath's time a month stated; D10; §10 item 2.
- skeptic minor "revision minus one" → §4.3 rollback to the last `release_manifest` row with `canary_passed = true`; D9; R3.
- skeptic minor "`cohort_monday`" → `cohort_key = invite_date` in §4.1 (grain, DDL comment, SQL 8), §4.4, §4.10, §9 item 4; §10 item 8 asks Muath to confirm Wednesdays (ADR-07, ADR-19).
- ADR-02 → package paths `packages/languages/<target>/` and `packages/native/<lang>/` throughout (§1 D7, §3.2, §4.2, §4.3, §4.9, §9); `learners.{native_language, target_language, residence_country, plan, tz}`; English and Arabic kept only as the pilot's instances of the general rule.
- ADR-03 → §4.10 and §7 week 0: `vendor-lab gate --target en`, the `recognizers` and `voices-blind` suites as the gate's regression form, `gate:` date in the target package's `versions.yaml`.
- ADR-04 / ADR-05 → three plans in `trial_to_paid`, `renewal_m2`, measure 29, `extra.by_plan`; `daily_extra` in measure 22, `on_demand_slow`, §4.6.1, the `episodes.extra` flag; `POST /v1/episodes/next` in §4.6.1 and §9.
- ADR-06 → see the conformance major above; also the editor mutation "one line that reads as a correction", `salma_explain` and the `salma.explain` flag, R9 as one-stage after-pass, D8's rule that the correction guard has no flag.
- ADR-07 → all dates; §7 heading and table; §4.10.
- ADR-08 → §9 item 1 (`HOME_REGION` default `eu-central-1`, one config key).
- ADR-09 → §4.9 Langfuse row (metadata only, `user_id` = research pseudonym, text only for `data_use` learners after `anonymize()`); the tracing chain reads prompts from the home region; §9 items 4 and 8.
- ADR-11 → `pipeline.editor_model` flag redefined (Opus fallback flagged `same_vendor_edit`, never code checks only); R1 and R3; `same_vendor_edit` counted as a degraded mode and queued for review.
- ADR-13 → §9 item 8 (`vendor_calls` in its own transaction, `occurred_at`).
- ADR-14 → §1 D8; §4.6 severities ("no alert changes what a learner hears"); §4.7 flag table (`host.model=haiku`, `teacher.model=sonnet` human-only; `tts.batch`, `episodes.extra` allowed to a spend mode); R8 levers in two groups; §8 row.
- ADR-15 → per-plan guard levels in R8 and `cost_runaway`; `daily_spend_100` formula; `plan_mix`, `blended_margin` (measure 29, §4.4, §4.10, §6 levers).
- ADR-16 → see the conformance blocker and skeptic blocker above; `privacy/verify` hourly against `expires_at` and `retention/daily` per learner-local midnight (§4.10, §9 items 4 and 7); heartbeat monitors renamed.
- ADR-17 → `/admin` pages on `forone_admin` without pgaudit, `forone_human` for psql (§1 D2, §3.1, §4.5.4, §6, §7 week 3, §9 items 1 and 7).
- ADR-19 → `episodes.state`, `call_turn_verbatim` (measure 17, R2, §9 item 3), `word_uses`, `learner_schedule.expects_drop`, `tools/call-bench` (§9 item 1), `cohort_key = invite_date`, `proofs.sessions_in_week` computed, `session_costs` as a table.
- ADR-20 → §9 items 1 and 7 (regime table, processors approved per regime); "PDPL" replaced by "every regime in 07 §4.9" in §1, §7 and §8; `crisis_resources` per ISO country in the native package's `versions.yaml`.
- ADR-21 → §4.10 dated row 12-02 (processor decision) pointing to 10-decision-records §10 item 3.
- ADR-22 → §10 reduced to one line each for items the register owns (on-call, reviewers, consent, budget); items specific to this document kept in full; old item 5 (founding renewal) removed as settled by ADR-04; old item 7 (stop line) kept because §10 item 15 of the register leaves it with 08 and 09.
- Front matter rewritten; §2 gained rows for law 7 and for the 2026-10-23 decisions; §11 added.
- Not applied: nothing was declined. Two fixes were applied in the ADR's form rather than the review's: the conformance blocker's "digest and reports at fixed UTC times" and the skeptic blocker's P1 threshold follow ADR-16's wording (06:00 UTC digest; 3 or more learners or 5%), and the conformance major on languages uses ADR-02's two package kinds (`packages/languages/<target>/`, `packages/native/<lang>/`) rather than the review's `packages/lang/<target>/`. One thing the skeptic's rollback fix implies but this document does not build: a `release_manifest` row per canary attempt, which 01's deploy workflow would have to write; it is listed in §9 item 1.
