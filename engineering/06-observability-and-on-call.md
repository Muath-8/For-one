# 06. Observability and on-call

Part of the For one engineering handbook. Written 2026-11-06 against architecture 09 (D1 to D13, §4.6 to §4.11) and 08 §4.3 to §4.5. The rule of this page: every signal is a row in Postgres, every alert is a SQL query with a runbook link, and nothing here is ever shown to a learner.

## 1. The tools, and what each holds

| Tool | Holds | Learner text? | Retention | Owner of the account |
|---|---|---|---|---|
| Postgres (`measure_points`, `vendor_calls`, `pipeline_steps`, `calls.metrics`, `alert_state`, `eval_runs`, `incidents`, `release_manifest`) | the facts about every run, call, cost and alert | no | the row's own rules | us |
| CloudWatch Logs and metrics | structured JSON logs from the four services, EMF counters, Fargate and RDS metrics, four dashboards | never | 30 days | AWS account |
| Langfuse Cloud (EU) | one trace per unit of work; metadata for every learner; prompt and completion text only for learners with `data_use = true`, names tokenized | only with opt-in | 30 days | Muath (cost domain) |
| Sentry (EU) | exceptions with scrubbed context; browser errors from `web` | never | 90 days | Muath |
| Better Stack | uptime checks on the public hostnames, heartbeats for the four crons that must never stop, the on-call schedule, phone escalation | never (ids only) | vendor default | Muath |
| `#forone-ops` Slack | alert titles with ids, deploy notes, canary results, nightly results | never | Slack default | Muath |
| `/admin/measures`, `/admin/gates`, `/admin/alerts`, `/admin/review`, `/admin/flags`, `/admin/incidents`, `/admin/privacy`, `/admin/vendors`, `/admin/costs` | server-rendered pages in `api` reading through `forone_readonly` | per role (handbook 09) | live | us |

No Datadog, no Grafana, no log SaaS: each would be one more processor holding learner ids for nothing the event log does not already hold.

## 2. Logs

One schema for all four services, emitted by `forone.ops.log` (structlog JSON) and scrubbed at the logger by `forone.ops.logscrub`:

```json
{"ts":"2026-12-09T04:41:12.318Z","level":"info","service":"workflows","env":"prod",
 "event":"step.completed","fn":"episode/produce","step":"editor","inngest_run_id":"01J...","trace_id":"a1b2...",
 "learner_id":"7f3c...","episode_id":"01JA...","session_id":null,"call_id":null,
 "learner_model_version":412,"prompt_version":"editor_rubric@1.1.0","vendor":"google","model":"gemini-3.8-flash",
 "latency_ms":4120,"cost_usd":0.0041,"outcome":"pass","degraded":false}
```

Allowed: every id, enums, counts, durations, costs, versions, vendor and step names, error classes, sanitized messages. Never: names, emails, phones, birth dates, any transcript or chat text, life facts or quotes, idea text, prompts, completions, feed tokens, OTP codes, keys. The scrubber drops any field classified as PII by `forone.learner.pii`, truncates strings over 200 characters, replaces typed-token patterns, and refuses any field named `text`, `quote`, `transcript`, `prompt`, `completion`, `content`, `body` (raises in dev, drops in prod with a counter). CI proves zero leaks over the PII corpus on every PR.

## 3. Traces

`trace_id` is minted by `api` per request and by `workflows` per Inngest run, carried as a scalar in every Inngest event's metadata, set on every adapter call, attached to every Sentry event and every Langfuse trace. A bad episode is followed as: `episodes.id` → `pipeline_runs.inngest_run_id` → the Langfuse trace → `pipeline_steps` (versions, cost) → `release_manifest` (what was deployed) → `learner_model_versions` (what the teacher read). The prompt and completion text for a learner without the opt-in is read from the learner's own rows by span id, under RLS, as an audited act (handbook 09 §4).

Sampling is 100% in the beta. At 10,000 learners Langfuse samples to 20% except calls in the assessment and claim path; logs stay at 100% because they hold no content.

## 4. The cost-per-session dashboard

`/admin/costs` is the page Muath opens every morning. It reads `vendor_calls` (one row per vendor call, priced from `price_book` at the time of the call) rolled up by `cost/rollup` into `session_costs` and `cost_reports`. Its definition of **cost per session** follows architecture 01 §6 and 08 D1: every vendor call attributable to the learner's day (the episode's production including rewrites and escalations, the call, re-transcription and pronunciation, Salma's notes and chat, the analyst and memory keeper, the proof share, the swap allowance), excluding fixed infrastructure, which is a separate line, and excluding sample episodes, pilots, canaries and vendor tests, which have their own kind ceilings.

What the page shows, top to bottom:

1. **The headline:** trailing 7-day mean cost per daily session against the $0.60 budget, the $0.80 warning and the $1.00 stop line, with the last 28 days as a line. The same number for the 2027-01-01 price book (what today would cost after the Gemini doubling), so the January jump is visible in December.
2. **Where the money went today:** a stacked bar by role (voice studio, call, teacher and writer, verbatim, notes and chat, after-session, proof, swap) and the same by vendor.
3. **The levers:** batch share of teacher and writer calls, cache hit rate per text role (alarm under 85%), escalation rate from batch (alarm over 20%), average episode minutes, average call minutes, host model in use, `spend_mode`.
4. **Distribution:** the ten most expensive sessions of the day with the reason column (`retry_storm`, `rewrite_loop`, `long_call`, `cache_miss`, `fallback_standard`) computed by the rollup, and a histogram.
5. **Today's spend** against the daily cap by environment and by kind (`sample`, `pilot`, `daily`), with the cap formula shown.
6. **Fixed cost** this month so far (AWS, Vercel, LiveKit, vendor minimums, pulled weekly from the billing APIs where they exist and entered by hand where they do not), divided by sessions, as its own line.
7. **Reconciliation:** last month's `vendor_calls` sum against each vendor's invoice, variance per vendor, alarm above 5%.

The weekly cost report (Monday 09:00 Riyadh, posted to Slack and stored in `cost_reports`) is the same page as a snapshot plus the stop-line plan text if one is open.

## 5. Alerts

`ops/alerts.yaml` holds every rule: a SQL predicate over the tables above, a window, a severity, a dedupe key and a runbook path. The Inngest cron `ops/watch` evaluates them every five minutes, writes `alert_state`, and calls `ops.page()` for P1 (Better Stack incident, phone), `ops.notify()` for P2 (Slack now) and the morning digest for P3. The cost alarms from architecture 08 §4.5 are rules in the same file.

The P1 families, the only ones that ring a phone:

| Family | Rule | Runbook |
|---|---|---|
| Drop at risk | an episode not `ready` at drop minus 45 min for any learner | R3 |
| Calls cannot run | streaming recognizer or both voice vendors degraded (5 failures in 10 min); LiveKit or `call-worker` unhealthy | R1, R2, R7 |
| Platform down | Better Stack uptime failure on `app.`, `api.`, or the feed; RDS failover; `outbox_growing` | R7 |
| Spend | daily spend over the cap (`halt`), a learner's day over the hard cost guard | R8 |
| Privacy | `privacy.audit_failed` for any window; a break-glass role assumption | R11, incident runbook |
| Crisis | `crisis.activated` (Slack to Muath at any hour; the in-product protocol has already run) | R10 |

P2 (Slack, within the day): latency budgets missed at p95, `fallback_3_in_7`, `notes_late`, cache hit rate low, vendor error rate over 5%, canary failed, `wrong_memory_rate`, reconciliation variance. P3 (digest at 08:30): everything else, including the nightly's findings.

Every alert links a runbook. A rule without a runbook path fails the `package` CI job.

## 6. Runbooks

Twelve one-page runbooks in `ops/runbooks/`, each with the same five headings: detect, first five minutes, fix, verify, tell the learner. They are summarised in architecture 09 §4.8 and are copied into the repo as the first ops task of build week 4, with these additions from this handbook:

- **R0 Handover** (`handover.md`): what the outgoing on-call writes on Tuesday at 12:00 Riyadh: open incidents, flags flipped this week, vendor state, anything degraded, the staging lock holder.
- **R13 Incident** (`incident.md`, from architecture 07 §4.15): the four severities, the `security_incidents` row, the 72-hour regulator clock, who speaks to whom. Rehearsed once in build week 5 as a tabletop.
- **R14 Deploy went wrong**: rollback with `tools/release rollback`, when a prompt version is the cause (revert the PR, cut again), when a migration is the cause (expand-then-contract means the old image still runs; if it does not, that is the incident).

The two admin actions runbooks rely on, both audited and idempotent: `pull episode` and `re-run after-pass`. Plus the `/admin/vendors` failover switch and the learner rebuild button. The on-call does not need SQL for any runbook step; if a runbook step needs SQL, the runbook gets an admin action instead.

## 7. On-call

From `ops/oncall.yaml` (architecture 09 §4.11), as policy:

- Weekly rotation, handover Tuesday 12:00 Riyadh. With two engineers, alternate weeks; with one, the engineer every week and Muath as primary on Fridays.
- Escalation to Muath after 15 minutes unacknowledged on P1.
- Protected hours 05:00 to 08:30 Riyadh: the drop window; a P1 is acknowledged within five minutes. Quiet hours 23:00 to 05:00: only a P1 can page.
- The 08:30 checklist every morning: `/admin/alerts` clear, every learner's drop published, yesterday's canary green, `/admin/costs` headline, `/admin/privacy` all windows green, the review queue depth, the nightly result.
- A weekly 30-minute ops review on Tuesdays: alerts fired, false positives to tune, flags flipped, cost trend, the review backlog.
- What the on-call never does alone: flip a vendor back from an understudy outside the release window, change a prompt version in prod, read learner audio without a reason row, send any message to a learner.
- What is accepted because the team is small: no second responder at night; a P2 found at 02:00 waits for 08:30; both voice vendors down at 03:00 means voice notes until morning.

Open for Muath (architecture 09 §10 #1): who is primary in the beta's first three days, whether Muath is the escalation at any hour, and whether the Better Stack on-call plan (about $30 a month) is in the budget.

## 8. Postmortems

Blameless, one page, within seven days, for: any P1, more than three learners late in one morning, any missed privacy window, any pulled episode, any wrong memory. Stored in `ops/postmortems/YYYY-MM-DD-<slug>.md` with the same headings every time (what happened, timeline, impact in learner terms, cause, what changes, what we got lucky on). Every postmortem produces at least one of: a fixture, an alert rule, a runbook change, or a test. A postmortem that produces only "be more careful" is sent back.

## 9. Feature flags and kill switches

`feature_flags` table, read with a 60-second cache, edited on `/admin/flags`, every change audited. Flags exist for P1 features, vendor levers and kill switches, never for a law. Every runbook's first fix is a flag or a vendor switch; a feature that ships without a kill switch is not done (handbook 10).
