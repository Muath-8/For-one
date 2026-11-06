# 10. Definition of done

Part of the For one engineering handbook. Written 2026-11-06. Three checklists: a story, a prompt or model change, and a release. A thing that fails a line is not done, whatever the ticket says.

## 1. A story is done when

**It works and is proven**
- [ ] The behaviour matches the PRD-v2 section or the architecture section the story cites, and the PR links it.
- [ ] Unit tests cover the new logic; integration tests cover any new table, event, endpoint or job.
- [ ] CI is green, including `eval-gate` if a versioned path moved.
- [ ] It was exercised once end to end on staging by the author (a synthetic learner's day, or the relevant slice), and the PR's "How tested" says how.

**It respects the product**
- [ ] No law is broken: no points, streaks, levels or "next episode" control; no "you are wrong"; claims only through the gate; nothing cost-related reaches a learner.
- [ ] Any learner-facing text is in `ui_strings`, in the learner's language first, and reads like Salma, not like a system.

**It respects the learner's data**
- [ ] Every new query is learner-scoped and under RLS; every new table has a policy and `learner_id`.
- [ ] No learner text in logs, traces (without the opt-in), Inngest events, Sentry, Slack or a vendor the register does not list.
- [ ] A new learner-voice object kind is wired into `audio/expire`, `learner/purge-audio`, `learner/delete`, `learner/export` and `privacy/verify`.
- [ ] A new human-readable surface writes an `audit_log` row per content read and respects the role matrix.

**It can be run**
- [ ] A new vendor call goes through the middleware, has a price row, and appears on `/admin/costs`.
- [ ] A kill switch or a vendor switch exists if the feature can misbehave in production.
- [ ] A new alert has a runbook; a new runbook has a detect rule.
- [ ] A new environment variable is in `.env.example`, in `Settings`, in Terraform's secret or task definition, and in handbook 02's table.
- [ ] Migrations are additive and downgrade works.

**It can be understood**
- [ ] The fakes still agree with the real adapters; any cassette was recorded with a synthetic learner.
- [ ] The PR body says why, what and how tested; an ADR exists if an architecture document was overruled.
- [ ] The handbook or the package README was updated if a rule changed.

## 2. A prompt, rule or model change is done when

- [ ] The file changed and `versions.yaml` bumped in the same PR, with the right semver step.
- [ ] The PR states the intended behaviour change and what must not move.
- [ ] `eval-gate` ran the mapped suites; no floor, ceiling or regression breached; the run id is on the PR.
- [ ] The reviewer read three sample outputs from the run and the diff, and is not the author.
- [ ] No per-learner text entered the file; the cached prefix is unchanged or the PR says it changed.
- [ ] The role is not pinned, or the window has ended.
- [ ] If it is a model change, the price row exists and the cost page shows the new line.
- [ ] If it is a bible, Muath approved. If it is a consent text or crisis resource, counsel did.
- [ ] The nightly after merge is green; the baseline was updated on `main`.

## 3. A release is done when

- [ ] Cut from `main` with `tools/release cut`; the manifest lists versions, flags, migrations and the eval run ids that cover the diff.
- [ ] Approved by someone other than the cutter (where there are two), inside the release window, with no P1 firing and not inside a freeze.
- [ ] Migrations ran; `api` and `workflows` rolled; `call-worker` drained and replaced outside the call windows.
- [ ] The canary episode and the canary call passed on the synthetic prod learner.
- [ ] The engineer watched `/admin/alerts` and `#forone-ops` for 30 minutes after.
- [ ] The manifest row has `deployed_at`, `approved_by`, `canary_passed`.
- [ ] Any flag the release depends on is at the intended state and recorded in the manifest.
- [ ] The handover note mentions it if the on-call changes before the next release.

## 4. The build is done (2026-12-22) when

The beta gate in PRD-v2 19 and architecture 09 D13 own the product criteria. The engineering criteria that sit under them:

- [ ] Every P0 item has a story that met section 1.
- [ ] `calls_50` passes every PRD 15 latency gate on staging two weeks running.
- [ ] `privacy/verify` has been green for 14 consecutive days on staging with daily synthetic traffic.
- [ ] The restore drill (week 5) restored staging from a prod-shaped backup in under 30 minutes.
- [ ] The incident tabletop (week 5) ran and its findings are closed.
- [ ] The processor register has a signed or accepted DPA for every vendor in `vendors.yaml`, and counsel has answered the region question.
- [ ] The on-call rota, Better Stack escalation and the twelve runbooks exist and the first on-call has read them.
- [ ] Cost per session on staging's synthetic traffic is under $0.70 with the chosen voice vendor, and the January price book shows the plan.
- [ ] Every account in handbook 07 §1 is open, in the company's name, with two-factor on and the engineers as members.
