# 06. Observability and operations

Part of the For one engineering handbook. Written 2026-11-06 against architecture 09 (D1 to D13, §4.6 to §4.11) and 08 §4.3 to §4.5; revised 2026-11-12 for ADR-25.2 (no on-call rota: fallbacks first, alerts to Muath, runbooks the agent runs when Muath asks). The rule of this page: every signal is a row in Postgres, every alert is a SQL query with a runbook link, and nothing here is ever shown to a learner.

## 1. The tools, and what each holds

| Tool | Holds | Learner text? | Retention | Account owner |
|---|---|---|---|---|
| Postgres (`measure_points`, `vendor_calls`, `pipeline_steps`, `calls.metrics`, `alert_state`, `eval_runs`, `incidents`, `release_manifest`) | the facts about every run, call, cost and alert | no | the row's own rules | us |
| CloudWatch Logs and metrics | structured JSON logs from the four services, EMF counters, Fargate and RDS metrics, four dashboards | never | 30 days | AWS account |
| Langfuse Cloud (EU) | one trace per unit of work; metadata for every learner; prompt and completion text only for learners with `data_use = true`, names tokenized | only with opt-in | 30 days | Muath |
| Sentry (EU) | exceptions with scrubbed context; browser errors from `web` | never | 90 days | Muath |
| Better Stack | uptime checks on the public hostnames, heartbeats for the four crons that must never stop, phone escalation to Muath for the P1 families | never (ids only) | vendor default | Muath |
| `#forone-ops` and `#forone-deploys` Slack | alert titles with ids, deploy notes, canary results, nightly results, the agent's release proposals | never | Slack default | Muath |
| `/admin/measures`, `/admin/gates`, `/admin/alerts`, `/admin/flags`, `/admin/incidents`, `/admin/privacy`, `/admin/vendors`, `/admin/costs` | server-rendered pages in `api` reading through `forone_readonly`, for Muath (`owner`) only | per page (handbook 09) | live | us |

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

`trace_id` is minted by `api` per request and by `workflows` per Inngest run, carried as a scalar in every Inngest event's metadata, set on every adapter call, attached to every Sentry event and every Langfuse trace. A bad episode is followed as: `episodes.id` → `pipeline_runs.inngest_run_id` → the Langfuse trace → `pipeline_steps` (versions, cost) → `release_manifest` (what was deployed) → `learner_model_versions` (what the teacher read). The prompt and completion text for a learner without the opt-in is read from the learner's own rows by span id, under RLS, as an audited act by Muath only (handbook 09 §4).

Sampling is 100% at launch. At 10,000 learners Langfuse samples to 20% except calls in the assessment and claim path; logs stay at 100% because they hold no content.

## 4. The cost-per-session dashboard

`/admin/costs` is the page Muath opens every morning. It reads `vendor_calls` (one row per vendor call, priced from `price_book` at the time of the call) rolled up by `cost/rollup` into `session_costs` and `cost_reports`. Its definition of **cost per session** follows architecture 01 §6 and 08 D1: every vendor call attributable to the learner's day (the episode's production including rewrites and escalations, the call, re-transcription and pronunciation, Salma (when asked) and chat, the analyst and memory keeper, the proof share, the swap allowance), excluding fixed infrastructure, which is a separate line, and excluding sample episodes, first episodes, canaries and vendor tests, which have their own kind ceilings.

What the page shows, top to bottom:

1. **The headline:** trailing 7-day mean cost per daily session against the $0.60 budget, the $0.80 warning and the $1.00 stop line, with the last 28 days as a line.
2. **Where the money went today:** a stacked bar by role (voice studio, call, teacher and writer, verbatim, Salma (when asked) and chat, after-session, proof, swap) and the same by vendor.
3. **The levers:** batch share of teacher and writer calls, cache hit rate per text role (alarm under 85%), escalation rate from batch (alarm over 20%), average episode minutes, average call minutes, host model in use, `spend_mode`.
4. **Distribution:** the ten most expensive sessions of the day with the reason column (`retry_storm`, `rewrite_loop`, `long_call`, `cache_miss`, `fallback_standard`) computed by the rollup, and a histogram.
5. **Today's spend** against the daily cap by environment and by kind (`sample`, `first`, `daily`), with the cap formula shown.
6. **Fixed cost** this month so far (AWS, Vercel, LiveKit, vendor minimums, pulled weekly from the billing APIs where they exist and entered by hand where they do not), divided by sessions, as its own line.
7. **Reconciliation:** last month's `vendor_calls` sum against each vendor's invoice, variance per vendor, alarm above 5%.

The weekly cost report (Monday 06:00 UTC, posted to Slack and stored in `cost_reports`) is the same page as a snapshot plus the stop-line plan text if one is open.

## 5. Alerts

`ops/alerts.yaml` holds every rule: a SQL predicate over the tables above, a window, a severity, a dedupe key and a runbook path. The Inngest cron `ops/watch` evaluates them every five minutes, writes `alert_state`, and calls `ops.page()` for P1 (Better Stack incident, phone to Muath), `ops.notify()` for P2 (Slack now) and the morning digest for P3. The cost alarms from architecture 08 §4.5 are rules in the same file.

The P1 families, the only ones that ring a phone, and the fallback that has already run when they do:

| Family | Rule | Fallback already running | Runbook |
|---|---|---|---|
| Drop at risk | an episode not `ready` at drop minus 45 min for any learner; `drops_late_systemic` | yesterday's episode stays on Today; the fallback episode is produced | R3 |
| Calls cannot run | streaming recognizer or both voice vendors degraded (5 failures in 10 min); LiveKit or `call-worker` unhealthy | the recognizer and voice understudies; then voice notes | R1, R2, R7 |
| Platform down | Better Stack uptime failure on `app.`, `api.`, or the feed; RDS failover; `outbox_growing` | the cached episode plays offline; the feed keeps serving cached audio | R7 |
| Spend | daily spend over the cap (`halt`), a learner's day over the hard cost guard | `halt` pauses new on-demand generation; calls are never cut | R8 |
| Privacy | `privacy.audit_failed` for any window; a break-glass role assumption | none; this one needs a person | R11, R13 |
| Crisis | `crisis.activated` (Slack to Muath; the in-product protocol has already run) | the protocol itself | R10 |

P2 (Slack, within the day): latency budgets missed at p95, `fallback_3_in_7`, cache hit rate low, vendor error rate over 5%, canary failed, `wrong_memory_rate`, reconciliation variance. P3 (digest at 06:00 UTC): everything else, including the nightly's findings.

## 6. Runbooks

Twelve one-page runbooks in `ops/runbooks/`, each with the same five headings: detect, first five minutes, fix, verify, tell the learner. They are summarised in architecture 09 §4.8, with these additions from this handbook:

- **R13 Incident** (`incident.md`, from architecture 07 §4.15): the four severities, the `security_incidents` row, the 72-hour regulator clock, what Muath tells whom. Rehearsed once as a tabletop before launch. A personal-data breach that must be notified is one of the triggers for engaging a lawyer (ADR-25.3).
- **R14 Deploy went wrong**: rollback with `tools/release rollback`, when a prompt version is the cause (revert the PR, cut again), when a migration is the cause (expand-then-contract means the old image still runs; if it does not, that is the incident).

Every runbook step is an admin action or a `tools/` command, never ad hoc SQL; if a step needs SQL, the runbook gets an admin action instead. The admin actions runbooks rely on, all audited and idempotent: `pull episode`, `re-run after-pass`, the `/admin/vendors` failover switch, the flag switches and the learner rebuild button. **Who runs them:** Muath from the admin pages, or the agent when Muath asks, through `ops.yml` (handbook 04 §2), which waits for Muath's approval and then runs the named action with the OIDC role. The agent never holds a prod credential of its own.

## 7. Operations without a rota

There is no on-call rota (ADR-25.2). The product absorbs what it can, and a person is needed only for what it cannot:

- **Fallbacks first.** Every P1 family above has an automatic fallback that runs before the page: yesterday's episode stays, the fallback episode is produced, the understudy voice takes over, the call becomes voice notes, `halt` stops runaway spend. A learner never waits for a human to keep the show running.
- **Alerts to Muath.** P1 rings Muath's phone at any hour, but only for the six families; P2 reaches Slack; P3 waits for the 06:00 UTC digest. There is no protected hour, because learners are in every timezone (architecture 09 D11, ADR-16). Muath decides whether a P1 that the fallback has absorbed waits until morning.
- **The agent works the follow-up.** When Muath asks, the agent reads the alert, the runbook and the ids-only diagnostics (handbook 09 §3), proposes the fix, runs the runbook action through `ops.yml`, and opens a story for any code change it needs.
- **The daily check.** A scheduled job posts the first-working-hour checklist to Slack each morning (architecture 09 §4.10): `/admin/alerts` clear, every learner's drop published, yesterday's canary green, the `/admin/costs` headline, `/admin/privacy` all windows green, the nightly result. Muath reads it; a red line becomes a story.
- **A weekly review** on Tuesdays, prepared by the agent as a short report: alerts fired, false positives to tune, flags flipped, cost trend.
- **Never without Muath:** flip a vendor back from an understudy, change a prompt version in prod, read learner content, send any message to a learner.
- **Accepted:** some overnight P1s are answered by the fallbacks and a person in the morning; both voice vendors down at 03:00 means voice notes until then.

## 8. Postmortems

Blameless, one page, written by the agent and read by Muath, for: any P1, more than three learners late in one morning, any missed privacy window, any pulled episode, any wrong memory. Stored in `ops/postmortems/<slug>.md` with the same headings every time (what happened, timeline, impact in learner terms, cause, what changes, what we got lucky on). Every postmortem produces at least one of: a fixture, an alert rule, a runbook change, or a test. A postmortem that produces only "be more careful" is sent back.

## 9. Feature flags and kill switches

`feature_flags` table, read with a 60-second cache, edited on `/admin/flags`, every change audited. Flags exist for v1.1 features, vendor levers and kill switches, never for a law. Every runbook's first fix is a flag or a vendor switch; a feature that ships without a kill switch is not done (handbook 10).
