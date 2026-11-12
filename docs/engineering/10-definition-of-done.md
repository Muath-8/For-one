# 10. Definition of done

Part of the For one engineering handbook. Written 2026-11-06; revised 2026-11-12 for ADR-25 (an AI coding agent builds it under Muath; no dates; version 1 launches once, with no Milestone 0 and no beta). Four checklists: a story, a prompt or model change, a release, and the launch. A thing that fails a line is not done, whatever the story says. The agent ticks each line in the PR body; the review pass checks the ticks; Muath approves.

## 1. A story is done when

**It was specified before it was built**
- [ ] Every acceptance criterion of the story is an automated test with a name that says which criterion it proves, committed before the code that makes it pass.
- [ ] The behaviour matches the PRD-v3 requirement or the architecture section the story cites, and the PR links it.
- [ ] Nothing in the change decides something the canon leaves open; any such question went to Muath and the answer is linked.

**It works and is proven**
- [ ] Unit tests cover the new logic; integration tests cover any new table, event, endpoint or job.
- [ ] CI is green, including `eval-gate` if a versioned path moved.
- [ ] The AI review pass has no open blocking finding, and neither has the security review pass if the change touches auth, keys, media URLs, the feed or deletion (ADR-25.11).
- [ ] It was exercised once end to end on staging (a synthetic learner's day, or the relevant slice), and the PR's "How tested" says how.

**It respects the product**
- [ ] No law is broken: no points, streaks, levels, autoplay or "next episode" control in the player (only the "Next one" button on Today while the portion remains, 24.B32); no "you are wrong"; claims only through the gate; nothing cost-related reaches a learner.
- [ ] Any learner-facing text is in the native package (`packages/native/<lang>/`), in the learner's language first, and reads like Salma, not like a system.

**It respects the learner's data**
- [ ] Every new query is learner-scoped and under RLS; every new table has a policy and `learner_id`.
- [ ] No learner text in logs, traces (without the opt-in), Inngest events, Sentry, Slack or a vendor the register does not list.
- [ ] A new learner-voice object kind is wired into `audio/expire`, `learner/purge-audio`, `learner/delete`, `learner/export` and `privacy/verify`.
- [ ] A new human-readable surface writes an `audit_log` row per content read and is open to the `owner` role only.

**It can be run**
- [ ] A new vendor call goes through the middleware, has a price row, and appears on `/admin/costs`.
- [ ] A kill switch or a vendor switch exists if the feature can misbehave in production.
- [ ] A new alert has a runbook and a fallback that runs before it pages; a new runbook has a detect rule and an admin action for every step.
- [ ] A new environment variable is in `.env.example`, in `Settings`, in Terraform's secret or task definition, and in handbook 02's table.
- [ ] Migrations are additive and downgrade works.

**It can be understood**
- [ ] The fakes still agree with the real adapters; any cassette was recorded with a synthetic learner.
- [ ] The PR body has the story id, why, what and how tested.
- [ ] The handbook or the package README was updated if a rule changed.

## 2. A prompt, rule or model change is done when

- [ ] The file changed and `versions.yaml` bumped in the same PR, with the right semver step.
- [ ] The PR states the intended behaviour change and what must not move.
- [ ] `eval-gate` ran the mapped suites; no floor, ceiling or regression breached; the run id is on the PR.
- [ ] The review pass read three sample outputs from the run and the diff, and found nothing blocking.
- [ ] No per-learner text entered the file; the cached prefix is unchanged or the PR says it changed.
- [ ] The role is not pinned, or the window has ended.
- [ ] If it is a model change, the price row exists and the cost page shows the new line.
- [ ] If it is a bible, the review pass checked it against the laws and ban lists and Muath approved it (ADR-25.7). If it is a consent text or crisis resource, it was checked against the self-review checklist and Muath approved it (ADR-25.3).
- [ ] The nightly after merge is green; the baseline was updated on `main`.

## 3. A release is done when

- [ ] Cut from `main` with `tools/release cut`; the manifest lists versions, flags, migrations and the eval run ids that cover the diff.
- [ ] Approved by Muath, inside the computed release window, with no P1 firing.
- [ ] Migrations ran; `api` and `workflows` rolled; `call-worker` drained and replaced outside the call windows.
- [ ] The canary episode and the canary call passed on the synthetic prod learner.
- [ ] No alert fired against the release in the 30 minutes after the canary, or the release was rolled back.
- [ ] The manifest row has `deployed_at`, `approved_by`, `canary_passed`.
- [ ] Any flag the release depends on is at the intended state and recorded in the manifest.

## 4. Version 1 is ready to launch when

The launch health measures in PRD-v3 16 and architecture 09 D13, read 4 and 8 weeks after launch, own the product criteria (ADR-25.5). The engineering criteria that sit under the launch, in the order the release plan reaches them:

- [ ] Every **v1** story has met section 1. **v1.1** stories may still be open.
- [ ] The scripted calls pass every PRD 15 latency gate on staging two weeks running.
- [ ] `privacy/verify` has been green for 14 consecutive days on staging with daily synthetic traffic.
- [ ] A restore of staging from a prod-shaped backup was rehearsed and took under 4 hours (NFR-207).
- [ ] The incident tabletop ran and its findings are closed.
- [ ] The OWASP ZAP baseline scan of staging has no open medium or higher alert, the dependency scans are clean, and every security-path change since the start passed the security review pass (ADR-25.11). No paid penetration test is required at launch.
- [ ] Deletion and export were verified end to end on a test learner in production.
- [ ] The processor register has a signed or accepted DPA for every vendor in `vendors.yaml`, and the self-review checklist is complete and approved by Muath (register A4).
- [ ] The alert rules, the fallbacks and the twelve runbooks exist, and each runbook's admin actions work through `ops.yml`.
- [ ] Cost per session on staging's synthetic traffic is under $0.70 with the chosen voice vendor at post-doubling prices, with a costed path to $0.35.
- [ ] Every account in handbook 07 §1 that v1 needs is open in the company's name, with two-factor on, and the domain is registered (A6).
