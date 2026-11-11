# E15 · Evals, observability and operations

*Architecture domain 09. Ships inside the other epics' weeks and costs about one engineer-week of its own; the story sizes below are the honest total. P0 here means "the beta cannot be run safely without it".*

### E15-S01 · Logging with the scrub corpus and paging
**As an** operator, **I want** structured JSON logs with a scrubber tested against a corpus of personal data, Sentry scrubbing, uptime checks and `ops.page()` to Slack, **so that** no log carries learner text and an outage is seen.
- **Given** the `pii_corpus`, **when** the scrubber test runs, **then** zero leaks; **given** a down check, **then** a page arrives within 5 minutes.
- Size: M · Priority: P0 · Week: Phase 1 · Due: Day-1 · Domain: 09 Operations · Depends on: E01-S06
- Requirements: FR-1050, NFR-306

### E15-S02 · Milestone 0 fixtures imported
**As an** engineer, **I want** `tools/import_m0.py` to write fixtures (learner files, scripts with hand coverage, editor reads, transcripts and tags, 30 clips, facts, similarity pairs), **so that** every suite has real data from day one.
- **Given** the import, **when** run, **then** every fixture listed in the operations design exists with its source clip's consent checked.
- Size: M · Priority: P0 · Week: Phase 1 · Due: Day-1 · Domain: 09 Operations · Depends on: E02-S01
- Requirements: NFR-501

### E15-S03 · Eval suites and the eval gate in CI
**As an** operator, **I want** suites for fitter, law scan, claim gate, recognizers, editor, writer, pipeline, memory, host governor replay, injection and analyst, with `eval-gate` running the mapped suites on prompt or rule changes, **so that** a prompt change cannot break law 7 unseen.
- **Given** a host prompt change that adds "that's wrong", **when** CI runs, **then** the law scan and governor replay fail the build.
- Size: L · Priority: P0 (law scan, governor, editor), P1 (the rest) · Week: Phase 2 · Due: Day-1 · Domain: 09 Operations · Depends on: E15-S02
- Requirements: FR-437, NFR-206, NFR-501

### E15-S04 · Alert rules for pipeline, client, call, cost, privacy and crisis
**As an** operator, **I want** `ops/alerts.yaml` with rules for missed drops, fallback rates, degraded editor, voice failover, slow first sound, slow host replies, governor violations, cost lines, privacy misses and crisis activations, **so that** the twelve things that go wrong page.
- **Given** an episode not ready before drop, **when** detected, **then** a page arrives within 5 minutes with the runbook link.
- Size: M · Priority: P0 · Week: Phase 4 · Due: Day-1 · Domain: 09 Operations · Depends on: E15-S01
- Requirements: NFR-113, NFR-201

### E15-S05 · Release manifest, feature flags and the freeze
**As an** operator, **I want** every release to record code, prompt and bible versions, flags to switch features without a deploy, and the pre-open freeze from 2027-03-15 12:00 to 03-17 12:00 UTC (with no releases 2026-12-31 to 2027-01-02), **so that** a bad prompt can be traced and pulled.
- **Given** a bad episode, **when** its release is looked up, **then** the manifest names every prompt version in it; **given** the `pull` action, **then** the episode is removed from Today and the feed.
- Size: M · Priority: P0 · Week: Phase 2 · Due: Day-1 · Domain: 09 Operations · Depends on: E01-S07
- Requirements: FR-503, NFR-206

### E15-S06 · Runbooks, on-call and the tabletop
**As an** operator, **I want** the twelve runbooks, the one-engineer on-call rota with Better Stack phone escalation for a systemic drop failure (ADR-24.12), the 08:30 checklist and one 60-minute tabletop (failover by hand, pull, re-run after-pass, wrong memory), **so that** the 05:40 drop failure has a known owner.
- **Given** the tabletop, **when** done before the pre-open freeze, **then** R1 to R4 and R12 were rehearsed and the gaps ticketed.
- **Given** the manual substitutes the release plan lists (section 5), **when** the beta opens, **then** each has a runbook line with an owner and a time limit: the purge (24 hours) and the hand export (72 hours, E13-S13), cancel and plan-change requests in Paddle (one working day, E12-S07, E12-S10), the failed-payment grace (E12-S11), a vetoed target (E10-S02), the reviewer's tokenized sheet (E13-S10, E15-S08), and the privacy, measures and gates SQL in the 08:30 checklist (E13-S11, E15-S07, E15-S09); each line is deleted when its story ships.
- Size: M · Priority: P0 · Week: Phase 6 · Due: Day-1 · Domain: 09 Operations · Depends on: E15-S04
- Requirements: NFR-201, NFR-202

### E15-S07 · Measures and the admin measures page
**As an** operator, **I want** the product measures (first sound, pilot time, speech minutes, talk share, worth it, return after gap, false claims, wrong memories, cost) computed daily with readable-from dates, **so that** the gates can be read at the gate review (2027-04-20, beta day 35) from the first day's data.
- **Given** the measures page, **when** opened, **then** each measure shows its value, its noise and the date it became readable.
- **Given** the event log from the first day, **when** the measures job first runs, **then** it back-fills every measure from the open (2027-03-17), including recognizer error by the learner's first language.
- Until it ships: the 08:30 checklist runs the measures as SQL on the event log (`forone_readonly`); the job back-fills from the open.
- Size: M · Priority: P0 · Week: Beta · Due: beta day 14 (2027-03-30) · Domain: 09 Operations · Depends on: E03-S08
- Requirements: FR-120, NFR-504

### E15-S08 · Review sampling and the review pages
**As an** operator, **I want** 10 random episodes per learner per month and a sample of calls queued for a person to read, with names tokenized, **so that** quality is judged by a human every month.
- **Given** the review queue, **when** a reviewer flags an episode, **then** the flag feeds the editor suite as a new fixture.
- Until it ships: as E13-S10: a tokenized sheet of 10 random episodes per learner, made by hand each month.
- Size: M · Priority: P0 · Week: Beta · Due: beta day 21 (2027-04-06) · Domain: 09 Operations · Depends on: E13-S10, E04-S13
- Requirements: FR-436, NFR-503

### E15-S09 · The gates page
**As an** operator, **I want** one page with every beta gate (trial to paid, week-4 active, sessions a week, speech minutes, recording change, renewal, worth it, cost, false claims, wrong memories, per-language quality) with pass, stop and readable-from, **so that** the gate review (2027-04-20) is a reading, not a debate.
- **Given** a gate below its stop line, **when** readable, **then** it is shown in plain words with the stop value beside it.
- Until it ships: the gates are read by SQL from the measures (runbook line in E15-S06).
- Size: M · Priority: P0 · Week: Beta · Due: beta day 29 (2027-04-14) · Domain: 09 Operations · Depends on: E15-S07
- Requirements: NFR-502, NFR-504

### E15-S10 · Synthetic learners and the canary
**As an** operator, **I want** 3 synthetic learners seeded from pilot files in the build and 50 in the beta, with a weekly canary episode, **so that** the pipeline is exercised without touching a real learner.
- **Given** the canary fails, **when** detected, **then** `canary_failed` pages.
- Size: M · Priority: P0 (3), P1 (50) · Week: Phase 6 · Due: Day-1 · Domain: 09 Operations · Depends on: E04-S07
- Requirements: FR-437, NFR-201

### E15-S11 · Vendor regression and the weekly digest
**As an** operator, **I want** a weekly digest of measures, cost and incidents, and a quarterly vendor regression run on the fixed fixtures, **so that** a silent vendor model change is caught.
- **Given** the first regression in beta week 1, **when** a vendor's score drops beyond the threshold, **then** an incident is opened.
- Size: S · Priority: P1 · Week: Beta · Domain: 09 Operations · Depends on: E15-S03
- Requirements: NFR-206
