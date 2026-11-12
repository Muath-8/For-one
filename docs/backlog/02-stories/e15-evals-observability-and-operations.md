# E15 · Evals, observability and operations

*Architecture domain 09. Operations for a product built by an AI coding agent and run by one person (ADR-25.2): automated fallbacks first, alerts to Muath, runbooks the agent can execute when asked. P0 here means "launch cannot be run safely without it".*

### E15-S01 · Logging with the scrub corpus and paging
**As an** operator, **I want** structured JSON logs with a scrubber tested against a corpus of personal data, Sentry scrubbing, uptime checks and `ops.page()` to Slack, **so that** no log carries learner text and an outage is seen.
- **Given** the `pii_corpus`, **when** the scrubber test runs, **then** zero leaks; **given** a down check, **then** a page arrives within 5 minutes.
- Size: M · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 09 Operations · Depends on: E01-S06
- Requirements: FR-1050, NFR-306

### E15-S02 · Fixtures from synthetic learners, scripted calls and open clips
**As the** coding agent, **I want** `tools/fixtures` to generate synthetic learner files with planted errors, facts and review histories, scripted call transcripts, scripts with hand-computed coverage, labelled editor packages, similarity pairs, and the clip set from E02-S01, **so that** every suite has data from the first day without a trial run (ADR-25.6).
- **Given** the generator, **when** run, **then** every fixture listed in the operations design exists, records its source and licence, and contains no real learner's data.
- Size: M · Priority: P0 · Phase: Phase 1 · Release: v1 · Domain: 09 Operations · Depends on: E02-S01
- Requirements: NFR-501

### E15-S03 · Eval suites and the eval gate in CI
**As an** operator, **I want** suites for fitter, law scan, claim gate, recognizers, editor, writer, pipeline, memory, host governor replay, injection and analyst, with `eval-gate` running the mapped suites on prompt or rule changes, **so that** a prompt change cannot break law 7 unseen.
- **Given** a host prompt change that adds "that's wrong", **when** CI runs, **then** the law scan and governor replay fail the build.
- Size: L · Priority: P0 (law scan, governor, editor), P1 (the rest) · Phase: Phase 2 · Release: v1 · Domain: 09 Operations · Depends on: E15-S02
- Requirements: FR-437, NFR-206, NFR-501

### E15-S04 · Alert rules for pipeline, client, call, cost, privacy and crisis
**As an** operator, **I want** `ops/alerts.yaml` with rules for missed drops, fallback rates, degraded editor, voice failover, slow first sound, slow host replies, governor violations, cost lines, privacy misses and crisis activations, **so that** the twelve things that go wrong page.
- **Given** an episode not ready before drop, **when** detected, **then** a page arrives within 5 minutes with the runbook link.
- Size: M · Priority: P0 · Phase: Phase 4 · Release: v1 · Domain: 09 Operations · Depends on: E15-S01
- Requirements: NFR-113, NFR-201

### E15-S05 · Release manifest, feature flags and the freeze
**As an** operator, **I want** every release to record code, prompt and bible versions, flags to switch features without a deploy, and a pre-launch freeze of two working days, **so that** a bad prompt can be traced and pulled.
- **Given** a bad episode, **when** its release is looked up, **then** the manifest names every prompt version in it; **given** the `pull` action, **then** the episode is removed from Today and the feed.
- Size: M · Priority: P0 · Phase: Phase 2 · Release: v1 · Domain: 09 Operations · Depends on: E01-S07
- Requirements: FR-503, NFR-206

### E15-S06 · Runbooks, alerts to Muath and the tabletop
**As an** operator, **I want** the twelve runbooks written as scripts the agent can run when Muath asks, alerts that reach Muath by push and, for a systemic drop failure, by phone (Better Stack), the morning checklist the agent runs and reports, and one 60-minute tabletop (failover, pull, re-run the after-pass, wrong memory), **so that** a 05:40 drop failure is handled by the automated fallbacks first and by a runbook second (ADR-25.2).
- **Given** the tabletop, **when** done before launch, **then** R1 to R4 and R12 were rehearsed, each by the agent running the runbook on staging at Muath's request, and the gaps ticketed.
- **Given** a fallback (yesterday's episode stays, voice notes), **when** it fires, **then** the learner sees no error and Muath gets one alert with the runbook link.
- Size: M · Priority: P0 · Phase: Phase 6 · Release: v1 · Domain: 09 Operations · Depends on: E15-S04, E01-S10
- Requirements: NFR-201, NFR-202

### E15-S07 · Measures and the admin measures page
**As an** operator, **I want** the product measures (first sound, first-episode time, speech minutes, talk share, worth it, return after gap, false claims, wrong memories, cost) computed daily with readable-from dates, **so that** the launch health measures can be read at 4 and 8 weeks from the first day's data.
- **Given** the measures page, **when** opened, **then** each measure shows its value, its noise and the date it became readable.
- **Given** the event log from the first day, **when** the measures job first runs, **then** it back-fills every measure from launch, including recognizer error by the learner's first language.
- Size: M · Priority: P0 · Phase: Phase 6 · Release: v1 · Domain: 09 Operations · Depends on: E03-S08
- Requirements: FR-120, NFR-504

### E15-S08 · Review sampling and the review pages
**As an** operator, **I want** 10 random episodes per learner per month and a sample of calls read by an AI review pass against the laws and the ban lists, with names tokenized, and a smaller sample read by Muath (ADR-25.7), **so that** quality is checked every month.
- **Given** the review queue, **when** a reviewer flags an episode, **then** the flag feeds the editor suite as a new fixture.
- Size: M · Priority: P0 · Phase: Phase 6 · Release: v1 · Domain: 09 Operations · Depends on: E13-S10, E04-S13
- Requirements: FR-436, NFR-503

### E15-S09 · The launch health page
**As an** operator, **I want** one page with every launch health measure (trial to paid, week-4 active, sessions a week, speech minutes, recording change, renewal, worth it, cost, false claims, wrong memories, per-language quality) with target, stop line and readable-from, **so that** the reviews 4 and 8 weeks after launch are a reading, not a debate (ADR-25.5).
- **Given** a measure below its stop line, **when** readable, **then** it is shown in plain words with the stop value beside it.
- Size: M · Priority: P1 · Phase: After launch · Release: v1.1 · Domain: 09 Operations · Depends on: E15-S07
- Requirements: NFR-502, NFR-504

### E15-S10 · Synthetic learners and the canary
**As an** operator, **I want** 3 synthetic learners from E15-S02 running through the build and 50 for the offline suite, with a weekly canary episode, **so that** the pipeline is exercised without touching a real learner.
- **Given** the canary fails, **when** detected, **then** `canary_failed` alerts Muath.
- Size: M · Priority: P0 (3), P1 (50) · Phase: Phase 6 · Release: v1 · Domain: 09 Operations · Depends on: E04-S07, E15-S02
- Requirements: FR-437, NFR-201

### E15-S11 · Vendor regression and the weekly digest
**As an** operator, **I want** a weekly digest of measures, cost and incidents, and a quarterly vendor regression run on the fixed fixtures, **so that** a silent vendor model change is caught.
- **Given** the first regression after launch, **when** a vendor's score drops beyond the threshold, **then** an incident is opened.
- Size: S · Priority: P1 · Phase: After launch · Release: v1.1 · Domain: 09 Operations · Depends on: E15-S03
- Requirements: NFR-206
