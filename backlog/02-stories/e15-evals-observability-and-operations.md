# E15 · Evals, observability and operations

*Architecture domain 09. Ships inside the other epics' weeks and costs about one engineer-week in total before 22 December. P0 here means "the beta cannot be run safely without it".*

### E15-S01 · Logging with the scrub corpus and paging
**As an** operator, **I want** structured JSON logs with a scrubber tested against a corpus of personal data, Sentry scrubbing, uptime checks and `ops.page()` to Slack, **so that** no log carries learner text and an outage is seen.
- **Given** the `pii_corpus`, **when** the scrubber test runs, **then** zero leaks; **given** a down check, **then** a page arrives within 5 minutes.
- Size: M · Priority: P0 · Week: W1 · Domain: 09 Operations · Depends on: E01-S06

### E15-S02 · Milestone 0 fixtures imported
**As an** engineer, **I want** `tools/import_m0.py` to write fixtures (learner files, scripts with hand coverage, editor reads, transcripts and tags, 30 clips, facts, similarity pairs), **so that** every suite has real data from day one.
- **Given** the import, **when** run, **then** every fixture listed in the operations design exists with its source clip's consent checked.
- Size: M · Priority: P0 · Week: W1 · Domain: 09 Operations · Depends on: E02-S01

### E15-S03 · Eval suites and the eval gate in CI
**As an** operator, **I want** suites for fitter, law scan, claim gate, recognizers, editor, writer, pipeline, memory, host governor replay, injection and analyst, with `eval-gate` running the mapped suites on prompt or rule changes, **so that** a prompt change cannot break law 7 unseen.
- **Given** a host prompt change that adds "that's wrong", **when** CI runs, **then** the law scan and governor replay fail the build.
- Size: L · Priority: P0 (law scan, governor, editor), P1 (the rest) · Week: W2 to W5 · Domain: 09 Operations · Depends on: E15-S02

### E15-S04 · Alert rules for pipeline, client, call, cost, privacy and crisis
**As an** operator, **I want** `ops/alerts.yaml` with rules for missed drops, fallback rates, degraded editor, voice failover, slow first sound, slow host replies, governor violations, cost lines, privacy misses and crisis activations, **so that** the twelve things that go wrong page.
- **Given** an episode not ready before drop, **when** detected, **then** a page arrives within 5 minutes with the runbook link.
- Size: M · Priority: P0 · Week: W2 to W5 · Domain: 09 Operations · Depends on: E15-S01

### E15-S05 · Release manifest, feature flags and the freeze
**As an** operator, **I want** every release to record code, prompt and bible versions, flags to switch features without a deploy, and a freeze from 19 December 12:00, **so that** a bad prompt can be traced and pulled.
- **Given** a bad episode, **when** its release is looked up, **then** the manifest names every prompt version in it; **given** the `pull` action, **then** the episode is removed from Today and the feed.
- Size: M · Priority: P0 · Week: W2 · Domain: 09 Operations · Depends on: E01-S07

### E15-S06 · Runbooks, on-call and the tabletop
**As an** operator, **I want** the twelve runbooks, an on-call rota with phone escalation, the 08:30 checklist and one 60-minute tabletop (failover by hand, pull, re-run after-pass, wrong memory), **so that** the 05:40 drop failure has a known owner.
- **Given** the tabletop, **when** done before 22 December, **then** R1 to R4 and R12 were rehearsed and the gaps ticketed.
- Size: M · Priority: P0 · Week: W5 · Domain: 09 Operations · Depends on: E15-S04

### E15-S07 · Measures and the admin measures page
**As an** operator, **I want** the product measures (first sound, pilot time, speech minutes, talk share, worth it, return after gap, false claims, wrong memories, cost) computed daily with readable-from dates, **so that** the gates can be read on 26 January from the first day's data.
- **Given** the measures page, **when** opened, **then** each measure shows its value, its noise and the date it became readable.
- Size: M · Priority: P0 · Week: W3 to W5 · Domain: 09 Operations · Depends on: E03-S08

### E15-S08 · Review sampling and the review pages
**As an** operator, **I want** 10 random episodes per learner per month and a sample of calls queued for a person to read, with names tokenized, **so that** quality is judged by a human every month.
- **Given** the review queue, **when** a reviewer flags an episode, **then** the flag feeds the editor suite as a new fixture.
- Size: M · Priority: P0 · Week: W5 · Domain: 09 Operations · Depends on: E13-S10, E04-S13

### E15-S09 · The gates page
**As an** operator, **I want** one page with every beta gate (trial to paid, week-4 active, sessions a week, speech minutes, recording change, renewal, worth it, cost, false claims, wrong memories, per-language quality) with pass, stop and readable-from, **so that** 26 January is a reading, not a debate.
- **Given** a gate below its stop line, **when** readable, **then** it is shown in plain words with the stop value beside it.
- Size: M · Priority: P0 · Week: W5 · Domain: 09 Operations · Depends on: E15-S07

### E15-S10 · Synthetic learners and the canary
**As an** operator, **I want** 3 synthetic learners seeded from pilot files in the build and 50 in the beta, with a weekly canary episode, **so that** the pipeline is exercised without touching a real learner.
- **Given** the canary fails, **when** detected, **then** `canary_failed` pages.
- Size: M · Priority: P0 (3), P1 (50) · Week: W2 · Domain: 09 Operations · Depends on: E04-S07

### E15-S11 · Vendor regression and the weekly digest
**As an** operator, **I want** a weekly digest of measures, cost and incidents, and a quarterly vendor regression run on the fixed fixtures, **so that** a silent vendor model change is caught.
- **Given** the first regression on 1 January, **when** a vendor's score drops beyond the threshold, **then** an incident is opened.
- Size: S · Priority: P1 · Week: Beta · Domain: 09 Operations · Depends on: E15-S03
